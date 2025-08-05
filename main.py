#!/usr/bin/env python3
"""
Syllabo - AI-Powered Learning Assistant
Main entry point for all features
"""

import os
import sys
import asyncio
from dotenv import load_dotenv
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.rule import Rule
from rich.prompt import Prompt
from rich.text import Text
from rich.align import Align

load_dotenv()
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

# Import components
from src.database import SyllaboDatabase
from src.logger import SyllaboLogger
from src.ai_client import AIClient
from src.syllabus_parser import SyllabusParser
from src.quiz_generator import QuizGenerator
from src.progress_dashboard import ProgressDashboard
from src.goals_manager import GoalsManager
from src.platform_integrator import PlatformIntegrator
from src.bookmark_manager import BookmarkManager
from src.study_session_manager import StudySessionManager
from src.spaced_repetition import SpacedRepetitionEngine

class SyllaboMain:
    """Main application class with all features"""
    
    def __init__(self):
        self.console = Console()
        self.logger = SyllaboLogger("main")
        
        # Initialize core components
        self.db = SyllaboDatabase()
        self.ai_client = AIClient()
        self.syllabus_parser = SyllabusParser()
        
        # Initialize feature modules
        self.spaced_repetition = SpacedRepetitionEngine()
        self.quiz_generator = QuizGenerator(self.ai_client, self.db)
        self.progress_dashboard = ProgressDashboard(self.db, self.spaced_repetition)
        self.goals_manager = GoalsManager(self.db)
        self.platform_integrator = PlatformIntegrator()
        self.bookmark_manager = BookmarkManager()
        self.study_session_manager = StudySessionManager(self.spaced_repetition)
    
    def print_banner(self):
        """Print enhanced application banner"""
        banner_text = Text()
        banner_text.append("SYLLABO", style="bold cyan")
        banner_text.append("\n")
        banner_text.append("AI-Powered Learning Assistant", style="bold white")
        banner_text.append("\n")
        banner_text.append("Your comprehensive educational resource manager", style="dim")
        
        banner_panel = Panel(
            Align.center(banner_text),
            border_style="bright_cyan",
            padding=(1, 2),
            title="[bold bright_blue]Welcome[/bold bright_blue]",
            title_align="center"
        )
        
        self.console.print(banner_panel)
        self.console.print("[dim]Ready to start learning![/dim]")
        self.console.print()
    
    def show_interactive_menu(self):
        """Show interactive main menu with all options"""
        self.console.print(Rule("[bold bright_cyan]Main Menu[/bold bright_cyan]", style="bright_cyan"))
        
        menu_options = [
            ("1", "analyze", "Analyze Syllabus", "Process syllabus and find learning resources"),
            ("2", "quiz", "Interactive Quizzes", "Generate and take quizzes from content"),
            ("3", "progress", "Progress Dashboard", "View learning progress and analytics"),
            ("4", "goals", "Study Goals", "Manage learning goals and milestones"),
            ("5", "platforms", "Multi-Platform Search", "Search across learning platforms"),
            ("6", "bookmarks", "Smart Bookmarks", "Manage video bookmarks and notes"),
            ("7", "session", "Study Sessions", "Pomodoro timer and focus sessions"),
            ("8", "review", "Spaced Repetition", "Review topics using spaced repetition"),
            ("9", "help", "Help & Documentation", "Get help and usage information"),
            ("0", "exit", "Exit", "Exit the application")
        ]
        
        # Create menu table
        menu_table = Table(
            show_header=True, 
            header_style="bold bright_magenta",
            border_style="bright_blue",
            title="[bold bright_white]Choose Your Action[/bold bright_white]",
            title_style="bold bright_white"
        )
        menu_table.add_column("Option", style="bright_cyan", width=8, justify="center")
        menu_table.add_column("Feature", style="bright_green", width=22)
        menu_table.add_column("Description", style="bright_white", width=45)
        
        for option, cmd, feature, desc in menu_options:
            menu_table.add_row(option, feature, desc)
        
        self.console.print(menu_table)
        self.console.print()
        
        return self._get_user_choice(menu_options)
    
    def _get_user_choice(self, menu_options):
        """Get user menu choice with validation"""
        valid_choices = [option[0] for option in menu_options]
        
        while True:
            try:
                choice = Prompt.ask(
                    "[bold bright_yellow]Select an option[/bold bright_yellow]",
                    choices=valid_choices,
                    default="1",
                    show_choices=False
                )
                
                for option, cmd, feature, desc in menu_options:
                    if choice == option:
                        self.console.print(f"[bright_green]Selected:[/bright_green] {feature}")
                        return cmd
                        
            except KeyboardInterrupt:
                self.console.print("\n[yellow]Operation cancelled[/yellow]")
                return "exit"
            except Exception as e:
                self.console.print(f"[red]Error: {e}[/red]")
                continue
    
    async def _handle_interactive_command(self, command):
        """Handle interactive command execution"""
        try:
            if command == 'analyze':
                await self._interactive_analyze()
            elif command == 'quiz':
                await self._interactive_quiz()
            elif command == 'progress':
                await self._interactive_progress()
            elif command == 'goals':
                await self._interactive_goals()
            elif command == 'platforms':
                await self._interactive_platforms()
            elif command == 'bookmarks':
                await self._interactive_bookmarks()
            elif command == 'session':
                await self._interactive_session()
            elif command == 'review':
                await self._interactive_review()
            else:
                self.console.print(f"[yellow]Unknown command: {command}[/yellow]")
                
        except Exception as e:
            self.console.print(f"[red]Error executing command: {e}[/red]")
            self.logger.error(f"Interactive command error: {e}")
    
    async def _interactive_analyze(self):
        """Interactive syllabus analysis"""
        self.console.print(Rule("[bold bright_blue]Syllabus Analysis Setup[/bold bright_blue]"))
        
        # Get input method
        input_choice = Prompt.ask(
            "[bright_yellow]How would you like to provide your syllabus?[/bright_yellow]",
            choices=["file", "text"],
            default="file"
        )
        
        if input_choice == "file":
            file_path = Prompt.ask("[bright_cyan]Enter syllabus file path[/bright_cyan]")
            if not file_path or not os.path.exists(file_path):
                self.console.print("[bright_red]File not found. Please check the path.[/bright_red]")
                return
            
            # Load and analyze file
            try:
                with self.console.status("[bright_cyan]Loading syllabus..."):
                    content = self.syllabus_parser.load_from_file(file_path)
                    title = os.path.basename(file_path)
                
                self.console.print(f"[bright_green]Loaded:[/bright_green] {title}")
                
                # Extract topics
                with self.console.status("[bright_cyan]Extracting topics with AI..."):
                    topics = await self.syllabus_parser.extract_topics(content, self.ai_client)
                
                if topics:
                    self.console.print(f"[bright_green]Found {len(topics)} topics[/bright_green]")
                    
                    # Show topics
                    topics_table = Table(title="Extracted Topics", border_style="bright_green")
                    topics_table.add_column("Topic", style="bright_cyan")
                    topics_table.add_column("Description", style="bright_white")
                    
                    for topic in topics[:5]:  # Show first 5
                        desc = topic.get('description', 'No description')
                        if len(desc) > 50:
                            desc = desc[:50] + "..."
                        topics_table.add_row(topic['name'], desc)
                    
                    if len(topics) > 5:
                        topics_table.add_row(f"... and {len(topics)-5} more", "[dim]Topics extracted[/dim]")
                    
                    self.console.print(topics_table)
                    
                    # Save to database
                    syllabus_id = self.db.save_syllabus(title, content)
                    self.db.save_topics(syllabus_id, topics)
                    self.console.print("[bright_green]Saved to database[/bright_green]")
                    
                else:
                    self.console.print("[bright_yellow]No topics found[/bright_yellow]")
                    
            except Exception as e:
                self.console.print(f"[bright_red]Error: {e}[/bright_red]")
        
        else:  # text input
            content = Prompt.ask("[bright_cyan]Enter syllabus text content[/bright_cyan]")
            if not content:
                self.console.print("[bright_red]No content provided[/bright_red]")
                return
            
            try:
                with self.console.status("[bright_cyan]Extracting topics with AI..."):
                    topics = await self.syllabus_parser.extract_topics(content, self.ai_client)
                
                if topics:
                    self.console.print(f"[bright_green]Found {len(topics)} topics[/bright_green]")
                else:
                    self.console.print("[bright_yellow]No topics found[/bright_yellow]")
                    
            except Exception as e:
                self.console.print(f"[bright_red]Error: {e}[/bright_red]")
    
    async def _interactive_quiz(self):
        """Interactive quiz generation and taking"""
        self.console.print(Rule("[bold bright_blue]Interactive Quizzes[/bold bright_blue]"))
        
        # Get available topics from database
        topics = self.db.get_all_topics()
        if not topics:
            self.console.print("[yellow]No topics found. Please analyze a syllabus first.[/yellow]")
            return
        
        # Show available topics
        topics_table = Table(title="Available Topics", border_style="bright_green")
        topics_table.add_column("ID", style="bright_cyan", width=5)
        topics_table.add_column("Topic", style="bright_white")
        
        for i, topic in enumerate(topics[:10], 1):
            topics_table.add_row(str(i), topic.get('name', 'Unknown'))
        
        self.console.print(topics_table)
        
        try:
            choice = int(Prompt.ask("[bright_yellow]Select topic number[/bright_yellow]", default="1"))
            if 1 <= choice <= len(topics):
                selected_topic = topics[choice - 1]
                
                with self.console.status("[bright_cyan]Generating quiz..."):
                    quiz_data = await self.quiz_generator.generate_quiz(selected_topic['name'])
                
                if quiz_data:
                    await self._take_quiz(quiz_data)
                else:
                    self.console.print("[yellow]Could not generate quiz for this topic[/yellow]")
            else:
                self.console.print("[red]Invalid selection[/red]")
        except ValueError:
            self.console.print("[red]Please enter a valid number[/red]")
    
    async def _take_quiz(self, quiz_data):
        """Take an interactive quiz"""
        self.console.print(f"\n[bold bright_green]Quiz: {quiz_data.get('title', 'Topic Quiz')}[/bold bright_green]")
        
        questions = quiz_data.get('questions', [])
        if not questions:
            self.console.print("[yellow]No questions available[/yellow]")
            return
        
        score = 0
        total = len(questions)
        
        for i, question in enumerate(questions, 1):
            self.console.print(f"\n[bold bright_cyan]Question {i}/{total}:[/bold bright_cyan]")
            self.console.print(question.get('question', ''))
            
            options = question.get('options', [])
            if options:
                for j, option in enumerate(options, 1):
                    self.console.print(f"  {j}. {option}")
                
                try:
                    answer = int(Prompt.ask("[bright_yellow]Your answer[/bright_yellow]"))
                    correct = question.get('correct_answer', 1)
                    
                    if answer == correct:
                        self.console.print("[bright_green]Correct![/bright_green]")
                        score += 1
                    else:
                        self.console.print(f"[bright_red]Incorrect. The correct answer was {correct}[/bright_red]")
                        
                except ValueError:
                    self.console.print("[red]Invalid answer[/red]")
        
        # Show final score
        percentage = (score / total) * 100
        self.console.print(f"\n[bold bright_green]Quiz Complete![/bold bright_green]")
        self.console.print(f"Score: {score}/{total} ({percentage:.1f}%)")
    
    async def _interactive_progress(self):
        """Interactive progress dashboard"""
        self.console.print(Rule("[bold bright_blue]Progress Dashboard[/bold bright_blue]"))
        
        try:
            progress_data = self.progress_dashboard.get_progress_summary()
            
            # Display progress summary
            progress_table = Table(title="Learning Progress", border_style="bright_green")
            progress_table.add_column("Metric", style="bright_cyan")
            progress_table.add_column("Value", style="bright_white")
            
            progress_table.add_row("Topics Studied", str(progress_data.get('topics_studied', 0)))
            progress_table.add_row("Quizzes Taken", str(progress_data.get('quizzes_taken', 0)))
            progress_table.add_row("Study Sessions", str(progress_data.get('study_sessions', 0)))
            progress_table.add_row("Average Score", f"{progress_data.get('average_score', 0):.1f}%")
            
            self.console.print(progress_table)
            
            # Show recent activity
            recent_activity = progress_data.get('recent_activity', [])
            if recent_activity:
                activity_table = Table(title="Recent Activity", border_style="bright_blue")
                activity_table.add_column("Date", style="bright_cyan")
                activity_table.add_column("Activity", style="bright_white")
                
                for activity in recent_activity[:5]:
                    activity_table.add_row(
                        activity.get('date', 'Unknown'),
                        activity.get('description', 'No description')
                    )
                
                self.console.print(activity_table)
            
        except Exception as e:
            self.console.print(f"[red]Error loading progress: {e}[/red]")
    
    async def _interactive_goals(self):
        """Interactive goals management"""
        self.console.print(Rule("[bold bright_blue]Study Goals[/bold bright_blue]"))
        
        action = Prompt.ask(
            "[bright_yellow]What would you like to do?[/bright_yellow]",
            choices=["view", "add", "update", "delete"],
            default="view"
        )
        
        if action == "view":
            goals = self.goals_manager.get_all_goals()
            if goals:
                goals_table = Table(title="Your Study Goals", border_style="bright_green")
                goals_table.add_column("Goal", style="bright_cyan")
                goals_table.add_column("Target", style="bright_white")
                goals_table.add_column("Progress", style="bright_yellow")
                goals_table.add_column("Status", style="bright_green")
                
                for goal in goals:
                    status = "✓ Complete" if goal.get('completed') else "In Progress"
                    goals_table.add_row(
                        goal.get('title', 'Unknown'),
                        goal.get('target_date', 'No deadline'),
                        f"{goal.get('progress', 0)}%",
                        status
                    )
                
                self.console.print(goals_table)
            else:
                self.console.print("[yellow]No goals set yet[/yellow]")
        
        elif action == "add":
            title = Prompt.ask("[bright_cyan]Goal title[/bright_cyan]")
            description = Prompt.ask("[bright_cyan]Goal description[/bright_cyan]")
            goal_type = Prompt.ask("[bright_cyan]Goal type[/bright_cyan]", choices=["daily", "weekly", "monthly", "milestone"], default="weekly")
            target_value = int(Prompt.ask("[bright_cyan]Target value[/bright_cyan]", default="1"))
            unit = Prompt.ask("[bright_cyan]Unit (minutes/topics/quizzes)[/bright_cyan]", default="topics")
            days_to_complete = int(Prompt.ask("[bright_cyan]Days to complete[/bright_cyan]", default="30"))
            
            goal_id = self.goals_manager.create_goal(title, description, goal_type, target_value, unit, days_to_complete)
            self.console.print(f"[bright_green]Goal created with ID: {goal_id}[/bright_green]")
    
    async def _interactive_platforms(self):
        """Interactive multi-platform search"""
        self.console.print(Rule("[bold bright_blue]Multi-Platform Search[/bold bright_blue]"))
        
        query = Prompt.ask("[bright_cyan]Enter search query[/bright_cyan]")
        if not query:
            self.console.print("[red]No query provided[/red]")
            return
        
        platform = Prompt.ask(
            "[bright_yellow]Select platform[/bright_yellow]",
            choices=["youtube", "coursera", "udemy", "all"],
            default="all"
        )
        
        with self.console.status(f"[bright_cyan]Searching {platform}..."):
            try:
                if platform == "all":
                    platform_results = await self.platform_integrator.search_all_platforms(query)
                    # Flatten results from all platforms
                    results = []
                    for platform_name, platform_courses in platform_results.items():
                        for course in platform_courses:
                            course['platform'] = platform_name
                            results.append(course)
                else:
                    results = await self.platform_integrator.search_platform(platform, query)
                    # Add platform name to each result
                    for result in results:
                        result['platform'] = platform
                
                if results:
                    results_table = Table(title=f"Search Results for '{query}'", border_style="bright_green")
                    results_table.add_column("Platform", style="bright_cyan")
                    results_table.add_column("Title", style="bright_white")
                    results_table.add_column("URL", style="bright_blue")
                    
                    for result in results[:10]:
                        results_table.add_row(
                            result.get('platform', 'Unknown'),
                            result.get('title', 'No title')[:50],
                            result.get('url', 'No URL')[:50]
                        )
                    
                    self.console.print(results_table)
                else:
                    self.console.print("[yellow]No results found[/yellow]")
                    
            except Exception as e:
                self.console.print(f"[red]Search error: {e}[/red]")
    
    async def _interactive_bookmarks(self):
        """Interactive bookmark management"""
        self.console.print(Rule("[bold bright_blue]Smart Bookmarks[/bold bright_blue]"))
        
        action = Prompt.ask(
            "[bright_yellow]What would you like to do?[/bright_yellow]",
            choices=["view", "add", "delete"],
            default="view"
        )
        
        if action == "view":
            bookmarks = self.bookmark_manager.get_all_bookmarks()
            if bookmarks:
                bookmarks_table = Table(title="Your Bookmarks", border_style="bright_green")
                bookmarks_table.add_column("Title", style="bright_cyan")
                bookmarks_table.add_column("URL", style="bright_white")
                bookmarks_table.add_column("Notes", style="bright_yellow")
                
                for bookmark in bookmarks[:10]:
                    notes = bookmark.get('notes', 'No notes')
                    if len(notes) > 30:
                        notes = notes[:30] + "..."
                    
                    bookmarks_table.add_row(
                        bookmark.get('title', 'Unknown'),
                        bookmark.get('url', 'No URL')[:40],
                        notes
                    )
                
                self.console.print(bookmarks_table)
            else:
                self.console.print("[yellow]No bookmarks saved yet[/yellow]")
        
        elif action == "add":
            title = Prompt.ask("[bright_cyan]Bookmark title[/bright_cyan]")
            url = Prompt.ask("[bright_cyan]URL[/bright_cyan]")
            notes = Prompt.ask("[bright_cyan]Notes (optional)[/bright_cyan]", default="")
            topic = Prompt.ask("[bright_cyan]Topic[/bright_cyan]", default="General")
            
            # For bookmark manager, we need video_id, video_title, timestamp, note, topic
            bookmark_id = self.bookmark_manager.add_bookmark(
                video_id=url,  # Using URL as video_id for general bookmarks
                video_title=title,
                timestamp="0:00",  # Default timestamp
                note=notes,
                topic=topic
            )
            self.console.print(f"[bright_green]Bookmark saved with ID: {bookmark_id}[/bright_green]")
    
    async def _interactive_session(self):
        """Interactive study session with Pomodoro timer"""
        self.console.print(Rule("[bold bright_blue]Study Sessions[/bold bright_blue]"))
        
        topic = Prompt.ask("[bright_cyan]Study topic[/bright_cyan]")
        duration = int(Prompt.ask("[bright_yellow]Session duration (minutes)[/bright_yellow]", default="25"))
        
        session = self.study_session_manager.start_study_session(topic, duration)
        
        self.console.print(f"[bright_green]Starting {duration}-minute study session for: {topic}[/bright_green]")
        self.console.print("[dim]Press Ctrl+C to end session early[/dim]")
        
        try:
            import time
            start_time = time.time()
            end_time = start_time + (duration * 60)
            
            while time.time() < end_time:
                remaining = int(end_time - time.time())
                mins, secs = divmod(remaining, 60)
                
                self.console.print(f"\r[bright_yellow]Time remaining: {mins:02d}:{secs:02d}[/bright_yellow]", end="")
                time.sleep(1)
            
            self.console.print(f"\n[bright_green]Session complete![/bright_green]")
            self.study_session_manager.end_session("completed")
            
        except KeyboardInterrupt:
            self.console.print(f"\n[yellow]Session ended early[/yellow]")
            self.study_session_manager.end_session("interrupted")
    
    async def _interactive_review(self):
        """Interactive spaced repetition review"""
        self.console.print(Rule("[bold bright_blue]Spaced Repetition Review[/bold bright_blue]"))
        
        # Get items due for review
        review_items = self.spaced_repetition.get_due_topics()
        
        if not review_items:
            self.console.print("[yellow]No items due for review today![/yellow]")
            self.console.print("[dim]Check back tomorrow or add new topics to review.[/dim]")
            return
        
        self.console.print(f"[bright_green]You have {len(review_items)} items to review[/bright_green]")
        
        for i, item in enumerate(review_items, 1):
            self.console.print(f"\n[bold bright_cyan]Review {i}/{len(review_items)}:[/bold bright_cyan]")
            self.console.print(f"Topic: {item.get('topic_name', 'Unknown')}")
            
            # Show the question or prompt
            self.console.print(f"Question: {item.get('question', 'Review this topic')}")
            
            Prompt.ask("[dim]Press Enter when ready to see the answer[/dim]", default="")
            
            # Show the answer
            self.console.print(f"Answer: {item.get('answer', 'No answer available')}")
            
            # Get user feedback
            difficulty = Prompt.ask(
                "[bright_yellow]How difficult was this? (1=Easy, 2=Medium, 3=Hard)[/bright_yellow]",
                choices=["1", "2", "3"],
                default="2"
            )
            
            # Update the spaced repetition schedule
            success = int(difficulty) <= 2  # Easy and Medium are considered success
            self.spaced_repetition.mark_review(item.topic_name, success)
        
        self.console.print(f"\n[bright_green]Review session complete![/bright_green]")
        self.console.print("[dim]Great job! Keep up the consistent practice.[/dim]")

