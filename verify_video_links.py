#!/usr/bin/env python3

import asyncio
import sys
import os
import re

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.youtube_client import YouTubeClient

def is_valid_youtube_video_id(video_id):
    """Check if a YouTube video ID is valid format"""
    if not video_id:
        return False
    # YouTube video IDs are 11 characters long and contain alphanumeric characters, hyphens, and underscores
    return len(video_id) == 11 and re.match(r'^[a-zA-Z0-9_-]+$', video_id)

async def verify_video_links():
    print("=" * 60)
    print("           VIDEO LINKS VERIFICATION")
    print("=" * 60)
    
    client = YouTubeClient()
    
    test_queries = [
        "Python programming tutorial",
        "Machine learning basics",
        "Data structures algorithms"
    ]
    
    for query in test_queries:
        print(f"\nTesting query: '{query}'")
        print("-" * 40)
        
        try:
            videos = await client.search_videos(query, max_results=2)
            
            if videos:
                print(f"Found {len(videos)} videos")
                
                for i, video in enumerate(videos, 1):
                    print(f"\nVideo {i}:")
                    print(f"  Title: {video['title']}")
                    print(f"  Channel: {video['channel']}")
                    print(f"  Video ID: {video['id']}")
                    
                    # Verify video ID format
                    if is_valid_youtube_video_id(video['id']):
                        print(f"  Video ID Status: Valid")
                    else:
                        print(f"  Video ID Status: Invalid - '{video['id']}'")
                    
                    # Generate and display the actual video link
                    video_url = f"https://youtube.com/watch?v={video['id']}"
                    print(f"  Direct Video Link: {video_url}")
                    
                    # Verify link format
                    if video_url.startswith("https://youtube.com/watch?v=") and len(video['id']) == 11:
                        print(f"  Link Status: Valid YouTube video link")
                    else:
                        print(f"  Link Status: Invalid link format")
                
            else:
                print("No videos found")
                
        except Exception as e:
            print(f"Error testing query '{query}': {e}")
    
    print(f"\n{'='*60}")
    print("VERIFICATION COMPLETE")
    print(f"{'='*60}")
    print("Key Points:")
    print("- Video IDs should be 11 characters long")
    print("- Links should be in format: https://youtube.com/watch?v=VIDEO_ID")
    print("- All links should be direct video links, not search links")

if __name__ == "__main__":
    asyncio.run(verify_video_links())