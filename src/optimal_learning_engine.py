"""
Optimal Learning Engine - Core system for intelligent video selection and study material generation.
Implements adaptive multi-modal learning strategy for maximum educational effectiveness.
"""

from typing import List, Dict, Optional, Tuple
import asyncio
from .video_analyzer import VideoAnalyzer
from .notes_generator import NotesGenerator
from .ai_client import AIClient


class OptimalLearningEngine:
    """Main engine for creating optimal learning experiences from video content"""
    
    def __init__(self, ai_client: AIClient):
        self.ai_client = ai_client
        self.video_analyzer = VideoAnalyzer(ai_client)
        self.notes_generator = NotesGenerator(ai_client)
    
    async def create_learning_experience(self, videos: List[Dict], topic: str) -> Dict:
        """Create complete learning experience from video list"""
        if not videos:
            return self._create_empty_response(topic)
        
        learning_path = await self.video_analyzer.analyze_videos(videos, topic)
        study_materials = await self.notes_generator.generate_optimal_study_materials(learning_path)
        
        return {
            'topic': topic,
            'learning_path': learning_path,
            'study_materials': study_materials,
            'summary': self._create_experience_summary(learning_path, study_materials)
        }
    
    def _create_empty_response(self, topic: str) -> Dict:
        """Create response when no videos are available"""
        return {
            'topic': topic,
            'learning_path': {
                'primary_video': None,
                'supplementary_videos': [],
                'learning_strategy': 'no_content_available'
            },
            'study_materials': {},
            'summary': {
                'total_videos': 0,
                'estimated_time': 0,
                'learning_objectives': [],
                'key_concepts': [],
                'study_plan': []
            }
        }
    
    def _create_experience_summary(self, learning_path: Dict, study_materials: Dict) -> Dict:
        """Create summary of the complete learning experience"""
        primary_video = learning_path.get('primary_video')
        supplementary_videos = learning_path.get('supplementary_videos', [])
        
        total_videos = 1 if primary_video else 0
        total_videos += len(supplementary_videos)
        
        estimated_time = learning_path.get('coverage_analysis', {}).get('estimated_study_time', 0)
        
        comprehensive_guide = study_materials.get('comprehensive_guide', {})
        
        return {
            'total_videos': total_videos,
            'estimated_time': estimated_time,
            'learning_strategy': learning_path.get('learning_strategy', 'unknown'),
            'learning_objectives': comprehensive_guide.get('learning_objectives', []),
            'key_concepts': comprehensive_guide.get('key_concepts_summary', []),
            'study_plan': comprehensive_guide.get('study_plan', []),
            'effectiveness_score': self._calculate_effectiveness_score(learning_path)
        }
    
    def _calculate_effectiveness_score(self, learning_path: Dict) -> float:
        """Calculate overall effectiveness score for the learning path"""
        primary_video = learning_path.get('primary_video')
        if not primary_video:
            return 0.0
        
        base_score = primary_video.get('composite_score', 5.0)
        
        supplementary_videos = learning_path.get('supplementary_videos', [])
        if supplementary_videos:
            avg_supplementary_score = sum(v.get('composite_score', 5.0) for v in supplementary_videos) / len(supplementary_videos)
            base_score = (base_score * 0.7) + (avg_supplementary_score * 0.3)
        
        strategy = learning_path.get('learning_strategy', '')
        if strategy == 'comprehensive_primary':
            base_score += 0.5
        
        return min(10.0, base_score)


