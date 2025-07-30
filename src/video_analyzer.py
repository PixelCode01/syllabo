from typing import List, Dict
from .youtube_client import YouTubeClient

class VideoAnalyzer:
    def __init__(self, ai_client):
        self.ai_client = ai_client
        self.youtube_client = YouTubeClient()
    
    async def analyze_videos(self, videos: List[Dict], topic: str) -> List[Dict]:
        analyzed_videos = []
        
        for video in videos:
            transcript = self.youtube_client.get_transcript(video['id'])
            comments = self.youtube_client.get_comments(video['id'])
            
            relevance_score = await self._calculate_relevance(
                video, transcript, topic
            )
            
            sentiment_score = await self._analyze_comments(comments)
            
            analyzed_video = {
                **video,
                'relevance_score': relevance_score,
                'sentiment_score': sentiment_score,
                'transcript_available': transcript is not None,
                'comment_count': len(comments)
            }
            
            analyzed_videos.append(analyzed_video)
        
        return sorted(analyzed_videos, key=lambda x: x['relevance_score'], reverse=True)
    
    async def _calculate_relevance(self, video: Dict, transcript: str, topic: str) -> float:
        content = f"Title: {video['title']}\nDescription: {video['description']}"
        if transcript:
            content += f"\nTranscript: {transcript[:1000]}"
        
        prompt = f"""
        Rate how relevant this video is to the topic "{topic}" on a scale of 1-10.
        Consider title, description, and transcript content.
        Return only a number between 1-10.
        
        Video content:
        {content}
        """
        
        try:
            response = await self.ai_client.get_completion(prompt)
            score = float(response.strip())
            return max(1.0, min(10.0, score))
        except:
            return 5.0
    
    async def _analyze_comments(self, comments: List[str]) -> float:
        if not comments:
            return 5.0
        
        sample_comments = comments[:10]
        comments_text = "\n".join(sample_comments)
        
        prompt = f"""
        Analyze the sentiment of these YouTube comments and rate the overall educational value
        on a scale of 1-10. Consider if viewers found the content helpful.
        Return only a number between 1-10.
        
        Comments:
        {comments_text}
        """
        
        try:
            response = await self.ai_client.get_completion(prompt)
            score = float(response.strip())
            return max(1.0, min(10.0, score))
        except:
            return 5.0