
import argparse

def create_parser():
    parser = argparse.ArgumentParser(
        description='Syllabo Enhanced - AI-Powered YouTube Video Finder',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
    Examples:
      # Interactive mode
      python syllabo.py interactive

      # Analyze a syllabus file
      python syllabo.py analyze --file course_syllabus.pdf --search-videos

      # Search for videos on a specific topic
      python syllabo.py search --topic "Neural Networks" --max-videos 5

      # Spaced repetition review
      python syllabo.py review due
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
    review_subparsers = review_parser.add_subparsers(dest='review_action', help='Review actions', required=True)

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

    return parser
