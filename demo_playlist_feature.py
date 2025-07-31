#!/usr/bin/env python3

import sys
import os
sys.path.append('src')

from src.youtube_client import YouTubeClient
from src.video_analyzer import VideoAnalyzer
from src.ai_client import AIClient
import asyncio

async def demo_playlist_feature():
    """Demo the new playlist functionality"""
    print("SYLLABO PLAYLIST FEATURE DEMO")
    print("=" * 50)
    print()
    
    # Initialize components
    youtube_client = YouTubeClient()
    ai_client = AIClient()
    video_analyzer = VideoAnalyzer(ai_client)
    
    topic = "Python Programming"
    print(f"Searching for resources on: {topic}")
    print()
    
    # Search for both videos and playlists
    print("1. Searching for videos...")
    videos = await youtube_client.search_videos(f"{topic} tutorial", 3)
    print(f"   Found {len(videos)} videos")
    
    print("2. Searching for playlists...")
    playlists = await youtube_client.search_playlists(f"{topic} course", 2)
    print(f"   Found {len(playlists)} playlists")
    print()
    
    if not videos and not playlists:
        print("No resources found. Using mock data for demonstration...")
        
        # Create mock data to demonstrate the feature
        videos = [
            {
                'id': 'mock_video_1',
                'title': 'Python Programming Tutorial for Beginners',
                'channel': 'Programming with Mosh',
                'duration': '45:30',
                'view_count': 2500000,
                'like_count': 85000,
                'description': 'Complete Python tutorial covering basics to advanced concepts',
                'type': 'video'
            }
        ]
        
        playlists = [
            {
                'id': 'mock_playlist_1',
                'title': 'Complete Python Course 2024',
                'channel': 'freeCodeCamp.org',
                'video_count': 25,
                'total_views': 1500000,
                'description': 'Comprehensive Python programming course from beginner to advanced',
                'type': 'playlist',
                'url': 'https://youtube.com/playlist?list=PLWKjhJtqVAblQe2CCWqV4Zy3LY01Z8aF1'
            }
        ]
        print("Using mock data to demonstrate playlist analysis...")
        print()
    
    # Analyze resources
    print("3. Analyzing resources with AI...")
    analysis_result = await video_analyzer.analyze_videos_and_playlists(videos, playlists, topic)
    
    # Display results
    print("4. ANALYSIS RESULTS")
    print("-" * 30)
    
    primary_resource = analysis_result.get('primary_resource')
    if primary_resource:
        resource_type = primary_resource.get('type', 'video')
        type_indicator = "[PLAYLIST]" if resource_type == 'playlist' else "[VIDEO]"
        
        print(f"PRIMARY RESOURCE: {type_indicator}")
        print(f"Title: {primary_resource['title']}")
        print(f"Channel: {primary_resource['channel']}")
        
        if resource_type == 'playlist':
            print(f"Videos: {primary_resource.get('video_count', 0)}")
            print(f"URL: {primary_resource.get('url', 'N/A')}")
        else:
            print(f"Duration: {primary_resource.get('duration', 'N/A')}")
            print(f"Views: {primary_resource.get('view_count', 0):,}")
        
        print(f"Relevance Score: {primary_resource.get('relevance_score', 0):.1f}/10")
        print(f"Overall Score: {primary_resource.get('composite_score', 0):.1f}/10")
        print()
    
    # Show supplementary resources
    supplementary_videos = analysis_result.get('supplementary_videos', [])
    supplementary_playlists = analysis_result.get('supplementary_playlists', [])
    
    if supplementary_videos or supplementary_playlists:
        print("SUPPLEMENTARY RESOURCES:")
        
        for video in supplementary_videos:
            print(f"- [VIDEO] {video['title']}")
            print(f"  Score: {video.get('composite_score', 0):.1f}/10")
        
        for playlist in supplementary_playlists:
            print(f"- [PLAYLIST] {playlist['title']}")
            print(f"  Score: {playlist.get('composite_score', 0):.1f}/10")
        print()
    
    # Show learning strategy
    strategy = analysis_result.get('learning_strategy', 'unknown')
    print(f"RECOMMENDED LEARNING STRATEGY: {strategy}")
    
    coverage = analysis_result.get('coverage_analysis', {})
    estimated_time = coverage.get('estimated_study_time', 0)
    print(f"ESTIMATED STUDY TIME: {estimated_time} minutes")
    
    print()
    print("=" * 50)
    print("DEMO COMPLETE")
    print()
    print("Key Features Demonstrated:")
    print("✓ Playlist search and discovery")
    print("✓ Combined video and playlist analysis")
    print("✓ Smart primary resource selection")
    print("✓ Comprehensive learning path creation")
    print("✓ Professional output formatting")

if __name__ == "__main__":
    asyncio.run(demo_playlist_feature())