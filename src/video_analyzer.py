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
    
    def ask_user_video_preference(self, topic: str) -> str:
        """Ask user about their video learning preference"""
        print(f"\nHow would you like to learn about '{topic}'?")
        print("1. One comprehensive video covering all aspects")
        print("2. Multiple focused videos for different subtopics")
        print("3. A complete playlist/course series")
        print("4. Let me decide based on available content")
        
        choice = input("Choose your preference (1-4, default: 4): ").strip()
        preference_map = {
            '1': 'single_comprehensive',
            '2': 'multiple_focused', 
            '3': 'playlist_series',
            '4': 'auto_decide'
        }
        return preference_map.get(choice, 'auto_decide')
    
    async def analyze_videos_and_playlists(self, videos: List[Dict], playlists: List[Dict], topic: str) -> Dict:
        """Analyze both videos and playlists for a topic"""
        self.logger.info(f"Analyzing {len(videos)} videos and {len(playlists)} playlists for topic: {topic}")
        
        # Analyze videos
        analyzed_videos = []
        if videos:
            batch_size = 3
            for i in range(0, len(videos), batch_size):
                batch = videos[i:i + batch_size]
                batch_tasks = []
                
                for video in batch:
                    batch_tasks.append(self._analyze_single_video(video, topic))
                
                batch_results = await asyncio.gather(*batch_tasks, return_exceptions=True)
                
                for result in batch_results:
                    if isinstance(result, Exception):
                        self.logger.error(f"Video analysis failed: {result}")
                    else:
                        analyzed_videos.append(result)
        
        # Analyze playlists
        analyzed_playlists = []
        if playlists:
            for playlist in playlists:
                analyzed_playlist = await self._analyze_single_playlist(playlist, topic)
                analyzed_playlists.append(analyzed_playlist)
        
        # Sort both by composite score
        analyzed_videos = sorted(analyzed_videos, key=lambda x: x['composite_score'], reverse=True)
        analyzed_playlists = sorted(analyzed_playlists, key=lambda x: x['composite_score'], reverse=True)
        
        self.logger.info(f"Analysis complete. Top video: {analyzed_videos[0]['title'] if analyzed_videos else 'None'}")
        self.logger.info(f"Top playlist: {analyzed_playlists[0]['title'] if analyzed_playlists else 'None'}")
        
        # Create comprehensive learning path with topic coverage analysis
        learning_path = self._create_comprehensive_learning_path(analyzed_videos, analyzed_playlists, topic)
        
        # Add detailed topic coverage information
        learning_path['topic_coverage_details'] = await self._analyze_detailed_topic_coverage(
            analyzed_videos, analyzed_playlists, topic
        )
        
        return learning_path
    
    async def analyze_videos(self, videos: List[Dict], topic: str) -> Dict:
        """Legacy method for backward compatibility"""
        return await self.analyze_videos_and_playlists(videos, [], topic)
    
    async def _analyze_single_video(self, video: Dict, topic: str) -> Dict:
        """Analyze a single video with comprehensive scoring"""
        try:
            transcript = self.youtube_client.get_transcript(video['id'])
            comments = self.youtube_client.get_comments(video['id'])
            
            relevance_score = await self._calculate_relevance(video, transcript, topic)
            sentiment_score = await self._analyze_comments(comments)
            quality_score = self._calculate_quality_score(video, transcript)
            engagement_score = self._calculate_engagement_score(video, comments)
            
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
    
    async def _analyze_single_playlist(self, playlist: Dict, topic: str) -> Dict:
        """Analyze a single playlist with comprehensive scoring"""
        try:
            # Calculate relevance score based on title and description
            relevance_score = await self._calculate_playlist_relevance(playlist, topic)
            
            # Calculate quality score based on video count, views, etc.
            quality_score = self._calculate_playlist_quality_score(playlist)
            
            # Calculate engagement score
            engagement_score = self._calculate_playlist_engagement_score(playlist)
            
            # For playlists, sentiment is estimated based on quality indicators
            sentiment_score = (quality_score + engagement_score) / 2
            
            # Calculate composite score
            composite_score = self._calculate_composite_score(
                relevance_score, sentiment_score, quality_score, engagement_score
            )
            
            analyzed_playlist = {
                **playlist,
                'relevance_score': relevance_score,
                'sentiment_score': sentiment_score,
                'quality_score': quality_score,
                'engagement_score': engagement_score,
                'composite_score': composite_score,
                'user_rating': 0.0,  # Playlists don't have user ratings yet
                'type': 'playlist'
            }
            
            return analyzed_playlist
        except Exception as e:
            self.logger.error(f"Failed to analyze playlist {playlist.get('id', 'unknown')}: {e}")
            # Return playlist with default scores
            return {
                **playlist,
                'relevance_score': 5.0,
                'sentiment_score': 5.0,
                'quality_score': 5.0,
                'engagement_score': 5.0,
                'composite_score': 5.0,
                'user_rating': 0.0,
                'type': 'playlist'
            }
    
    async def _calculate_playlist_relevance(self, playlist: Dict, topic: str) -> float:
        """Calculate how relevant the playlist is to the topic"""
        content_parts = [f"Title: {playlist['title']}"]
        
        if playlist.get('description'):
            content_parts.append(f"Description: {playlist['description'][:500]}")
        
        content_parts.append(f"Channel: {playlist['channel']}")
        content_parts.append(f"Video count: {playlist.get('video_count', 0)} videos")
        
        content = "\n".join(content_parts)
        
        prompt = f"""Analyze how relevant this educational YouTube playlist is to the topic "{topic}".
Consider the title, description, channel, and video count.

Rate relevance on a scale of 1-10 where:
- 1-3: Not relevant or off-topic
- 4-6: Somewhat relevant, touches on the topic
- 7-8: Highly relevant, directly addresses the topic
- 9-10: Extremely relevant, comprehensive course coverage

Playlist to analyze:
{content[:1000]}

Respond with only a number between 1 and 10."""
        
        try:
            response = await self.ai_client.get_completion(prompt)
            score_match = re.search(r'\b([1-9]|10)\b', response.strip())
            if score_match:
                score = float(score_match.group(1))
                return max(1.0, min(10.0, score))
            else:
                self.logger.warning(f"Could not parse playlist relevance score from: {response}")
                return 5.0
        except Exception as e:
            self.logger.error(f"Playlist relevance calculation failed: {e}")
            return 5.0
    
    def _calculate_playlist_quality_score(self, playlist: Dict) -> float:
        """Calculate playlist quality based on various factors"""
        score = 5.0
        
        # Video count scoring (prefer 5-50 video playlists)
        video_count = playlist.get('video_count', 0)
        
        if 5 <= video_count <= 50:
            score += 2.0
        elif 3 <= video_count <= 100:
            score += 1.0
        elif video_count < 3:
            score -= 2.0
        elif video_count > 100:
            score -= 1.0
        
        # Total views scoring
        total_views = playlist.get('total_views', 0)
        if total_views > 500000:
            score += 2.0
        elif total_views > 100000:
            score += 1.0
        elif total_views < 10000:
            score -= 1.0
        
        # Channel quality indicators
        channel = playlist.get('channel', '').lower()
        if any(indicator in channel for indicator in ['university', 'academy', 'education', 'school', 'institute']):
            score += 1.0
        
        # Title quality indicators
        title = playlist.get('title', '').lower()
        if any(indicator in title for indicator in ['course', 'tutorial', 'complete', 'full', 'comprehensive', 'series']):
            score += 1.0
        
        return max(1.0, min(10.0, score))
    
    def _calculate_playlist_engagement_score(self, playlist: Dict) -> float:
        """Calculate playlist engagement score"""
        score = 5.0
        
        video_count = playlist.get('video_count', 0)
        total_views = playlist.get('total_views', 0)
        
        if video_count > 0 and total_views > 0:
            avg_views_per_video = total_views / video_count
            
            # Higher average views per video indicates better engagement
            if avg_views_per_video > 50000:
                score += 2.0
            elif avg_views_per_video > 10000:
                score += 1.0
            elif avg_views_per_video < 1000:
                score -= 1.0
        
        # Recent updates indicate active maintenance
        last_updated = playlist.get('last_updated', '').lower()
        if any(indicator in last_updated for indicator in ['day', 'week', 'month']):
            score += 0.5
        
        return max(1.0, min(10.0, score))
    
    def _create_comprehensive_learning_path(self, analyzed_videos: List[Dict], 
                                          analyzed_playlists: List[Dict], topic: str) -> Dict:
        """Create comprehensive learning path with both videos and playlists"""
        
        # Determine the best primary resource (playlist vs video)
        best_playlist = analyzed_playlists[0] if analyzed_playlists else None
        best_video = analyzed_videos[0] if analyzed_videos else None
        
        primary_resource = None
        learning_strategy = 'no_resources_found'
        
        if best_playlist and best_video:
            # Compare scores and characteristics
            if (best_playlist['composite_score'] > best_video['composite_score'] + 1.0 and 
                best_playlist.get('video_count', 0) >= 5):
                primary_resource = best_playlist
                learning_strategy = 'playlist_primary'
            else:
                primary_resource = best_video
                learning_strategy = 'video_primary_with_playlist_supplement'
        elif best_playlist:
            primary_resource = best_playlist
            learning_strategy = 'playlist_only'
        elif best_video:
            primary_resource = best_video
            learning_strategy = 'video_only'
        
        # Build supplementary resources
        supplementary_videos = []
        supplementary_playlists = []
        
        if primary_resource:
            # Add supplementary videos (excluding primary if it's a video)
            for video in analyzed_videos[:5]:
                if (video['id'] != primary_resource.get('id') and 
                    video['relevance_score'] >= 6.0 and
                    video['composite_score'] >= 6.0):
                    
                    video['coverage_type'] = self._determine_coverage_type(video, primary_resource, topic)
                    supplementary_videos.append(video)
            
            # Add supplementary playlists (excluding primary if it's a playlist)
            for playlist in analyzed_playlists[:3]:
                if (playlist['id'] != primary_resource.get('id') and 
                    playlist['relevance_score'] >= 6.0 and
                    playlist['composite_score'] >= 6.0):
                    
                    playlist['coverage_type'] = self._determine_playlist_coverage_type(playlist, primary_resource, topic)
                    supplementary_playlists.append(playlist)
        
        # Create coverage analysis
        coverage_analysis = self._analyze_comprehensive_coverage(
            primary_resource, supplementary_videos[:2], supplementary_playlists[:2], topic
        )
        
        return {
            'topic': topic,
            'primary_resource': primary_resource,
            'supplementary_videos': supplementary_videos[:2],
            'supplementary_playlists': supplementary_playlists[:2],
            'coverage_analysis': coverage_analysis,
            'learning_strategy': learning_strategy,
            'total_resources': 1 + len(supplementary_videos[:2]) + len(supplementary_playlists[:2]) if primary_resource else 0
        }
    
    def _determine_playlist_coverage_type(self, playlist: Dict, primary_resource: Dict, topic: str) -> str:
        """Determine what type of coverage this playlist provides"""
        video_count = playlist.get('video_count', 0)
        title_lower = playlist['title'].lower()
        
        if video_count <= 5:
            return 'focused_series'
        elif 5 < video_count <= 20:
            if any(word in title_lower for word in ['advanced', 'deep', 'detailed', 'complete']):
                return 'comprehensive_course'
            elif any(word in title_lower for word in ['beginner', 'intro', 'basics', 'fundamentals']):
                return 'foundation_course'
            else:
                return 'structured_learning'
        else:
            return 'extensive_course'
    
    def _analyze_comprehensive_coverage(self, primary_resource: Dict, 
                                      supplementary_videos: List[Dict], 
                                      supplementary_playlists: List[Dict], topic: str) -> Dict:
        """Analyze comprehensive topic coverage including playlists"""
        coverage = {
            'primary_covers': [],
            'supplementary_coverage': [],
            'recommended_study_order': [],
            'estimated_study_time': 0
        }
        
        if not primary_resource:
            return coverage
        
        # Analyze primary resource
        if primary_resource.get('type') == 'playlist':
            coverage['primary_covers'] = ['comprehensive_course_content']
            # Estimate 10 minutes per video on average
            estimated_time = primary_resource.get('video_count', 0) * 10
            coverage['estimated_study_time'] = estimated_time
            
            coverage['recommended_study_order'].append({
                'resource': primary_resource,
                'purpose': 'Primary Course - Complete structured learning path',
                'type': 'playlist',
                'estimated_minutes': estimated_time
            })
        else:
            coverage['primary_covers'] = self._extract_coverage_keywords(primary_resource, topic)
            primary_duration = self._parse_duration_to_minutes(primary_resource.get('duration', '0:00'))
            coverage['estimated_study_time'] = primary_duration
            
            coverage['recommended_study_order'].append({
                'resource': primary_resource,
                'purpose': 'Primary Video - Foundation understanding',
                'type': 'video',
                'estimated_minutes': primary_duration
            })
        
        # Add supplementary playlists
        for playlist in supplementary_playlists:
            estimated_time = playlist.get('video_count', 0) * 10
            coverage['estimated_study_time'] += estimated_time
            
            purpose_map = {
                'focused_series': 'Focused Series - Specific aspect deep dive',
                'comprehensive_course': 'Alternative Course - Different comprehensive approach',
                'foundation_course': 'Foundation Course - Build fundamental understanding',
                'structured_learning': 'Structured Learning - Organized topic exploration',
                'extensive_course': 'Extensive Course - Comprehensive topic coverage'
            }
            
            coverage['recommended_study_order'].append({
                'resource': playlist,
                'purpose': purpose_map.get(playlist.get('coverage_type', ''), 'Supplementary playlist'),
                'type': 'playlist',
                'estimated_minutes': estimated_time
            })
        
        # Add supplementary videos
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
                'resource': video,
                'purpose': purpose_map.get(video.get('coverage_type', ''), 'Supplementary content'),
                'type': 'video',
                'estimated_minutes': duration
            })
        
        return coverage
    
    async def _analyze_detailed_topic_coverage(self, videos: List[Dict], 
                                             playlists: List[Dict], topic: str) -> Dict:
        """Provide detailed analysis of what topics are covered in videos"""
        all_content = videos + playlists
        
        if not all_content:
            return {
                'coverage_summary': f'No content found for {topic}',
                'covered_subtopics': [],
                'missing_subtopics': self._get_expected_subtopics(topic),
                'content_recommendations': []
            }
        
        # Analyze what subtopics are covered
        covered_subtopics = set()
        content_analysis = []
        
        for content in all_content[:5]:  # Analyze top 5 pieces of content
            analysis = await self._analyze_content_topics(content, topic)
            content_analysis.append(analysis)
            covered_subtopics.update(analysis['subtopics'])
        
        # Determine missing subtopics
        expected_subtopics = self._get_expected_subtopics(topic)
        missing_subtopics = [st for st in expected_subtopics if st not in covered_subtopics]
        
        # Generate recommendations
        recommendations = self._generate_content_recommendations(
            content_analysis, covered_subtopics, missing_subtopics, topic
        )
        
        return {
            'coverage_summary': f'Found {len(covered_subtopics)} subtopics covered out of {len(expected_subtopics)} expected',
            'covered_subtopics': list(covered_subtopics),
            'missing_subtopics': missing_subtopics,
            'content_analysis': content_analysis,
            'content_recommendations': recommendations,
            'learning_completeness': len(covered_subtopics) / len(expected_subtopics) * 100 if expected_subtopics else 0
        }
    
    async def _analyze_content_topics(self, content: Dict, main_topic: str) -> Dict:
        """Analyze what specific subtopics a piece of content covers"""
        title = content.get('title', '')
        description = content.get('description', '')
        content_type = content.get('type', 'video')
        
        # Use AI to analyze topic coverage
        try:
            prompt = f"""Analyze what specific subtopics this {content_type} covers for the main topic "{main_topic}".

Title: {title}
Description: {description[:300]}

List the specific subtopics covered. Be precise and focus on educational content.
Format as a simple list of subtopics."""

            response = await self.ai_client.get_completion(prompt)
            
            # Parse subtopics from response
            subtopics = []
            for line in response.split('\n'):
                line = line.strip()
                if line and not line.startswith('#'):
                    clean_topic = line.lstrip('•-*123456789. ').strip()
                    if clean_topic and len(clean_topic) > 3:
                        subtopics.append(clean_topic.lower())
            
            return {
                'content_title': title,
                'content_type': content_type,
                'subtopics': subtopics[:8],  # Limit to 8 subtopics
                'coverage_quality': self._assess_coverage_quality(title, description, main_topic)
            }
            
        except Exception as e:
            self.logger.error(f"Content topic analysis failed: {e}")
            # Fallback to keyword-based analysis
            return self._fallback_topic_analysis(content, main_topic)
    
    def _fallback_topic_analysis(self, content: Dict, main_topic: str) -> Dict:
        """Fallback topic analysis using keyword matching"""
        title = content.get('title', '').lower()
        description = content.get('description', '').lower()
        text = f"{title} {description}"
        
        # Topic-specific keyword mapping
        keyword_mapping = {
            'python': ['syntax', 'variables', 'functions', 'classes', 'modules', 'data_types', 'loops', 'conditionals'],
            'machine_learning': ['supervised', 'unsupervised', 'algorithms', 'training', 'models', 'features', 'classification', 'regression'],
            'data_science': ['analysis', 'visualization', 'statistics', 'pandas', 'numpy', 'cleaning', 'exploration'],
            'javascript': ['variables', 'functions', 'objects', 'arrays', 'dom', 'events', 'async', 'promises']
        }
        
        # Find relevant keywords
        topic_key = main_topic.lower().replace(' ', '_')
        relevant_keywords = []
        
        for key, keywords in keyword_mapping.items():
            if key in topic_key or topic_key in key:
                relevant_keywords = keywords
                break
        
        # Find matching subtopics
        found_subtopics = []
        for keyword in relevant_keywords:
            if keyword in text:
                found_subtopics.append(keyword)
        
        return {
            'content_title': content.get('title', ''),
            'content_type': content.get('type', 'video'),
            'subtopics': found_subtopics,
            'coverage_quality': 'estimated'
        }
    
    def _get_expected_subtopics(self, topic: str) -> List[str]:
        """Get expected subtopics for a given main topic"""
        topic_lower = topic.lower()
        
        expected_topics = {
            'python': [
                'basic syntax', 'variables and data types', 'control structures', 
                'functions', 'classes and objects', 'modules and packages',
                'error handling', 'file operations', 'libraries'
            ],
            'machine learning': [
                'supervised learning', 'unsupervised learning', 'data preprocessing',
                'feature selection', 'model evaluation', 'algorithms comparison',
                'overfitting and underfitting', 'cross validation'
            ],
            'data science': [
                'data collection', 'data cleaning', 'exploratory analysis',
                'statistical analysis', 'data visualization', 'hypothesis testing',
                'predictive modeling', 'result interpretation'
            ],
            'javascript': [
                'syntax and basics', 'variables and scope', 'functions',
                'objects and arrays', 'dom manipulation', 'event handling',
                'asynchronous programming', 'error handling'
            ]
        }
        
        # Find matching expected topics
        for key, topics in expected_topics.items():
            if key in topic_lower or any(word in key for word in topic_lower.split()):
                return topics
        
        # Generic fallback
        return [
            'fundamentals', 'basic concepts', 'practical applications',
            'advanced topics', 'best practices', 'real-world examples'
        ]
    
    def _assess_coverage_quality(self, title: str, description: str, topic: str) -> str:
        """Assess the quality of topic coverage"""
        text = f"{title} {description}".lower()
        
        # Quality indicators
        comprehensive_indicators = ['complete', 'full', 'comprehensive', 'entire', 'all']
        beginner_indicators = ['beginner', 'intro', 'basics', 'fundamentals', 'start']
        advanced_indicators = ['advanced', 'expert', 'deep', 'detailed', 'master']
        practical_indicators = ['practical', 'hands-on', 'project', 'example', 'tutorial']
        
        quality_score = 0
        quality_type = []
        
        if any(indicator in text for indicator in comprehensive_indicators):
            quality_score += 3
            quality_type.append('comprehensive')
        
        if any(indicator in text for indicator in beginner_indicators):
            quality_score += 1
            quality_type.append('beginner-friendly')
        
        if any(indicator in text for indicator in advanced_indicators):
            quality_score += 2
            quality_type.append('advanced')
        
        if any(indicator in text for indicator in practical_indicators):
            quality_score += 2
            quality_type.append('practical')
        
        if quality_score >= 4:
            return 'excellent'
        elif quality_score >= 2:
            return 'good'
        else:
            return 'basic'
    
    def _generate_content_recommendations(self, content_analysis: List[Dict], 
                                        covered_subtopics: set, missing_subtopics: List[str], 
                                        topic: str) -> List[str]:
        """Generate recommendations based on content analysis"""
        recommendations = []
        
        # Analyze content quality distribution
        excellent_content = [c for c in content_analysis if c['coverage_quality'] == 'excellent']
        good_content = [c for c in content_analysis if c['coverage_quality'] == 'good']
        
        if excellent_content:
            recommendations.append(f"Start with '{excellent_content[0]['content_title']}' for comprehensive coverage")
        elif good_content:
            recommendations.append(f"Begin with '{good_content[0]['content_title']}' for solid foundation")
        
        # Recommendations for missing topics
        if missing_subtopics:
            recommendations.append(f"Look for additional content covering: {', '.join(missing_subtopics[:3])}")
        
        # Learning path recommendations
        if len(content_analysis) > 1:
            recommendations.append("Watch multiple videos to get different perspectives on the topic")
        
        # Completeness recommendations
        coverage_percentage = len(covered_subtopics) / (len(covered_subtopics) + len(missing_subtopics)) * 100
        if coverage_percentage < 70:
            recommendations.append("Consider supplementing with additional resources for complete understanding")
        
        return recommendations[:4]  # Limit to 4 recommendations
    
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