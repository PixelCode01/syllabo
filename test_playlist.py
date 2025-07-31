#!/usr/bin/env python3

import sys
import os
sys.path.append('src')

from src.youtube_client import YouTubeClient
import asyncio

async def test_playlist_search():
    client = YouTubeClient()
    print("Testing playlist search...")
    
    playlists = await client.search_playlists('machine learning', 2)
    print(f'Found {len(playlists)} playlists')
    
    for i, p in enumerate(playlists, 1):
        print(f'{i}. {p.get("title", "Unknown")} ({p.get("video_count", 0)} videos)')
        print(f'   Channel: {p.get("channel", "Unknown")}')
        print(f'   URL: {p.get("url", "No URL")}')
        print()

if __name__ == "__main__":
    asyncio.run(test_playlist_search())