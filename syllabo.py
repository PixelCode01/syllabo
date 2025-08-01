#!/usr/bin/env python3

# Standard library imports
import os
import sys
import json
import argparse
import asyncio
import time
from datetime import datetime
from typing import List, Dict, Any, Optional

# Third-party imports
from dotenv import load_dotenv
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.rule import Rule
from rich.progress import Progress

# Load environment variables from .env file
load_dotenv()

# Add src directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

# Local imports
from src.syllabus_parser import SyllabusParser
from src.youtube_client import YouTubeClient
from src.ai_client import AIClient
from src.video_analyzer import VideoAnalyzer
from src.database import SyllaboDatabase
from src.logger import SyllaboLogger
from src.spaced_repetition import SpacedRepetitionEngine
from src.notification_system import NotificationSystem
from src.quiz_generator import QuizGenerator
from src.progress_dashboard import ProgressDashboard
from src.goals_manager import GoalsManager
from src.platform_integrator import PlatformIntegrator
from src.podcast_integrator import PodcastIntegrator
from src.bookmark_manager import BookmarkManager
from src.difficulty_analyzer import DifficultyAnalyzer
from src.study_session_manager import StudySessionManager
from src.cli.formatting import OutputFormatter
from src.cli.error_handler import CLIErrorHandler
from src.cli.session_history import SessionHistory
from src.cli.validation import InputValidator

