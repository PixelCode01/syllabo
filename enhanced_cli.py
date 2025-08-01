#!/usr/bin/env python3

import argparse
import asyncio
from syllabo import EnhancedSyllaboCLI

def create_parser():
    """Create enhanced argument parser with new features"""
    parser = argparse.ArgumentParser(description="Syllabo Enhanced - AI-Powered Learning Assistant")
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Existing commands (analyze, search, etc.)
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
    platforms_parser.add_argument('--include-coursera', action='store_true', help='Include Coursera')
    platforms_parser.add_argument('--include-edx', action='store_true', help='Include edX')
    platforms_parser.add_argument('--include-khan', action='store_true', help='Include Khan Academy')
    
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

async def handle_quiz_command(cli, args):
    """Handle quiz-related commands"""
    if args.action == 'generate':
        if not args.topic:
            print("Error: --topic is required for quiz generation")
            return
        
        if args.content_file:
            with open(args.content_file, 'r') as f:
                content = f.read()
        else:
            content = f"Educational content about {args.topic}"
        
        quiz = await cli.quiz_generator.generate_quiz_from_content(
            content, args.topic, args.num_questions
        )
        
        if 'error' in quiz:
            print(f"Error generating quiz: {quiz['error']}")
        else:
            print(f"Generated quiz for {args.topic} with {len(quiz['questions'])} questions")
            
            # Ask if user wants to take the quiz
            take_now = input("Take the quiz now? (y/n): ").lower().startswith('y')
            if take_now:
                results = cli.quiz_generator.take_quiz(quiz)
                cli.quiz_generator.save_quiz_results(results)
    
    elif args.action == 'take':
        print("Quiz taking functionality - load existing quiz")
    
    elif args.action == 'history':
        print("Quiz history functionality")

def handle_progress_command(cli, args):
    """Handle progress dashboard commands"""
    cli.progress_dashboard.show_dashboard()
    
    if args.export:
        report = cli.progress_dashboard.generate_progress_report()
        filename = f"progress_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        with open(filename, 'w') as f:
            f.write(report)
        print(f"Progress report exported to: {filename}")

def handle_goals_command(cli, args):
    """Handle goals management commands"""
    if args.action == 'create':
        if not all([args.title, args.type, args.target, args.unit]):
            print("Error: --title, --type, --target, and --unit are required")
            return
        
        goal_id = cli.goals_manager.create_goal(
            args.title, args.description or "", args.type,
            args.target, args.unit
        )
        print(f"Created goal: {args.title} (ID: {goal_id})")
    
    elif args.action == 'list':
        active_goals = cli.goals_manager.get_active_goals()
        if not active_goals:
            print("No active goals")
            return
        
        print("ACTIVE GOALS")
        print("-" * 40)
        for goal in active_goals:
            progress = (goal.current_value / goal.target_value) * 100
            print(f"{goal.title}")
            print(f"  Progress: {goal.current_value}/{goal.target_value} {goal.unit} ({progress:.1f}%)")
            print(f"  Type: {goal.goal_type}")
            print()
    
    elif args.action == 'suggest':
        suggestions = cli.goals_manager.suggest_goals()
        print("SUGGESTED GOALS")
        print("-" * 40)
        for i, suggestion in enumerate(suggestions, 1):
            print(f"{i}. {suggestion['title']}")
            print(f"   Target: {suggestion['target']} {suggestion['unit']}")
            print(f"   Type: {suggestion['type']}")
            print()

async def handle_platforms_command(cli, args):
    """Handle multi-platform search commands"""
    print(f"Searching multiple platforms for: {args.topic}")
    
    results = await cli.platform_integrator.search_all_platforms(args.topic)
    
    for platform, courses in results.items():
        if courses:
            print(f"\n{platform.upper()}")
            print("-" * 30)
            
            if args.free_only:
                courses = cli.platform_integrator.filter_by_preference(courses, free_only=True)
            
            for i, course in enumerate(courses, 1):
                print(f"{i}. {course['title']}")
                print(f"   Provider: {course['provider']}")
                print(f"   Free: {'Yes' if course.get('free', False) else 'No'}")
                print(f"   URL: {course['url']}")
                print()

