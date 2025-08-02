#!/usr/bin/env python3
"""
Syllabo - AI-Powered Learning Assistant
Main entry point for all features
"""

import os
import sys
import json
import argparse
import asyncio
import time
from datetime import datetime
from typing import List, Dict, Any, Optional
from dotenv import load_dotenv
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.rule import Rule
from rich.progress import Progress

# Load environment variables
load_dotenv()

# Add src directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

# Import all components
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
from src.export_system import ExportSystem

class SyllaboMain:
    """Main application class with all features"""
    
    def __init__(self):
        self.console = Console()
        self.logger = SyllaboLogger("main")
        
        # Initialize core components
        self.db = SyllaboDatabase()
        self.ai_client = AIClient()
        self.youtube_client = YouTubeClient()
        self.video_analyzer = VideoAnalyzer(self.ai_client)
        self.syllabus_parser = SyllabusParser()
        self.spaced_repetition = SpacedRepetitionEngine()
        self.notifications = NotificationSystem()
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
        """Print enhanced application banner"""
        banner_text = """
[bold cyan]███████╗██╗   ██╗██╗     ██╗      █████╗ ██████╗  ██████╗ 
██╔════╝╚██╗ ██╔╝██║     ██║     ██╔══██╗██╔══██╗██╔═══██╗
███████╗ ╚████╔╝ ██║     ██║     ███████║██████╔╝██║   ██║
╚════██║  ╚██╔╝  ██║     ██║     ██╔══██║██╔══██╗██║   ██║
███████║   ██║   ███████╗███████╗██║  ██║██████╔╝╚██████╔╝
╚══════╝   ╚═╝   ╚══════╝╚══════╝╚═╝  ╚═╝╚═════╝  ╚═════╝[/bold cyan]

[bold white]AI-Powered Learning Assistant[/bold white]
[dim]Your comprehensive educational resource manager[/dim]
        """
        
        self.console.print(Panel(
            banner_text.strip(),
            border_style="cyan",
            padding=(1, 2)
        ))
        
        # Show quick stats
        self._show_quick_stats()
    
    def _show_quick_stats(self):
        """Show quick statistics and status"""
        try:
            # Get basic stats
            active_goals = len(self.goals_manager.get_active_goals())
            due_reviews = len(self.spaced_repetition.get_due_topics())
            total_bookmarks = len(self.bookmark_manager.bookmarks)
            
            stats_table = Table(show_header=False, box=None, padding=(0, 2))
            stats_table.add_column(style="green")
            stats_table.add_column(style="yellow") 
            stats_table.add_column(style="blue")
            stats_table.add_column(style="magenta")
            
            stats_table.add_row(
                f"Active Goals: {active_goals}",
                f"Due Reviews: {due_reviews}",
                f"Bookmarks: {total_bookmarks}",
                f"Session: {'Active' if self.study_session_manager.current_session else 'None'}"
            )
            
            self.console.print(stats_table)
            self.console.print()
            
        except Exception:
            # If stats fail, just continue silently
            pass
    
    def show_interactive_menu(self):
        """Show interactive main menu"""
        self.console.print(Rule("[bold cyan]Main Menu[/bold cyan]"))
        
        menu_options = [
            ("1", "analyze", "Analyze Syllabus", "Process syllabus and find learning resources"),
            ("2", "quiz", "Interactive Quizzes", "Generate and take quizzes from content"),
            ("3", "progress", "Progress Dashboard", "View learning progress and analytics"),
            ("4", "goals", "Study Goals", "Manage learning goals and milestones"),
            ("5", "platforms", "Multi-Platform Search", "Search across learning platforms"),
            ("6", "bookmarks", "Smart Bookmarks", "Manage video bookmarks and notes"),
            ("7", "session", "Study Sessions", "Pomodoro timer and focus sessions"),
            ("9", "help", "Help & Documentation", "Get help and usage information"),
            ("10", "exit", "Exit", "Exit the application")
        ]
        
        menu_table = Table(show_header=True, header_style="bold magenta")
        menu_table.add_column("Option", style="cyan", width=8)
        menu_table.add_column("Feature", style="green", width=20)
        menu_table.add_column("Description", style="white", width=40)
        
        for option, cmd, feature, desc in menu_options:
            menu_table.add_row(option, feature, desc)
        
        self.console.print(menu_table)
        self.console.print()
        
        return self._get_user_choice(menu_options)
    
    def _get_user_choice(self, menu_options):
        """Get user menu choice with validation"""
        while True:
            choice = input("Select an option (1-10): ").strip()
            
            for option, cmd, feature, desc in menu_options:
                if choice == option:
                    return cmd
            
            self.console.print(f"[red]Invalid choice '{choice}'. Please select 1-10.[/red]")
    
    def show_feature_help(self, feature):
        """Show contextual help for features"""
        help_text = {
            "analyze": """
[bold cyan]Syllabus Analysis[/bold cyan]
Analyze your course syllabus to extract topics and find learning resources.

[yellow]Quick Start:[/yellow]
• python main.py analyze --file syllabus.pdf --search-videos --print-results
• python main.py analyze --text "Your syllabus content" --include-podcasts

[yellow]Options:[/yellow]
• --file: Path to syllabus file (PDF or text)
• --text: Direct syllabus text input
• --search-videos: Find YouTube videos for topics
• --include-podcasts: Include educational podcasts
• --include-reading: Include articles and papers
• --add-to-review: Add topics to spaced repetition
• --difficulty-filter: Filter by beginner/intermediate/advanced
            """,
            "quiz": """
[bold cyan]Interactive Quiz System[/bold cyan]
Generate and take AI-powered quizzes from your study content.

[yellow]Commands:[/yellow]
• python main.py quiz generate --topic "Machine Learning" --num-questions 10
• python main.py quiz take
• python main.py quiz history

[yellow]Features:[/yellow]
• AI-generated questions from content
• Multiple choice, true/false, and short answer
• Automatic scoring and feedback
• Progress tracking
            """,
            "progress": """
[bold cyan]Progress Dashboard[/bold cyan]
Track your learning progress with visual analytics.

[yellow]Commands:[/yellow]
• python main.py progress
• python main.py progress --export

[yellow]Features:[/yellow]
• Study streak tracking
• Topic mastery levels
• Weekly activity summary
• Upcoming review schedule
• Exportable progress reports
            """
        }
        
        if feature in help_text:
            self.console.print(Panel(help_text[feature].strip(), title=f"Help: {feature.title()}", border_style="yellow"))
        else:
            self.console.print(f"[yellow]Help for '{feature}' - Use --help flag with the command for detailed options[/yellow]")
    
    async def analyze_syllabus(self, args):
        """Analyze syllabus with enhanced UI and progress tracking"""
        start_time = time.time()
        
        # Enhanced header
        self.console.print(Rule("[bold blue]Syllabus Analysis[/bold blue]"))
        
        # Load syllabus content with progress
        with Progress() as progress:
            task = progress.add_task("[cyan]Loading syllabus content...", total=100)
            
            if args.file:
                progress.update(task, advance=20)
                try:
                    syllabus_content = self.syllabus_parser.load_from_file(args.file)
                    syllabus_title = os.path.basename(args.file)
                    progress.update(task, advance=30)
                    self.console.print(f"[green]✓[/green] Loaded syllabus: [cyan]{syllabus_title}[/cyan]")
                except Exception as e:
                    self.console.print(f"[red]✗ Error loading file: {e}[/red]")
                    return
            elif args.text:
                progress.update(task, advance=30)
                syllabus_content = args.text
                syllabus_title = f"Direct input - {datetime.now().strftime('%Y-%m-%d %H:%M')}"
                self.console.print(f"[green]✓[/green] Loaded text content ([cyan]{len(args.text)} characters[/cyan])")
            else:
                progress.update(task, completed=100)
                self.console.print("[red]✗ Error: Please provide either --file or --text[/red]")
                return
            
            progress.update(task, advance=20)
            
            # Extract topics with AI
            progress.update(task, description="[cyan]Extracting topics with AI...")
            try:
                topics = await self.syllabus_parser.extract_topics(syllabus_content, self.ai_client)
                progress.update(task, advance=30)
                
                if topics:
                    self.console.print(f"[green]✓[/green] Found [bold green]{len(topics)}[/bold green] topics")
                    
                    # Show topics preview
                    if len(topics) <= 5:
                        topic_list = ", ".join([t['name'] for t in topics])
                    else:
                        topic_list = ", ".join([t['name'] for t in topics[:3]]) + f" and {len(topics)-3} more"
                    
                    self.console.print(f"[dim]Topics: {topic_list}[/dim]")
                else:
                    self.console.print("[yellow]⚠ No topics found. Try refining your syllabus content.[/yellow]")
                    return
                    
            except Exception as e:
                self.console.print(f"[red]✗ Error extracting topics: {e}[/red]")
                return
            
            progress.update(task, completed=100)
        
        # Save to database
        self.console.print("[cyan]Saving to database...[/cyan]")
        syllabus_id = self.db.save_syllabus(syllabus_title, syllabus_content)
        topic_ids = self.db.save_topics(syllabus_id, topics)
        self.console.print("[green]✓[/green] Saved to database")
        
        # Search for content if requested
        if args.search_videos or args.include_podcasts or args.include_reading:
            self.console.print(Rule("[bold yellow]Content Discovery[/bold yellow]"))
            await self._search_comprehensive_content(topics, args)
        
        # Add to spaced repetition if requested
        if args.add_to_review:
            self.console.print(Rule("[bold magenta]Spaced Repetition[/bold magenta]"))
            added_count = self._add_topics_to_review(topics)
            if added_count > 0:
                self.console.print(f"[green]✓[/green] Added {added_count} topics to review schedule")
                self.console.print("[dim]Use 'python main.py progress' to see your review schedule[/dim]")
        
        # Final summary
        processing_time = time.time() - start_time
        self._show_analysis_summary(syllabus_title, topics, processing_time, args)
    
    def _show_analysis_summary(self, title, topics, processing_time, args):
        """Show comprehensive analysis summary"""
        summary_table = Table(title="Analysis Summary", show_header=False)
        summary_table.add_column("Metric", style="cyan")
        summary_table.add_column("Value", style="green")
        
        summary_table.add_row("Syllabus", title)
        summary_table.add_row("Topics Found", str(len(topics)))
        summary_table.add_row("Processing Time", f"{processing_time:.1f}s")
        
        if args.search_videos:
            summary_table.add_row("Video Search", "✓ Enabled")
        if args.include_podcasts:
            summary_table.add_row("Podcast Search", "✓ Enabled")
        if args.include_reading:
            summary_table.add_row("Reading Materials", "✓ Enabled")
        if args.add_to_review:
            summary_table.add_row("Added to Reviews", "✓ Yes")
        
        self.console.print(summary_table)
        
        # Next steps suggestions
        self.console.print(Rule("[bold green]Next Steps[/bold green]"))
        suggestions = [
            "📊 View progress: python main.py progress",
            "🧠 Take a quiz: python main.py quiz generate --topic 'Topic Name'",
            "⏱️ Start study session: python main.py session start --topic 'Topic Name'",
            "🎯 Set goals: python main.py goals create --title 'Daily Study' --type daily --target 30 --unit minutes"
        ]
        
        for suggestion in suggestions:
            self.console.print(f"  {suggestion}")
        
        self.console.print()
    
    async def _search_comprehensive_content(self, topics, args):
        """Search for comprehensive content across platforms with enhanced UI"""
        total_topics = len(topics)
        
        with Progress() as progress:
            main_task = progress.add_task("[cyan]Searching content across platforms...", total=total_topics)
            
            for i, topic in enumerate(topics, 1):
                topic_name = topic['name']
                progress.update(main_task, description=f"[cyan]Searching: {topic_name} ({i}/{total_topics})[/cyan]")
                
                all_content = {}
                content_found = 0
                
                # YouTube videos
                if args.search_videos:
                    try:
                        videos = await self.youtube_client.search_videos(topic_name, args.max_videos or 5)
                        if videos:
                            analyzed_videos = await self.video_analyzer.analyze_videos_and_playlists(videos, [], topic_name)
                            all_content['videos'] = analyzed_videos.get('supplementary_videos', [])
                            content_found += len(all_content['videos'])
                    except Exception as e:
                        self.console.print(f"[yellow]⚠ Video search failed for {topic_name}: {e}[/yellow]")
                
                # Multi-platform courses
                if hasattr(args, 'include_platforms') and args.include_platforms:
                    try:
                        platform_results = await self.platform_integrator.search_all_platforms(topic_name)
                        all_content['courses'] = platform_results
                        content_found += sum(len(courses) for courses in platform_results.values())
                    except Exception as e:
                        self.console.print(f"[yellow]⚠ Platform search failed for {topic_name}: {e}[/yellow]")
                
                # Podcasts and reading
                if args.include_podcasts:
                    try:
                        podcasts = self.podcast_integrator.search_podcasts(topic_name)
                        all_content['podcasts'] = podcasts
                        content_found += len(podcasts)
                    except Exception as e:
                        self.console.print(f"[yellow]⚠ Podcast search failed for {topic_name}: {e}[/yellow]")
                
                if args.include_reading:
                    try:
                        reading = self.podcast_integrator.search_reading_resources(topic_name)
                        all_content['reading'] = reading
                        content_found += len(reading)
                    except Exception as e:
                        self.console.print(f"[yellow]⚠ Reading search failed for {topic_name}: {e}[/yellow]")
                
                # Apply difficulty filter if specified
                if hasattr(args, 'difficulty_filter') and args.difficulty_filter:
                    all_content = self._filter_by_difficulty(all_content, args.difficulty_filter)
                
                # Show progress update
                if content_found > 0:
                    self.console.print(f"[green]✓[/green] Found {content_found} resources for [cyan]{topic_name}[/cyan]")
                else:
                    self.console.print(f"[yellow]⚠[/yellow] No resources found for [cyan]{topic_name}[/cyan]")
                
                # Display results
                if args.print_results:
                    self._display_content_results(topic_name, all_content)
                
                progress.update(main_task, advance=1)
    
    def _filter_by_difficulty(self, content, difficulty_level):
        """Filter content by difficulty level"""
        filtered_content = {}
        
        for content_type, items in content.items():
            if items:
                # Analyze difficulty for items that don't have it
                analyzed_items = self.difficulty_analyzer.batch_analyze_difficulty(items)
                filtered_items = self.difficulty_analyzer.filter_by_difficulty(analyzed_items, difficulty_level)
                filtered_content[content_type] = filtered_items
        
        return filtered_content
    
    def _display_content_results(self, topic_name, content):
        """Display content results in formatted tables"""
        self.console.print(f"\n[bold yellow]Results for: {topic_name}[/bold yellow]")
        
        for content_type, items in content.items():
            if items:
                table = Table(title=f"{content_type.title()}")
                table.add_column("Title", style="cyan")
                table.add_column("Source", style="yellow")
                table.add_column("Difficulty", style="green")
                table.add_column("URL", style="blue")
                
                for item in items[:5]:  # Show top 5
                    table.add_row(
                        item.get('title', 'Unknown')[:50],
                        item.get('source', item.get('channel', 'Unknown')),
                        item.get('difficulty_level', 'N/A'),
                        item.get('url', '')[:50]
                    )
                
                self.console.print(table)
    
    def _add_topics_to_review(self, topics):
        """Add topics to spaced repetition system"""
        added_count = 0
        for topic in topics:
            if self.spaced_repetition.add_topic(topic['name'], topic.get('description', '')):
                added_count += 1
        
        self.console.print(f"[green]Added {added_count} topics to review schedule[/green]")
    
    async def handle_quiz_command(self, args):
        """Handle quiz-related commands with enhanced UI"""
        self.console.print(Rule(f"[bold magenta]Quiz System - {args.action.title()}[/bold magenta]"))
        
        if args.action == 'generate':
            if not args.topic:
                self.console.print("[red]✗ Error: --topic is required for quiz generation[/red]")
                self.show_feature_help('quiz')
                return
            
            # Load content with progress
            with Progress() as progress:
                task = progress.add_task("[cyan]Preparing quiz content...", total=100)
                
                if args.content_file:
                    try:
                        with open(args.content_file, 'r') as f:
                            content = f.read()
                        progress.update(task, advance=30)
                        self.console.print(f"[green]✓[/green] Loaded content from [cyan]{args.content_file}[/cyan]")
                    except Exception as e:
                        self.console.print(f"[red]✗ Error loading file: {e}[/red]")
                        return
                else:
                    content = f"Educational content about {args.topic}"
                    progress.update(task, advance=30)
                    self.console.print(f"[yellow]⚠[/yellow] Using default content for [cyan]{args.topic}[/cyan]")
                
                progress.update(task, advance=20, description="[cyan]Generating quiz with AI...")
                
                try:
                    quiz = await self.quiz_generator.generate_quiz_from_content(
                        content, args.topic, args.num_questions or 5
                    )
                    progress.update(task, advance=50)
                    
                    if 'error' in quiz:
                        self.console.print(f"[red]✗ Error generating quiz: {quiz['error']}[/red]")
                        return
                    
                    progress.update(task, completed=100)
                    
                except Exception as e:
                    self.console.print(f"[red]✗ Quiz generation failed: {e}[/red]")
                    return
            
            # Show quiz summary
            quiz_info = Table(title="Quiz Generated", show_header=False)
            quiz_info.add_column("Property", style="cyan")
            quiz_info.add_column("Value", style="green")
            
            quiz_info.add_row("Topic", args.topic)
            quiz_info.add_row("Questions", str(len(quiz['questions'])))
            quiz_info.add_row("Difficulty", quiz.get('difficulty', 'Mixed'))
            
            self.console.print(quiz_info)
            
            # Interactive quiz taking option
            self.console.print("\n[bold yellow]Options:[/bold yellow]")
            self.console.print("1. Take quiz now")
            self.console.print("2. Save for later")
            self.console.print("3. Preview questions")
            
            choice = input("\nSelect option (1-3): ").strip()
            
            if choice == '1':
                self.console.print(Rule("[bold green]Starting Quiz[/bold green]"))
                results = self.quiz_generator.take_quiz(quiz)
                self.quiz_generator.save_quiz_results(results)
                self._show_quiz_results(results)
            elif choice == '2':
                # Save quiz logic here
                self.console.print("[green]✓[/green] Quiz saved for later")
            elif choice == '3':
                self._preview_quiz_questions(quiz)
            else:
                self.console.print("[yellow]Invalid choice. Quiz saved for later.[/yellow]")
        
        elif args.action == 'take':
            self.console.print("[yellow]Quiz taking functionality - load existing quiz[/yellow]")
        
        elif args.action == 'history':
            self.console.print("[yellow]Quiz history functionality[/yellow]")
    
    def _show_quiz_results(self, results):
        """Show quiz results with enhanced formatting"""
        score = results['score']
        
        # Determine performance level
        if score >= 90:
            performance = "[bold green]Excellent![/bold green]"
            emoji = "🎉"
        elif score >= 80:
            performance = "[bold blue]Great job![/bold blue]"
            emoji = "👏"
        elif score >= 70:
            performance = "[bold yellow]Good work![/bold yellow]"
            emoji = "👍"
        else:
            performance = "[bold red]Keep practicing![/bold red]"
            emoji = "💪"
        
        # Results summary
        results_panel = Panel(
            f"{emoji} {performance}\n\n"
            f"Score: [bold]{score:.1f}%[/bold]\n"
            f"Correct: [green]{results['correct_answers']}[/green] / [blue]{results['total_questions']}[/blue]\n"
            f"Topic: [cyan]{results['topic']}[/cyan]",
            title="Quiz Results",
            border_style="green" if score >= 70 else "yellow"
        )
        
        self.console.print(results_panel)
        
        # Suggestions based on performance
        if score < 70:
            self.console.print("\n[bold yellow]Suggestions:[/bold yellow]")
            self.console.print("• Review the topic materials")
            self.console.print("• Try a study session: python main.py session start --topic '" + results['topic'] + "'")
            self.console.print("• Add to spaced repetition for regular review")
    
    def _preview_quiz_questions(self, quiz):
        """Preview quiz questions without answers"""
        self.console.print(Rule("[bold cyan]Quiz Preview[/bold cyan]"))
        
        for i, question in enumerate(quiz['questions'], 1):
            self.console.print(f"\n[bold]{i}. {question['question']}[/bold]")
            
            if question['type'] == 'multiple_choice':
                for j, option in enumerate(question['options']):
                    self.console.print(f"   {chr(65+j)}. {option}")
            elif question['type'] == 'true_false':
                self.console.print("   True / False")
            else:
                self.console.print("   [Short answer question]")
        
        self.console.print(f"\n[dim]Total questions: {len(quiz['questions'])}[/dim]")
    
    def handle_progress_command(self, args):
        """Handle progress dashboard commands with enhanced UI"""
        self.console.print(Rule("[bold green]Learning Progress Dashboard[/bold green]"))
        
        try:
            self.progress_dashboard.show_dashboard()
            
            if args.export:
                with Progress() as progress:
                    task = progress.add_task("[cyan]Generating progress report...", total=100)
                    
                    report = self.progress_dashboard.generate_progress_report()
                    progress.update(task, advance=80)
                    
                    filename = f"progress_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
                    with open(filename, 'w') as f:
                        f.write(report)
                    progress.update(task, completed=100)
                    
                    self.console.print(f"[green]✓ Progress report exported to: {filename}[/green]")
            
            # Show quick actions
            self.console.print(Rule("[bold cyan]Quick Actions[/bold cyan]"))
            actions = [
                "🎯 Set new goal: python main.py goals create",
                "📚 Start study session: python main.py session start --topic 'Topic Name'",
                "🧠 Take a quiz: python main.py quiz generate --topic 'Topic Name'",
                "📖 Review due topics: Check spaced repetition schedule"
            ]
            
            for action in actions:
                self.console.print(f"  {action}")
                
        except Exception as e:
            self.console.print(f"[red]✗ Error loading progress dashboard: {e}[/red]")
    
    def handle_goals_command(self, args):
        """Handle goals management commands"""
        if args.action == 'create':
            if not all([args.title, args.type, args.target, args.unit]):
                self.console.print("[red]Error: --title, --type, --target, and --unit are required[/red]")
                return
            
            goal_id = self.goals_manager.create_goal(
                args.title, args.description or "", args.type,
                args.target, args.unit
            )
            self.console.print(f"[green]Created goal: {args.title} (ID: {goal_id})[/green]")
        
        elif args.action == 'list':
            active_goals = self.goals_manager.get_active_goals()
            if not active_goals:
                self.console.print("[yellow]No active goals[/yellow]")
                return
            
            table = Table(title="Active Goals")
            table.add_column("Title", style="cyan")
            table.add_column("Progress", style="green")
            table.add_column("Type", style="yellow")
            
            for goal in active_goals:
                progress = (goal.current_value / goal.target_value) * 100
                table.add_row(
                    goal.title,
                    f"{goal.current_value}/{goal.target_value} {goal.unit} ({progress:.1f}%)",
                    goal.goal_type
                )
            
            self.console.print(table)
        
        elif args.action == 'suggest':
            suggestions = self.goals_manager.suggest_goals()
            table = Table(title="Suggested Goals")
            table.add_column("Title", style="cyan")
            table.add_column("Target", style="green")
            table.add_column("Type", style="yellow")
            
            for suggestion in suggestions:
                table.add_row(
                    suggestion['title'],
                    f"{suggestion['target']} {suggestion['unit']}",
                    suggestion['type']
                )
            
            self.console.print(table)
    
    async def handle_platforms_command(self, args):
        """Handle multi-platform search commands"""
        self.console.print(f"[cyan]Searching multiple platforms for: {args.topic}[/cyan]")
        
        results = await self.platform_integrator.search_all_platforms(args.topic)
        
        for platform, courses in results.items():
            if courses:
                if args.free_only:
                    courses = self.platform_integrator.filter_by_preference(courses, free_only=True)
                
                if courses:
                    table = Table(title=f"{platform.title()} Courses")
                    table.add_column("Title", style="cyan")
                    table.add_column("Provider", style="yellow")
                    table.add_column("Free", style="green")
                    table.add_column("URL", style="blue")
                    
                    for course in courses:
                        table.add_row(
                            course['title'][:50],
                            course['provider'],
                            "Yes" if course.get('free', False) else "No",
                            course['url'][:50]
                        )
                    
                    self.console.print(table)
    
    def handle_bookmarks_command(self, args):
        """Handle bookmark management commands"""
        if args.action == 'add':
            if not all([args.video_id, args.video_title, args.timestamp, args.note, args.topic]):
                self.console.print("[red]Error: --video-id, --video-title, --timestamp, --note, and --topic are required[/red]")
                return
            
            bookmark_id = self.bookmark_manager.add_bookmark(
                args.video_id, args.video_title, args.timestamp,
                args.note, args.topic, args.tags or [], args.importance or 3
            )
            self.console.print(f"[green]Added bookmark: {bookmark_id}[/green]")
        
        elif args.action == 'list':
            if args.topic:
                bookmarks = self.bookmark_manager.get_bookmarks_by_topic(args.topic)
            for bookmark in bookmarks:
                table.add_row(
                    bookmark.video_title[:30],
                    bookmark.timestamp,
                    bookmark.note[:40],
                    "⭐" * bookmark.importance
                )
            
            self.console.print(table)
        
        elif args.action == 'search':
            if not args.query:
                self.console.print("[red]Error: --query is required for search[/red]")
                return
            
            results = self.bookmark_manager.search_bookmarks(args.query)
            self.console.print(f"[green]Found {len(results)} bookmarks matching '{args.query}'[/green]")
            
            for bookmark in results:
                self.console.print(f"[cyan]{bookmark.video_title}[/cyan] - {bookmark.timestamp}")
                self.console.print(f"  Note: {bookmark.note}")
        
        elif args.action == 'export':
            filename = self.bookmark_manager.export_bookmarks(args.format or 'json')
            self.console.print(f"[green]Bookmarks exported to: {filename}[/green]")
    
    def handle_session_command(self, args):
        """Handle study session commands with enhanced UI"""
        self.console.print(Rule(f"[bold blue]Study Session - {args.action.title()}[/bold blue]"))
        
        if args.action == 'start':
            if not args.topic:
                self.console.print("[red]✗ Error: --topic is required to start a session[/red]")
                self.show_feature_help('session')
                return
            
            # Show session setup
            session_info = Table(title="Starting Study Session", show_header=False)
            session_info.add_column("Setting", style="cyan")
            session_info.add_column("Value", style="green")
            
            session_info.add_row("Topic", args.topic)
            session_info.add_row("Duration", f"{args.duration or 25} minutes")
            session_info.add_row("Technique", "Pomodoro")
            
            self.console.print(session_info)
            
            session = self.study_session_manager.start_study_session(args.topic, args.duration or 25)
            
            self.console.print(f"[green]✓ Study session started![/green]")
            self.console.print(f"[dim]Focus on: {args.topic}[/dim]")
            self.console.print(f"[dim]Use 'python main.py session break' when you need a break[/dim]")
        
        elif args.action == 'break':
            success = self.study_session_manager.take_break(args.break_type or 'short')
            if success:
                break_duration = 5 if args.break_type == 'short' else 15
                self.console.print(f"[yellow]⏸️ Taking a {args.break_type or 'short'} break ({break_duration} minutes)[/yellow]")
                self.console.print("[dim]Relax and recharge! You'll get a notification when it's time to return.[/dim]")
            else:
                self.console.print("[red]✗ No active session to take a break from[/red]")
                self.console.print("[dim]Start a session first: python main.py session start --topic 'Your Topic'[/dim]")
        
        elif args.action == 'end':
            summary = self.study_session_manager.end_session("completed", args.notes or "")
            if 'error' in summary:
                self.console.print(f"[red]✗ {summary['error']}[/red]")
            else:
                # Enhanced session summary
                focus_score = summary['focus_score']
                
                if focus_score >= 0.9:
                    performance = "[bold green]Excellent focus![/bold green] 🎯"
                elif focus_score >= 0.7:
                    performance = "[bold blue]Good focus![/bold blue] 👍"
                else:
                    performance = "[bold yellow]Room for improvement[/bold yellow] 💪"
                
                summary_panel = Panel(
                    f"{performance}\n\n"
                    f"Duration: [cyan]{summary['duration']} minutes[/cyan]\n"
                    f"Focus Score: [green]{focus_score:.2f}[/green]\n"
                    f"Breaks Taken: [yellow]{summary['breaks_taken']}[/yellow]",
                    title="Session Complete",
                    border_style="green"
                )
                
                self.console.print(summary_panel)
                
                # Suggestions for next steps
                self.console.print("\n[bold cyan]What's next?[/bold cyan]")
                self.console.print("• Take a quiz to test your knowledge")
                self.console.print("• Review your progress dashboard")
                self.console.print("• Start another session on a different topic")
        
        elif args.action == 'stats':
            stats = self.study_session_manager.get_session_stats()
            if stats['current_session']:
                session = stats['current_session']
                
                # Progress bar for current session
                elapsed = session['elapsed_minutes']
                planned = session['planned_duration']
                progress_percent = min((elapsed / planned) * 100, 100)
                
                progress_bar = "█" * int(progress_percent / 5) + "░" * (20 - int(progress_percent / 5))
                
                session_panel = Panel(
                    f"Topic: [cyan]{session['topic']}[/cyan]\n"
                    f"Progress: [{progress_bar}] {progress_percent:.1f}%\n"
                    f"Time: [green]{elapsed}[/green] / [blue]{planned}[/blue] minutes\n"
                    f"Breaks: [yellow]{session['breaks_taken']}[/yellow]",
                    title="Active Session",
                    border_style="blue"
                )
                
                self.console.print(session_panel)
                
                # Show session controls
                self.console.print("\n[bold cyan]Session Controls:[/bold cyan]")
                self.console.print("• Take break: python main.py session break")
                self.console.print("• End session: python main.py session end")
                
            else:
                self.console.print("[yellow]No active session[/yellow]")
                self.console.print("[dim]Start a session: python main.py session start --topic 'Your Topic'[/dim]")

