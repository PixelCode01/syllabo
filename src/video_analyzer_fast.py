"""
Fast video analysis methods for improved performance
"""

from typing import List, Dict
import re
import asyncio

class FastVideoAnalyzer:
    """Fast video analysis methods to improve performance"""
    
    def _fast_filter_videos(self, videos: List[Dict], topic: str) -> List[Dict]:
        """Quickly filter videos based on title and metadata relevance"""
        topic_words = set(topic.lower().split())
        
        scored_videos = []
        for video in videos:
            score = 0
            title = video.get('title', '').lower()
            channel = video.get('channel', '').lower()
            
            # Title relevance (quick scoring)
            title_words = set(title.split())
            overlap = len(topic_words.intersection(title_words))
            score += overlap * 5
            
            # Educational keywords
            educational_terms = ['tutorial', 'course', 'learn', 'explained', 'guide', 'lecture']
            for term in educational_terms:
                if term in title:
                    score += 3
            
            # Quality indicators
            quality_terms = ['complete', 'comprehensive', 'beginner', 'step by step']
            for term in quality_terms:
                if term in title:
                    score += 2
            
            # Avoid low-quality content
            if any(bad in title for bad in ['shorts', 'meme', 'funny', 'reaction']):
                score -= 5
            
            # Duration check (prefer 5+ minutes)
            duration = video.get('duration', '0:00')
            if duration.startswith('0:0') and len(duration) <= 4:  # Very short
                score -= 3
            
            video['quick_score'] = score
            scored_videos.append(video)
        
        # Sort by quick score
        return sorted(scored_videos, key=lambda x: x.get('quick_score', 0), reverse=True)
    
    def _fast_filter_playlists(self, playlists: List[Dict], topic: str) -> List[Dict]:
        """Quickly filter playlists based on relevance"""
        topic_words = set(topic.lower().split())
        
        scored_playlists = []
        for playlist in playlists:
            score = 0
            title = playlist.get('title', '').lower()
            
            # Title relevance
            title_words = set(title.split())
            overlap = len(topic_words.intersection(title_words))
            score += overlap * 5
            
            # Course indicators
            course_terms = ['course', 'series', 'complete', 'tutorial', 'bootcamp']
            for term in course_terms:
                if term in title:
                    score += 4
            
            playlist['quick_score'] = score
            scored_playlists.append(playlist)
        
        return sorted(scored_playlists, key=lambda x: x.get('quick_score', 0), reverse=True)
    
    async def _analyze_single_video_fast(self, video: Dict, topic: str) -> Dict:
        """Fast video analysis with minimal AI calls"""
        try:
            # Quick relevance scoring based on metadata
            relevance_score = self._calculate_fast_relevance(video, topic)
            
            # Quick quality assessment
            quality_score = self._calculate_fast_quality(video)
            
            # Composite score
            composite_score = (relevance_score * 0.6 + quality_score * 0.4)
            
            video.update({
                'relevance_score': relevance_score,
                'quality_score': quality_score,
                'composite_score': composite_score,
                'analysis_method': 'fast'
            })
            
            return video
            
        except Exception as e:
            # Fallback to basic scoring
            return self._fast_analyze_video(video, topic)
    
    def _fast_analyze_video(self, video: Dict, topic: str) -> Dict:
        """Ultra-fast video analysis without AI"""
        relevance_score = self._calculate_fast_relevance(video, topic)
        quality_score = self._calculate_fast_quality(video)
        composite_score = (relevance_score * 0.6 + quality_score * 0.4)
        
        video.update({
            'relevance_score': relevance_score,
            'quality_score': quality_score,
            'composite_score': composite_score,
            'analysis_method': 'ultra_fast'
        })
        
        return video
    
    def _calculate_fast_relevance(self, video: Dict, topic: str) -> float:
        """Calculate relevance score quickly without AI"""
        score = 5.0
        topic_words = set(topic.lower().split())
        
        title = video.get('title', '').lower()
        description = video.get('description', '').lower()
        
        # Title matching
        title_words = set(title.split())
        title_overlap = len(topic_words.intersection(title_words))
        score += min(title_overlap * 2, 4)  # Max 4 points from title
        
        # Educational keywords in title
        educational_keywords = [
            'tutorial', 'course', 'learn', 'explained', 'guide', 
            'lecture', 'fundamentals', 'introduction', 'basics'
        ]
        for keyword in educational_keywords:
            if keyword in title:
                score += 0.5
        
        # Topic-specific keywords
        if any(word in title for word in topic_words):
            score += 1
        
        # Description matching (if available)
        if description:
            desc_words = set(description.split())
            desc_overlap = len(topic_words.intersection(desc_words))
            score += min(desc_overlap * 0.5, 2)  # Max 2 points from description
        
        return min(score, 10.0)
    
    def _calculate_fast_quality(self, video: Dict) -> float:
        """Calculate quality score quickly without AI"""
        score = 5.0
        
        # Duration scoring
        duration = video.get('duration', '0:00')
        duration_minutes = self._parse_duration_to_minutes(duration)
        
        if 10 <= duration_minutes <= 60:
            score += 2
        elif 5 <= duration_minutes <= 90:
            score += 1
        elif duration_minutes < 2:
            score -= 2
        
        # View count scoring
        view_count = video.get('view_count', 0)
        if isinstance(view_count, (int, float)):
            if view_count > 100000:
                score += 1.5
            elif view_count > 10000:
                score += 1
            elif view_count < 1000:
                score -= 0.5
        
        # Channel credibility (quick check)
        channel = video.get('channel', '').lower()
        educational_channels = [
            'khan academy', 'mit', 'stanford', 'coursera', 'freecodecamp',
            'programming with mosh', 'traversy media', 'corey schafer'
        ]
        
        for edu_channel in educational_channels:
            if edu_channel in channel:
                score += 2
                break
        
        # Title quality indicators
        title = video.get('title', '').lower()
        quality_indicators = ['complete', 'comprehensive', 'full', 'step by step']
        for indicator in quality_indicators:
            if indicator in title:
                score += 0.5
        
        return min(score, 10.0)
    
    def _parse_duration_to_minutes(self, duration_str: str) -> int:
        """Parse duration string to minutes"""
        try:
            parts = duration_str.split(':')
            if len(parts) == 2:  # MM:SS
                return int(parts[0])
            elif len(parts) == 3:  # HH:MM:SS
                return int(parts[0]) * 60 + int(parts[1])
            else:
                return 0
        except:
            return 0