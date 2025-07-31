#!/usr/bin/env python3

import os
import sys
import time
from datetime import datetime, timedelta

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.spaced_repetition import SpacedRepetitionEngine
from src.notification_system import NotificationSystem

def demo_spaced_repetition():
    """Demonstrate the spaced repetition system"""
    print("Spaced Repetition System Demo")
    print("=" * 50)
    
    # Initialize the system
    engine = SpacedRepetitionEngine("demo_spaced_repetition.json")
    notifications = NotificationSystem()
    
    # Clear any existing demo data
    if os.path.exists("demo_spaced_repetition.json"):
        os.remove("demo_spaced_repetition.json")
    
    print("\n1. Adding sample topics to review schedule...")
    
    # Add some sample topics
    topics = [
        ("Neural Networks", "Forward and backward propagation algorithms"),
        ("Machine Learning", "Supervised and unsupervised learning techniques"),
        ("Data Structures", "Arrays, linked lists, trees, and graphs"),
        ("Algorithms", "Sorting, searching, and optimization algorithms"),
        ("Python Programming", "Object-oriented programming and data types")
    ]
    
    for topic_name, description in topics:
        engine.add_topic(topic_name, description)
        print(f"   Added: {topic_name}")
    
    print(f"\nAdded {len(topics)} topics to the review schedule")
    
    print("\n2. Current review schedule:")
    all_topics = engine.get_all_topics()
    for topic in all_topics:
        print(f"   • {topic['topic_name']} - Next review: {topic['next_review_date']} ({topic['days_until_review']} days)")
    
    print("\n3. Simulating some reviews...")
    
    # Simulate some reviews by manipulating the data
    # Mark Neural Networks as reviewed successfully
    engine.mark_review("Neural Networks", True)
    print("   ✓ Marked 'Neural Networks' as successful review")
    
    # Mark Machine Learning as failed review
    engine.mark_review("Machine Learning", False)
    print("   ✗ Marked 'Machine Learning' as failed review")
    
    # Mark Data Structures as successful
    engine.mark_review("Data Structures", True)
    print("   ✓ Marked 'Data Structures' as successful review")
    
    print("\n4. Updated review schedule after reviews:")
    updated_topics = engine.get_all_topics()
    for topic in sorted(updated_topics, key=lambda x: x['days_until_review']):
        status_icon = "🔴" if topic['days_until_review'] <= 0 else "🟡" if topic['days_until_review'] <= 1 else "🟢"
        print(f"   {status_icon} {topic['topic_name']:<20} | {topic['mastery_level']:<12} | Next: {topic['days_until_review']} days | Success: {topic['success_rate']}%")
    
    print("\n5. Study statistics:")
    summary = engine.get_study_summary()
    print(f"   Total Topics: {summary['total_topics']}")
    print(f"   Due Now: {summary['due_now']}")
    print(f"   Due Today: {summary['due_today']}")
    print(f"   Mastered Topics: {summary['mastered_topics']}")
    print(f"   Average Success Rate: {summary['average_success_rate']}%")
    
    print("\n6. Topics due for review:")
    due_topics = engine.get_due_topics()
    if due_topics:
        for item in due_topics:
            print(f"   📚 {item.topic_name} - {item.description}")
    else:
        print("   No topics are due for review right now")
    
    print("\n7. Testing notification system...")
    if notifications.notifications_enabled:
        if due_topics:
            notifications.notify_due_reviews(len(due_topics))
            print(f"   📱 Sent notification for {len(due_topics)} due topics")
        else:
            notifications.send_notification("Syllabo Demo", "Spaced repetition system is working!")
            print("   📱 Sent demo notification")
    else:
        print("   📱 Notifications not available on this system")
    
    print("\n8. Detailed topic analysis:")
    for topic_name in ["Neural Networks", "Machine Learning"]:
        stats = engine.get_topic_stats(topic_name)
        if stats:
            print(f"\n   {topic_name}:")
            print(f"      Mastery Level: {stats['mastery_level']}")
            print(f"      Success Rate: {stats['success_rate']}%")
            print(f"      Current Interval: {stats['current_interval']} days")
            print(f"      Next Review: {stats['next_review_date']}")
    
    print("\n" + "=" * 50)
    print("Demo completed!")
    print("\nTo continue using the system:")
    print("• Use 'python forgetmenot.py' for standalone spaced repetition")
    print("• Use 'python syllabo_enhanced.py review' for integrated features")
    print("• Check 'SPACED_REPETITION_GUIDE.md' for complete documentation")
    
    # Clean up demo file
    if os.path.exists("demo_spaced_repetition.json"):
        os.remove("demo_spaced_repetition.json")
        print("\nDemo data cleaned up")

if __name__ == "__main__":
    demo_spaced_repetition()