def create_parser():
    """Create comprehensive argument parser"""
    parser = argparse.ArgumentParser(description="Syllabo - AI-Powered Learning Assistant")
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Analyze command
    analyze_parser = subparsers.add_parser('analyze', help='Analyze syllabus')
    analyze_parser.add_argument('--file', help='Syllabus file path')
    analyze_parser.add_argument('--text', help='Direct syllabus text')
    analyze_parser.add_argument('--search-videos', action='store_true', help='Search for videos')
    analyze_parser.add_argument('--add-to-review', action='store_true', help='Add topics to spaced repetition')
    analyze_parser.add_argument('--print-results', action='store_true', help='Print results to terminal')
    analyze_parser.add_argument('--max-videos', type=int, default=5, help='Maximum videos per topic')
    analyze_parser.add_argument('--include-podcasts', action='store_true', help='Include podcast recommendations')
    analyze_parser.add_argument('--include-reading', action='store_true', help='Include reading materials')
    analyze_parser.add_argument('--difficulty-filter', choices=['beginner', 'intermediate', 'advanced'], help='Filter by difficulty')
    
    # Quiz system
    quiz_parser = subparsers.add_parser('quiz', help='Interactive quiz system')
    quiz_parser.add_argument('action', choices=['generate', 'take', 'history'], help='Quiz action')
    quiz_parser.add_argument('--topic', help='Topic for quiz')
    quiz_parser.add_argument('--content-file', help='File with content to generate quiz from')
    quiz_parser.add_argument('--num-questions', type=int, default=5, help='Number of questions')
    
    # Progress dashboard
    progress_parser = subparsers.add_parser('progress', help='View progress dashboard')
    progress_parser.add_argument('--export', action='store_true', help='Export progress report')
    
    # Goals management
    goals_parser = subparsers.add_parser('goals', help='Manage study goals')
    goals_parser.add_argument('action', choices=['create', 'list', 'update', 'suggest'], help='Goals action')
    goals_parser.add_argument('--title', help='Goal title')
    goals_parser.add_argument('--description', help='Goal description')
    goals_parser.add_argument('--type', choices=['daily', 'weekly', 'monthly', 'milestone'], help='Goal type')
    goals_parser.add_argument('--target', type=int, help='Target value')
    goals_parser.add_argument('--unit', help='Unit (minutes, topics, etc.)')
    
    # Multi-platform search
    platforms_parser = subparsers.add_parser('platforms', help='Search multiple learning platforms')
    platforms_parser.add_argument('--topic', required=True, help='Topic to search')
    platforms_parser.add_argument('--free-only', action='store_true', help='Show only free resources')
    
    # Bookmarks
    bookmarks_parser = subparsers.add_parser('bookmarks', help='Manage video bookmarks')
    bookmarks_parser.add_argument('action', choices=['add', 'list', 'search', 'export'], help='Bookmark action')
    bookmarks_parser.add_argument('--video-id', help='Video ID')
    bookmarks_parser.add_argument('--video-title', help='Video title')
    bookmarks_parser.add_argument('--timestamp', help='Timestamp (MM:SS or HH:MM:SS)')
    bookmarks_parser.add_argument('--note', help='Bookmark note')
    bookmarks_parser.add_argument('--topic', help='Topic')
    bookmarks_parser.add_argument('--tags', nargs='+', help='Tags')
    bookmarks_parser.add_argument('--importance', type=int, choices=[1,2,3,4,5], default=3, help='Importance (1-5)')
    bookmarks_parser.add_argument('--query', help='Search query')
    bookmarks_parser.add_argument('--format', choices=['json', 'csv', 'markdown'], default='json', help='Export format')
    
    # Study sessions
    session_parser = subparsers.add_parser('session', help='Manage study sessions')
    session_parser.add_argument('action', choices=['start', 'break', 'end', 'stats'], help='Session action')
    session_parser.add_argument('--topic', help='Study topic')
    session_parser.add_argument('--duration', type=int, default=25, help='Planned duration in minutes')
    session_parser.add_argument('--break-type', choices=['short', 'long'], default='short', help='Break type')
    session_parser.add_argument('--notes', help='Session notes')
    
    # Leaderboard
    
    return parser