class EnhancedSyllaboCLI: 
    def __init__(self, 
                 logger=None, 
                 db=None, 
                 ai_client=None, 
                 youtube_client=None, 
                 video_analyzer=None, 
                 syllabus_parser=None,
                 spaced_repetition=None,
                 notifications=None,
                 theme='minimal'):
        """Initialize the CLI with dependencies

        Args:
            logger: Optional logger instance
            db: Optional database instance
            ai_client: Optional AI client instance
            youtube_client: Optional YouTube client instance
            video_analyzer: Optional video analyzer instance
            syllabus_parser: Optional syllabus parser instance
            spaced_repetition: Optional spaced repetition engine instance
            notifications: Optional notification system instance
            theme: UI theme (minimal or high-contrast)
        """
        # Use provided instances or create new ones
        self.logger = logger or SyllaboLogger("cli")
        self.db = db or SyllaboDatabase()
        self.ai_client = ai_client or AIClient()
        self.youtube_client = youtube_client or YouTubeClient()
        self.video_analyzer = video_analyzer or VideoAnalyzer(self.ai_client)
        self.syllabus_parser = syllabus_parser or SyllabusParser()
        self.spaced_repetition = spaced_repetition or SpacedRepetitionEngine()
        self.notifications = notifications or NotificationSystem()

        # Initialize formatting and UI components
        self.formatter = OutputFormatter(theme)
        self.console = self.formatter.console
        self.error_handler = CLIErrorHandler(self.formatter)
        self.session_history = SessionHistory()
        
        # Initialize export system
        from src.export_system import ExportSystem
        self.exporter = ExportSystem()
        
        # Initialize new feature systems
        self.quiz_generator = QuizGenerator(self.ai_client, self.db)
        self.progress_dashboard = ProgressDashboard(self.db, self.spaced_repetition)
        self.goals_manager = GoalsManager(self.db)
        self.platform_integrator = PlatformIntegrator()
        self.podcast_integrator = PodcastIntegrator()
        self.bookmark_manager = BookmarkManager()
        self.difficulty_analyzer = DifficultyAnalyzer(self.ai_client)
        self.study_session_manager = StudySessionManager(self.spaced_repetition)
    
    def print_banner(self):
        self.console.print(Panel.fit("[bold cyan]SYLLABO ENHANCED[/bold cyan]", subtitle="AI-Powered Educational Resource Finder"))
    
    async def run(self, args) -> Dict[str, Any]:
        """Run the CLI with the given arguments

        Args:
            args: Parsed command line arguments

        Returns:
            Dictionary with command execution results
        """
        self.print_banner()
        analyze = self.error_handler.handle_async_command_error(self.analyze_syllabus)
        search = self.error_handler.handle_async_command_error(self.search_videos)
        export = self.error_handler.handle_async_command_error(self.export_results)

        result = {}

        try:
            if args.command == 'analyze':
                result = await analyze(args)
            elif args.command == 'search':
                result = await search(args)
            elif args.command == 'history':
                result = self.show_history(args)
            elif args.command == 'export':
                result = await export(args)
            elif args.command == 'review':
                result = self.handle_review_commands(args)
            elif args.command == 'ai-status':
                result = await self.handle_ai_status(args)
            else:
                self.show_help()
                result = {'status': 'help_displayed'}

            return result or {'status': 'completed'}

        except Exception as e:
            self.error_handler._display_error(e)
            return {'status': 'error', 'error_message': str(e)}
            
    async def analyze_syllabus(self, args) -> Dict[str, Any]:
        """Analyze syllabus and extract topics

        Args:
            args: Command-line arguments

        Returns:
            Dictionary with analysis results
        """
        start_time = time.time()
        result = {
            'status': 'started',
            'syllabus_title': None,
            'topic_count': 0,
            'video_count': 0,
            'missing_topics': [],
            'processing_time': 0
        }

        # Create progress for better user feedback
        progress = self.formatter.create_progress_bar()

        with progress:
            # Task for overall progress
            main_task = progress.add_task("[bold blue]Analyzing syllabus...", total=100)

            # 1. Load syllabus content
            progress.update(main_task, advance=10, description="[bold blue]Loading syllabus content...")

            if args.file:
                is_valid, error = InputValidator.validate_file_path(args.file)
                if not is_valid:
                    self.formatter.print_error(error)
                    return {'status': 'error', 'error': error}

                self.formatter.print_info(f"Loading syllabus from file: {args.file}")
                syllabus_content = self.syllabus_parser.load_from_file(args.file)
                syllabus_title = os.path.basename(args.file)
            elif args.text:
                syllabus_content = args.text
                syllabus_title = f"Direct input - {datetime.now().strftime('%Y-%m-%d %H:%M')}"
                self.formatter.print_info("Analyzing provided text content...")
            else:
                self.formatter.print_error("Please provide either --file or --text")
                return {'status': 'error', 'error': 'No input provided'}

            result['syllabus_title'] = syllabus_title

            # 2. Extract topics using AI
            progress.update(main_task, advance=20, description="[bold blue]Extracting topics using AI...")
            topics = await self.syllabus_parser.extract_topics(syllabus_content, self.ai_client)
            result['topic_count'] = len(topics)

            # 3. Identify potentially missed topics
            progress.update(main_task, advance=10, description="[bold blue]Identifying missed topics...")
            missing_topics = await self._identify_missing_topics(syllabus_content, topics)
            result['missing_topics'] = missing_topics

            # Show topic analysis summary
            self.formatter.print_title(f"Topic Analysis Summary for: {syllabus_title}")
            self.formatter.print_success(f"Found {len(topics)} topics")

            if missing_topics:
                self.formatter.print_info(f"Potentially missed topics: {', '.join(missing_topics[:3])}")

            if not topics:
                self.formatter.print_warning("No clear topics found. Try refining your syllabus content.")
                result['status'] = 'completed_no_topics'
                result['processing_time'] = time.time() - start_time
                return result

            # 4. Save to database
            progress.update(main_task, advance=10, description="[bold blue]Saving to database...")
            syllabus_id = self.db.save_syllabus(syllabus_title, syllabus_content)
            topic_ids = self.db.save_topics(syllabus_id, topics)
            result['syllabus_id'] = syllabus_id

            # 5. Search for videos if requested
            if args.search_videos:
                progress.update(main_task, advance=10, description="[bold blue]Searching for videos...")
                topic_results = await self.search_for_topics_enhanced(topics, topic_ids, args.max_videos, progress, main_task)

                total_videos = sum(len(videos) for videos in topic_results.values())
                result['video_count'] = total_videos
                if args.print_results:
                    self.print_video_results(topic_results, args.max_videos)
                if args.save or args.export_format:
                    # Preview export if requested
                    if args.preview:
                        should_export = self.formatter.show_export_preview(
                            topic_results, 
                            args.export_format or 'json'
                        )
                        if not should_export:
                            self.formatter.print_info("Export cancelled by user")
                        else:
                            await self.save_comprehensive_results(topic_results, syllabus_title, args.export_format or 'json')
                    else:
                        await self.save_comprehensive_results(topic_results, syllabus_title, args.export_format or 'json')

                # Add topics to spaced repetition if requested
                if args.add_to_review:
                    progress.update(main_task, advance=10, description="[bold blue]Adding topics to review schedule...")
                    added_count = self.add_topics_to_spaced_repetition(topics)
                    result['topics_added_to_review'] = added_count
            else:
                # Still offer to add topics to spaced repetition
                if args.add_to_review:
                    progress.update(main_task, advance=20, description="[bold blue]Adding topics to review schedule...")
                    added_count = self.add_topics_to_spaced_repetition(topics)
                    result['topics_added_to_review'] = added_count

                self.formatter.print_info("To search for videos, add --search-videos flag")
                self.formatter.print_info("To see results in terminal, add --print-results flag")

            # Complete progress
            progress.update(main_task, completed=100, description="[bold green]Analysis completed!")

        # Calculate final processing time
        processing_time = time.time() - start_time
        result['processing_time'] = processing_time
        result['status'] = 'completed'

        # Show final summary
        video_info = f", {result['video_count']} videos found" if args.search_videos else ""
        self.formatter.print_success(
            f"Completed analysis: {len(topics)} topics{video_info} in {processing_time:.1f}s"
        )

        return result
        
    async def search_for_topics_enhanced(self, topics: List[Dict], topic_ids: List[int], max_videos: int, 
                                progress=None, parent_task=None) -> Dict[str, List[Dict]]:
        """Search for videos and playlists across all topics

        Args:
            topics: List of topic dictionaries
            topic_ids: List of topic database IDs
            max_videos: Maximum videos to find per topic
            progress: Optional progress bar instance to use
            parent_task: Optional parent task ID for nested progress
        
        Returns:
            Dictionary mapping topic names to lists of video/playlist resources
        """
        all_results = {}

        # Validate input
        if not topics or not topic_ids:
            self.formatter.print_warning("No topics provided for search")
            return all_results

        if len(topics) != len(topic_ids):
            self.formatter.print_warning("Topic list and ID list length mismatch")
            return all_results
            
        # Create progress bar if not provided
        using_external_progress = progress is not None
        if not progress:
            progress = self.formatter.create_progress_bar()

        # Start progress tracking
        with progress if not using_external_progress else progress.dummy():
            # Create search task
            search_task = progress.add_task(
                "[cyan]Searching for videos and playlists...", 
                total=len(topics)
            )

            # Update parent task if provided
            if parent_task:
                progress.update(parent_task, advance=10, description="[bold blue]Searching for videos...")

            # Process each topic
            for i, (topic, topic_id) in enumerate(zip(topics, topic_ids)):
                topic_name = topic['name']
                progress.update(
                    search_task, 
                    advance=1, 
                    description=f"[cyan]Searching for: {topic_name} ({i+1}/{len(topics)})"
                )

                try:
                    # Create enhanced search query
                    enhanced_query = self._enhance_search_query(topic_name, topic.get('subtopics', []))

                    # Search both videos and playlists
                    videos = await self.youtube_client.search_videos(enhanced_query, max_videos)
                    playlists = await self.youtube_client.search_playlists(enhanced_query, max(2, max_videos // 3))

                    if videos or playlists:
                        # Update progress
                        progress.update(
                            search_task, 
                            description=f"[cyan]Analyzing content for: {topic_name} ({i+1}/{len(topics)})"
                        )

                        # Use the comprehensive analysis method
                        analysis_result = await self.video_analyzer.analyze_videos_and_playlists(videos, playlists, topic_name)

                        # Extract all resources from the analysis result
                        all_resources = []

                        # Add primary resource
                        if analysis_result.get('primary_resource'):
                            all_resources.append(analysis_result['primary_resource'])

                        # Add supplementary videos
                        all_resources.extend(analysis_result.get('supplementary_videos', []))

                        # Add supplementary playlists
                        all_resources.extend(analysis_result.get('supplementary_playlists', []))

                        # Filter for quality
                        quality_resources = [r for r in all_resources if r.get('relevance_score', 0) >= 4.0]

                        # Update progress
                        progress.update(
                            search_task, 
                            description=f"[cyan]Saving {len(quality_resources)} resources for: {topic_name}"
                        )

                        # Save to database
                        for resource in quality_resources:
                            self.db.save_video(resource)  # This method can handle both videos and playlists
                            self.db.link_topic_video(topic_id, resource['id'], resource['relevance_score'])

                        all_results[topic_name] = quality_resources

                        # Show mini summary in progress
                        progress.update(
                            search_task, 
                            description=f"[green]Found {len(quality_resources)} resources for: {topic_name}"
                        )
                    else:
                        self.formatter.print_warning(f"No videos or playlists found for '{topic_name}'")
                        all_results[topic_name] = []

                except Exception as e:
                    self.logger.error(f"Failed to search resources for {topic_name}: {e}")
                    self.formatter.print_error(f"Error searching for '{topic_name}': {str(e)}")
                    all_results[topic_name] = []

            # Update parent task if provided
            if parent_task:
                progress.update(parent_task, advance=10, description="[bold blue]Search completed")

        return all_results
        
    async def search_videos(self, args):
        """Search for videos and playlists for a specific topic"""
        if not args.topic:
            self.formatter.print_error("Please provide a topic to search for")
            return
        
        start_time = time.time()
        self.formatter.print_info(f"Searching videos and playlists for: {args.topic}")
        
        enhanced_query = f"{args.topic} tutorial explained"
        videos = await self.youtube_client.search_videos(enhanced_query, args.max_videos)
        playlists = await self.youtube_client.search_playlists(enhanced_query, max(2, args.max_videos // 3))
        
        if not videos and not playlists:
            self.formatter.print_warning("No videos or playlists found")
            self.formatter.print_info("Try a different topic name or check your internet connection")
            return
        
        self.formatter.print_info(f"Found {len(videos)} videos and {len(playlists)} playlists, analyzing with AI...")
        
        analysis_result = await self.video_analyzer.analyze_videos_and_playlists(videos, playlists, args.topic)
        
        # Extract all resources from the analysis result
        all_resources = []
        
        # Add primary resource
        if analysis_result.get('primary_resource'):
            all_resources.append(analysis_result['primary_resource'])
        all_resources.extend(analysis_result.get('supplementary_videos', []))
        
        # Add supplementary playlists
        all_resources.extend(analysis_result.get('supplementary_playlists', []))
        
        quality_resources = [r for r in all_resources if r.get('relevance_score', 0) >= 3.0]
        
        if not quality_resources:
            self.formatter.print_warning("No high-quality resources found for this topic")
            self.formatter.print_info("Try refining your topic or search for a broader term")
            return
        
        topic_results = {args.topic: quality_resources}
        
        self.print_video_results(topic_results, min(args.max_videos, 10))
        
        processing_time = time.time() - start_time
        self.formatter.print_success(f"Completed search: 1 topic, {len(quality_resources)} videos found in {processing_time:.1f}s")
        
        if args.save:
            await self.save_video_results(quality_resources, args.topic, args.export_format or 'json')
            
    async def _identify_missing_topics(self, syllabus_content: str, found_topics: List[Dict]) -> List[str]:
        """Identify topics that might have been missed by AI extraction"""
        # Use AI to identify potentially missed topics
        found_topic_names = [t['name'] for t in found_topics]
        found_topics_str = ", ".join(found_topic_names)
        
        prompt = f"""Analyze this syllabus content and identify any important topics that might have been missed.
        
Already found topics: {found_topics_str}

Syllabus content:
{syllabus_content[:1500]}

List any additional important topics that seem to be mentioned but weren't captured in the found topics.
Respond with a simple list, one topic per line, or "None" if no additional topics are found."""
        
        try:
            response = await self.ai_client.get_completion(prompt)
            if response.strip().lower() == "none" or "error:" in response.lower():
                return []
            
            # Parse the response into a list
            missing_topics = [line.strip() for line in response.split('\n') if line.strip() and not line.strip().startswith('-')]
            return missing_topics[:5]  # Limit to 5 additional topics
        except Exception as e:
            self.logger.error(f"Failed to identify missing topics: {e}")
            return []
            
    def print_video_results(self, topic_results: Dict[str, List[Dict]], max_videos: int) -> None:
        """Display video results in a formatted table
        
        Args:
            topic_results: Dictionary mapping topic names to lists of video resources
            max_videos: Maximum number of videos to display per topic
        """
        self.console.print(Rule("Top Video Recommendations"))
        
        for topic_name, videos in topic_results.items():
            if not videos:
                continue
                
            self.console.print(Panel(f"{topic_name}", expand=False, style="bold"))
            
            table = Table(show_header=True, header_style="bold magenta", expand=True)
            table.add_column("No.", style="dim", width=4)
            table.add_column("Title", style="cyan", min_width=20)
            table.add_column("Channel", style="yellow")
            table.add_column("Score", justify="right", style="green")
            table.add_column("URL", style="blue")
            
            for i, video in enumerate(videos[:max_videos], 1):
                resource_type = video.get('type', 'video')
                url = f"https://youtube.com/watch?v={video.get('id', '')}" if resource_type == 'video' else f"https://youtube.com/playlist?list={video.get('id', '')}"
                
                table.add_row(
                    str(i),
                    f"[{'PLAYLIST' if resource_type == 'playlist' else ''}] {video.get('title', 'Unknown Title')[:60]}",
                    video.get('channel', 'Unknown Channel'),
                    f"{video.get('relevance_score', 0):.1f}/10",
                    url
                )
                
            self.console.print(table)
    
    async def save_video_results(self, videos: List[Dict], topic: str, format_type: str = 'json'):
        """Save video results to a file using the export system
        
        Args:
            videos: List of video resources to save
            topic: The topic name for the videos
            format_type: Export format (json, csv, md, html)
            
        Returns:
            Dictionary with status and filename or error message
        """
        try:
            filename = self.exporter.export_to_file(videos, topic, format_type)
            self.formatter.print_success(f"Results saved to: {filename}")
            return {'status': 'success', 'filename': filename}
        except Exception as e:
            self.logger.error(f"Failed to save results: {e}")
            self.formatter.print_error(f"Failed to save results: {e}")
            return {'status': 'error', 'error': str(e)}
            
    async def save_comprehensive_results(self, topic_results: Dict[str, List[Dict]], syllabus_title: str, format_type: str = 'json'):
        """Save comprehensive results for all topics to a file
        
        Args:
            topic_results: Dictionary mapping topic names to lists of video resources
            syllabus_title: The title of the syllabus
            format_type: Export format (json, csv, md, html)
            
        Returns:
            Dictionary with status and filename or error message
        """
        try:
            filename = self.exporter.export_comprehensive(topic_results, format_type)
            self.formatter.print_success(f"Comprehensive results saved to: {filename}")
            return {'status': 'success', 'filename': filename}
        except Exception as e:
            self.logger.error(f"Failed to save comprehensive results: {e}")
            self.formatter.print_error(f"Failed to save comprehensive results: {e}")
            return {'status': 'error', 'error': str(e)}
            
    def add_topics_to_spaced_repetition(self, topics: List[Dict]) -> int:
        """Add topics to the spaced repetition system for scheduled review
        
        Args:
            topics: List of topic dictionaries with 'name' and optional 'description' keys
            
        Returns:
            Number of topics successfully added to the review schedule
        """
        added_count = 0
        for topic in topics:
            if self.spaced_repetition.add_topic(topic['name'], topic.get('description', '')):
                added_count += 1
                
        if added_count > 0:
            self.formatter.print_success(f"Added {added_count} topics to spaced repetition schedule")
            self.formatter.print_info("Use 'python syllabo.py review list' to see your review schedule")
        else:
            self.formatter.print_warning("All topics were already in your review schedule")
            
        return added_count
    
    def _enhance_search_query(self, topic_name: str, subtopics: List[str]) -> str:
        """Build better search query with subtopics
        
        Args:
            topic_name: The main topic name
            subtopics: List of subtopics related to the main topic
            
        Returns:
            Enhanced search query string limited to 100 characters
        """
        query_parts = [topic_name, "tutorial", "explained"]
        
        if subtopics:
            main_subtopic = subtopics[0]
            query_parts.insert(1, main_subtopic)
        
        enhanced_query = " ".join(query_parts)
        return enhanced_query[:100]
        
    async def export_results(self, args) -> Dict[str, Any]:
        """Export results for a specific syllabus
        
        Args:
            args: Command-line arguments with syllabus_id and format
            
        Returns:
            Dictionary with export status and details
        """
        if not args.syllabus_id:
            self.formatter.print_error("Please provide a syllabus ID to export.")
            self.show_history(type('obj', (object,), {'limit': 5})())
            return {'status': 'error', 'error': 'No syllabus ID provided'}
            
        self.formatter.print_info(f"Exporting results for syllabus ID: {args.syllabus_id}")
        
        syllabus = self.db.get_syllabus_by_id(args.syllabus_id)
        if not syllabus:
            self.formatter.print_error(f"Syllabus with ID {args.syllabus_id} not found.")
            return {'status': 'error', 'error': 'Syllabus not found'}
            
        topics = self.db.get_topics_by_syllabus_id(args.syllabus_id)
        if not topics:
            self.formatter.print_warning(f"No topics found for syllabus: {syllabus['title']}")
            return {'status': 'warning', 'message': 'No topics found'}
            
        topic_results = {topic['name']: self.db.get_topic_videos(topic['id']) for topic in topics}
        
        if not any(topic_results.values()):
            self.formatter.print_warning("No video results found for this syllabus.")
            return {'status': 'warning', 'message': 'No video results found'}
            
        return await self.save_comprehensive_results(topic_results, syllabus['title'], args.format)
        
    def handle_review_commands(self, args) -> Dict[str, Any]:
        """Handle spaced repetition review system commands
        
        Args:
            args: Command-line arguments with review_action
            
        Returns:
            Dictionary with command execution status
        """
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
            result = action(args)
            return result or {'status': 'completed'}
        else:
            self.show_review_help()
            return {'status': 'help_displayed'}
            
    def add_review_topic(self, args) -> Dict[str, Any]:
        """Add a topic to the spaced repetition system
        
        Args:
            args: Command-line arguments with topic and description
            
        Returns:
            Dictionary with operation status
        """
        if not args.topic:
            self.formatter.print_error("Please provide a topic name with --topic")
            return {'status': 'error', 'error': 'No topic provided'}
            
        if self.spaced_repetition.add_topic(args.topic, args.description or ""):
            self.formatter.print_success(f"Added '{args.topic}' to review schedule")
            return {'status': 'success', 'topic': args.topic}
        else:
            self.formatter.print_warning(f"Topic '{args.topic}' is already in your review schedule")
            return {'status': 'warning', 'message': 'Topic already exists'}
            
    def list_review_topics(self, args) -> Dict[str, Any]:
        """List all topics in the spaced repetition system
        
        Args:
            args: Command-line arguments
            
        Returns:
            Dictionary with operation status and topics
        """
        topics = self.spaced_repetition.get_all_topics()
        if not topics:
            self.formatter.print_warning("No topics in your review schedule")
            return {'status': 'warning', 'message': 'No topics found'}
            
        self.formatter.print_title("Your Review Schedule")
        
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Topic", style="cyan", width=30)
        table.add_column("Mastery", justify="center", width=12)
        table.add_column("Success Rate", justify="center", width=12)
        table.add_column("Next Review", justify="center", width=12)
        table.add_column("Interval", justify="center", width=10)
        
        # Safe sorting with None handling
        def safe_sort_key(topic):
            days = topic.get('days_until_review')
            return days if days is not None else 0
        
        for topic in sorted(topics, key=safe_sort_key):
            mastery_color = {'Learning': 'red', 'Beginner': 'yellow', 'Intermediate': 'blue', 
                             'Advanced': 'green', 'Mastered': 'bright_green'}.get(topic['mastery_level'], 'white')
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
        self.formatter.print_success(
            f"Summary: {summary['total_topics']} topics, {summary['due_now']} due now, {summary['mastered_topics']} mastered"
        )
        
        return {'status': 'success', 'topics': topics, 'summary': summary}
        
    def show_due_reviews(self, args) -> Dict[str, Any]:
        """Show topics that are due for review
        
        Args:
            args: Command-line arguments with notify option
            
        Returns:
            Dictionary with operation status and due topics
        """
        due_topics = self.spaced_repetition.get_due_topics()
        if not due_topics:
            self.formatter.print_success("No topics are due for review right now")
            return {'status': 'success', 'due_topics': []}
            
        self.formatter.print_title(f"You have {len(due_topics)} topic{'s' if len(due_topics) != 1 else ''} due for review")
        
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
            
        return {'status': 'success', 'due_topics': [t.__dict__ for t in due_topics]}
        
    def mark_topic_review(self, args) -> Dict[str, Any]:
        """Mark a topic as reviewed
        
        Args:
            args: Command-line arguments with topic and success flag
            
        Returns:
            Dictionary with operation status
        """
        if not args.topic:
            self.formatter.print_error("Please provide a topic name with --topic")
            return {'status': 'error', 'error': 'No topic provided'}
            
        if self.spaced_repetition.mark_review(args.topic, args.success):
            self.formatter.print_success(f"Marked '{args.topic}' as {'successful' if args.success else 'failed'} review")
            return {'status': 'success', 'topic': args.topic, 'success': args.success}
        else:
            self.formatter.print_warning(f"Topic '{args.topic}' not found in review schedule")
            return {'status': 'warning', 'message': 'Topic not found'}
            
    def show_review_stats(self, args) -> Dict[str, Any]:
        """Show statistics for the spaced repetition system
        
        Args:
            args: Command-line arguments with optional topic
            
        Returns:
            Dictionary with operation status and statistics
        """
        if args.topic:
            stats = self.spaced_repetition.get_topic_stats(args.topic)
            if not stats:
                self.formatter.print_warning(f"Topic '{args.topic}' not found")
                return {'status': 'warning', 'message': 'Topic not found'}
                
            panel = Panel(
                f"Mastery Level: {stats['mastery_level']}\n"
                f"Success Rate: {stats['success_rate']}%\n"
                f"Next Review: {stats['next_review_date']}",
                title=f"Stats for {stats['topic_name']}",
                expand=False
            )
            self.console.print(panel)
            return {'status': 'success', 'stats': stats}
        else:
            summary = self.spaced_repetition.get_study_summary()
            
            table = Table(show_header=True, header_style="bold magenta")
            table.add_column("Metric", style="cyan")
            table.add_column("Value", style="yellow")
            table.add_row("Total Topics", str(summary['total_topics']))
            table.add_row("Mastered Topics", str(summary['mastered_topics']))
            table.add_row("Average Success Rate", f"{summary['average_success_rate']}%")
            
            self.console.print(Panel(table, title="Overall Review Statistics", expand=False))
            return {'status': 'success', 'summary': summary}
            
    def remove_review_topic(self, args) -> Dict[str, Any]:
        """Remove a topic from the spaced repetition system
        
        Args:
            args: Command-line arguments with topic
            
        Returns:
            Dictionary with operation status
        """
        if not args.topic:
            self.formatter.print_error("Please provide a topic name with --topic")
            return {'status': 'error', 'error': 'No topic provided'}
            
        if self.spaced_repetition.remove_topic(args.topic):
            self.formatter.print_success(f"Removed '{args.topic}' from review schedule")
            return {'status': 'success', 'topic': args.topic}
        else:
            self.formatter.print_warning(f"Topic '{args.topic}' not found")
            return {'status': 'warning', 'message': 'Topic not found'}
            
    def show_help(self):
        """Display a help panel with available commands."""
        self.console.print(Panel.fit(
            '[bold cyan]Welcome to Syllabo Enhanced![/bold cyan]\n\n' 
            'Your AI-powered assistant for discovering educational content on YouTube. \n\n' 
            'To get started, choose one of the commands below. For detailed options, add [cyan]--help[/cyan] to any command.',
            title='[bold]Syllabo Enhanced[/bold]', 
            subtitle='[italic]AI-Powered Educational Resource Finder[/italic]',
            border_style='blue'
        ))

        table = Table(show_header=True, header_style="bold magenta", box=None)
        table.add_column("Command", style="cyan", no_wrap=True, width=15)
        table.add_column("Description", style="white")

        table.add_row("interactive", "Launch the interactive shell for a guided experience.")
        table.add_row("analyze", "Analyze a syllabus from a file or text to extract key topics.")
        table.add_row("search", "Find educational videos on a specific topic.")
        table.add_row("history", "View a history of your past syllabus analyses.")
        table.add_row("export", "Export your syllabus analysis results to various formats.")
        table.add_row("review", "Manage your spaced repetition study schedule.")
        table.add_row("ai-status", "Check AI service status and test functionality.")
        
        self.console.print(table)
        
    def show_review_help(self):
        """Show help for review commands"""
        review_help_panel = Panel(
            "Review commands:\n  add, list, due, mark, stats, remove\n"
            "Use 'python syllabo.py review [command]' for details.",
            title="Review Help",
            border_style="bold blue"
        )
        self.console.print(review_help_panel)
        
    def show_history(self, args):
        """Show history of recent syllabi"""
        self.console.print(Panel("Recent Syllabi", style="bold"))
        recent_syllabi = self.db.get_recent_syllabi(args.limit)
        if not recent_syllabi:
            self.formatter.print_warning("No syllabi found in database")
            return
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("ID", style="dim", width=6)
        table.add_column("Title")
        table.add_column("Created At", justify="right")
        for syllabus in recent_syllabi:
            table.add_row(str(syllabus['id']), syllabus['title'], syllabus['created_at'])
        self.console.print(table)

    async def handle_ai_status(self, args) -> Dict[str, Any]:
        """Handle AI status and testing commands
        
        Args:
            args: Command-line arguments with test and verbose flags
            
        Returns:
            Dictionary with command execution status
        """
        self.formatter.print_title("AI Services Status")
        
        # Show service configuration
        if args.verbose:
            self.console.print(Panel(
                self.ai_client.get_service_status(),
                title="Service Configuration",
                border_style="blue"
            ))
            self.console.print()
        
        if args.test:
            # Run comprehensive tests
            self.formatter.print_info("Testing all AI services...")
            
            with Progress() as progress:
                task = progress.add_task("Testing services...", total=100)
                
                # Test services
                service_results = await self.ai_client.test_services()
                progress.update(task, advance=50)
                
                # Test functionality
                test_results = await self._test_ai_functionality()
                progress.update(task, advance=50)
            
            # Display results
            self._display_service_results(service_results)
            self._display_functionality_results(test_results)
            
            return {
                'status': 'success',
                'service_results': service_results,
                'test_results': test_results
            }
        else:
            # Quick status check
            service_results = await self.ai_client.test_services()
            self._display_service_results(service_results)
            
            return {
                'status': 'success',
                'service_results': service_results
            }
    
    async def _test_ai_functionality(self) -> Dict[str, bool]:
        """Test different AI functionality types"""
        test_cases = {
            'Topic Extraction': 'Extract topics from: Python programming covers variables, functions, and data structures.',
            'Relevance Rating': 'Rate relevance of "Python Tutorial" to topic "Python Programming"',
            'Content Analysis': 'Analyze this content: Machine learning uses algorithms to find patterns in data.',
            'Difficulty Assessment': 'Assess difficulty: Advanced neural network optimization techniques'
        }
        
        results = {}
        for test_name, prompt in test_cases.items():
            try:
                result = await self.ai_client.get_completion(prompt)
                results[test_name] = not result.startswith("Error:")
            except:
                results[test_name] = False
        
        return results
    
    def _display_service_results(self, service_results: Dict[str, bool]):
        """Display service test results in a table"""
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Service", style="cyan", width=20)
        table.add_column("Status", justify="center", width=15)
        table.add_column("Description", style="dim")
        
        service_descriptions = {
            'Gemini': 'Google Gemini API (requires API key)',
            'HackClub AI': 'Free AI service for educational use',
            'Free GPT': 'Community-maintained free GPT service',
            'GPT4Free': 'Open-source free AI service',
            'Intelligent Fallback': 'Local text analysis algorithms'
        }
        
        for service, status in service_results.items():
            status_text = "[green]✓ Working[/green]" if status else "[red]✗ Failed[/red]"
            description = service_descriptions.get(service, "AI service")
            table.add_row(service, status_text, description)
        
        self.console.print(table)
    
    def _display_functionality_results(self, test_results: Dict[str, bool]):
        """Display functionality test results"""
        self.console.print()
        self.formatter.print_title("Functionality Tests")
        
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Function", style="cyan", width=20)
        table.add_column("Status", justify="center", width=15)
        
        for function, status in test_results.items():
            status_text = "[green]✓ Working[/green]" if status else "[red]✗ Failed[/red]"
            table.add_row(function, status_text)
        
        self.console.print(table)
        
        # Summary
        working_count = sum(test_results.values())
        total_count = len(test_results)
        
        if working_count == total_count:
            self.formatter.print_success(f"All {total_count} AI functions are working correctly")
        elif working_count > 0:
            self.formatter.print_warning(f"{working_count}/{total_count} AI functions are working")
        else:
            self.formatter.print_error("No AI functions are working - using fallback algorithms only")


async def main():
    """Main entry point for the application"""
    from src.cli.commands import create_parser
    
    # Create argument parser
    parser = create_parser()
    args = parser.parse_args()
    
    # Initialize CLI
    cli = EnhancedSyllaboCLI()
    
    try:
        # Run the CLI with parsed arguments
        result = await cli.run(args)
        return result
    except KeyboardInterrupt:
        print("\nOperation cancelled by user")
        return {"status": "cancelled"}
    except Exception as e:
        print(f"\nError: {str(e)}")
        return {"status": "error", "error": str(e)}


if __name__ == "__main__":
    # Run the main function
    asyncio.run(main())