def handle_bookmarks_command(cli, args):
    """Handle bookmark management commands"""
    if args.action == 'add':
        if not all([args.video_id, args.video_title, args.timestamp, args.note, args.topic]):
            print("Error: --video-id, --video-title, --timestamp, --note, and --topic are required")
            return
        
        bookmark_id = cli.bookmark_manager.add_bookmark(
            args.video_id, args.video_title, args.timestamp,
            args.note, args.topic, args.tags or [], args.importance
        )
        print(f"Added bookmark: {bookmark_id}")
    
    elif args.action == 'list':
        if args.topic:
            bookmarks = cli.bookmark_manager.get_bookmarks_by_topic(args.topic)
        else:
            bookmarks = list(cli.bookmark_manager.bookmarks.values())
        
        if not bookmarks:
            print("No bookmarks found")
            return
        
        print("BOOKMARKS")
        print("-" * 50)
        for bookmark in bookmarks:
            print(f"{bookmark.video_title} - {bookmark.timestamp}")
            print(f"  Note: {bookmark.note}")
            print(f"  Topic: {bookmark.topic}")
            print(f"  Importance: {'⭐' * bookmark.importance}")
            print()
    
    elif args.action == 'search':
        if not args.query:
            print("Error: --query is required for search")
            return
        
        results = cli.bookmark_manager.search_bookmarks(args.query)
        print(f"Found {len(results)} bookmarks matching '{args.query}'")
        
        for bookmark in results:
            print(f"{bookmark.video_title} - {bookmark.timestamp}")
            print(f"  Note: {bookmark.note}")
            print()
    
    elif args.action == 'export':
        filename = cli.bookmark_manager.export_bookmarks(args.format)
        print(f"Bookmarks exported to: {filename}")

def handle_session_command(cli, args):
    """Handle study session commands"""
    if args.action == 'start':
        if not args.topic:
            print("Error: --topic is required to start a session")
            return
        
        session = cli.study_session_manager.start_study_session(args.topic, args.duration)
        print(f"Started study session: {args.topic} for {args.duration} minutes")
    
    elif args.action == 'break':
        success = cli.study_session_manager.take_break(args.break_type)
        if success:
            print(f"Taking a {args.break_type} break")
        else:
            print("No active session to take a break from")
    
    elif args.action == 'end':
        summary = cli.study_session_manager.end_session("completed", args.notes or "")
        if 'error' in summary:
            print(summary['error'])
        else:
            print(f"Session completed: {summary['duration']} minutes")
            print(f"Focus score: {summary['focus_score']:.2f}")
    
    elif args.action == 'stats':
        stats = cli.study_session_manager.get_session_stats()
        if stats['current_session']:
            session = stats['current_session']
            print(f"Current session: {session['topic']}")
            print(f"Elapsed: {session['elapsed_minutes']} minutes")
            print(f"Planned: {session['planned_duration']} minutes")
        else:
            print("No active session")

async def main():
    """Enhanced main function with new features"""
    parser = create_parser()
    args = parser.parse_args()
    
    cli = EnhancedSyllaboCLI()
    
    try:
        if args.command == 'quiz':
            await handle_quiz_command(cli, args)
        elif args.command == 'progress':
            handle_progress_command(cli, args)
        elif args.command == 'goals':
            handle_goals_command(cli, args)
        elif args.command == 'platforms':
            await handle_platforms_command(cli, args)
        elif args.command == 'bookmarks':
            handle_bookmarks_command(cli, args)
        elif args.command == 'session':
            handle_session_command(cli, args)
        else:
            # Handle existing commands
            await cli.run(args)
    
    except KeyboardInterrupt:
        print("\nOperation cancelled by user")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(main())