async def main():
    """Enhanced main application entry point with interactive mode"""
    parser = create_parser()
    args = parser.parse_args()
    
    app = SyllaboMain()
    app.print_banner()
    
    try:
        # If no command provided, show interactive menu
        if not args.command:
            while True:
                command = app.show_interactive_menu()
                
                if command == 'exit':
                    app.console.print("[bold cyan]Thank you for using Syllabo![/bold cyan]")
                    break
                elif command == 'help':
                    app.console.print(Rule("[bold yellow]Available Commands[/bold yellow]"))
                    parser.print_help()
                    input("\nPress Enter to continue...")
                else:
                    # Create mock args for interactive commands
                    mock_args = type('Args', (), {
                        'command': command,
                        'file': None,
                        'text': None,
                        'search_videos': False,
                        'include_podcasts': False,
                        'include_reading': False,
                        'add_to_review': False,
                        'print_results': True,
                        'max_videos': 5
                    })()
                    
                    if command == 'analyze':
                        # Get user input for analysis
                        app.console.print(Rule("[bold blue]Syllabus Analysis Setup[/bold blue]"))
                        file_path = input("Enter syllabus file path (or press Enter to input text): ").strip()
                        
                        if file_path:
                            mock_args.file = file_path
                        else:
                            text_content = input("Enter syllabus text content: ").strip()
                            if text_content:
                                mock_args.text = text_content
                            else:
                                app.console.print("[red]No content provided[/red]")
                                continue
                        
                        # Ask for additional options
                        mock_args.search_videos = input("Search for videos? (y/n): ").lower().startswith('y')
                        mock_args.include_podcasts = input("Include podcasts? (y/n): ").lower().startswith('y')
                        mock_args.include_reading = input("Include reading materials? (y/n): ").lower().startswith('y')
                        mock_args.add_to_review = input("Add to spaced repetition? (y/n): ").lower().startswith('y')
                        
                        await app.analyze_syllabus(mock_args)
                    
                    elif command == 'quiz':
                        # Interactive quiz setup
                        app.console.print(Rule("[bold magenta]Quiz Setup[/bold magenta]"))
                        topic = input("Enter topic for quiz: ").strip()
                        if not topic:
                            app.console.print("[red]Topic is required[/red]")
                            continue
                        
                        num_questions = input("Number of questions (default 5): ").strip()
                        try:
                            num_questions = int(num_questions) if num_questions else 5
                        except ValueError:
                            num_questions = 5
                        
                        quiz_args = type('Args', (), {
                            'action': 'generate',
                            'topic': topic,
                            'content_file': None,
                            'num_questions': num_questions
                        })()
                        
                        await app.handle_quiz_command(quiz_args)
                    
                    elif command == 'progress':
                        progress_args = type('Args', (), {'export': False})()
                        app.handle_progress_command(progress_args)
                    
                    elif command == 'goals':
                        goals_args = type('Args', (), {'action': 'list'})()
                        app.handle_goals_command(goals_args)
                    
                    elif command == 'session':
                        session_args = type('Args', (), {'action': 'stats'})()
                        app.handle_session_command(session_args)
                    
                    input("\nPress Enter to continue...")
                    app.console.clear()
                    app.print_banner()
        
        # Handle command-line arguments
        elif args.command == 'analyze':
            await app.analyze_syllabus(args)
        elif args.command == 'quiz':
            await app.handle_quiz_command(args)
        elif args.command == 'progress':
            app.handle_progress_command(args)
        elif args.command == 'goals':
            app.handle_goals_command(args)
        elif args.command == 'platforms':
            await app.handle_platforms_command(args)
        elif args.command == 'bookmarks':
            app.handle_bookmarks_command(args)
        elif args.command == 'session':
            app.handle_session_command(args)
        else:
            parser.print_help()
    
    except KeyboardInterrupt:
        app.console.print("\n[yellow]Operation cancelled by user[/yellow]")
    except Exception as e:
        app.console.print(f"[red]Error: {e}[/red]")

if __name__ == "__main__":
    asyncio.run(main())