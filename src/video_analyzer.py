from typing import List, Dict
import asyncio
import re
from .youtube_client import YouTubeClient
from .feedback_system import FeedbackSystem
from .logger import SyllaboLogger

class VideoAnalyzer:
    def __init__(self, ai_client):
        self.ai_client = ai_client
        self.youtube_client = YouTubeClient()
        self.feedback_system = FeedbackSystem()
        self.logger = SyllaboLogger("video_analyzer")
    
    async def analyze_videos(self, videos: List[Dict], topic: str) -> Dict:
        self.logger.info(f"Analyzing {len(videos)} videos for topic: {topic}")
        analyzed_videos = []
        
        # Process videos in batches to avoid overwhelming APIs
        batch_size = 3
        for i in range(0, len(videos), batch_size):
            batch = videos[i:i + batch_size]
            batch_tasks = []
            
            for video in batch:
                batch_tasks.append(self._analyze_single_video(video, topic))
            
            # Process batch concurrently
            batch_results = await asyncio.gather(*batch_tasks, return_exceptions=True)
            
            for result in batch_results:
                if isinstance(result, Exception):
                    self.logger.error(f"Video analysis failed: {result}")
                else:
                    analyzed_videos.append(result)
        
        # Sort by composite score
        analyzed_videos = sorted(analyzed_videos, key=lambda x: x['composite_score'], reverse=True)
        self.logger.info(f"Analysis complete. Top video: {analyzed_videos[0]['title'] if analyzed_videos else 'None'}")
        
        # Apply optimal learning strategy
        return self._create_optimal_learning_path(analyzed_videos, topic)
    
    async def _analyze_single_video(self, video: Dict, topic: str) -> Dict:
        """Analyze a single video with comprehensive scoring"""
        try:
            # Get additional data
            transcript = self.youtube_client.get_transcript(video['id'])
            comments = self.youtube_client.get_comments(video['id'])
            
            # Calculate various scores
            relevance_score = await self._calculate_relevance(video, transcript, topic)
            sentiment_score = await self._analyze_comments(comments)
            quality_score = self._calculate_quality_score(video, transcript)
            engagement_score = self._calculate_engagement_score(video, comments)
            
            # Calculate composite score
            composite_score = self._calculate_composite_score(
                relevance_score, sentiment_score, quality_score, engagement_score
            )
            
            user_rating = self.feedback_system.get_average_rating(video['id'])
            
            analyzed_video = {
                **video,
                'relevance_score': relevance_score,
                'sentiment_score': sentiment_score,
                'quality_score': quality_score,
                'engagement_score': engagement_score,
                'composite_score': composite_score,
                'user_rating': user_rating,
                'transcript_available': transcript is not None,
                'comment_count': len(comments),
                'transcript_length': len(transcript) if transcript else 0
            }
            
            return analyzed_video
        except Exception as e:
            self.logger.error(f"Failed to analyze video {video.get('id', 'unknown')}: {e}")
            # Return video with default scores
            return {
                **video,
                'relevance_score': 5.0,
                'sentiment_score': 5.0,
                'quality_score': 5.0,
                'engagement_score': 5.0,
                'composite_score': 5.0,
                'user_rating': 0.0,
                'transcript_available': False,
                'comment_count': 0,
                'transcript_length': 0
            }
    
    async def _calculate_relevance(self, video: Dict, transcript: str, topic: str) -> float:
        """Calculate how relevant the video is to the topic"""
        content_parts = [f"Title: {video['title']}"]
        
        if video.get('description'):
            content_parts.append(f"Description: {video['description'][:500]}")
        
        if transcript:
            # Use first and middle parts of transcript for better coverage
            transcript_sample = transcript[:800]
            if len(transcript) > 1600:
                mid_point = len(transcript) // 2
                transcript_sample += " ... " + transcript[mid_point:mid_point + 400]
            content_parts.append(f"Transcript sample: {transcript_sample}")
        
        content = "\n".join(content_parts)
        
        prompt = f"""Analyze how relevant this educational video is to the topic "{topic}".
Consider the title, description, and transcript content.

Rate relevance on a scale of 1-10 where:
- 1-3: Not relevant or off-topic
- 4-6: Somewhat relevant, touches on the topic
- 7-8: Highly relevant, directly addresses the topic
- 9-10: Extremely relevant, comprehensive coverage

Content to analyze:
{content[:1500]}

Respond with only a number between 1 and 10."""
        
        try:
            response = await self.ai_client.get_completion(prompt)
            # Extract number from response
            score_match = re.search(r'\b([1-9]|10)\b', response.strip())
            if score_match:
                score = float(score_match.group(1))
                return max(1.0, min(10.0, score))
            else:
                self.logger.warning(f"Could not parse relevance score from: {response}")
                return 5.0
        except Exception as e:
            self.logger.error(f"Relevance calculation failed: {e}")
            return 5.0
    
    async def _analyze_comments(self, comments: List[str]) -> float:
        """Analyze comment sentiment and educational value"""
        if not comments:
            return 5.0
        
        # Sample comments for analysis
        sample_comments = comments[:15]
        comments_text = "\n".join([f"- {comment[:200]}" for comment in sample_comments])
        
        prompt = f"""Analyze these YouTube comments to determine if viewers found the educational content helpful and engaging.

Rate the overall sentiment and educational value on a scale of 1-10 where:
- 1-3: Mostly negative, unhelpful, or confused viewers
- 4-6: Mixed reactions, some found it helpful
- 7-8: Mostly positive, viewers found it educational
- 9-10: Extremely positive, highly praised for educational value

Comments:
{comments_text}

Respond with only a number between 1 and 10."""
        
        try:
            response = await self.ai_client.get_completion(prompt)
            score_match = re.search(r'\b([1-9]|10)\b', response.strip())
            if score_match:
                score = float(score_match.group(1))
                return max(1.0, min(10.0, score))
            else:
                self.logger.warning(f"Could not parse sentiment score from: {response}")
                return 5.0
        except Exception as e:
            self.logger.error(f"Comment analysis failed: {e}")
            return 5.0
    
    def _calculate_quality_score(self, video: Dict, transcript: str) -> float:
        """Calculate video quality based on various factors"""
        score = 5.0
        
        # Duration scoring (prefer 10-60 minute videos)
        duration_str = video.get('duration', '0:00')
        duration_minutes = self._parse_duration_to_minutes(duration_str)
        
        if 10 <= duration_minutes <= 60:
            score += 2.0
        elif 5 <= duration_minutes <= 90:
            score += 1.0
        elif duration_minutes < 3:
            score -= 2.0
        
        # View count scoring (logarithmic scale)
        view_count = video.get('view_count', 0)
        if view_count > 100000:
            score += 2.0
        elif view_count > 10000:
            score += 1.0
        elif view_count < 1000:
            score -= 1.0
        
        # Like ratio scoring
        like_count = video.get('like_count', 0)
        if view_count > 0 and like_count > 0:
            like_ratio = like_count / view_count
            if like_ratio > 0.02:  # 2% like ratio is good
                score += 1.0
            elif like_ratio > 0.01:
                score += 0.5
        
        # Transcript availability bonus
        if transcript and len(transcript) > 500:
            score += 1.0
        
        return max(1.0, min(10.0, score))
    
    def _calculate_engagement_score(self, video: Dict, comments: List[str]) -> float:
        """Calculate engagement score based on comments and interactions"""
        score = 5.0
        view_count = video.get('view_count', 0)
        
        if view_count == 0:
            return score
        
        # Comment engagement
        comment_count = len(comments)
        comment_ratio = comment_count / view_count if view_count > 0 else 0
        
        if comment_ratio > 0.001:  # 0.1% comment ratio is good
            score += 2.0
        elif comment_ratio > 0.0005:
            score += 1.0
        
        # Like engagement
        like_count = video.get('like_count', 0)
        like_ratio = like_count / view_count if view_count > 0 else 0
        
        if like_ratio > 0.02:
            score += 1.5
        elif like_ratio > 0.01:
            score += 1.0
        
        return max(1.0, min(10.0, score))
    
    def _calculate_composite_score(self, relevance: float, sentiment: float, 
                                 quality: float, engagement: float) -> float:
        """Calculate weighted composite score"""
        # Weights: relevance is most important
        weights = {
            'relevance': 0.4,
            'sentiment': 0.25,
            'quality': 0.2,
            'engagement': 0.15
        }
        
        composite = (
            relevance * weights['relevance'] +
            sentiment * weights['sentiment'] +
            quality * weights['quality'] +
            engagement * weights['engagement']
        )
        
        return round(composite, 2)
    
    def _create_optimal_learning_path(self, analyzed_videos: List[Dict], topic: str) -> Dict:
        """Create optimal learning path with primary video and supplements"""
        if not analyzed_videos:
            return {
                'topic': topic,
                'primary_video': None,
                'supplementary_videos': [],
                'coverage_analysis': {},
                'learning_strategy': 'no_videos_found'
            }
        
        primary_candidates = []
        for video in analyzed_videos[:5]:
            duration_minutes = self._parse_duration_to_minutes(video.get('duration', '0:00'))
            if (video['relevance_score'] >= 7.0 and 
                15 <= duration_minutes <= 90 and 
                video['composite_score'] >= 7.0):
                primary_candidates.append(video)
        
        if primary_candidates:
            primary_video = primary_candidates[0]
            strategy = 'comprehensive_primary'
        else:
            primary_video = analyzed_videos[0]
            strategy = 'best_available_primary'
        
        supplementary = []
        for video in analyzed_videos[1:6]:
            if (video['id'] != primary_video['id'] and 
                video['relevance_score'] >= 6.0 and
                video['composite_score'] >= 6.0):
                
                video['coverage_type'] = self._determine_coverage_type(video, primary_video, topic)
                supplementary.append(video)
        
        coverage_analysis = self._analyze_topic_coverage(primary_video, supplementary, topic)
        
        return {
            'topic': topic,
            'primary_video': primary_video,
            'supplementary_videos': supplementary[:3],
            'coverage_analysis': coverage_analysis,
            'learning_strategy': strategy,
            'total_videos': len([primary_video] + supplementary[:3])
        }
    
    def _determine_coverage_type(self, video: Dict, primary_video: Dict, topic: str) -> str:
        """Determine what type of coverage this video provides"""
        duration_minutes = self._parse_duration_to_minutes(video.get('duration', '0:00'))
        title_lower = video['title'].lower()
        
        if duration_minutes <= 15:
            if any(word in title_lower for word in ['example', 'practice', 'problem', 'exercise']):
                return 'practice_examples'
            elif any(word in title_lower for word in ['quick', 'summary', 'overview', 'intro']):
                return 'quick_review'
            else:
                return 'focused_concept'
        
        elif 15 < duration_minutes <= 45:
            if any(word in title_lower for word in ['advanced', 'deep', 'detailed', 'complete']):
                return 'deep_dive'
            elif any(word in title_lower for word in ['tutorial', 'how to', 'step by step']):
                return 'practical_tutorial'
            else:
                return 'concept_explanation'
        
        else:
            return 'comprehensive_alternative'
    
    def _analyze_topic_coverage(self, primary_video: Dict, supplementary_videos: List[Dict], topic: str) -> Dict:
        """Analyze what aspects of the topic are covered"""
        coverage = {
            'primary_covers': self._extract_coverage_keywords(primary_video, topic),
            'gaps_filled_by_supplements': [],
            'recommended_study_order': [],
            'estimated_study_time': 0
        }
        
        # Calculate study time
        primary_duration = self._parse_duration_to_minutes(primary_video.get('duration', '0:00'))
        coverage['estimated_study_time'] = primary_duration
        
        # Build study order
        coverage['recommended_study_order'].append({
            'video': primary_video,
            'purpose': 'Foundation - Start here for comprehensive overview',
            'duration_minutes': primary_duration
        })
        
        for video in supplementary_videos:
            duration = self._parse_duration_to_minutes(video.get('duration', '0:00'))
            coverage['estimated_study_time'] += duration
            
            purpose_map = {
                'practice_examples': 'Practice - Apply concepts with examples',
                'quick_review': 'Review - Quick reinforcement of key points',
                'focused_concept': 'Deep Focus - Specific concept explanation',
                'deep_dive': 'Advanced - Detailed exploration of concepts',
                'practical_tutorial': 'Tutorial - Step-by-step implementation',
                'concept_explanation': 'Explanation - Alternative perspective',
                'comprehensive_alternative': 'Alternative - Different comprehensive approach'
            }
            
            coverage['recommended_study_order'].append({
                'video': video,
                'purpose': purpose_map.get(video.get('coverage_type', ''), 'Supplementary content'),
                'duration_minutes': duration
            })
        
        return coverage
    
    def _extract_coverage_keywords(self, video: Dict, topic: str) -> List[str]:
        """Extract what specific aspects this video covers"""
        title = video['title'].lower()
        description = video.get('description', '').lower()
        
        # Common educational keywords
        coverage_indicators = []
        
        if any(word in title for word in ['introduction', 'intro', 'basics', 'fundamentals']):
            coverage_indicators.append('fundamentals')
        
        if any(word in title for word in ['advanced', 'complex', 'detailed']):
            coverage_indicators.append('advanced_concepts')
        
        if any(word in title for word in ['example', 'practice', 'problem']):
            coverage_indicators.append('practical_examples')
        
        if any(word in title for word in ['theory', 'concept', 'principle']):
            coverage_indicators.append('theoretical_foundation')
        
        if any(word in title for word in ['application', 'real world', 'use case']):
            coverage_indicators.append('real_world_applications')
        
        return coverage_indicators if coverage_indicators else ['general_coverage']
    
    def _parse_duration_to_minutes(self, duration_str: str) -> int:
        """Parse duration string to minutes"""
        try:
            parts = duration_str.split(':')
            if len(parts) == 2:  # MM:SS
                return int(parts[0])
            elif len(parts) == 3:  # HH:MM:SS
                return int(parts[0]) * 60 + int(parts[1])
            return 0
        except:
            return 0