class LearningPathOptimizer:
    """Optimizes learning paths based on user preferences and constraints"""
    
    def __init__(self):
        self.time_constraints = {
            'quick': 60,      # 1 hour max
            'standard': 180,  # 3 hours max
            'comprehensive': 360  # 6 hours max
        }
    
    def optimize_for_time(self, learning_path: Dict, time_preference: str) -> Dict:
        """Optimize learning path based on time constraints"""
        max_time = self.time_constraints.get(time_preference, 180)
        
        primary_video = learning_path.get('primary_video')
        if not primary_video:
            return learning_path
        
        primary_duration = self._parse_duration_to_minutes(primary_video.get('duration', '0:00'))
        remaining_time = max_time - primary_duration
        
        if remaining_time <= 0:
            learning_path['supplementary_videos'] = []
            learning_path['coverage_analysis']['estimated_study_time'] = primary_duration
            return learning_path
        
        optimized_supplementary = []
        current_time = 0
        
        for video in learning_path.get('supplementary_videos', []):
            video_duration = self._parse_duration_to_minutes(video.get('duration', '0:00'))
            if current_time + video_duration <= remaining_time:
                optimized_supplementary.append(video)
                current_time += video_duration
            else:
                break
        
        learning_path['supplementary_videos'] = optimized_supplementary
        learning_path['coverage_analysis']['estimated_study_time'] = primary_duration + current_time
        
        return learning_path
    
    def optimize_for_difficulty(self, learning_path: Dict, difficulty_preference: str) -> Dict:
        """Optimize learning path based on difficulty preference"""
        if difficulty_preference == 'beginner':
            return self._filter_beginner_content(learning_path)
        elif difficulty_preference == 'advanced':
            return self._prioritize_advanced_content(learning_path)
        else:
            return learning_path
    
    def _filter_beginner_content(self, learning_path: Dict) -> Dict:
        """Filter content to focus on beginner-friendly materials"""
        supplementary_videos = learning_path.get('supplementary_videos', [])
        beginner_friendly = []
        
        for video in supplementary_videos:
            title_lower = video['title'].lower()
            if any(word in title_lower for word in ['beginner', 'intro', 'basics', 'fundamentals', 'getting started']):
                beginner_friendly.append(video)
            elif video.get('coverage_type') in ['quick_review', 'practice_examples']:
                beginner_friendly.append(video)
        
        learning_path['supplementary_videos'] = beginner_friendly[:3]
        return learning_path
    
    def _prioritize_advanced_content(self, learning_path: Dict) -> Dict:
        """Prioritize advanced content in the learning path"""
        supplementary_videos = learning_path.get('supplementary_videos', [])
        advanced_content = []
        other_content = []
        
        for video in supplementary_videos:
            if video.get('coverage_type') in ['deep_dive', 'comprehensive_alternative']:
                advanced_content.append(video)
            else:
                other_content.append(video)
        
        reordered = advanced_content + other_content
        learning_path['supplementary_videos'] = reordered[:3]
        return learning_path
    
    def _parse_duration_to_minutes(self, duration_str: str) -> int:
        """Parse duration string to minutes"""
        try:
            parts = duration_str.split(':')
            if len(parts) == 2:
                return int(parts[0])
            elif len(parts) == 3:
                return int(parts[0]) * 60 + int(parts[1])
            return 0
        except:
            return 0


class StudySessionPlanner:
    """Plans study sessions based on learning paths and user constraints"""
    
    def __init__(self):
        self.session_types = {
            'focused': 45,      # 45 minute focused sessions
            'standard': 60,     # 1 hour standard sessions
            'extended': 90      # 1.5 hour extended sessions
        }
    
    def create_session_plan(self, learning_path: Dict, session_type: str = 'standard') -> List[Dict]:
        """Create structured study session plan"""
        session_length = self.session_types.get(session_type, 60)
        sessions = []
        
        primary_video = learning_path.get('primary_video')
        if not primary_video:
            return sessions
        
        primary_duration = self._parse_duration_to_minutes(primary_video.get('duration', '0:00'))
        
        if primary_duration <= session_length:
            sessions.append({
                'session': 1,
                'type': 'foundation',
                'content': [primary_video],
                'duration': primary_duration,
                'objectives': ['Build foundational understanding', 'Take comprehensive notes']
            })
        else:
            num_sessions = (primary_duration + session_length - 1) // session_length
            for i in range(num_sessions):
                start_time = i * session_length
                end_time = min((i + 1) * session_length, primary_duration)
                sessions.append({
                    'session': i + 1,
                    'type': 'foundation',
                    'content': [f"{primary_video['title']} (Part {i + 1})"],
                    'duration': end_time - start_time,
                    'objectives': [f'Study minutes {start_time}-{end_time}', 'Take detailed notes']
                })
        
        current_session = len(sessions) + 1
        for video in learning_path.get('supplementary_videos', []):
            video_duration = self._parse_duration_to_minutes(video.get('duration', '0:00'))
            coverage_type = video.get('coverage_type', 'supplementary')
            
            sessions.append({
                'session': current_session,
                'type': coverage_type,
                'content': [video],
                'duration': video_duration,
                'objectives': self._get_session_objectives(coverage_type)
            })
            current_session += 1
        
        return sessions
    
    def _get_session_objectives(self, coverage_type: str) -> List[str]:
        """Get session objectives based on coverage type"""
        objectives_map = {
            'practice_examples': ['Work through examples', 'Practice similar problems'],
            'quick_review': ['Reinforce key concepts', 'Fill knowledge gaps'],
            'deep_dive': ['Master advanced concepts', 'Connect to foundation'],
            'practical_tutorial': ['Follow step-by-step', 'Implement solutions'],
            'concept_explanation': ['Understand alternative perspectives', 'Compare approaches']
        }
        return objectives_map.get(coverage_type, ['Study supplementary content', 'Take notes'])
    
    def _parse_duration_to_minutes(self, duration_str: str) -> int:
        """Parse duration string to minutes"""
        try:
            parts = duration_str.split(':')
            if len(parts) == 2:
                return int(parts[0])
            elif len(parts) == 3:
                return int(parts[0]) * 60 + int(parts[1])
            return 0
        except:
            return 0