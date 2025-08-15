#!/usr/bin/env python3
"""
Demo script showing the enhanced features that address user feedback
"""

import asyncio
import sys
import os
from pathlib import Path

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.resource_manager import ResourceManager
from src.persistent_quiz_manager import PersistentQuizManager
from src.ai_client import AIClient

async def demo_enhanced_features():
    """Demonstrate the new enhanced features"""
    print("🎓 SYLLABO ENHANCED FEATURES DEMO")
    print("=" * 50)
    print("Addressing user feedback about direct links and persistent storage\n")
    
    # Initialize components
    resource_manager = ResourceManager()
    ai_client = AIClient()
    quiz_manager = PersistentQuizManager(ai_client)
    
    # Demo 1: Resource Management with Direct Links
    print("📚 DEMO 1: Enhanced Resource Management")
    print("-" * 40)
    
    # Sample resources with direct links (simulating what would be found)
    sample_resources = {
        'videos': [
            {
                'id': 'dQw4w9WgXcQ',
                'title': 'Python Programming Complete Course',
                'channel': 'Programming with Mosh',
                'duration': '6:14:07',
                'view_count': 2500000,
                'description': 'Complete Python tutorial for beginners',
                'direct_link': 'https://www.youtube.com/watch?v=dQw4w9WgXcQ',
                'embed_link': 'https://www.youtube.com/embed/dQw4w9WgXcQ'
            },
            {
                'id': 'abc123def',
                'title': 'Python Data Structures Explained',
                'channel': 'Corey Schafer',
                'duration': '45:30',
                'view_count': 850000,
                'description': 'Deep dive into Python data structures',
                'direct_link': 'https://www.youtube.com/watch?v=abc123def',
                'embed_link': 'https://www.youtube.com/embed/abc123def'
            }
        ],
        'playlists': [
            {
                'id': 'PLrAXtmRdnEQy',
                'title': 'Complete Python Course Playlist',
                'channel': 'freeCodeCamp.org',
                'video_count': 25,
                'total_views': 5000000,
                'description': 'Comprehensive Python learning playlist',
                'direct_link': 'https://www.youtube.com/playlist?list=PLrAXtmRdnEQy'
            }
        ],
        'books': [
            {
                'title': 'Python Crash Course',
                'author': 'Eric Matthes',
                'type': 'paid',
                'price': '$39.99',
                'topics': ['basics', 'projects'],
                'amazon_search': 'https://www.amazon.com/s?k=Python+Crash+Course+Eric+Matthes',
                'google_books': 'https://books.google.com/books?q=Python+Crash+Course+Eric+Matthes'
            }
        ],
        'courses': [
            {
                'title': 'Complete Python Bootcamp',
                'platform': 'Udemy',
                'type': 'paid',
                'price': '$84.99',
                'topics': ['basics', 'advanced'],
                'platform_search': 'https://www.udemy.com/courses/search/?q=Complete+Python+Bootcamp'
            }
        ]
    }
    
    # Save resources with direct links
    print("💾 Saving resources with direct links...")
    saved_files = resource_manager.save_learning_resources(
        "Python Programming", sample_resources, include_links=True
    )
    
    print("✅ Resources saved in multiple formats:")
    for format_type, file_path in saved_files.items():
        print(f"   📄 {format_type.upper()}: {file_path}")
    
    print("\n🔗 Direct links included:")
    print(f"   🎥 Video: {sample_resources['videos'][0]['direct_link']}")
    print(f"   📚 Playlist: {sample_resources['playlists'][0]['direct_link']}")
    print(f"   📖 Book search: {sample_resources['books'][0]['amazon_search']}")
    
    # Demo 2: Persistent Quiz Management
    print(f"\n📝 DEMO 2: Persistent Quiz Management")
    print("-" * 40)
    
    print("🧠 Creating quiz based on the resources...")
    try:
        quiz_data = await quiz_manager.create_quiz_from_resources(
            "Python Programming", sample_resources, num_questions=3, difficulty='mixed'
        )
        
        print(f"✅ Quiz created: {quiz_data.get('title')}")
        print(f"   📊 Questions: {quiz_data.get('total_questions')}")
        print(f"   ⏱️  Estimated time: {quiz_data.get('estimated_time')} minutes")
        print(f"   🆔 Quiz ID: {quiz_data.get('id')}")
        
        # Show that quiz is based on actual resources
        source_resources = quiz_data.get('source_resources', {})
        if source_resources:
            print("   📚 Based on these resources:")
            for resource_type, resources in source_resources.items():
                for resource in resources:
                    print(f"      • {resource.get('title', 'Unknown')}")
        
        # Simulate taking the quiz (save a mock attempt)
        print("\n🎯 Simulating quiz attempt...")
        mock_answers = [
            {'question_number': 1, 'is_correct': True, 'user_answer': 'A'},
            {'question_number': 2, 'is_correct': False, 'user_answer': 'B'},
            {'question_number': 3, 'is_correct': True, 'user_answer': 'C'}
        ]
        
        success = quiz_manager.save_quiz_attempt(
            quiz_data.get('id'), 2, 3, mock_answers, 5
        )
        
        if success:
            print("✅ Quiz attempt saved!")
            print("   📊 Score: 2/3 (66.7%)")
            print("   ⏱️  Time: 5 minutes")
        
    except Exception as e:
        print(f"❌ Error creating quiz: {e}")
        print("   (This might happen if AI client is not configured)")
    
    # Demo 3: Show saved resources and quizzes
    print(f"\n📋 DEMO 3: Persistent Storage")
    print("-" * 40)
    
    # Show saved resources
    saved_resources = resource_manager.get_saved_resources()
    print(f"💾 Saved resource files: {len(saved_resources)}")
    for resource in saved_resources:
        print(f"   📚 {resource.get('topic')} - {resource.get('total_count')} resources")
    
    # Show saved quizzes
    saved_quizzes = quiz_manager.get_saved_quizzes()
    print(f"📝 Saved quizzes: {len(saved_quizzes)}")
    for quiz in saved_quizzes:
        print(f"   🧠 {quiz.get('title')} - {quiz.get('total_questions')} questions")
        print(f"      Attempts: {quiz.get('attempts')}, Best: {quiz.get('best_score')}%")
    
    print(f"\n🎉 DEMO COMPLETE!")
    print("=" * 50)
    print("✅ Key improvements implemented:")
    print("   🔗 Direct links to YouTube videos and playlists")
    print("   💾 Resources saved in multiple formats (TXT, CSV, HTML)")
    print("   📝 Quizzes created from actual recommended resources")
    print("   🔄 Persistent quiz storage for retaking")
    print("   📊 Quiz statistics and progress tracking")
    print("   📱 Clickable HTML files for easy access")
    
    print(f"\n💡 User can now:")
    print("   • Click links to go directly to YouTube videos/playlists")
    print("   • Save resource lists for future reference")
    print("   • Create quizzes based on actual content they'll study")
    print("   • Retake quizzes and track improvement over time")
    print("   • Access everything offline through saved files")

if __name__ == "__main__":
    asyncio.run(demo_enhanced_features())