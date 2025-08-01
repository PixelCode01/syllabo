from typing import Dict, List, Optional, Tuple
import json
from datetime import datetime
from .database import SyllaboDatabase
from .ai_client import AIClient
from .logger import SyllaboLogger

class ContentRecommender:
    """Intelligent content recommendation system"""
    
    def __init__(self, db: SyllaboDatabase = None, ai_client: AIClient = None):
        self.db = db or SyllaboDatabase()
        self.ai_client = ai_client or AIClient()
        self.logger = SyllaboLogger("content_recommender")
    
    async def get_personalized_recommendations(self, user_profile: Dict) -> List[Dict]:
        """Generate personalized content recommendations based on user profile"""
        learning_style = user_profile.get('learning_style', 'visual')
        difficulty_preference = user_profile.get('difficulty', 'intermediate')
        time_available = user_profile.get('study_time_minutes', 30)
        
        recommendations = []
        
        # Get topics that need review from spaced repetition system
        due_topics = self._get_due_topics()
        
        for topic_name in due_topics:
            content = self._find_optimal_content_offline(
                topic_name, learning_style, difficulty_preference, time_available
            )
            recommendations.append({
                'topic': topic_name,
                'content': content,
                'priority': self._calculate_priority_offline(topic_name),
                'estimated_time': self._estimate_study_time_offline(content)
            })
        
        return sorted(recommendations, key=lambda x: x['priority'], reverse=True)
    
    def _get_due_topics(self) -> List[str]:
        """Get topics that need review"""
        if hasattr(self, 'spaced_repetition') and self.spaced_repetition:
            due_items = self.spaced_repetition.get_due_topics()
            return [item.topic_name for item in due_items[:5]]
        else:
            # Return some default topics for demonstration
            return ['Python Basics', 'Data Structures', 'Algorithms']
    
    def _find_optimal_content_offline(self, topic: str, learning_style: str, 
                                    difficulty: str, time_available: int) -> List[Dict]:
        """Find optimal content without external APIs"""
        content = []
        
        # Content database organized by topic and learning style
        content_database = {
            'python': {
                'visual': [
                    {'type': 'video', 'title': 'Python Visual Tutorial', 'duration': 25, 'difficulty': 'beginner'},
                    {'type': 'infographic', 'title': 'Python Syntax Guide', 'duration': 10, 'difficulty': 'beginner'}
                ],
                'auditory': [
                    {'type': 'podcast', 'title': 'Python Explained', 'duration': 30, 'difficulty': 'intermediate'},
                    {'type': 'audio_book', 'title': 'Learn Python by Listening', 'duration': 45, 'difficulty': 'beginner'}
                ],
                'kinesthetic': [
                    {'type': 'interactive', 'title': 'Python Coding Exercise', 'duration': 20, 'difficulty': 'intermediate'},
                    {'type': 'project', 'title': 'Build a Python App', 'duration': 60, 'difficulty': 'advanced'}
                ]
            },
            'data structures': {
                'visual': [
                    {'type': 'animation', 'title': 'Data Structures Visualized', 'duration': 35, 'difficulty': 'intermediate'},
                    {'type': 'diagram', 'title': 'Tree and Graph Structures', 'duration': 15, 'difficulty': 'advanced'}
                ],
                'auditory': [
                    {'type': 'lecture', 'title': 'Data Structures Explained', 'duration': 40, 'difficulty': 'intermediate'}
                ],
                'kinesthetic': [
                    {'type': 'coding_challenge', 'title': 'Implement Data Structures', 'duration': 50, 'difficulty': 'advanced'}
                ]
            }
        }
        
        # Find matching content
        topic_key = topic.lower().replace(' ', '_')
        for key in content_database:
            if key in topic_key or topic_key in key:
                style_content = content_database[key].get(learning_style, [])
                
                # Filter by difficulty and time
                for item in style_content:
                    if (item['difficulty'] == difficulty or difficulty == 'any') and \
                       item['duration'] <= time_available:
                        content.append(item)
                
                break
        
        # If no specific content found, provide generic recommendations
        if not content:
            content = [
                {'type': 'tutorial', 'title': f'{topic} Tutorial', 'duration': min(30, time_available), 'difficulty': difficulty},
                {'type': 'practice', 'title': f'{topic} Exercises', 'duration': min(20, time_available), 'difficulty': difficulty}
            ]
        
        return content[:3]  # Return top 3 recommendations
    
    def _calculate_priority_offline(self, topic: str) -> float:
        """Calculate priority based on topic characteristics"""
        # Simple priority calculation based on topic name analysis
        priority_keywords = {
            'fundamental': 0.9,
            'basic': 0.8,
            'advanced': 0.6,
            'python': 0.85,
            'algorithm': 0.9,
            'data': 0.8
        }
        
        topic_lower = topic.lower()
        priority = 0.5  # Base priority
        
        for keyword, weight in priority_keywords.items():
            if keyword in topic_lower:
                priority = max(priority, weight)
        
        return priority
    
    def _estimate_study_time_offline(self, content: List[Dict]) -> int:
        """Estimate total study time for content"""
        return sum(item.get('duration', 20) for item in content)
    
    async def suggest_learning_path(self, syllabus_topics: List[str]) -> Dict:
        """Create an optimal learning path through syllabus topics"""
        # Analyze topic dependencies and create learning sequence
        dependencies = await self._analyze_topic_dependencies(syllabus_topics)
        
        learning_path = {
            'sequence': self._create_optimal_sequence(syllabus_topics, dependencies),
            'milestones': self._define_milestones(syllabus_topics),
            'estimated_timeline': self._estimate_completion_time(syllabus_topics),
            'prerequisite_map': dependencies
        }
        
        return learning_path
    
    def recommend_study_schedule(self, available_hours_per_week: int) -> Dict:
        """Generate optimal study schedule based on spaced repetition"""
        schedule = {
            'daily_sessions': [],
            'weekly_goals': [],
            'review_sessions': [],
            'break_recommendations': []
        }
        
        # Implementation would create personalized schedule
        return schedule
    
    async def find_alternative_resources(self, topic: str, 
                                       current_resource_id: str) -> List[Dict]:
        """Find alternative learning resources for a topic"""
        # Search for different types of content (videos, articles, courses)
        alternatives = []
        
        # Different learning modalities
        modalities = ['video', 'article', 'interactive', 'podcast', 'book']
        
        for modality in modalities:
            resources = await self._search_by_modality(topic, modality)
            alternatives.extend(resources)
        
        return alternatives[:10]  # Return top 10 alternatives