async def main():
    """Main application entry point"""
    
    # If no arguments provided, go directly to interactive mode
    if len(sys.argv) == 1:
        app = SyllaboMain()
        app.print_banner()
        
        # Interactive menu loop
        while True:
            command = app.show_interactive_menu()
            
            if command == 'exit':
                app.console.print(Panel(
                    "[bold bright_cyan]Thank you for using Syllabo![/bold bright_cyan]\n[dim]Keep learning and growing![/dim]",
                    border_style="bright_cyan",
                    title="[bold bright_white]Goodbye[/bold bright_white]"
                ))
                break
            elif command == 'help':
                from src.cli.commands import create_parser
                parser = create_parser()
                app.console.print(Rule("[bold bright_yellow]Available Commands[/bold bright_yellow]"))
                parser.print_help()
                Prompt.ask("\n[dim]Press Enter to continue[/dim]", default="")
            else:
                await app._handle_interactive_command(command)
                Prompt.ask("\n[dim]Press Enter to continue[/dim]", default="")
                app.console.clear()
                app.print_banner()
        return
    
    # Handle command line arguments
    from src.cli.commands import create_parser
    parser = create_parser()
    args = parser.parse_args()
    app = SyllaboMain()
    
    try:
        # Handle different commands
        if args.command == 'analyze':
            await app._interactive_analyze()
        else:
            parser.print_help()
    
    except KeyboardInterrupt:
        print("\nOperation cancelled by user")
    except Exception as e:
        print(f"ERROR: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main())