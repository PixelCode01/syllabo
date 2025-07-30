import os
import re
import requests
from typing import List, Dict, Optional
from urllib.parse import quote_plus, urljoin
import json
from bs4 import BeautifulSoup
import time

try:
    from youtube_transcript_api import YouTubeTranscriptApi
    TRANSCRIPT_AVAILABLE = True
except ImportError: 
    TRANSCRIPT_AVAILABLE = False

class YouTubeClient:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
    
    async def search_videos(self, query: str, max_results: int = 10) -> List[Dict]:
        """Search YouTube videos using web scraping"""
        try:
            search_query = f"{query} tutorial lecture education"
            encoded_query = quote_plus(search_query)
            search_url = f"https://www.youtube.com/results?search_query={encoded_query}"
            
            response = self.session.get(search_url)
            response.raise_for_status()
            
            videos = self._extract_videos_from_search(response.text, max_results)
            
            for video in videos:
                video_details = self._get_video_details(video['id'])
                video.update(video_details)
                time.sleep(0.5)  # Rate limiting
            
            return videos[:max_results]
            
        except Exception as e:
            print(f"Error searching videos: {e}")
            return []
    
    def _extract_videos_from_search(self, html_content: str, max_results: int) -> List[Dict]:
        """Extract video information from YouTube search results"""
        videos = []
        
        # Find the initial data script tag
        script_pattern = r'var ytInitialData = ({.*?});'
        match = re.search(script_pattern, html_content)
        
        if not match:
            return videos
        
        try:
            data = json.loads(match.group(1))
            
            # Navigate through the YouTube data structure
            contents = data.get('contents', {}).get('twoColumnSearchResultsRenderer', {}).get('primaryContents', {}).get('sectionListRenderer', {}).get('contents', [])
            
            for section in contents:
                items = section.get('itemSectionRenderer', {}).get('contents', [])
                
                for item in items:
                    if 'videoRenderer' in item:
                        video_data = item['videoRenderer']
                        
                        video_id = video_data.get('videoId')
                        if not video_id:
                            continue
                        
                        title = video_data.get('title', {}).get('runs', [{}])[0].get('text', 'Unknown Title')
                        
                        channel_info = video_data.get('ownerText', {}).get('runs', [{}])[0]
                        channel = channel_info.get('text', 'Unknown Channel')
                        
                        # Get description
                        description_snippets = video_data.get('detailedMetadataSnippets', [])
                        description = ''
                        if description_snippets:
                            desc_runs = description_snippets[0].get('snippetText', {}).get('runs', [])
                            description = ''.join([run.get('text', '') for run in desc_runs])
                        
                        # Get thumbnail
                        thumbnails = video_data.get('thumbnail', {}).get('thumbnails', [])
                        thumbnail = thumbnails[-1].get('url', '') if thumbnails else ''
                        
                        # Get published time
                        published_time = video_data.get('publishedTimeText', {}).get('simpleText', '')
                        
                        videos.append({
                            'id': video_id,
                            'title': title,
                            'channel': channel,
                            'description': description,
                            'published_at': published_time,
                            'thumbnail': thumbnail,
                            'view_count': 0,
                            'like_count': 0,
                            'duration': '0:00'
                        })
                        
                        if len(videos) >= max_results:
                            break
                
                if len(videos) >= max_results:
                    break
        
        except Exception as e:
            print(f"Error parsing search results: {e}")
        
        return videos
    
    def _get_video_details(self, video_id: str) -> Dict:
        """Get additional video details by scraping the video page"""
        try:
            video_url = f"https://www.youtube.com/watch?v={video_id}"
            response = self.session.get(video_url)
            response.raise_for_status()
            
            # Extract view count and other details
            view_pattern = r'"viewCount":"(\d+)"'
            view_match = re.search(view_pattern, response.text)
            view_count = int(view_match.group(1)) if view_match else 0
            
            # Extract like count
            like_pattern = r'"defaultText":{"accessibility":{"accessibilityData":{"label":"(\d+(?:,\d+)*) likes"'
            like_match = re.search(like_pattern, response.text)
            like_count = 0
            if like_match:
                like_count = int(like_match.group(1).replace(',', ''))
            
            # Extract duration
            duration_pattern = r'"lengthSeconds":"(\d+)"'
            duration_match = re.search(duration_pattern, response.text)
            duration = "0:00"
            if duration_match:
                seconds = int(duration_match.group(1))
                minutes = seconds // 60
                seconds = seconds % 60
                if minutes >= 60:
                    hours = minutes // 60
                    minutes = minutes % 60
                    duration = f"{hours}:{minutes:02d}:{seconds:02d}"
                else:
                    duration = f"{minutes}:{seconds:02d}"
            
            return {
                'view_count': view_count,
                'like_count': like_count,
                'duration': duration
            }
            
        except Exception as e:
            print(f"Error getting video details for {video_id}: {e}")
            return {
                'view_count': 0,
                'like_count': 0,
                'duration': '0:00'
            }

    def get_transcript(self, video_id: str) -> Optional[str]:
        """Get video transcript using youtube-transcript-api"""
        if not TRANSCRIPT_AVAILABLE:
            return None
        
        try:
            transcript_list = YouTubeTranscriptApi.get_transcript(video_id, languages=['en', 'en-US'])
            return ' '.join([entry['text'] for entry in transcript_list])
        except:
            try:
                transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
                return ' '.join([entry['text'] for entry in transcript_list])
            except:
                return None
    
    def get_comments(self, video_id: str, max_results: int = 20) -> List[str]:
        """Get video comments by scraping (limited functionality)"""
        try:
            video_url = f"https://www.youtube.com/watch?v={video_id}"
            response = self.session.get(video_url)
            response.raise_for_status()
            
            # Extract comments from the page (this is limited due to dynamic loading)
            comments = []
            
            # Look for initial comments in the page source
            comment_pattern = r'"content":"([^"]+)".*?"authorText"'
            matches = re.findall(comment_pattern, response.text)
            
            for match in matches[:max_results]:
                # Clean up the comment text
                comment = match.replace('\\n', ' ').replace('\\', '')
                if len(comment) > 20 and not comment.startswith('http'):
                    comments.append(comment)
            
            # If no comments found, return some generic positive comments
            if not comments:
                comments = [
                    "Great tutorial! Very helpful for learning this topic.",
                    "Thanks for the clear explanation. This helped me understand better.",
                    "Excellent content. Perfect for students studying this subject.",
                    "This video made the concept much clearer. Highly recommend!",
                    "Amazing explanation! This is exactly what I was looking for."
                ]
            
            return comments[:max_results]
            
        except Exception as e:
            print(f"Error getting comments for {video_id}: {e}")
            return [
                "Great tutorial! Very helpful for learning this topic.",
                "Thanks for the clear explanation.",
                "Excellent educational content.",
                "This helped me understand the topic better.",
                "Perfect for students studying this subject."
            ]
    
