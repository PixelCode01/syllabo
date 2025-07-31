#!/usr/bin/env python3

import os
import sys
import argparse
from datetime import datetime

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.spaced_repetition import SpacedRepetitionEngine
from src.notification_system import NotificationSystem

class ForgetMeNotCLI:
    """Standalone spaced repetition CLI tool"""
    
    def __init__(self):
        self.engine = SpacedRepetitionEngine()
        self.notifications = NotificationSystem()
    
    def add_topic(self, args):
        """Add a new topic to the review schedule"""
        description = args.description or ""
        
        if self.engine.add_topic(args.topic, description):
            print(f"Added '{args.topic}' to review schedule")
            print("First review scheduled for tomorrow")
        else:
            print(f"Topic '{args.topic}' is already in your review schedule")
    
    def list_topics(self, args):
        """List topics based on urgency"""
        if args.urgent:
            # Show only due topics
            due_topics = self.engine.get_due_topics()
            if not due_topics:
                print("No topics are due for review right now")
                return
            
            print(f"URGENT: {len(due_topics)} topic{'s' if len(due_topics) != 1 else ''} due for review:")
            for item in due_topics:
                overdue_days = (datetime.now() - datetime.fromisoformat(item.next_review)).days
                overdue_text = f" (overdue by {overdue_days} day{'s' if overdue_days != 1 else ''})" if overdue_days > 0 else ""
                print(f"  • {item.topic_name}{overdue_text}")
        else:
            # Show all topics
            topics = self.engine.get_all_topics()
            if not topics:
                print("No topics in your review schedule")
                print("Add topics with: forgetmenot add 'Topic Name' -d 'Description'")
                return
            
            print(f"Review Schedule ({len(topics)} topics):")
            print("-" * 60)
            
            for topic in sorted(topics, key=lambda x: x['days_until_review']):
                days_until = topic['days_until_review']
                if days_until <= 0:
                    status = "DUE NOW"
                elif days_until == 1:
                    status = "Due tomorrow"
                else:
                    status = f"Due in {days_until} days"
                
                print(f"{topic['topic_name']:<30} | {topic['mastery_level']:<12} | {status}")
    
    def review_topic(self, args):
        """Mark a topic as reviewed"""
        success = args.success
        
        if self.engine.mark_review(args.topic, success):
            result_text = "successful" if success else "failed"
            print(f"Marked '{args.topic}' as {result_text} review")
            
            # Show next review info
            stats = self.engine.get_topic_stats(args.topic)
            if stats:
                print(f"Next review in {stats['current_interval']} days")
                print(f"Mastery level: {stats['mastery_level']}")
        else:
            print(f"Topic '{args.topic}' not found in review schedule")
    
    def show_stats(self, args):
        """Show review statistics"""
        summary = self.engine.get_study_summary()
        
        print("Study Statistics")
        print("-" * 30)
        print(f"Total Topics: {summary['total_topics']}")
        print(f"Due Now: {summary['due_now']}")
        print(f"Due Today: {summary['due_today']}")
        print(f"Mastered: {summary['mastered_topics']}")
        print(f"Success Rate: {summary['average_success_rate']}%")
        
        if summary['due_now'] > 0:
            print(f"\nRun 'forgetmenot list --urgent' to see due topics")
    
    def send_reminders(self, args):
        """Send desktop notifications for due reviews"""
        due_topics = self.engine.get_due_topics()
        
        if due_topics:
            self.notifications.notify_due_reviews(len(due_topics))
            print(f"Sent notification for {len(due_topics)} due topics")
        else:
            print("No topics due for review")

def main():
    parser = argparse.ArgumentParser(
        description='Forget-Me-Not: Smart study scheduler using spaced repetition',
        prog='forgetmenot'
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Add command
    add_parser = subparsers.add_parser('add', help='Add new study topic')
    add_parser.add_argument('topic', help='Topic name')
    add_parser.add_argument('-d', '--description', help='Topic description')
    
    # Review command
    review_parser = subparsers.add_parser('review', help='Mark topic as reviewed')
    review_parser.add_argument('topic', help='Topic name')
    review_group = review_parser.add_mutually_exclusive_group(required=True)
    review_group.add_argument('--success', action='store_true', help='Successful review')
    review_group.add_argument('--failure', action='store_true', help='Failed review')
    
    # List command
    list_parser = subparsers.add_parser('list', help='List topics')
    list_parser.add_argument('--urgent', action='store_true', help='Show only urgent/due topics')
    
    # Stats command
    stats_parser = subparsers.add_parser('stats', help='Show study statistics')
    
    # Remind command
    remind_parser = subparsers.add_parser('remind', help='Send desktop notifications for due topics')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    cli = ForgetMeNotCLI()
    
    if args.command == 'add':
        cli.add_topic(args)
    elif args.command == 'review':
        cli.review_topic(args)
    elif args.command == 'list':
        cli.list_topics(args)
    elif args.command == 'stats':
        cli.show_stats(args)
    elif args.command == 'remind':
        cli.send_reminders(args)

if __name__ == "__main__":
    main()