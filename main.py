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

# Third-party imports
from dotenv import load_dotenv
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.rule import Rule
from rich.progress import Progress

load_dotenv()
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
    
    async def analyze_syllabus(self, args):
        """Analyze syllabus with enhanced UI and progress tracking"""
        start_time = time.time()
        
        self.console.print(Rule("[bold blue]Syllabus Analysis[/bold blue]"))
        
        # Load syllabus content
        if args.file:
            try:
                syllabus_content = self.syllabus_parser.load_from_file(args.file)
                syllabus_title = os.path.basename(args.file)
                self.console.print(f"[green]Loaded syllabus: [cyan]{syllabus_title}[/cyan]")
            except Exception as e:
                self.console.print(f"[red]Error loading file: {e}[/red]")
                return
        elif args.text:
            syllabus_content = args.text
            syllabus_title = f"Direct input - {datetime.now().strftime('%Y-%m-%d %H:%M')}"
            self.console.print(f"[green]Loaded text content ([cyan]{len(args.text)} characters[/cyan])")
        else:
            self.console.print("[red]Please provide either --file or --text[/red]")
            return
        
        # Extract topics with AI
        try:
            topics = await self.syllabus_parser.extract_topics(syllabus_content, self.ai_client)
            if topics:
                self.console.print(f"[green]Found [bold green]{len(topics)}[/bold green] topics")
            else:
                self.console.print("[yellow]No topics found. Try refining your syllabus content.[/yellow]")
                return
        except Exception as e:
            self.console.print(f"[red]Error extracting topics: {e}[/red]")
            return
        
        # Save to database
        syllabus_id = self.db.save_syllabus(syllabus_title, syllabus_content)
        topic_ids = self.db.save_topics(syllabus_id, topics)
        self.console.print("[green]Saved to database[/green]")
        
        # Search for content if requested
        if args.search_videos:
            await self._search_videos_for_topics(topics, args)
        
        # Add to spaced repetition if requested
        if args.add_to_review:
            added_count = self._add_topics_to_review(topics)
            if added_count > 0:
                self.console.print(f"[green]Added {added_count} topics to review schedule[/green]")
        
        # Show results if requested
        if args.print_results:
            self._display_analysis_results(topics)
    
    async def _search_videos_for_topics(self, topics, args):
        """Search for videos for each topic"""
        self.console.print(Rule("[bold yellow]Video Search[/bold yellow]"))
        
        for topic in topics:
            try:
                videos = await self.youtube_client.search_videos(topic['name'], args.max_videos or 5)
                if videos:
                    self.console.print(f"[green]Found {len(videos)} videos for [cyan]{topic['name']}[/cyan]")
                else:
                    self.console.print(f"[yellow]No videos found for [cyan]{topic['name']}[/cyan]")
            except Exception as e:
                self.console.print(f"[red]Video search failed for {topic['name']}: {e}[/red]")
    
    def _add_topics_to_review(self, topics):
        """Add topics to spaced repetition system"""
        added_count = 0
        for topic in topics:
            if self.spaced_repetition.add_topic(topic['name'], topic.get('description', '')):
                added_count += 1
        return added_count
    
    def _display_analysis_results(self, topics):
        """Display analysis results in a formatted table"""
        table = Table(title="Extracted Topics")
        table.add_column("Topic", style="cyan")
        table.add_column("Subtopics", style="yellow")
        
        for topic in topics:
            subtopics = ', '.join(topic.get('subtopics', []))
            table.add_row(topic['name'], subtopics[:50] + "..." if len(subtopics) > 50 else subtopics)
        
        self.console.print(table)

