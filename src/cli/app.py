import os
import sys
import asyncio
import time
from datetime import datetime
from typing import List, Dict

from src.syllabus_parser import SyllabusParser
from src.youtube_client import YouTubeClient
from src.ai_client import AIClient
from src.video_analyzer import VideoAnalyzer
from src.database import SyllaboDatabase
from src.logger import SyllaboLogger
from src.spaced_repetition import SpacedRepetitionEngine
from src.notification_system import NotificationSystem
from src.export_system import ExportSystem

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.progress import Progress
from rich.rule import Rule

from src.cli.interactive import InteractiveMode

class SyllaboApp:
    def __init__(self):
        self.logger = SyllaboLogger("cli")
        self.db = SyllaboDatabase()
        self.ai_client = AIClient()
        self.youtube_client = YouTubeClient()
        self.video_analyzer = VideoAnalyzer(self.ai_client)
        self.syllabus_parser = SyllabusParser()
        self.console = Console()
        self.spaced_repetition = SpacedRepetitionEngine()
        self.notifications = NotificationSystem()
        self.exporter = ExportSystem()

    def print_banner(self):
        self.console.print(Panel.fit(
            "SYLLABO ENHANCED",
            subtitle="AI-Powered Educational Resource Finder",
            style="bold cyan"
        ))

    async def run(self, args):
        self.print_banner()
        if args.command == 'interactive':
            interactive_mode = InteractiveMode()
            await interactive_mode.run()
        elif args.command == 'analyze':
            await self.analyze_syllabus(args)
        elif args.command == 'search':
            await self.search_videos(args)
        elif args.command == 'history':
            self.show_history(args)
        elif args.command == 'export':
            await self.export_results(args)
        elif args.command == 'review':
            self.handle_review_commands(args)
        else:
            self.show_help()

    async def analyze_syllabus(self, args):
        start_time = time.time()
        if args.file:
            if not os.path.exists(args.file):
                self.console.print(f"Error: File '{args.file}' not found", style="bold red")
                return
            self.console.print(f"Loading syllabus from file: {args.file}")
            syllabus_content = self.syllabus_parser.load_from_file(args.file)
            syllabus_title = os.path.basename(args.file)
        elif args.text:
            syllabus_content = args.text
            syllabus_title = f"Direct input - {datetime.now().strftime('%Y-%m-%d %H:%M')}"
            self.console.print("Analyzing provided text content...")
        else:
            self.console.print("Error: Please provide either --file or --text", style="bold red")
            return
        self.console.print("Extracting topics using AI...")
        topics = await self.syllabus_parser.extract_topics(syllabus_content, self.ai_client)
        if not topics:
            self.console.print("No clear topics found. Try refining your syllabus content.", style="yellow")
            return
        syllabus_id = self.db.save_syllabus(syllabus_title, syllabus_content)
        topic_ids = self.db.save_topics(syllabus_id, topics)
        if args.search_videos:
            self.console.print("Searching for videos...")
            topic_results = await self.search_for_topics_enhanced(topics, topic_ids, args.max_videos)
            if args.print_results:
                self.print_video_results(topic_results, args.max_videos)
            total_videos = sum(len(videos) for videos in topic_results.values())
            processing_time = time.time() - start_time
            self.console.print(Panel(
                f"Analysis complete: {len(topics)} topics, {total_videos} videos found in {processing_time:.1f}s",
                style="green"
            ))
            if args.save or args.export_format:
                await self.save_comprehensive_results(topic_results, syllabus_title, args.export_format or 'json')
            if args.add_to_review:
                self.add_topics_to_spaced_repetition(topics)
        else:
            if args.add_to_review:
                self.add_topics_to_spaced_repetition(topics)

    async def search_videos(self, args):
        if not args.topic:
            self.console.print("Error: Please provide a topic to search for", style="bold red")
            return
        start_time = time.time()
        self.console.print(f"Searching videos and playlists for: {args.topic}")
        enhanced_query = f"{args.topic} tutorial explained"
        videos = await self.youtube_client.search_videos(enhanced_query, args.max_videos)
        playlists = await self.youtube_client.search_playlists(enhanced_query, max(2, args.max_videos // 3))
        if not videos and not playlists:
            self.console.print("No videos or playlists found", style="yellow")
            return
        self.console.print(f"Found {len(videos)} videos and {len(playlists)} playlists, analyzing with AI...")
        analysis_result = await self.video_analyzer.analyze_videos_and_playlists(videos, playlists, args.topic)
        all_resources = []
        if analysis_result.get('primary_resource'):
            all_resources.append(analysis_result['primary_resource'])
        all_resources.extend(analysis_result.get('supplementary_videos', []))
        all_resources.extend(analysis_result.get('supplementary_playlists', []))
        quality_resources = [r for r in all_resources if r.get('relevance_score', 0) >= 3.0]
        if not quality_resources:
            self.console.print("No high-quality resources found for this topic", style="yellow")
            return
        topic_results = {args.topic: quality_resources}
        self.print_video_results(topic_results, min(args.max_videos, 10))
        processing_time = time.time() - start_time
        self.console.print(Panel(
            f"Search complete: 1 topic, {len(quality_resources)} videos found in {processing_time:.1f}s",
            style="green"
        ))
        if args.save:
            await self.save_video_results(quality_resources, args.topic, args.export_format or 'json')

    async def search_for_topics_enhanced(self, topics: List[Dict], topic_ids: List[int], max_videos: int) -> Dict[str, List[Dict]]:
        all_results = {}
        with Progress(console=self.console) as progress:
            task = progress.add_task("Searching for videos and playlists...", total=len(topics))
            for i, (topic, topic_id) in enumerate(zip(topics, topic_ids)):
                topic_name = topic['name']
                progress.update(task, advance=1, description=f"Searching for: {topic_name}")
                try:
                    enhanced_query = self._enhance_search_query(topic_name, topic.get('subtopics', []))
                    videos = await self.youtube_client.search_videos(enhanced_query, max_videos)
                    playlists = await self.youtube_client.search_playlists(enhanced_query, max(2, max_videos // 3))
                    if videos or playlists:
                        analysis_result = await self.video_analyzer.analyze_videos_and_playlists(videos, playlists, topic_name)
                        all_resources = []
                        if analysis_result.get('primary_resource'):
                            all_resources.append(analysis_result['primary_resource'])
                        all_resources.extend(analysis_result.get('supplementary_videos', []))
                        all_resources.extend(analysis_result.get('supplementary_playlists', []))
                        quality_resources = [r for r in all_resources if r.get('relevance_score', 0) >= 4.0]
                        for resource in quality_resources:
                            self.db.save_video(resource)
                            self.db.link_topic_video(topic_id, resource['id'], resource['relevance_score'])
                        all_results[topic_name] = quality_resources
                    else:
                        all_results[topic_name] = []
                except Exception as e:
                    self.logger.error(f"Failed to search resources for {topic_name}: {e}")
                    all_results[topic_name] = []
        return all_results

    def _enhance_search_query(self, topic_name: str, subtopics: List[str]) -> str:
        query_parts = [topic_name, "tutorial", "explained"]
        if subtopics:
            query_parts.insert(1, subtopics[0])
        return " ".join(query_parts)[:100]

    async def save_video_results(self, videos: List[Dict], topic: str, format_type: str = 'json'):
        try:
            filename = self.exporter.export_to_file(videos, topic, format_type)
            self.console.print(f"Results saved to: {filename}", style="green")
        except Exception as e:
            self.logger.error(f"Failed to save results: {e}")
            self.console.print(f"Failed to save results: {e}", style="bold red")

    async def save_comprehensive_results(self, topic_results: Dict[str, List[Dict]], syllabus_title: str, format_type: str = 'json'):
        try:
            filename = self.exporter.export_comprehensive(topic_results, format_type)
            self.console.print(f"Comprehensive results saved to: {filename}", style="green")
        except Exception as e:
            self.logger.error(f"Failed to save comprehensive results: {e}")
            self.console.print(f"Failed to save comprehensive results: {e}", style="bold red")

    def show_history(self, args):
        self.console.print(Panel("Recent Syllabi", style="bold"))
        recent_syllabi = self.db.get_recent_syllabi(args.limit)
        if not recent_syllabi:
            self.console.print("No syllabi found in database", style="yellow")
            return
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("ID", style="dim", width=6)
        table.add_column("Title")
        table.add_column("Created At", justify="right")
        for syllabus in recent_syllabi:
            table.add_row(str(syllabus['id']), syllabus['title'], syllabus['created_at'])
        self.console.print(table)

    async def export_results(self, args):
        if not args.syllabus_id:
            self.console.print("Error: Please provide a syllabus ID to export.", style="bold red")
            self.show_history(type('obj', (object,), {'limit': 5})())
            return
        self.console.print(f"Exporting results for syllabus ID: {args.syllabus_id}")
        syllabus = self.db.get_syllabus_by_id(args.syllabus_id)
        if not syllabus:
            self.console.print(f"Error: Syllabus with ID {args.syllabus_id} not found.", style="bold red")
            return
        topics = self.db.get_topics_by_syllabus_id(args.syllabus_id)
        if not topics:
            self.console.print(f"No topics found for syllabus: {syllabus['title']}", style="yellow")
            return
        topic_results = {topic['name']: self.db.get_topic_videos(topic['id']) for topic in topics}
        if not any(topic_results.values()):
            self.console.print("No video results found for this syllabus.", style="yellow")
            return
        await self.save_comprehensive_results(topic_results, syllabus['title'], args.format)

    def print_video_results(self, topic_results: Dict[str, List[Dict]], max_videos: int):
        self.console.print(Rule("Top Video Recommendations"))
        for topic_name, videos in topic_results.items():
            if not videos:
                continue
            self.console.print(Panel(f"{topic_name}", expand=False, style="bold"))
            table = Table(show_header=True, header_style="bold magenta")
            table.add_column("No.", style="dim", width=4)
            table.add_column("Title", style="cyan", no_wrap=True)
            table.add_column("Channel", style="yellow")
            table.add_column("Score", justify="right", style="green")
            table.add_column("URL", style="blue")
            for i, video in enumerate(videos[:max_videos], 1):
                table.add_row(
                    str(i),
                    video.get('title', 'Unknown Title')[:60],
                    video.get('channel', 'Unknown Channel'),
                    f"{video.get('relevance_score', 0):.1f}/10",
                    f"https://youtube.com/watch?v={video.get('id', '')}"
                )
            self.console.print(table)

    def add_topics_to_spaced_repetition(self, topics: List[Dict]):
        added_count = sum(1 for topic in topics if self.spaced_repetition.add_topic(topic['name'], topic.get('description', '')))
        if added_count > 0:
            self.console.print(f"Added {added_count} topics to spaced repetition schedule", style="green")
            self.console.print("Use 'python syllabo.py review list' to see your review schedule")
        else:
            self.console.print("All topics were already in your review schedule", style="yellow")

    def handle_review_commands(self, args):
        actions = {
            'add': self.add_review_topic,
            'list': self.list_review_topics,
            'due': self.show_due_reviews,
            'mark': self.mark_topic_review,
            'stats': self.show_review_stats,
            'remove': self.remove_review_topic,
        }
        action = actions.get(args.review_action)
        if action:
            action(args)
        else:
            self.show_review_help()

    def add_review_topic(self, args):
        if not args.topic:
            self.console.print("Error: Please provide a topic name with --topic", style="bold red")
            return
        if self.spaced_repetition.add_topic(args.topic, args.description or ""):
            self.console.print(f"Added '{args.topic}' to review schedule", style="green")
        else:
            self.console.print(f"Topic '{args.topic}' is already in your review schedule", style="yellow")

    def list_review_topics(self, args):
        topics = self.spaced_repetition.get_all_topics()
        if not topics:
            self.console.print("No topics in your review schedule", style="yellow")
            return
        self.console.print(Panel("Your Review Schedule", style="bold"))
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Topic", style="cyan", width=30)
        table.add_column("Mastery", justify="center", width=12)
        table.add_column("Success Rate", justify="center", width=12)
        table.add_column("Next Review", justify="center", width=12)
        table.add_column("Interval", justify="center", width=10)
        for topic in sorted(topics, key=lambda x: x['days_until_review']):
            mastery_color = {'Learning': 'red', 'Beginner': 'yellow', 'Intermediate': 'blue', 'Advanced': 'green', 'Mastered': 'bright_green'}.get(topic['mastery_level'], 'white')
            next_review_text = f"Due now" if topic['days_until_review'] <= 0 else f"{topic['days_until_review']} days"
            table.add_row(
                topic['topic_name'][:28] + "..." if len(topic['topic_name']) > 28 else topic['topic_name'],
                f"[{mastery_color}]{topic['mastery_level']}[/{mastery_color}]",
                f"{topic['success_rate']}%",
                next_review_text,
                f"{topic['current_interval']}d"
            )
        self.console.print(table)
        summary = self.spaced_repetition.get_study_summary()
        self.console.print(Panel(
            f"Summary: {summary['total_topics']} topics, {summary['due_now']} due now, {summary['mastered_topics']} mastered",
            style="green"
        ))

    def show_due_reviews(self, args):
        due_topics = self.spaced_repetition.get_due_topics()
        if not due_topics:
            self.console.print("No topics are due for review right now", style="green")
            return
        self.console.print(Panel(f"You have {len(due_topics)} topic{'s' if len(due_topics) != 1 else ''} due for review", style="bold"))
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("No.", style="dim", width=4)
        table.add_column("Topic", style="cyan")
        table.add_column("Description", style="yellow")
        for i, item in enumerate(due_topics, 1):
            table.add_row(
                str(i),
                item.topic_name,
                item.description or "No description"
            )
        self.console.print(table)
        if args.notify:
            self.notifications.notify_due_reviews(len(due_topics))

    def mark_topic_review(self, args):
        if not args.topic:
            self.console.print("Error: Please provide a topic name with --topic", style="bold red")
            return
        if self.spaced_repetition.mark_review(args.topic, args.success):
            self.console.print(f"Marked '{args.topic}' as {'successful' if args.success else 'failed'} review", style="green")
        else:
            self.console.print(f"Topic '{args.topic}' not found in review schedule", style="yellow")

    def show_review_stats(self, args):
        if args.topic:
            stats = self.spaced_repetition.get_topic_stats(args.topic)
            if not stats:
                self.console.print(f"Topic '{args.topic}' not found", style="yellow")
                return
            panel = Panel(
                f"Mastery Level: {stats['mastery_level']}\n"
                f"Success Rate: {stats['success_rate']}%\n"
                f"Next Review: {stats['next_review_date']}",
                title=f"Stats for {stats['topic_name']}",
                expand=False
            )
            self.console.print(panel)
        else:
            summary = self.spaced_repetition.get_study_summary()
            table = Table(show_header=True, header_style="bold magenta")
            table.add_column("Metric", style="cyan")
            table.add_column("Value", style="yellow")
            table.add_row("Total Topics", str(summary['total_topics']))
            table.add_row("Mastered Topics", str(summary['mastered_topics']))
            table.add_row("Average Success Rate", f"{summary['average_success_rate']}%")
            self.console.print(Panel(table, title="Overall Review Statistics", expand=False))

    def remove_review_topic(self, args):
        if not args.topic:
            self.console.print("Error: Please provide a topic name with --topic", style="bold red")
            return
        if self.spaced_repetition.remove_topic(args.topic):
            self.console.print(f"Removed '{args.topic}' from review schedule", style="green")
        else:
            self.console.print(f"Topic '{args.topic}' not found", style="yellow")

    def show_review_help(self):
        self.console.print(Panel(
            "Review commands:\n  add, list, due, mark, stats, remove\n"
            "Use 'python syllabo.py review [command]' for details.",
            style="bold"
        ))

    def show_help(self):
        self.console.print(Panel(
            "Usage: python syllabo.py [command] [options]\n\n"
            "Commands:\n"
            "  analyze   Analyze syllabus and extract topics\n"
            "  search    Search videos for a specific topic\n"
            "  history   Show recent syllabi and searches\n"
            "  export    Export results in various formats\n"
            "  review    Spaced repetition review system\n\n"
            "For help on a command, use: python syllabo.py [command] --help",
            style="bold"
        ))
import os
import sys
import asyncio
from typing import Optional, Dict, Any, List
import argparse

from src.cli.formatting import OutputFormatter
from src.cli.validation import InputValidator
from src.cli.error_handler import CLIErrorHandler, exit_gracefully
from src.cli.session_history import SessionHistory
from src.cli.commands import create_parser
from src.config import Config

class SyllaboApp:
    """Main CLI application controller"""

    def __init__(self):
        """Initialize the CLI application"""
        self.config = Config()
        self.formatter = OutputFormatter(self.config.cli_theme)
        self.error_handler = CLIErrorHandler(self.formatter)
        self.session_history = SessionHistory(self.config.export_directory)
        self.validator = InputValidator()

    async def run(self, args: Optional[List[str]] = None) -> None:
        """Run the CLI application

        Args:
            args: Command-line arguments (uses sys.argv if None)
        """
        # Parse arguments
        parser = create_parser()

        if args is None:
            # Use sys.argv for standalone execution
            parsed_args = parser.parse_args()
        else:
            # Use provided args for integration with other code
            parsed_args = parser.parse_args(args)

        # Set up debug mode if requested
        if hasattr(parsed_args, 'debug') and parsed_args.debug:
            self.error_handler.set_debug_mode(True)

        # Check API keys and show warning if needed
        self._check_api_keys()

        # Handle commands
        try:
            # Track command in session history
            command_result = "Command started"
            self.session_history.add_command(
                parsed_args.command,
                vars(parsed_args),
                command_result
            )

            # Validate input based on command
            self._validate_command_args(parsed_args)

            # Handle interactive mode
            if parsed_args.command == 'interactive':
                from src.cli.interactive import InteractiveShell
                from src.syllabus_parser import SyllabusParser
                from src.youtube_client import YouTubeClient
                from src.ai_client import AIClient
                from src.video_analyzer import VideoAnalyzer
                from src.database import SyllaboDatabase
                from src.spaced_repetition import SpacedRepetitionEngine

                # Create main application components for interactive mode
                db = SyllaboDatabase()
                ai_client = AIClient()
                youtube_client = YouTubeClient()
                video_analyzer = VideoAnalyzer(ai_client)
                syllabus_parser = SyllabusParser()
                spaced_repetition = SpacedRepetitionEngine()

                # Create CLI instance
                from syllabo_enhanced import EnhancedSyllaboCLI
                cli = EnhancedSyllaboCLI()

                # Run interactive shell
                shell = InteractiveShell(cli, parsed_args.theme)
                await shell.run()
                return

            # For non-interactive commands, import and run CLI
            from syllabo_enhanced import EnhancedSyllaboCLI
            cli = EnhancedSyllaboCLI()

            # Show progress indicator for long-running commands
            with self.formatter.console.status(f"Running {parsed_args.command} command..."):
                result = await cli.run(parsed_args)

            # Update session history with result
            self.session_history.add_command(
                parsed_args.command,
                vars(parsed_args),
                "Command completed successfully"
            )

            # Show command summary if appropriate
            if hasattr(parsed_args, 'show_summary') and parsed_args.show_summary:
                self._show_command_summary(parsed_args, result)

            # Handle session export if requested
            if hasattr(parsed_args, 'export_session') and parsed_args.export_session:
                self._export_session_history(parsed_args)

        except Exception as e:
            # Handle and display error
            self.error_handler._display_error(e)

            # Update session history with error
            self.session_history.add_command(
                parsed_args.command if hasattr(parsed_args, 'command') else "unknown",
                vars(parsed_args) if parsed_args else {},
                f"Error: {str(e)}"
            )

            # Exit with error code
            sys.exit(1)

    def _check_api_keys(self) -> None:
        """Check if required API keys are configured"""
        api_keys = self.config.get_api_keys()
        api_status = self.config.validate_api_keys()

        # Show warning if YouTube API key is missing
        if not api_status.get('youtube', False):
            self.formatter.print_warning(
                "YouTube API key not configured. Some features may use mock data."
            )
            self.formatter.print_info(
                "Add YOUTUBE_API_KEY to your .env file for full functionality."
            )

        # Show warning if AI API key is missing
        if not api_status.get('gemini', False):
            self.formatter.print_warning(
                "Gemini API key not configured. AI features may be limited."
            )
            self.formatter.print_info(
                "Add GEMINI_API_KEY to your .env file for full AI functionality."
            )

    def _validate_command_args(self, args: argparse.Namespace) -> None:
        """Validate command arguments based on command type

        Args:
            args: Parsed command arguments

        Raises:
            ValueError: If validation fails
        """
        if args.command == 'analyze':
            is_valid, error = self.validator.validate_analyze_args(vars(args))
            if not is_valid:
                raise ValueError(error)

        elif args.command == 'search':
            is_valid, error = self.validator.validate_search_args(vars(args))
            if not is_valid:
                raise ValueError(error)

        elif args.command == 'review' and hasattr(args, 'review_action'):
            is_valid, error = self.validator.validate_review_args(vars(args))
            if not is_valid:
                raise ValueError(error)

    def _show_command_summary(self, args: argparse.Namespace, result: Any) -> None:
        """Show a summary panel after command execution

        Args:
            args: Command arguments
            result: Command execution result
        """
        summary_data = {}

        # Build summary based on command type
        if args.command == 'analyze':
            source = args.file if hasattr(args, 'file') and args.file else 'text input'
            summary_data = {
                'Command': 'Analyze Syllabus',
                'Source': source,
                'Videos Searched': 'Yes' if args.search_videos else 'No',
                'Topics Found': result.get('topic_count', 'N/A'),
                'Videos Found': result.get('video_count', 'N/A'),
                'Processing Time': f"{result.get('processing_time', 0):.2f}s"
            }

        elif args.command == 'search':
            summary_data = {
                'Command': 'Search Videos',
                'Topic': args.topic,
                'Videos Found': result.get('video_count', 'N/A'),
                'Quality Videos': result.get('quality_video_count', 'N/A'),
                'Processing Time': f"{result.get('processing_time', 0):.2f}s"
            }

        elif args.command == 'review':
            action = args.review_action if hasattr(args, 'review_action') else 'unknown'
            summary_data = {
                'Command': f'Review - {action}',
                'Status': result.get('status', 'completed'),
                'Topics Affected': result.get('topics_affected', 'N/A'),
            }

        # Display the summary panel
        if summary_data:
            self.formatter.print_summary_panel("Command Summary", summary_data)

    def _export_session_history(self, args: argparse.Namespace) -> None:
        """Export session history if requested

        Args:
            args: Command arguments
        """
        format_type = getattr(args, 'export_format', 'json')

        # Show preview if requested
        if hasattr(args, 'preview') and args.preview:
            preview = self.session_history.get_session_preview()
            self.formatter.create_panel("Session History Preview", preview)

            # Confirm export
            if not self.formatter.confirm_action("Export session history?"):
                self.formatter.print_info("Export cancelled")
                return

        # Export the session history
        exported_file = self.session_history.export_session(format_type)
        self.formatter.print_success(f"Session history exported to: {exported_file}")


def main():
    """Main entry point for the CLI application"""
    app = SyllaboApp()
    try:
        asyncio.run(app.run())
    except KeyboardInterrupt:
        # Handle Ctrl+C gracefully
        formatter = OutputFormatter()
        exit_gracefully(formatter, "Operation cancelled by user", error=False)
    except Exception as e:
        # Handle unexpected errors
        formatter = OutputFormatter()
        exit_gracefully(formatter, f"Unexpected error: {e}", error=True)


if __name__ == "__main__":
    main()