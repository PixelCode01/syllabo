import os
from googleapiclient.discovery import build
from youtube_transcript_api import YouTubeTranscriptApi
from typing import List, Dict, Optional

class YouTubeClient:
    def __init__(self):
        self.api_key = os.getenv('YOUTUBE_API_KEY')
        self.youtube = build('youtube', 'v3', developerKey=self.api_key)
    
    async def search_videos(self, query: str, max_results: int = 10) -> List[Dict]:
        search_response = self.youtube.search().list(
            q=query + " tutorial lecture education",
            part='id,snippet',
            maxResults=max_results,
            type='video',
            order='relevance',
            videoDuration='medium'
        ).execute()
        
        videos = []
        video_ids = []
        
        for item in search_response['items']:
            video_id = item['id']['videoId']
            video_ids.append(video_id)
            
            videos.append({
                'id': video_id,
                'title': item['snippet']['title'],
                'channel': item['snippet']['channelTitle'],
                'description': item['snippet']['description'],
                'published_at': item['snippet']['publishedAt'],
                'thumbnail': item['snippet']['thumbnails']['default']['url']
            })
        
        video_details = self.youtube.videos().list(
            part='statistics,contentDetails',
            id=','.join(video_ids)
        ).execute()
        
        for i, video in enumerate(videos):
            if i < len(video_details['items']):
                details = video_details['items'][i]
                video['view_count'] = int(details['statistics'].get('viewCount', 0))
                video['like_count'] = int(details['statistics'].get('likeCount', 0))
                video['duration'] = self._parse_duration(details['contentDetails']['duration'])
        
        return videos
    
    def get_transcript(self, video_id: str) -> Optional[str]:
        try:
            transcript_list = YouTubeTranscriptApi.get_transcript(video_id, languages=['en', 'en-US'])
            return ' '.join([entry['text'] for entry in transcript_list])
        except:
            try:
                transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
                return ' '.join([entry['text'] for entry in transcript_list])
            except:
                return None
    
    def get_comments(self, video_id: str, max_results: int = 50) -> List[str]:
        try:
            comments_response = self.youtube.commentThreads().list(
                part='snippet',
                videoId=video_id,
                maxResults=max_results,
                order='relevance'
            ).execute()
            
            comments = []
            for item in comments_response['items']:
                comment = item['snippet']['topLevelComment']['snippet']['textDisplay']
                comments.append(comment)
            
            return comments
        except:
            return []
    
    def _parse_duration(self, duration: str) -> str:
        import re
        match = re.match(r'PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?', duration)
        if not match:
            return "0:00"
        
        hours, minutes, seconds = match.groups()
        hours = int(hours) if hours else 0
        minutes = int(minutes) if minutes else 0
        seconds = int(seconds) if seconds else 0
        
        if hours > 0:
            return f"{hours}:{minutes:02d}:{seconds:02d}"
        return f"{minutes}:{seconds:02d}"