#!/usr/bin/env python3

import asyncio
import sys
import os

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.youtube_client import YouTubeClient

async def test_youtube_scraping():
    print("Testing YouTube scraping without API...")
    print("-" * 40)
    
    client = YouTubeClient()
    
    # Test search
    print("Searching for 'Python programming tutorial'...")
    try:
        videos = await client.search_videos("Python programming tutorial", max_results=2)
        
        if videos:
            print(f"Success! Found {len(videos)} videos:")
            for i, video in enumerate(videos, 1):
                print(f"\n{i}. {video['title']}")
                print(f"   Channel: {video['channel']}")
                print(f"   Duration: {video['duration']}")
                print(f"   Views: {video.get('view_count', 0):,}")
                print(f"   Video ID: {video['id']}")
                print(f"   Direct Link: https://youtube.com/watch?v={video['id']}")
                
                # Verify the video ID is valid
                if video['id'] and len(video['id']) == 11:
                    print(f"   Video ID Format: Valid (11 characters)")
                else:
                    print(f"   Video ID Format: Invalid - {video['id']}")
            
            # Test transcript
            print(f"\nTesting transcript for first video...")
            transcript = client.get_transcript(videos[0]['id'])
            if transcript:
                print(f"Transcript found! Length: {len(transcript)} characters")
                print(f"Sample: {transcript[:100]}...")
            else:
                print("No transcript available for this video")
            
            print("\nYouTube scraping test completed successfully!")
            
        else:
            print("No videos found - there might be an issue with scraping")
            
    except Exception as e:
        print(f"Error during test: {e}")

if __name__ == "__main__":
    asyncio.run(test_youtube_scraping())