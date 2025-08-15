#!/usr/bin/env python3
"""
Demo showing enhanced video search for calculus syllabus
"""

import sys
import os
import asyncio

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from main import SyllaboMain

async def demo_calculus_search():
    """Demo enhanced search for the calculus syllabus"""
    
    print("🎓 ENHANCED CALCULUS VIDEO SEARCH DEMO")
    print("=" * 60)
    
    # The syllabus from the user
    syllabus_title = "Advanced Calculus"
    topics = [
        "Successive Differentiation and Mean Value Theorem",
        "Leibnitz Theorem", 
        "Generalized Mean Value Theorem",
        "Taylor's and Maclaurin's Expansion of Functions",
        "Increasing and decreasing functions",
        "Concavity, Convexity and Inflection point",
        "Extrema of functions"
    ]
    
    print(f"📚 Syllabus: {syllabus_title}")
    print(f"📋 Topics: {len(topics)} main topics")
    for i, topic in enumerate(topics, 1):
        print(f"   {i}. {topic}")
    
    app = SyllaboMain()
    
    try:
        print(f"\n🔍 Performing enhanced video search...")
        
        # Use the enhanced search
        youtube_resources = await app._enhanced_video_search_for_syllabus(syllabus_title, topics)
        
        print(f"\n📊 SEARCH RESULTS:")
        print(f"   Videos found: {len(youtube_resources.get('videos', []))}")
        print(f"   Unique channels: {youtube_resources.get('channel_diversity', {}).get('total_channels', 0)}")
        print(f"   Diversity score: {youtube_resources.get('channel_diversity', {}).get('diversity_score', 0):.2f}")
        
        # Show top videos
        videos = youtube_resources.get('videos', [])
        if videos:
            print(f"\n🎥 TOP VIDEOS FOUND:")
            print("-" * 50)
            
            for i, video in enumerate(videos[:8], 1):  # Show top 8
                title = video.get('title', 'Unknown')
                channel = video.get('channel', 'Unknown')
                duration = video.get('duration', 'Unknown')
                views = video.get('view_count', 0)
                topic = video.get('search_topic', 'General')
                
                print(f"{i}. {title}")
                print(f"   📺 {channel} • ⏱️ {duration} • 👁️ {views:,} views")
                print(f"   🎯 Topic: {topic}")
                if 'direct_link' in video:
                    print(f"   🔗 {video['direct_link']}")
                print()
        
        # Show topic coverage
        coverage = youtube_resources.get('topic_coverage', {})
        if coverage:
            print(f"📈 TOPIC COVERAGE ANALYSIS:")
            print("-" * 40)
            
            for topic, info in list(coverage.items())[:6]:
                quality = info.get('coverage_quality', 'Unknown')
                video_count = info.get('video_count', 0)
                
                quality_emoji = {
                    'Excellent': '🟢',
                    'Good': '🟡', 
                    'Fair': '🔵',
                    'Limited': '🔴',
                    'No coverage': '⚫'
                }.get(quality, '⚪')
                
                print(f"{quality_emoji} {topic}: {quality} ({video_count} videos)")
        
        # Show missing topics
        missing = youtube_resources.get('missing_topics', [])
        if missing:
            print(f"\n⚠️  TOPICS NEEDING MORE COVERAGE:")
            for topic in missing:
                print(f"   • {topic}")
        
        # Show study order
        study_order = youtube_resources.get('study_order', [])
        if study_order:
            print(f"\n📚 RECOMMENDED STUDY ORDER:")
            print("-" * 40)
            
            for i, video in enumerate(study_order[:5], 1):
                title = video.get('title', 'Unknown')[:50] + "..." if len(video.get('title', '')) > 50 else video.get('title', 'Unknown')
                channel = video.get('channel', 'Unknown')
                print(f"{i}. {title}")
                print(f"   📺 {channel}")
        
        print(f"\n🎉 ENHANCED SEARCH COMPLETE!")
        print("=" * 60)
        print("✅ Benefits of Enhanced Search:")
        print("   • Comprehensive topic coverage")
        print("   • Reduced repetitive content")
        print("   • Channel diversity for different teaching styles")
        print("   • Organized study progression")
        print("   • Quality-based ranking")
        print("   • Missing topic identification")
        
        return True
        
    except Exception as e:
        print(f"❌ Enhanced search demo failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = asyncio.run(demo_calculus_search())
    if success:
        print("\n✅ DEMO COMPLETED SUCCESSFULLY")
    else:
        print("\n❌ DEMO FAILED")
    sys.exit(0 if success else 1)