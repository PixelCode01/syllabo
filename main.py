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
        """Print application banner"""
        self.console.print(Panel.fit(
            "[bold cyan]SYLLABO - AI-POWERED LEARNING ASSISTANT[/bold cyan]", 
            subtitle="All-in-One Educational Resource Manager"
        ))
    
    async def analyze_syllabus(self, args):
        """Analyze syllabus with enhanced features"""
        start_time = time.time()
        self.console.print(f"[bold blue]Analyzing syllabus...[/bold blue]")
        
        if args.file:
            syllabus_content = self.syllabus_parser.load_from_file(args.file)
            syllabus_title = os.path.basename(args.file)
        elif args.text:
            syllabus_content = args.text
            syllabus_title = f"Direct input - {datetime.now().strftime('%Y-%m-%d %H:%M')}"
        else:
            self.console.print("[red]Error: Please provide either --file or --text[/red]")
            return
        
        # Extract topics
        topics = await self.syllabus_parser.extract_topics(syllabus_content, self.ai_client)
        self.console.print(f"[green]Found {len(topics)} topics[/green]")
        
        # Save to database
        syllabus_id = self.db.save_syllabus(syllabus_title, syllabus_content)
        topic_ids = self.db.save_topics(syllabus_id, topics)
        
        # Search for content if requested
        if args.search_videos or args.include_podcasts or args.include_reading:
            await self._search_comprehensive_content(topics, args)
        
        # Add to spaced repetition if requested
        if args.add_to_review:
            self._add_topics_to_review(topics)
        
        processing_time = time.time() - start_time
        self.console.print(f"[green]Analysis completed in {processing_time:.1f}s[/green]")
    
    async def _search_comprehensive_content(self, topics, args):
        """Search for comprehensive content across platforms"""
        for topic in topics:
            topic_name = topic['name']
            self.console.print(f"[cyan]Searching content for: {topic_name}[/cyan]")
            
            all_content = {}
            
            # YouTube videos
            if args.search_videos:
                videos = await self.youtube_client.search_videos(topic_name, args.max_videos or 5)
                if videos:
                    analyzed_videos = await self.video_analyzer.analyze_videos_and_playlists(videos, [], topic_name)
                    all_content['videos'] = analyzed_videos.get('supplementary_videos', [])
            
            # Multi-platform courses
            if hasattr(args, 'include_platforms') and args.include_platforms:
                platform_results = await self.platform_integrator.search_all_platforms(topic_name)
                all_content['courses'] = platform_results
            
            # Podcasts and reading
            if args.include_podcasts:
                podcasts = self.podcast_integrator.search_podcasts(topic_name)
                all_content['podcasts'] = podcasts
            
            if args.include_reading:
                reading = self.podcast_integrator.search_reading_resources(topic_name)
                all_content['reading'] = reading
            
            # Apply difficulty filter if specified
            if hasattr(args, 'difficulty_filter') and args.difficulty_filter:
                all_content = self._filter_by_difficulty(all_content, args.difficulty_filter)
            
            # Display results
            if args.print_results:
                self._display_content_results(topic_name, all_content)
    
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
        """Handle quiz-related commands"""
        if args.action == 'generate':
            if not args.topic:
                self.console.print("[red]Error: --topic is required for quiz generation[/red]")
                return
            
            if args.content_file:
                with open(args.content_file, 'r') as f:
                    content = f.read()
            else:
                content = f"Educational content about {args.topic}"
            
            quiz = await self.quiz_generator.generate_quiz_from_content(
                content, args.topic, args.num_questions or 5
            )
            
            if 'error' in quiz:
                self.console.print(f"[red]Error generating quiz: {quiz['error']}[/red]")
            else:
                self.console.print(f"[green]Generated quiz for {args.topic} with {len(quiz['questions'])} questions[/green]")
                
                # Ask if user wants to take the quiz
                take_now = input("Take the quiz now? (y/n): ").lower().startswith('y')
                if take_now:
                    results = self.quiz_generator.take_quiz(quiz)
                    self.quiz_generator.save_quiz_results(results)
        
        elif args.action == 'take':
            self.console.print("[yellow]Quiz taking functionality - load existing quiz[/yellow]")
        
        elif args.action == 'history':
            self.console.print("[yellow]Quiz history functionality[/yellow]")
    
    def handle_progress_command(self, args):
        """Handle progress dashboard commands"""
        self.progress_dashboard.show_dashboard()
        
        if args.export:
            report = self.progress_dashboard.generate_progress_report()
            filename = f"progress_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
            with open(filename, 'w') as f:
                f.write(report)
            self.console.print(f"[green]Progress report exported to: {filename}[/green]")
    
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
            else:
                bookmarks = list(self.bookmark_manager.bookmarks.values())
            
            if not bookmarks:
                self.console.print("[yellow]No bookmarks found[/yellow]")
                return
            
            table = Table(title="Bookmarks")
            table.add_column("Video", style="cyan")
            table.add_column("Timestamp", style="yellow")
            table.add_column("Note", style="green")
            table.add_column("Importance", style="red")
            
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
        """Handle study session commands"""
        if args.action == 'start':
            if not args.topic:
                self.console.print("[red]Error: --topic is required to start a session[/red]")
                return
            
            session = self.study_session_manager.start_study_session(args.topic, args.duration or 25)
            self.console.print(f"[green]Started study session: {args.topic} for {args.duration or 25} minutes[/green]")
        
        elif args.action == 'break':
            success = self.study_session_manager.take_break(args.break_type or 'short')
            if success:
                self.console.print(f"[yellow]Taking a {args.break_type or 'short'} break[/yellow]")
            else:
                self.console.print("[red]No active session to take a break from[/red]")
        
        elif args.action == 'end':
            summary = self.study_session_manager.end_session("completed", args.notes or "")
            if 'error' in summary:
                self.console.print(f"[red]{summary['error']}[/red]")
            else:
                self.console.print(f"[green]Session completed: {summary['duration']} minutes[/green]")
                self.console.print(f"Focus score: {summary['focus_score']:.2f}")
        
        elif args.action == 'stats':
            stats = self.study_session_manager.get_session_stats()
            if stats['current_session']:
                session = stats['current_session']
                self.console.print(f"[cyan]Current session: {session['topic']}[/cyan]")
                self.console.print(f"Elapsed: {session['elapsed_minutes']} minutes")
                self.console.print(f"Planned: {session['planned_duration']} minutes")
            else:
                self.console.print("[yellow]No active session[/yellow]")

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
    
    return parser

async def main():
    """Main application entry point"""
    parser = create_parser()
    args = parser.parse_args()
    
    app = SyllaboMain()
    app.print_banner()
    
    try:
        if args.command == 'analyze':
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
        print("\nOperation cancelled by user")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(main())