async def main():
    """Main application entry point"""
    # Import CLI parser
    from src.cli.commands import create_parser
    
    parser = create_parser()
    args = parser.parse_args()
    
    app = SyllaboMain()
    app.print_banner()
    
    try:
        # Handle commands
        if args.command == 'analyze':
            await app.analyze_syllabus(args)
        elif args.command == 'search':
            # Handle search command
            app.console.print(f"[cyan]Searching for: {args.topic}[/cyan]")
            try:
                videos = await app.youtube_client.search_videos(args.topic, args.max_videos)
                if videos:
                    table = Table(title=f"Videos for: {args.topic}")
                    table.add_column("Title", style="cyan")
                    table.add_column("Channel", style="yellow")
                    table.add_column("Duration", style="green")
                    
                    for video in videos:
                        table.add_row(
                            video.get('title', 'Unknown')[:40] + "...",
                            video.get('channel', 'Unknown')[:20] + "...",
                            video.get('duration', 'N/A')
                        )
                    
                    app.console.print(table)
                else:
                    app.console.print(f"[yellow]No videos found for: {args.topic}[/yellow]")
            except Exception as e:
                app.console.print(f"[red]Search failed: {e}[/red]")
        
        elif args.command == 'history':
            # Handle history command
            app.console.print("[cyan]Analysis History[/cyan]")
            try:
                history = app.db.get_recent_analyses(args.limit)
                if history:
                    table = Table(title="Recent Analyses")
                    table.add_column("ID", style="cyan")
                    table.add_column("Title", style="green")
                    table.add_column("Topics", style="yellow")
                    table.add_column("Date", style="blue")
                    
                    for item in history:
                        table.add_row(
                            str(item.get('id', 'N/A')),
                            item.get('title', 'Unknown')[:30] + "...",
                            str(item.get('topic_count', 0)),
                            item.get('created_at', 'Unknown')[:15]
                        )
                    
                    app.console.print(table)
                else:
                    app.console.print("[yellow]No analysis history found[/yellow]")
            except Exception as e:
                app.console.print(f"[red]Error loading history: {e}[/red]")
        
        elif args.command == 'review':
            # Handle review command
            app.console.print(f"[magenta]Spaced Repetition - {args.review_action.title()}[/magenta]")
            
            if args.review_action == 'add':
                success = app.spaced_repetition.add_topic(args.topic, args.description or "")
                if success:
                    app.console.print(f"[green]Added topic to review: {args.topic}[/green]")
                else:
                    app.console.print(f"[yellow]Topic already exists: {args.topic}[/yellow]")
            
            elif args.review_action == 'due':
                due_topics = app.spaced_repetition.get_due_topics()
                if due_topics:
                    app.console.print(f"[yellow]{len(due_topics)} topics due for review:[/yellow]")
                    for topic in due_topics:
                        app.console.print(f"• [cyan]{topic.topic_name}[/cyan]")
                else:
                    app.console.print("[green]No topics due for review today[/green]")
            
            elif args.review_action == 'list':
                topics = app.spaced_repetition.get_all_topics()
                if topics:
                    table = Table(title="Review Schedule")
                    table.add_column("Topic", style="cyan")
                    table.add_column("Next Review", style="yellow")
                    table.add_column("Reviews", style="blue")
                    
                    for topic in topics:
                        table.add_row(
                            topic.get('topic_name', 'Unknown'),
                            topic.get('next_review', 'N/A'),
                            str(topic.get('total_reviews', 0))
                        )
                    
                    app.console.print(table)
                else:
                    app.console.print("[yellow]No topics in review schedule[/yellow]")
        
        elif args.command == 'ai-status':
            # Handle AI status command
            app.console.print("[cyan]AI Services Status[/cyan]")
            
            services = {
                'AI Client': app.ai_client.test_connection(),
                'YouTube API': app.youtube_client.test_connection(),
                'Database': app.db.test_connection()
            }
            
            table = Table(title="Service Status")
            table.add_column("Service", style="cyan")
            table.add_column("Status", style="green")
            
            for service_name, test_result in services.items():
                if asyncio.iscoroutine(test_result):
                    test_result = await test_result
                status = "✓ Working" if test_result else "✗ Failed"
                table.add_row(service_name, status)
            
            app.console.print(table)
        
        else:
            parser.print_help()
    
    except KeyboardInterrupt:
        app.console.print("\n[yellow]Operation cancelled by user[/yellow]")
    except Exception as e:
        app.console.print(f"[red]Error: {e}[/red]")

if __name__ == "__main__":
    asyncio.run(main())