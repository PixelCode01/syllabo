 
import argparse

def create_parser():
    parser = argparse.ArgumentParser(
        description='Syllabo Enhanced - AI-Powered YouTube Video Finder',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
    Examples:
      # Interactive mode
      python main.py interactive

      # Analyze a syllabus file
      python main.py analyze --file course_syllabus.pdf --search-videos

      # Search for videos on a specific topic
      python main.py search --topic "Neural Networks" --max-videos 5

      # Spaced repetition review
      python main.py review due
    '''
    )
    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    # Interactive command
    interactive_parser = subparsers.add_parser(
        'interactive', 
        help='Run in interactive mode',
        description='Launch an interactive shell with command completion and keyboard shortcuts.'
    )
    interactive_parser.add_argument(
        '--theme',
        choices=['minimal', 'high-contrast'],
        default='minimal',
        help='Display theme for the interactive shell'
    )

    # Analyze command
    analyze_parser = subparsers.add_parser(
        'analyze', 
        help='Analyze syllabus and extract topics',
        description='Extract key topics from a syllabus file or text and optionally find relevant videos.'
    )
    analyze_parser.add_argument(
        '--file', '-f', 
        help='Path to syllabus file (supports PDF, DOC, DOCX, or plain text)'
    )
    analyze_parser.add_argument(
        '--text', '-t', 
        help='Syllabus text directly (use quotes: "Course covers neural networks and deep learning".)'
    )
    analyze_parser.add_argument(
        '--search-videos', 
        action='store_true', 
        help='Automatically search for relevant videos after topic extraction'
    )
    analyze_parser.add_argument(
        '--max-videos', 
        type=int, 
        default=5, 
        help='Maximum number of videos to find per topic (default: 5)'
    )
    analyze_parser.add_argument(
        '--print-results', 
        action='store_true', 
        help='Print detailed analysis results in the terminal'
    )
    analyze_parser.add_argument(
        '--save', 
        action='store_true', 
        help='Save analysis results to a file in the exports directory'
    )
    analyze_parser.add_argument(
        '--export-format', 
        choices=['json', 'csv', 'markdown', 'html'], 
        default='json', 
        help='Format for exported results (default: json)'
    )
    analyze_parser.add_argument(
        '--add-to-review', 
        action='store_true', 
        help='Add extracted topics to your spaced repetition review schedule'
    )
    analyze_parser.add_argument(
        '--preview', 
        action='store_true',
        help='Show a preview of the export before saving'
    )
    analyze_parser.add_argument(
        '--include-podcasts', 
        action='store_true', 
        help='Include educational podcasts in search results'
    )
    analyze_parser.add_argument(
        '--include-reading', 
        action='store_true', 
        help='Include reading materials and articles'
    )
    analyze_parser.add_argument(
        '--difficulty-filter', 
        choices=['beginner', 'intermediate', 'advanced'], 
        help='Filter content by difficulty level'
    )

    # Search command
    search_parser = subparsers.add_parser(
        'search', 
        help='Search for educational videos on a specific topic',
        description='Find and analyze educational videos related to a specific learning topic.'
    )
    search_parser.add_argument(
        '--topic', 
        required=True, 
        help='Topic to search for (e.g., "Neural Networks", "Linear Algebra".)'
    )
    search_parser.add_argument(
        '--max-videos', 
        type=int, 
        default=10, 
        help='Maximum number of videos to find and analyze (default: 10)'
    )
    search_parser.add_argument(
        '--save', 
        action='store_true', 
        help='Save search results to a file in the exports directory'
    )
    search_parser.add_argument(
        '--export-format', 
        choices=['json', 'csv', 'markdown', 'html'], 
        default='json', 
        help='Format for exported results (default: json)'
    )
    search_parser.add_argument(
        '--enhanced', 
        action='store_true',
        help='Use enhanced search with AI query expansion for better results'
    )
    search_parser.add_argument(
        '--preview', 
        action='store_true',
        help='Show a preview of the export before saving'
    )

    # History command
    history_parser = subparsers.add_parser(
        'history', 
        help='Show recent syllabi and searches',
        description='Display a history of your recent syllabi analyses and topic searches.'
    )
    history_parser.add_argument(
        '--limit', 
        type=int, 
        default=10, 
        help='Number of history items to show (default: 10)'
    )
    history_parser.add_argument(
        '--export-session', 
        action='store_true',
        help='Export your current session history to a log file'
    )
    history_parser.add_argument(
        '--preview', 
        action='store_true',
        help='Preview what will be exported before saving'
    )

    # Export command
    export_parser = subparsers.add_parser(
        'export', 
        help='Export analysis results to a file',
        description='Export analysis results for a specific syllabus ID to various formats.'
    )
    export_parser.add_argument(
        '--syllabus-id', 
        type=int, 
        required=True, 
        help='ID of the syllabus analysis to export (find IDs with the history command)'
    )
    export_parser.add_argument(
        '--format', 
        choices=['json', 'csv', 'markdown', 'html'], 
        default='json', 
        help='Format for exported results (default: json)'
    )
    export_parser.add_argument(
        '--preview', 
        action='store_true',
        help='Show a preview of the export before saving'
    )

    # Review command
    review_parser = subparsers.add_parser(
        'review', 
        help='Spaced repetition review system',
        description='Manage your spaced repetition review schedule for effective learning.'
    )
    review_subparsers = review_parser.add_subparsers(dest='review_action', help='Review actions')

    # Add topic subcommand
    add_review_parser = review_subparsers.add_parser(
        'add', 
        help='Add a topic to your review schedule',
        description='Add a new topic to your spaced repetition review schedule.'
    )
    add_review_parser.add_argument(
        '--topic', 
        required=True, 
        help='Name of the topic to add (e.g., "Neural Networks", "Linear Algebra")'
    )
    add_review_parser.add_argument(
        '--description', '-d', 
        help='Optional description of the topic content for context'
    )

    # List topics subcommand
    list_review_parser = review_subparsers.add_parser(
        'list', 
        help='List all topics in your review schedule',
        description='Display a table of all topics in your spaced repetition review schedule.'
    )
    list_review_parser.add_argument(
        '--format',
        choices=['table', 'json', 'csv'],
        default='table',
        help='Output format for the list (default: table)'
    )

    # Due topics subcommand
    due_review_parser = review_subparsers.add_parser(
        'due', 
        help='Show topics due for review today',
        description='Display all topics that are scheduled for review today.'
    )
    due_review_parser.add_argument(
        '--notify', 
        action='store_true', 
        help='Send a desktop notification for due reviews'
    )
    due_review_parser.add_argument(
        '--format',
        choices=['table', 'json', 'csv'],
        default='table',
        help='Output format for due reviews (default: table)'
    )

    # Mark review subcommand
    mark_review_parser = review_subparsers.add_parser(
        'mark', 
        help='Mark a topic as reviewed',
        description='Record your review attempt and schedule the next review based on your performance.'
    )
    mark_review_parser.add_argument(
        '--topic', 
        required=True, 
        help='Name of the topic you reviewed'
    )
    mark_group = mark_review_parser.add_mutually_exclusive_group(required=True)
    mark_group.add_argument(
        '--success', 
        action='store_true', 
        help='Mark review as successful (extends interval to next review)'
    )
    mark_group.add_argument(
        '--failure', 
        action='store_true', 
        help='Mark review as failed (resets interval for more frequent review)'
    )

    # Stats subcommand
    stats_review_parser = review_subparsers.add_parser(
        'stats', 
        help='Show review statistics',
        description='Display statistics about your review schedule and progress.'
    )
    stats_review_parser.add_argument(
        '--topic', 
        help='Show statistics for a specific topic only'
    )
    stats_review_parser.add_argument(
        '--format',
        choices=['table', 'json', 'csv'],
        default='table',
        help='Output format for statistics (default: table)'
    )

    # Remove topic subcommand
    remove_review_parser = review_subparsers.add_parser(
        'remove', 
        help='Remove a topic from your review schedule',
        description='Permanently remove a topic from your spaced repetition review schedule.'
    )
    remove_review_parser.add_argument(
        '--topic', 
        required=True, 
        help='Name of the topic to remove from the schedule'
    )

    # Help subcommand
    help_review_parser = review_subparsers.add_parser(
        'help', 
        help='Show detailed help for the review system',
        description='Display detailed help and examples for using the spaced repetition system.'
    )

    # Quiz command
    quiz_parser = subparsers.add_parser(
        'quiz', 
        help='Interactive quiz system',
        description='Generate and take AI-powered quizzes from topics, syllabus files, or text content.'
    )
    quiz_parser.add_argument(
        '--topic', 
        help='Specific topic for the quiz (optional - will prompt if not provided)'
    )
    quiz_parser.add_argument(
        '--num-questions', 
        type=int, 
        default=5, 
        help='Number of questions to generate (default: 5)'
    )
    quiz_parser.add_argument(
        '--content-file', 
        help='File with content to base quiz on (supports PDF, DOC, DOCX, or plain text)'
    )
    quiz_parser.add_argument(
        '--source', 
        choices=['topics', 'syllabus', 'text'], 
        help='Quiz source: topics (from database), syllabus (from file), or text (direct input)'
    )

    # Progress command
    progress_parser = subparsers.add_parser(
        'progress', 
        help='Learning progress dashboard',
        description='Track your learning progress with visual analytics.'
    )
    progress_parser.add_argument('--export', action='store_true', help='Export progress report')

    # Goals command
    goals_parser = subparsers.add_parser(
        'goals', 
        help='Study goals management',
        description='Manage learning goals and milestones.'
    )
    goals_subparsers = goals_parser.add_subparsers(dest='action', help='Goals actions')
    
    # Create goal subcommand
    create_goal_parser = goals_subparsers.add_parser('create', help='Create a new goal')
    create_goal_parser.add_argument('--title', required=True, help='Goal title')
    create_goal_parser.add_argument('--description', help='Goal description')
    create_goal_parser.add_argument('--type', required=True, choices=['daily', 'weekly', 'monthly'], help='Goal type')
    create_goal_parser.add_argument('--target', type=int, required=True, help='Target value')
    create_goal_parser.add_argument('--unit', required=True, help='Unit (minutes, hours, topics, etc.)')
    
    # List goals subcommand
    list_goals_parser = goals_subparsers.add_parser('list', help='List active goals')
    
    # Suggest goals subcommand
    suggest_goals_parser = goals_subparsers.add_parser('suggest', help='Get goal suggestions')

    # Platforms command
    platforms_parser = subparsers.add_parser(
        'platforms', 
        help='Multi-platform search',
        description='Search across multiple learning platforms.'
    )
    platforms_parser.add_argument('--topic', required=True, help='Topic to search for')
    platforms_parser.add_argument('--free-only', action='store_true', help='Show only free courses')

    # Bookmarks command
    bookmarks_parser = subparsers.add_parser(
        'bookmarks', 
        help='Smart bookmarks management',
        description='Manage video bookmarks and notes.'
    )
    bookmarks_subparsers = bookmarks_parser.add_subparsers(dest='action', help='Bookmark actions')
    
    # Add bookmark subcommand
    add_bookmark_parser = bookmarks_subparsers.add_parser('add', help='Add a new bookmark')
    add_bookmark_parser.add_argument('--video-id', required=True, help='Video ID')
    add_bookmark_parser.add_argument('--video-title', required=True, help='Video title')
    add_bookmark_parser.add_argument('--timestamp', required=True, help='Timestamp (e.g., 5:30)')
    add_bookmark_parser.add_argument('--note', required=True, help='Note about this bookmark')
    add_bookmark_parser.add_argument('--topic', required=True, help='Related topic')
    add_bookmark_parser.add_argument('--tags', nargs='*', help='Tags for the bookmark')
    add_bookmark_parser.add_argument('--importance', type=int, choices=[1,2,3,4,5], help='Importance level (1-5)')
    
    # List bookmarks subcommand
    list_bookmarks_parser = bookmarks_subparsers.add_parser('list', help='List bookmarks')
    list_bookmarks_parser.add_argument('--topic', help='Filter by topic')
    
    # Search bookmarks subcommand
    search_bookmarks_parser = bookmarks_subparsers.add_parser('search', help='Search bookmarks')
    search_bookmarks_parser.add_argument('--query', required=True, help='Search query')
    
    # Export bookmarks subcommand
    export_bookmarks_parser = bookmarks_subparsers.add_parser('export', help='Export bookmarks')
    export_bookmarks_parser.add_argument('--format', choices=['json', 'csv'], default='json', help='Export format')

    # Session command
    session_parser = subparsers.add_parser(
        'session', 
        help='Study sessions with Pomodoro timer',
        description='Manage study sessions with focus tracking.'
    )
    session_subparsers = session_parser.add_subparsers(dest='action', help='Session actions')
    
    # Start session subcommand
    start_session_parser = session_subparsers.add_parser('start', help='Start a study session')
    start_session_parser.add_argument('--topic', required=True, help='Topic to study')
    start_session_parser.add_argument('--duration', type=int, default=25, help='Session duration in minutes')
    
    # Break subcommand
    break_session_parser = session_subparsers.add_parser('break', help='Take a break')
    break_session_parser.add_argument('--break-type', choices=['short', 'long'], default='short', help='Break type')
    
    # End session subcommand
    end_session_parser = session_subparsers.add_parser('end', help='End current session')
    end_session_parser.add_argument('--notes', help='Session notes')
    
    # Session stats subcommand
    stats_session_parser = session_subparsers.add_parser('stats', help='Show session statistics')

    # AI Status command
    ai_parser = subparsers.add_parser(
        'ai-status', 
        help='Check AI service status and test functionality',
        description='Test all available AI services and show their current status.'
    )
    ai_parser.add_argument(
        '--test', 
        action='store_true', 
        help='Run comprehensive tests on all AI services'
    )
    ai_parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Show detailed information about each service'
    )

    # Configuration command
    config_parser = subparsers.add_parser(
        'config', 
        help='Manage API keys and application configuration',
        description='Configure YouTube Data API and Gemini API keys for enhanced functionality.'
    )
    config_subparsers = config_parser.add_subparsers(dest='config_action', help='Configuration actions')
    
    # Show config subcommand
    show_config_parser = config_subparsers.add_parser('show', help='Show current configuration status')
    
    # Set YouTube API key subcommand
    youtube_config_parser = config_subparsers.add_parser('youtube', help='Configure YouTube Data API key')
    youtube_config_parser.add_argument('--key', help='YouTube Data API key')
    
    # Set Gemini API key subcommand
    gemini_config_parser = config_subparsers.add_parser('gemini', help='Configure Gemini API key')
    gemini_config_parser.add_argument('--key', help='Gemini API key')
    
    # Test APIs subcommand
    test_config_parser = config_subparsers.add_parser('test', help='Test API connections')
    test_config_parser.add_argument('--service', choices=['youtube', 'gemini', 'all'], default='all', help='Service to test')
    
    # Reset config subcommand
    reset_config_parser = config_subparsers.add_parser('reset', help='Reset configuration to defaults')

    return parser
