#!/usr/bin/env python3
"""
Syllabo - AI-Powered Learning Assistant
Main entry point for all features
"""

import os
import sys
import asyncio
from typing import Dict, List
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
from src.notes_generator import NotesGenerator
from src.video_analyzer import VideoAnalyzer
from src.resource_finder import ResourceFinder
from src.youtube_client import YouTubeClient

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
        
        # Initialize new enhanced modules
        self.notes_generator = NotesGenerator(self.ai_client)
        self.youtube_client = YouTubeClient()
        self.video_analyzer = VideoAnalyzer(self.ai_client)
        self.resource_finder = ResourceFinder(self.ai_client)
    
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
            ("2", "quiz", "Interactive Quizzes", "Generate quizzes from topics, syllabus, or text"),
            ("3", "progress", "Progress Dashboard", "View learning progress and analytics"),
            ("4", "goals", "Study Goals", "Manage learning goals and milestones"),
            ("5", "platforms", "Multi-Platform Search", "Search across learning platforms"),
            ("6", "bookmarks", "Smart Bookmarks", "Manage video bookmarks and notes"),
            ("7", "session", "Study Sessions", "Pomodoro timer and focus sessions"),
            ("8", "review", "Spaced Repetition", "Review topics using spaced repetition"),
            ("9", "videos", "Smart Video Analysis", "Find and analyze educational videos"),
            ("10", "resources", "Resource Finder", "Find books, courses, and learning materials"),
            ("11", "notes", "Generate Study Notes", "Create notes and questions from content"),
            ("12", "help", "Help & Documentation", "Get help and usage information"),
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
            elif command == 'videos':
                await self._interactive_videos()
            elif command == 'resources':
                await self._interactive_resources()
            elif command == 'notes':
                await self._interactive_notes()
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
                    
                    # Enhanced analysis workflow - integrate new features
                    await self._comprehensive_analysis_workflow(topics)
                    
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
                    
                    # Enhanced analysis workflow for text input
                    await self._comprehensive_analysis_workflow(topics)
                else:
                    self.console.print("[bright_yellow]No topics found[/bright_yellow]")
                    
            except Exception as e:
                self.console.print(f"[bright_red]Error: {e}[/bright_red]")
    
    async def _interactive_quiz(self):
        """Interactive quiz generation and taking"""
        self.console.print(Rule("[bold bright_blue]Interactive Quizzes[/bold bright_blue]"))
        
        # Give user options for quiz generation
        quiz_source = Prompt.ask(
            "[bright_yellow]How would you like to generate the quiz?[/bright_yellow]",
            choices=["topics", "syllabus", "text"],
            default="topics"
        )
        
        if quiz_source == "topics":
            await self._quiz_from_topics()
        elif quiz_source == "syllabus":
            await self._quiz_from_syllabus()
        else:  # text
            await self._quiz_from_text()
    
    async def _quiz_from_topics(self):
        """Generate quiz from existing database topics"""
        # Get available topics from database
        topics = self.db.get_all_topics()
        if not topics:
            self.console.print("[yellow]No topics found. Please analyze a syllabus first or use syllabus/text option.[/yellow]")
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
                
                # Ask for number of questions
                num_questions = int(Prompt.ask("[bright_yellow]Number of questions[/bright_yellow]", default="5"))
                
                with self.console.status("[bright_cyan]Generating quiz..."):
                    quiz_data = await self.quiz_generator.generate_quiz(selected_topic['name'], num_questions)
                
                if quiz_data:
                    await self._take_quiz(quiz_data)
                else:
                    self.console.print("[yellow]Could not generate quiz for this topic[/yellow]")
            else:
                self.console.print("[red]Invalid selection[/red]")
        except ValueError:
            self.console.print("[red]Please enter a valid number[/red]")
    
    async def _quiz_from_syllabus(self):
        """Generate quiz from syllabus file"""
        file_path = Prompt.ask("[bright_cyan]Enter syllabus file path[/bright_cyan]")
        if not file_path or not os.path.exists(file_path):
            self.console.print("[bright_red]File not found. Please check the path.[/bright_red]")
            return
        
        try:
            # Load syllabus content
            with self.console.status("[bright_cyan]Loading syllabus..."):
                content = self.syllabus_parser.load_from_file(file_path)
                title = os.path.basename(file_path)
            
            self.console.print(f"[bright_green]Loaded:[/bright_green] {title}")
            
            # Get quiz parameters
            topic_name = Prompt.ask("[bright_cyan]Quiz topic/subject[/bright_cyan]", default=title)
            num_questions = int(Prompt.ask("[bright_yellow]Number of questions[/bright_yellow]", default="5"))
            
            # Generate quiz from content
            with self.console.status("[bright_cyan]Generating quiz from syllabus..."):
                quiz_data = await self.quiz_generator.generate_quiz_from_content(content, topic_name, num_questions)
            
            if quiz_data:
                await self._take_quiz(quiz_data)
            else:
                self.console.print("[yellow]Could not generate quiz from this syllabus[/yellow]")
                
        except Exception as e:
            self.console.print(f"[bright_red]Error: {e}[/bright_red]")
    
    async def _quiz_from_text(self):
        """Generate quiz from direct text input"""
        self.console.print("[bright_cyan]Enter your study content (press Enter twice when done):[/bright_cyan]")
        
        lines = []
        empty_lines = 0
        
        while empty_lines < 2:
            try:
                line = input()
                if line.strip() == "":
                    empty_lines += 1
                else:
                    empty_lines = 0
                lines.append(line)
            except KeyboardInterrupt:
                self.console.print("\n[yellow]Input cancelled[/yellow]")
                return
        
        content = "\n".join(lines).strip()
        
        if not content:
            self.console.print("[bright_red]No content provided[/bright_red]")
            return
        
        try:
            # Get quiz parameters
            topic_name = Prompt.ask("[bright_cyan]Quiz topic/subject[/bright_cyan]", default="Study Material")
            num_questions = int(Prompt.ask("[bright_yellow]Number of questions[/bright_yellow]", default="5"))
            
            # Generate quiz from content
            with self.console.status("[bright_cyan]Generating quiz from your content..."):
                quiz_data = await self.quiz_generator.generate_quiz_from_content(content, topic_name, num_questions)
            
            if quiz_data:
                await self._take_quiz(quiz_data)
            else:
                self.console.print("[yellow]Could not generate quiz from this content[/yellow]")
                
        except ValueError:
            self.console.print("[red]Please enter a valid number for questions[/red]")
        except Exception as e:
            self.console.print(f"[bright_red]Error: {e}[/bright_red]")
    
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
            self.console.print(f"Topic: {item.topic_name}")
            
            if item.description:
                self.console.print(f"Description: {item.description}")
            
            Prompt.ask("[dim]Press Enter when ready to mark your review[/dim]", default="")
            
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
    
    async def _handle_analyze_command(self, args):
        """Handle analyze command from CLI"""
        await self._interactive_analyze()
    
    async def _handle_search_command(self, args):
        """Handle search command from CLI"""
        if not args.topic:
            self.console.print("[red]Error: Topic is required for search[/red]")
            return
        
        self.console.print(f"[bright_cyan]Searching for videos on: {args.topic}[/bright_cyan]")
        
        try:
            # Use the video analyzer to find relevant videos
            videos = await self.video_analyzer.find_videos(args.topic, max_results=args.max_videos)
            
            if videos:
                self.console.print(f"[bright_green]Found {len(videos)} videos[/bright_green]")
                
                # Display results in a table
                videos_table = Table(title=f"Search Results for '{args.topic}'", border_style="bright_green")
                videos_table.add_column("Title", style="bright_cyan", width=40)
                videos_table.add_column("Channel", style="bright_white", width=20)
                videos_table.add_column("Duration", style="bright_yellow", width=10)
                videos_table.add_column("Views", style="bright_blue", width=10)
                
                for video in videos:
                    videos_table.add_row(
                        video.get('title', 'Unknown')[:37] + "..." if len(video.get('title', '')) > 40 else video.get('title', 'Unknown'),
                        video.get('channel', 'Unknown')[:17] + "..." if len(video.get('channel', '')) > 20 else video.get('channel', 'Unknown'),
                        video.get('duration', 'Unknown'),
                        video.get('view_count', 'Unknown')
                    )
                
                self.console.print(videos_table)
                
                if args.save:
                    # Save results to file
                    import json
                    import os
                    os.makedirs('exports', exist_ok=True)
                    filename = f"exports/search_{args.topic.replace(' ', '_')}.{args.export_format}"
                    
                    if args.export_format == 'json':
                        with open(filename, 'w') as f:
                            json.dump(videos, f, indent=2)
                    
                    self.console.print(f"[bright_green]Results saved to {filename}[/bright_green]")
            else:
                self.console.print("[yellow]No videos found for this topic[/yellow]")
                
        except Exception as e:
            self.console.print(f"[red]Search error: {e}[/red]")
    
    async def _handle_review_command(self, args):
        """Handle review command from CLI"""
        if not args.review_action:
            self.console.print("[red]Error: Review action is required[/red]")
            return
        
        if args.review_action == 'add':
            if not args.topic:
                self.console.print("[red]Error: Topic is required for adding to review[/red]")
                return
            
            success = self.spaced_repetition.add_topic(args.topic, args.description or "")
            if success:
                self.console.print(f"[bright_green]Added '{args.topic}' to review schedule[/bright_green]")
            else:
                self.console.print(f"[yellow]Topic '{args.topic}' is already in your review schedule[/yellow]")
        
        elif args.review_action == 'list':
            topics = self.spaced_repetition.get_all_topics()
            if not topics:
                self.console.print("[yellow]No topics in your review schedule[/yellow]")
                return
            
            topics_table = Table(title="Your Review Schedule", border_style="bright_green")
            topics_table.add_column("Topic", style="bright_cyan", width=30)
            topics_table.add_column("Mastery", style="bright_white", width=12)
            topics_table.add_column("Success Rate", style="bright_yellow", width=12)
            topics_table.add_column("Next Review", style="bright_blue", width=12)
            
            for topic in topics:
                mastery_color = {
                    'Learning': 'red', 'Beginner': 'yellow', 'Intermediate': 'blue', 
                    'Advanced': 'green', 'Mastered': 'bright_green'
                }.get(topic['mastery_level'], 'white')
                
                next_review_text = "Due now" if topic['days_until_review'] <= 0 else f"{topic['days_until_review']} days"
                
                topics_table.add_row(
                    topic['topic_name'][:27] + "..." if len(topic['topic_name']) > 30 else topic['topic_name'],
                    f"[{mastery_color}]{topic['mastery_level']}[/{mastery_color}]",
                    f"{topic['success_rate']}%",
                    next_review_text
                )
            
            self.console.print(topics_table)
            
            summary = self.spaced_repetition.get_study_summary()
            self.console.print(f"[bright_green]Summary: {summary['total_topics']} topics, {summary['due_now']} due now, {summary['mastered_topics']} mastered[/bright_green]")
        
        elif args.review_action == 'due':
            due_topics = self.spaced_repetition.get_due_topics()
            if not due_topics:
                self.console.print("[bright_green]No topics are due for review right now[/bright_green]")
                return
            
            self.console.print(f"[bright_yellow]You have {len(due_topics)} topic{'s' if len(due_topics) != 1 else ''} due for review[/bright_yellow]")
            
            due_table = Table(title="Topics Due for Review", border_style="bright_red")
            due_table.add_column("No.", style="dim", width=4)
            due_table.add_column("Topic", style="bright_cyan")
            due_table.add_column("Description", style="bright_white")
            
            for i, item in enumerate(due_topics, 1):
                due_table.add_row(
                    str(i),
                    item.topic_name,
                    item.description or "No description"
                )
            
            self.console.print(due_table)
        
        elif args.review_action == 'mark':
            if not args.topic:
                self.console.print("[red]Error: Topic is required for marking review[/red]")
                return
            
            success = self.spaced_repetition.mark_review(args.topic, args.success)
            if success:
                result_text = "successful" if args.success else "failed"
                self.console.print(f"[bright_green]Marked '{args.topic}' as {result_text} review[/bright_green]")
            else:
                self.console.print(f"[yellow]Topic '{args.topic}' not found in review schedule[/yellow]")
        
        elif args.review_action == 'stats':
            if args.topic:
                stats = self.spaced_repetition.get_topic_stats(args.topic)
                if not stats:
                    self.console.print(f"[yellow]Topic '{args.topic}' not found[/yellow]")
                    return
                
                stats_panel = Panel(
                    f"Mastery Level: {stats['mastery_level']}\n"
                    f"Success Rate: {stats['success_rate']}%\n"
                    f"Total Reviews: {stats['total_reviews']}\n"
                    f"Success Streak: {stats['success_streak']}\n"
                    f"Next Review: {stats['next_review_date']}\n"
                    f"Current Interval: {stats['current_interval']} days",
                    title=f"Stats for {stats['topic_name']}",
                    border_style="bright_blue"
                )
                self.console.print(stats_panel)
            else:
                summary = self.spaced_repetition.get_study_summary()
                analytics = self.spaced_repetition.get_learning_analytics()
                
                stats_table = Table(title="Review Statistics", border_style="bright_blue")
                stats_table.add_column("Metric", style="bright_cyan")
                stats_table.add_column("Value", style="bright_white")
                
                stats_table.add_row("Total Topics", str(summary['total_topics']))
                stats_table.add_row("Due Now", str(summary['due_now']))
                stats_table.add_row("Due Today", str(summary['due_today']))
                stats_table.add_row("Mastered Topics", str(summary['mastered_topics']))
                stats_table.add_row("Average Success Rate", f"{summary['average_success_rate']}%")
                stats_table.add_row("Total Reviews", str(analytics['total_reviews']))
                stats_table.add_row("Retention Rate", f"{analytics['retention_rate']}%")
                
                self.console.print(stats_table)
        
        elif args.review_action == 'remove':
            if not args.topic:
                self.console.print("[red]Error: Topic is required for removal[/red]")
                return
            
            success = self.spaced_repetition.remove_topic(args.topic)
            if success:
                self.console.print(f"[bright_green]Removed '{args.topic}' from review schedule[/bright_green]")
            else:
                self.console.print(f"[yellow]Topic '{args.topic}' not found in review schedule[/yellow]")
    
    async def _handle_goals_command(self, args):
        """Handle goals command from CLI"""
        if not args.action:
            self.console.print("[red]Error: Goals action is required[/red]")
            return
        
        if args.action == 'create':
            if not all([args.title, args.type, args.target, args.unit]):
                self.console.print("[red]Error: Title, type, target, and unit are required for creating goals[/red]")
                return
            
            goal_id = self.goals_manager.create_goal(
                title=args.title,
                description=args.description or "",
                goal_type=args.type,
                target_value=args.target,
                unit=args.unit
            )
            self.console.print(f"[bright_green]Goal created with ID: {goal_id}[/bright_green]")
        
        elif args.action == 'list':
            goals = self.goals_manager.get_all_goals()
            if not goals:
                self.console.print("[yellow]No goals set yet[/yellow]")
                return
            
            goals_table = Table(title="Your Study Goals", border_style="bright_green")
            goals_table.add_column("Goal", style="bright_cyan", width=25)
            goals_table.add_column("Type", style="bright_white", width=10)
            goals_table.add_column("Progress", style="bright_yellow", width=15)
            goals_table.add_column("Status", style="bright_blue", width=12)
            goals_table.add_column("Deadline", style="bright_magenta", width=12)
            
            for goal in goals:
                progress_percent = (goal.current_value / goal.target_value * 100) if goal.target_value > 0 else 0
                status = "✓ Complete" if goal.completed else "In Progress"
                status_color = "bright_green" if goal.completed else "bright_yellow"
                
                from datetime import datetime
                try:
                    deadline = datetime.fromisoformat(goal.deadline).strftime('%Y-%m-%d')
                except:
                    deadline = "No deadline"
                
                goals_table.add_row(
                    goal.title[:22] + "..." if len(goal.title) > 25 else goal.title,
                    goal.goal_type.capitalize(),
                    f"{goal.current_value}/{goal.target_value} {goal.unit} ({progress_percent:.1f}%)",
                    f"[{status_color}]{status}[/{status_color}]",
                    deadline
                )
            
            self.console.print(goals_table)
            
            summary = self.goals_manager.get_goal_summary()
            self.console.print(f"[bright_green]Summary: {summary['total_goals']} total, {summary['active_goals']} active, {summary['completed_goals']} completed[/bright_green]")
        
        elif args.action == 'suggest':
            suggestions = self.goals_manager.suggest_goals("beginner")  # Default to beginner
            
            suggestions_table = Table(title="Goal Suggestions", border_style="bright_blue")
            suggestions_table.add_column("Title", style="bright_cyan")
            suggestions_table.add_column("Type", style="bright_white")
            suggestions_table.add_column("Target", style="bright_yellow")
            
            for suggestion in suggestions:
                suggestions_table.add_row(
                    suggestion['title'],
                    suggestion['type'].capitalize(),
                    f"{suggestion['target']} {suggestion['unit']}"
                )
            
            self.console.print(suggestions_table)
            self.console.print("[dim]Use 'goals create' command to add any of these goals[/dim]")
    
    async def _handle_quiz_command(self, args):
        """Handle quiz command from CLI"""
        await self._interactive_quiz()
    
    async def _handle_progress_command(self, args):
        """Handle progress command from CLI"""
        await self._interactive_progress()
    
    async def _handle_session_command(self, args):
        """Handle session command from CLI"""
        await self._interactive_session()
    
    async def _handle_bookmarks_command(self, args):
        """Handle bookmarks command from CLI"""
        await self._interactive_bookmarks()
    
    async def _handle_platforms_command(self, args):
        """Handle platforms command from CLI"""
        await self._interactive_platforms()
    
    def _show_help(self):
        """Show comprehensive help information"""
        help_text = """
[bold bright_cyan]Syllabo - AI-Powered Learning Assistant[/bold bright_cyan]

[bright_white]Available Commands:[/bright_white]
• analyze    - Analyze syllabus and extract topics
• search     - Search for educational videos
• review     - Spaced repetition system
• goals      - Study goals management
• quiz       - Interactive quizzes from topics, syllabus, or text
• progress   - Learning progress dashboard
• session    - Study sessions with Pomodoro timer
• bookmarks  - Smart bookmarks management
• platforms  - Multi-platform search

[bright_white]Examples:[/bright_white]
  python main.py analyze --file syllabus.pdf
  python main.py search --topic "Machine Learning"
  python main.py review add --topic "Neural Networks"
  python main.py goals create --title "Daily Study" --type daily --target 30 --unit minutes

[bright_white]Interactive Mode:[/bright_white]
  python main.py interactive

For detailed help on any command, use:
  python main.py [command] --help
        """
        
        help_panel = Panel(
            help_text,
            title="[bold bright_blue]Help & Documentation[/bold bright_blue]",
            border_style="bright_blue",
            padding=(1, 2)
        )
        
        self.console.print(help_panel)
    
    async def _comprehensive_analysis_workflow(self, topics: List[Dict]):
        """Comprehensive analysis workflow integrating videos, resources, and notes generation"""
        self.console.print(Rule("[bold bright_magenta]Comprehensive Learning Analysis[/bold bright_magenta]"))
        
        # Ask user what they want to do with the extracted topics
        self.console.print(f"\n[bright_green]Great! I found {len(topics)} topics from your syllabus.[/bright_green]")
        self.console.print("[bright_white]Let me help you create a complete learning plan with:[/bright_white]")
        self.console.print("• Educational videos and playlists")
        self.console.print("• Books, courses, and learning resources")
        self.console.print("• Study notes and questions")
        self.console.print("• Spaced repetition schedule")
        
        proceed = Prompt.ask(
            "\n[bright_yellow]Would you like me to create a comprehensive learning plan? (y/n)[/bright_yellow]",
            default="y"
        ).lower() == 'y'
        
        if not proceed:
            self.console.print("[dim]You can always run individual features later from the main menu.[/dim]")
            return
        
        # Get user preferences for the analysis
        preferences = await self._get_analysis_preferences()
        
        # Process each topic
        topic_names = [topic.get('name', '') for topic in topics[:5]]  # Limit to first 5 topics
        
        self.console.print(f"\n[bright_cyan]Processing {len(topic_names)} topics...[/bright_cyan]")
        
        for i, topic_name in enumerate(topic_names, 1):
            self.console.print(f"\n{'-'*60}")
            self.console.print(f"[bold bright_blue]Topic {i}/{len(topic_names)}: {topic_name}[/bold bright_blue]")
            self.console.print(f"{'-'*60}")
            
            # 1. Find and analyze videos if requested
            if preferences.get('include_videos', True):
                await self._analyze_topic_videos(topic_name, preferences)
            
            # 2. Find learning resources if requested
            if preferences.get('include_resources', True):
                await self._find_topic_resources(topic_name, preferences)
            
            # 3. Add to spaced repetition if requested
            if preferences.get('add_to_spaced_repetition', True):
                self._add_topic_to_spaced_repetition(topic_name, topics[i-1])
            
            # Small delay between topics for better UX
            if i < len(topic_names):
                self.console.print("[dim]Moving to next topic...[/dim]")
                await asyncio.sleep(1)
        
        # Final summary and recommendations
        await self._display_analysis_summary(topic_names, preferences)
    
    async def _get_analysis_preferences(self) -> Dict:
        """Get user preferences for comprehensive analysis"""
        self.console.print("\n[bold bright_yellow]Analysis Preferences[/bold bright_yellow]")
        
        preferences = {}
        
        # Video analysis preferences
        preferences['include_videos'] = Prompt.ask(
            "[bright_cyan]Find and analyze educational videos? (y/n)[/bright_cyan]",
            default="y"
        ).lower() == 'y'
        
        if preferences['include_videos']:
            print("\nVideo learning preferences:")
            print("1. One comprehensive video per topic")
            print("2. Multiple focused videos per topic")
            print("3. Playlists and course series")
            print("4. Let AI decide based on available content")
            
            video_pref = Prompt.ask(
                "[bright_cyan]Choose video preference (1-4)[/bright_cyan]",
                choices=["1", "2", "3", "4"],
                default="4"
            )
            
            pref_map = {
                "1": "single_comprehensive",
                "2": "multiple_focused", 
                "3": "playlist_series",
                "4": "auto_decide"
            }
            preferences['video_preference'] = pref_map[video_pref]
            
            # Notes generation preferences
            preferences['generate_notes'] = Prompt.ask(
                "[bright_cyan]Generate study notes and questions from videos? (y/n)[/bright_cyan]",
                default="y"
            ).lower() == 'y'
        
        # Resource finder preferences
        preferences['include_resources'] = Prompt.ask(
            "[bright_cyan]Find books, courses, and learning materials? (y/n)[/bright_cyan]",
            default="y"
        ).lower() == 'y'
        
        if preferences['include_resources']:
            print("\nResource preferences:")
            print("1. Free resources only")
            print("2. Paid resources only")
            print("3. Both free and paid resources")
            
            resource_pref = Prompt.ask(
                "[bright_cyan]Choose resource preference (1-3)[/bright_cyan]",
                choices=["1", "2", "3"],
                default="3"
            )
            
            pref_map = {"1": "free", "2": "paid", "3": "both"}
            preferences['resource_preference'] = pref_map[resource_pref]
        
        # Spaced repetition preferences
        preferences['add_to_spaced_repetition'] = Prompt.ask(
            "[bright_cyan]Add topics to spaced repetition system? (y/n)[/bright_cyan]",
            default="y"
        ).lower() == 'y'
        
        return preferences
    
    async def _analyze_topic_videos(self, topic_name: str, preferences: Dict):
        """Analyze videos for a specific topic"""
        self.console.print(f"[bright_cyan]🎥 Finding videos for: {topic_name}[/bright_cyan]")
        
        try:
            with self.console.status(f"Searching for {topic_name} videos..."):
                # Search for videos and playlists
                videos = await self.youtube_client.search_videos(topic_name, 8)
                playlists = await self.youtube_client.search_playlists(topic_name, 3)
                
                if not videos and not playlists:
                    self.console.print(f"[yellow]No videos found for {topic_name}[/yellow]")
                    return
                
                # Analyze content
                analysis = await self.video_analyzer.analyze_videos_and_playlists(videos, playlists, topic_name)
                
                # Display concise results
                self._display_topic_video_summary(analysis, topic_name)
                
                # Generate notes if requested
                if preferences.get('generate_notes', False) and analysis.get('primary_resource'):
                    await self._generate_topic_notes(analysis['primary_resource'], topic_name)
                
        except Exception as e:
            self.console.print(f"[red]Error analyzing videos for {topic_name}: {e}[/red]")
    
    def _display_topic_video_summary(self, analysis: Dict, topic_name: str):
        """Display concise video analysis summary"""
        primary = analysis.get('primary_resource')
        if primary:
            content_type = "Video" if primary.get('type') != 'playlist' else "Playlist"
            self.console.print(f"[bright_green]✓ Best {content_type}:[/bright_green] {primary['title']}")
            self.console.print(f"  Channel: {primary['channel']} | Score: {primary.get('composite_score', 0):.1f}/10")
            
            # Show topic coverage if available
            coverage = analysis.get('topic_coverage_details', {})
            if coverage:
                completeness = coverage.get('learning_completeness', 0)
                self.console.print(f"  Coverage: {completeness:.0f}% of expected topics")
                
                missing = coverage.get('missing_subtopics', [])
                if missing and len(missing) <= 3:
                    self.console.print(f"  [yellow]Missing: {', '.join(missing)}[/yellow]")
        
        # Show supplementary content count
        supp_videos = len(analysis.get('supplementary_videos', []))
        supp_playlists = len(analysis.get('supplementary_playlists', []))
        if supp_videos or supp_playlists:
            self.console.print(f"  [dim]+ {supp_videos} supplementary videos, {supp_playlists} playlists[/dim]")
    
    async def _generate_topic_notes(self, content: Dict, topic_name: str):
        """Generate notes for a topic's primary content"""
        try:
            # Set preferences for automatic generation
            self.notes_generator.set_user_preferences({
                'generate_notes': True,
                'generate_questions': True,
                'notes_style': 'concise'
            })
            
            # Generate notes without status display to avoid conflicts
            notes_data = await self.notes_generator.generate_study_notes(topic_name, content, None)
            
            # Display concise summary
            notes_count = len(notes_data.get('notes', []))
            questions_count = len(notes_data.get('questions', []))
            concepts_count = len(notes_data.get('key_concepts', []))
            
            self.console.print(f"[bright_green]✓ Generated:[/bright_green] {notes_count} notes, {questions_count} questions, {concepts_count} key concepts")
                
        except Exception as e:
            self.console.print(f"[red]Error generating notes: {e}[/red]")
    
    async def _find_topic_resources(self, topic_name: str, preferences: Dict):
        """Find learning resources for a specific topic"""
        self.console.print(f"[bright_cyan]📚 Finding resources for: {topic_name}[/bright_cyan]")
        
        try:
            resource_pref = preferences.get('resource_preference', 'both')
            topic_resources = await self.resource_finder._find_topic_resources(topic_name, resource_pref)
            
            # Display concise summary
            books_count = len(topic_resources.get('books', []))
            courses_count = len(topic_resources.get('courses', []))
            other_count = len(topic_resources.get('resources', []))
            
            if books_count or courses_count or other_count:
                self.console.print(f"[bright_green]✓ Found:[/bright_green] {books_count} books, {courses_count} courses, {other_count} other resources")
                
                # Show top resource
                all_resources = topic_resources.get('books', []) + topic_resources.get('courses', [])
                if all_resources:
                    top_resource = all_resources[0]
                    resource_type = "Book" if 'author' in top_resource else "Course"
                    price_tag = "Free" if top_resource.get('type') == 'free' else "Paid"
                    self.console.print(f"  [bright_white]Top {resource_type}:[/bright_white] {top_resource['title']} ({price_tag})")
            else:
                self.console.print(f"[yellow]Limited resources found for {topic_name}[/yellow]")
                    
        except Exception as e:
            self.console.print(f"[red]Error finding resources for {topic_name}: {e}[/red]")
    
    def _add_topic_to_spaced_repetition(self, topic_name: str, topic_data: Dict):
        """Add topic to spaced repetition system"""
        try:
            description = topic_data.get('description', f'Study topic: {topic_name}')
            success = self.spaced_repetition.add_topic(topic_name, description)
            
            if success:
                self.console.print(f"[bright_green]✓ Added to spaced repetition:[/bright_green] {topic_name}")
            else:
                self.console.print(f"[dim]Already in spaced repetition: {topic_name}[/dim]")
                
        except Exception as e:
            self.console.print(f"[red]Error adding to spaced repetition: {e}[/red]")
    
    async def _display_analysis_summary(self, topic_names: List[str], preferences: Dict):
        """Display final analysis summary and next steps"""
        self.console.print(f"\n{'='*60}")
        self.console.print("[bold bright_green]COMPREHENSIVE ANALYSIS COMPLETE[/bold bright_green]")
        self.console.print(f"{'='*60}")
        
        self.console.print(f"\n[bright_cyan]Processed {len(topic_names)} topics:[/bright_cyan]")
        for topic in topic_names:
            self.console.print(f"• {topic}")
        
        # Show what was included
        included_features = []
        if preferences.get('include_videos'):
            included_features.append("Video analysis and recommendations")
        if preferences.get('generate_notes'):
            included_features.append("Study notes and questions generation")
        if preferences.get('include_resources'):
            included_features.append("Books and courses discovery")
        if preferences.get('add_to_spaced_repetition'):
            included_features.append("Spaced repetition scheduling")
        
        if included_features:
            self.console.print(f"\n[bright_yellow]Features included:[/bright_yellow]")
            for feature in included_features:
                self.console.print(f"✓ {feature}")
        
        # Next steps recommendations
        self.console.print(f"\n[bold bright_magenta]Recommended Next Steps:[/bold bright_magenta]")
        
        if preferences.get('add_to_spaced_repetition'):
            due_count = len(self.spaced_repetition.get_due_topics())
            if due_count > 0:
                self.console.print(f"• Review {due_count} topics due for spaced repetition (Menu option 8)")
            else:
                self.console.print("• Start reviewing topics tomorrow using spaced repetition (Menu option 8)")
        
        if preferences.get('include_videos'):
            self.console.print("• Watch recommended videos and take notes")
            self.console.print("• Use generated study questions for self-assessment")
        
        if preferences.get('include_resources'):
            self.console.print("• Explore recommended books and courses for deeper learning")
        
        self.console.print("• Set learning goals to track your progress (Menu option 4)")
        self.console.print("• Start focused study sessions with Pomodoro timer (Menu option 7)")
        
        self.console.print(f"\n[bright_green]Your learning journey is ready to begin![/bright_green]")
        self.console.print("[dim]All data has been saved and is accessible from the main menu.[/dim]")
    
    async def _interactive_videos(self):
        """Interactive video search and analysis"""
        self.console.print(Rule("[bold bright_blue]Smart Video Analysis[/bold bright_blue]"))
        
        topic = Prompt.ask("[bright_cyan]Enter topic to search for videos[/bright_cyan]")
        if not topic:
            self.console.print("[red]No topic provided[/red]")
            return
        
        # Ask user preference
        preference = self.video_analyzer.ask_user_video_preference(topic)
        
        with self.console.status(f"[bright_cyan]Searching for {topic} videos..."):
            try:
                # Search for videos and playlists
                videos = await self.youtube_client.search_videos(topic, 10)
                playlists = await self.youtube_client.search_playlists(topic, 5)
                
                if not videos and not playlists:
                    self.console.print("[yellow]No videos or playlists found[/yellow]")
                    return
                
                # Analyze content
                analysis = await self.video_analyzer.analyze_videos_and_playlists(videos, playlists, topic)
                
                # Display results
                self._display_video_analysis(analysis, topic)
                
                # Ask if user wants notes and questions
                if analysis.get('primary_resource'):
                    generate_notes = Prompt.ask(
                        "[bright_yellow]Generate study notes and questions for the recommended content? (y/n)[/bright_yellow]",
                        default="y"
                    ).lower() == 'y'
                    
                    if generate_notes:
                        await self._generate_content_notes(analysis['primary_resource'], topic)
                
            except Exception as e:
                self.console.print(f"[red]Video search error: {e}[/red]")
    
    def _display_video_analysis(self, analysis: Dict, topic: str):
        """Display video analysis results"""
        self.console.print(f"\n[bold bright_green]Video Analysis Results for '{topic}'[/bold bright_green]")
        
        primary = analysis.get('primary_resource')
        if primary:
            self.console.print(f"\n[bold bright_cyan]Recommended Primary Content:[/bold bright_cyan]")
            content_type = "📺 Video" if primary.get('type') != 'playlist' else "📚 Playlist"
            self.console.print(f"{content_type} {primary['title']}")
            self.console.print(f"Channel: {primary['channel']}")
            self.console.print(f"Score: {primary.get('composite_score', 0):.1f}/10")
            
            if primary.get('type') == 'playlist':
                self.console.print(f"Videos: {primary.get('video_count', 0)}")
            else:
                self.console.print(f"Duration: {primary.get('duration', 'Unknown')}")
        
        # Display topic coverage
        coverage = analysis.get('topic_coverage_details', {})
        if coverage:
            self.console.print(f"\n[bold bright_yellow]Topic Coverage Analysis:[/bold bright_yellow]")
            self.console.print(f"Coverage: {coverage.get('learning_completeness', 0):.0f}%")
            
            covered = coverage.get('covered_subtopics', [])
            if covered:
                self.console.print(f"Covered topics: {', '.join(covered[:5])}")
            
            missing = coverage.get('missing_subtopics', [])
            if missing:
                self.console.print(f"[yellow]Missing topics: {', '.join(missing[:3])}[/yellow]")
            
            recommendations = coverage.get('content_recommendations', [])
            if recommendations:
                self.console.print(f"\n[bold bright_magenta]Recommendations:[/bold bright_magenta]")
                for rec in recommendations:
                    self.console.print(f"• {rec}")
        
        # Display supplementary content
        supplementary_videos = analysis.get('supplementary_videos', [])
        supplementary_playlists = analysis.get('supplementary_playlists', [])
        
        if supplementary_videos or supplementary_playlists:
            self.console.print(f"\n[bold bright_cyan]Additional Resources:[/bold bright_cyan]")
            
            for video in supplementary_videos[:3]:
                self.console.print(f"📺 {video['title']} ({video.get('duration', 'Unknown')})")
            
            for playlist in supplementary_playlists[:2]:
                self.console.print(f"📚 {playlist['title']} ({playlist.get('video_count', 0)} videos)")
    
    async def _generate_content_notes(self, content: Dict, topic: str):
        """Generate notes and questions for content"""
        with self.console.status("[bright_cyan]Generating study notes and questions..."):
            try:
                # Ask user preferences first
                preferences = self.notes_generator.ask_user_preferences()
                
                # Generate notes (transcript would be fetched in real implementation)
                notes_data = await self.notes_generator.generate_study_notes(topic, content, None)
                
                # Display generated materials
                self.console.print(f"\n[bold bright_green]Generated Study Materials[/bold bright_green]")
                
                if notes_data.get('notes') and preferences.get('generate_notes'):
                    self.console.print(f"\n[bold bright_cyan]Study Notes:[/bold bright_cyan]")
                    for i, note in enumerate(notes_data['notes'], 1):
                        self.console.print(f"{i}. {note}")
                
                if notes_data.get('questions') and preferences.get('generate_questions'):
                    self.console.print(f"\n[bold bright_yellow]Study Questions:[/bold bright_yellow]")
                    for i, question in enumerate(notes_data['questions'], 1):
                        self.console.print(f"{i}. {question}")
                
                if notes_data.get('key_concepts'):
                    self.console.print(f"\n[bold bright_magenta]Key Concepts:[/bold bright_magenta]")
                    for concept in notes_data['key_concepts']:
                        self.console.print(f"• {concept}")
                
            except Exception as e:
                self.console.print(f"[red]Error generating notes: {e}[/red]")
    
    async def _interactive_resources(self):
        """Interactive resource finder"""
        self.console.print(Rule("[bold bright_blue]Resource Finder[/bold bright_blue]"))
        
        # Get topics from database or user input
        topics = self.db.get_all_topics()
        
        if topics:
            self.console.print("[bright_green]Found topics from your syllabus:[/bright_green]")
            for i, topic in enumerate(topics[:10], 1):
                self.console.print(f"{i}. {topic.get('name', 'Unknown')}")
            
            use_existing = Prompt.ask(
                "[bright_yellow]Use existing topics? (y/n)[/bright_yellow]",
                default="y"
            ).lower() == 'y'
            
            if use_existing:
                topic_names = [topic.get('name', '') for topic in topics[:10]]
            else:
                topic_input = Prompt.ask("[bright_cyan]Enter topics (comma-separated)[/bright_cyan]")
                topic_names = [t.strip() for t in topic_input.split(',') if t.strip()]
        else:
            topic_input = Prompt.ask("[bright_cyan]Enter topics to find resources for (comma-separated)[/bright_cyan]")
            topic_names = [t.strip() for t in topic_input.split(',') if t.strip()]
        
        if not topic_names:
            self.console.print("[red]No topics provided[/red]")
            return
        
        # Ask for resource preference
        preference = self.resource_finder._ask_user_preference()
        
        with self.console.status(f"[bright_cyan]Finding resources for {len(topic_names)} topics..."):
            try:
                resources = await self.resource_finder.find_resources_for_syllabus(topic_names, preference)
                
                # Display results using the built-in display method
                self.resource_finder.display_resources(resources)
                
            except Exception as e:
                self.console.print(f"[red]Resource search error: {e}[/red]")
    
    async def _interactive_notes(self):
        """Interactive notes generation"""
        self.console.print(Rule("[bold bright_blue]Generate Study Notes[/bold bright_blue]"))
        
        # Get user preferences
        preferences = self.notes_generator.ask_user_preferences()
        
        if not preferences.get('generate_notes') and not preferences.get('generate_questions'):
            self.console.print("[yellow]No content generation selected[/yellow]")
            return
        
        # Get topic and content
        topic = Prompt.ask("[bright_cyan]Enter topic for note generation[/bright_cyan]")
        if not topic:
            self.console.print("[red]No topic provided[/red]")
            return
        
        content_source = Prompt.ask(
            "[bright_yellow]Content source[/bright_yellow]",
            choices=["video_search", "manual_input"],
            default="video_search"
        )
        
        if content_source == "video_search":
            # Search for a video and generate notes
            with self.console.status(f"[bright_cyan]Searching for {topic} content..."):
                try:
                    videos = await self.youtube_client.search_videos(topic, 3)
                    if videos:
                        # Use the first video
                        video = videos[0]
                        self.console.print(f"[bright_green]Using video: {video['title']}[/bright_green]")
                        
                        notes_data = await self.notes_generator.generate_study_notes(topic, video, None)
                        self._display_generated_notes(notes_data, preferences)
                    else:
                        self.console.print("[yellow]No videos found for the topic[/yellow]")
                except Exception as e:
                    self.console.print(f"[red]Error: {e}[/red]")
        
        else:
            # Manual content input
            content_text = Prompt.ask("[bright_cyan]Enter content text or description[/bright_cyan]")
            if content_text:
                # Create a mock video object
                mock_video = {
                    'title': f"Manual content for {topic}",
                    'description': content_text,
                    'id': 'manual_input',
                    'channel': 'User Input'
                }
                
                notes_data = await self.notes_generator.generate_study_notes(topic, mock_video, content_text)
                self._display_generated_notes(notes_data, preferences)
    
    def _display_generated_notes(self, notes_data: Dict, preferences: Dict):
        """Display generated notes and questions"""
        self.console.print(f"\n[bold bright_green]Generated Study Materials for '{notes_data['topic']}'[/bold bright_green]")
        
        if notes_data.get('notes') and preferences.get('generate_notes'):
            self.console.print(f"\n[bold bright_cyan]Study Notes:[/bold bright_cyan]")
            for i, note in enumerate(notes_data['notes'], 1):
                self.console.print(f"{i}. {note}")
        
        if notes_data.get('questions') and preferences.get('generate_questions'):
            self.console.print(f"\n[bold bright_yellow]Study Questions:[/bold bright_yellow]")
            for i, question in enumerate(notes_data['questions'], 1):
                self.console.print(f"{i}. {question}")
        
        if notes_data.get('key_concepts'):
            self.console.print(f"\n[bold bright_magenta]Key Concepts:[/bold bright_magenta]")
            for concept in notes_data['key_concepts']:
                self.console.print(f"• {concept}")
        
        if notes_data.get('study_tips'):
            self.console.print(f"\n[bold bright_blue]Study Tips:[/bold bright_blue]")
            for tip in notes_data['study_tips']:
                self.console.print(f"• {tip}")

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
            await app._handle_analyze_command(args)
        elif args.command == 'search':
            await app._handle_search_command(args)
        elif args.command == 'review':
            await app._handle_review_command(args)
        elif args.command == 'goals':
            await app._handle_goals_command(args)
        elif args.command == 'quiz':
            await app._handle_quiz_command(args)
        elif args.command == 'progress':
            await app._handle_progress_command(args)
        elif args.command == 'session':
            await app._handle_session_command(args)
        elif args.command == 'bookmarks':
            await app._handle_bookmarks_command(args)
        elif args.command == 'platforms':
            await app._handle_platforms_command(args)
        elif args.command == 'interactive':
            # Interactive mode
            while True:
                try:
                    app.print_banner()
                    command = app.show_interactive_menu()
                    
                    if command == 'exit':
                        app.console.print("[bright_green]Thanks for using Syllabo![/bright_green]")
                        break
                    elif command == 'help':
                        app._show_help()
                        Prompt.ask("\n[dim]Press Enter to continue[/dim]", default="")
                    else:
                        await app._handle_interactive_command(command)
                        Prompt.ask("\n[dim]Press Enter to continue[/dim]", default="")
                        app.console.clear()
                except KeyboardInterrupt:
                    app.console.print("\n[bright_green]Thanks for using Syllabo![/bright_green]")
                    break
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