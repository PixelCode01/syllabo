"""
AI-Powered Learning Engine
Implements adaptive learning paths, intelligent analytics, and predictive learning features
"""

import json
import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, asdict
import statistics
from .ai_client import AIClient
from .database import SyllaboDatabase
from .logger import SyllaboLogger

@dataclass
class LearningProfile:
    """User's learning profile and preferences"""
    user_id: str
    learning_style: str  # visual, auditory, kinesthetic, reading
    current_level: str   # beginner, intermediate, advanced
    preferred_difficulty: float  # 0.0 to 1.0
    study_pace: str     # slow, normal, fast
    attention_span: int  # minutes
    optimal_study_times: List[str]  # time slots
    knowledge_areas: Dict[str, float]  # topic -> mastery level
    learning_goals: List[str]
    created_at: str
    updated_at: str

@dataclass
class ConceptNode:
    """Represents a learning concept with prerequisites and relationships"""
    concept_id: str
    name: str
    description: str
    difficulty_level: float  # 0.0 to 1.0
    prerequisites: List[str]  # concept_ids
    related_concepts: List[str]
    estimated_time: int  # minutes to master
    mastery_threshold: float  # 0.0 to 1.0
    content_types: List[str]  # video, text, quiz, practice

@dataclass
class LearningPath:
    """Adaptive learning path for a user"""
    path_id: str
    user_id: str
    goal: str
    concepts: List[ConceptNode]
    current_position: int
    estimated_completion: str
    difficulty_progression: List[float]
    created_at: str
    updated_at: str

@dataclass
class PerformanceMetrics:
    """Tracks user performance and learning analytics"""
    user_id: str
    concept_id: str
    attempts: int
    successes: int
    avg_score: float
    time_spent: int  # minutes
    last_attempt: str
    mastery_level: float  # 0.0 to 1.0
    retention_rate: float
    learning_velocity: float  # concepts per day

class AILearningEngine:
    """Main AI learning engine with adaptive capabilities"""
    
    def __init__(self, ai_client: AIClient = None, db: SyllaboDatabase = None):
        self.ai_client = ai_client or AIClient()
        self.db = db or SyllaboDatabase()
        self.logger = SyllaboLogger("ai_learning_engine")
        
        # Data storage paths
        self.data_dir = "data/ai_learning"
        os.makedirs(self.data_dir, exist_ok=True)
        
        self.profiles_file = os.path.join(self.data_dir, "learning_profiles.json")
        self.paths_file = os.path.join(self.data_dir, "learning_paths.json")
        self.metrics_file = os.path.join(self.data_dir, "performance_metrics.json")
        self.concepts_file = os.path.join(self.data_dir, "concept_graph.json")
        
        # Load existing data
        self.learning_profiles: Dict[str, LearningProfile] = self._load_profiles()
        self.learning_paths: Dict[str, LearningPath] = self._load_paths()
        self.performance_metrics: Dict[str, PerformanceMetrics] = self._load_metrics()
        self.concept_graph: Dict[str, ConceptNode] = self._load_concepts()
    
    def _load_profiles(self) -> Dict[str, LearningProfile]:
        """Load learning profiles from file"""
        if os.path.exists(self.profiles_file):
            try:
                with open(self.profiles_file, 'r') as f:
                    data = json.load(f)
                    return {
                        uid: LearningProfile(**profile_data)
                        for uid, profile_data in data.items()
                    }
            except Exception as e:
                self.logger.error(f"Error loading profiles: {e}")
        return {}
    
    def _load_paths(self) -> Dict[str, LearningPath]:
        """Load learning paths from file"""
        if os.path.exists(self.paths_file):
            try:
                with open(self.paths_file, 'r') as f:
                    data = json.load(f)
                    paths = {}
                    for path_id, path_data in data.items():
                        # Convert concept data back to ConceptNode objects
                        concepts = [ConceptNode(**c) for c in path_data['concepts']]
                        path_data['concepts'] = concepts
                        paths[path_id] = LearningPath(**path_data)
                    return paths
            except Exception as e:
                self.logger.error(f"Error loading paths: {e}")
        return {}
    
    def _load_metrics(self) -> Dict[str, PerformanceMetrics]:
        """Load performance metrics from file"""
        if os.path.exists(self.metrics_file):
            try:
                with open(self.metrics_file, 'r') as f:
                    data = json.load(f)
                    return {
                        key: PerformanceMetrics(**metrics_data)
                        for key, metrics_data in data.items()
                    }
            except Exception as e:
                self.logger.error(f"Error loading metrics: {e}")
        return {}
    
    def _load_concepts(self) -> Dict[str, ConceptNode]:
        """Load concept graph from file"""
        if os.path.exists(self.concepts_file):
            try:
                with open(self.concepts_file, 'r') as f:
                    data = json.load(f)
                    return {
                        concept_id: ConceptNode(**concept_data)
                        for concept_id, concept_data in data.items()
                    }
            except Exception as e:
                self.logger.error(f"Error loading concepts: {e}")
        return {}
    
    def save_data(self):
        """Save all data to files"""
        try:
            # Save profiles
            with open(self.profiles_file, 'w') as f:
                json.dump({
                    uid: asdict(profile) 
                    for uid, profile in self.learning_profiles.items()
                }, f, indent=2)
            
            # Save paths
            with open(self.paths_file, 'w') as f:
                paths_data = {}
                for path_id, path in self.learning_paths.items():
                    path_dict = asdict(path)
                    # Convert ConceptNode objects to dicts
                    path_dict['concepts'] = [asdict(c) for c in path.concepts]
                    paths_data[path_id] = path_dict
                json.dump(paths_data, f, indent=2)
            
            # Save metrics
            with open(self.metrics_file, 'w') as f:
                json.dump({
                    key: asdict(metrics)
                    for key, metrics in self.performance_metrics.items()
                }, f, indent=2)
            
            # Save concepts
            with open(self.concepts_file, 'w') as f:
                json.dump({
                    concept_id: asdict(concept)
                    for concept_id, concept in self.concept_graph.items()
                }, f, indent=2)
                
        except Exception as e:
            self.logger.error(f"Error saving data: {e}")
    
    async def create_learning_profile(self, user_id: str, 
                                    initial_assessment: Dict[str, Any]) -> LearningProfile:
        """Create a learning profile based on initial assessment"""
        try:
            # Analyze learning style from assessment
            learning_style = await self._analyze_learning_style(initial_assessment)
            
            # Determine current level
            current_level = self._assess_current_level(initial_assessment)
            
            # Create profile
            profile = LearningProfile(
                user_id=user_id,
                learning_style=learning_style,
                current_level=current_level,
                preferred_difficulty=initial_assessment.get('difficulty_preference', 0.5),
                study_pace=initial_assessment.get('study_pace', 'normal'),
                attention_span=initial_assessment.get('attention_span', 30),
                optimal_study_times=initial_assessment.get('study_times', ['morning']),
                knowledge_areas={},
                learning_goals=initial_assessment.get('goals', []),
                created_at=datetime.now().isoformat(),
                updated_at=datetime.now().isoformat()
            )
            
            self.learning_profiles[user_id] = profile
            self.save_data()
            
            return profile
            
        except Exception as e:
            self.logger.error(f"Error creating learning profile: {e}")
            raise
    
    async def _analyze_learning_style(self, assessment: Dict[str, Any]) -> str:
        """Use AI to analyze learning style from assessment responses"""
        try:
            prompt = f"""
            Analyze this learning assessment and determine the primary learning style:
            
            Assessment responses: {json.dumps(assessment, indent=2)}
            
            Based on the responses, classify the learning style as one of:
            - visual: prefers diagrams, charts, visual aids
            - auditory: prefers lectures, discussions, audio content
            - kinesthetic: prefers hands-on practice, interactive exercises
            - reading: prefers text-based learning, written materials
            
            Respond with just the learning style name.
            """
            
            response = await self.ai_client.get_completion(prompt)
            style = response.strip().lower()
            
            if style in ['visual', 'auditory', 'kinesthetic', 'reading']:
                return style
            else:
                return 'visual'  # default
                
        except Exception as e:
            self.logger.error(f"Error analyzing learning style: {e}")
            return 'visual'  # default fallback
    
    def _assess_current_level(self, assessment: Dict[str, Any]) -> str:
        """Assess current knowledge level from assessment"""
        score = assessment.get('knowledge_score', 0.5)
        
        if score < 0.3:
            return 'beginner'
        elif score < 0.7:
            return 'intermediate'
        else:
            return 'advanced'
    
    async def generate_adaptive_learning_path(self, user_id: str, 
                                            subject: str, 
                                            topics: List[str]) -> LearningPath:
        """Generate an adaptive learning path for a user"""
        try:
            profile = self.learning_profiles.get(user_id)
            if not profile:
                raise ValueError(f"No learning profile found for user {user_id}")
            
            # Build concept graph for the subject
            concepts = await self._build_concept_graph(subject, topics, profile)
            
            # Order concepts based on prerequisites and difficulty
            ordered_concepts = self._order_concepts_by_prerequisites(concepts)
            
            # Adjust difficulty progression based on user profile
            difficulty_progression = self._calculate_difficulty_progression(
                ordered_concepts, profile
            )
            
            # Create learning path
            path_id = f"{user_id}_{subject}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            
            path = LearningPath(
                path_id=path_id,
                user_id=user_id,
                goal=f"Master {subject}",
                concepts=ordered_concepts,
                current_position=0,
                estimated_completion=self._estimate_completion_time(
                    ordered_concepts, profile
                ),
                difficulty_progression=difficulty_progression,
                created_at=datetime.now().isoformat(),
                updated_at=datetime.now().isoformat()
            )
            
            self.learning_paths[path_id] = path
            self.save_data()
            
            return path
            
        except Exception as e:
            self.logger.error(f"Error generating learning path: {e}")
            raise
    
    async def _build_concept_graph(self, subject: str, topics: List[str], 
                                 profile: LearningProfile) -> List[ConceptNode]:
        """Build a concept graph with prerequisites using AI"""
        try:
            prompt = f"""
            Create a learning concept graph for the subject "{subject}" with these topics:
            {json.dumps(topics, indent=2)}
            
            For each topic, identify:
            1. Prerequisites (what must be learned first)
            2. Difficulty level (0.0 to 1.0)
            3. Estimated learning time in minutes
            4. Related concepts
            
            User profile:
            - Learning style: {profile.learning_style}
            - Current level: {profile.current_level}
            - Preferred difficulty: {profile.preferred_difficulty}
            
            Respond with JSON in this format:
            {{
                "concepts": [
                    {{
                        "concept_id": "unique_id",
                        "name": "Topic Name",
                        "description": "Brief description",
                        "difficulty_level": 0.5,
                        "prerequisites": ["prerequisite_id1", "prerequisite_id2"],
                        "related_concepts": ["related_id1"],
                        "estimated_time": 45,
                        "mastery_threshold": 0.8,
                        "content_types": ["video", "quiz", "practice"]
                    }}
                ]
            }}
            """
            
            response = await self.ai_client.get_completion(prompt)
            
            try:
                data = json.loads(response)
                concepts = []
                
                for concept_data in data.get('concepts', []):
                    concept = ConceptNode(
                        concept_id=concept_data.get('concept_id', ''),
                        name=concept_data.get('name', ''),
                        description=concept_data.get('description', ''),
                        difficulty_level=concept_data.get('difficulty_level', 0.5),
                        prerequisites=concept_data.get('prerequisites', []),
                        related_concepts=concept_data.get('related_concepts', []),
                        estimated_time=concept_data.get('estimated_time', 30),
                        mastery_threshold=concept_data.get('mastery_threshold', 0.8),
                        content_types=concept_data.get('content_types', ['video', 'quiz'])
                    )
                    concepts.append(concept)
                    
                    # Add to concept graph
                    self.concept_graph[concept.concept_id] = concept
                
                return concepts
                
            except json.JSONDecodeError:
                self.logger.error("Failed to parse AI response for concept graph")
                return self._create_fallback_concepts(topics)
                
        except Exception as e:
            self.logger.error(f"Error building concept graph: {e}")
            return self._create_fallback_concepts(topics)
    
    def _create_fallback_concepts(self, topics: List[str]) -> List[ConceptNode]:
        """Create fallback concepts when AI fails"""
        concepts = []
        for i, topic in enumerate(topics):
            concept = ConceptNode(
                concept_id=f"concept_{i}",
                name=topic,
                description=f"Learn about {topic}",
                difficulty_level=0.5,
                prerequisites=[f"concept_{i-1}"] if i > 0 else [],
                related_concepts=[],
                estimated_time=30,
                mastery_threshold=0.8,
                content_types=['video', 'quiz']
            )
            concepts.append(concept)
            self.concept_graph[concept.concept_id] = concept
        
        return concepts
    
    def _order_concepts_by_prerequisites(self, concepts: List[ConceptNode]) -> List[ConceptNode]:
        """Order concepts based on prerequisites using topological sort"""
        # Create adjacency list
        graph = {concept.concept_id: concept.prerequisites for concept in concepts}
        concept_map = {concept.concept_id: concept for concept in concepts}
        
        # Topological sort
        visited = set()
        temp_visited = set()
        ordered = []
        
        def visit(concept_id):
            if concept_id in temp_visited:
                return  # Cycle detected, skip
            if concept_id in visited:
                return
            
            temp_visited.add(concept_id)
            
            for prereq in graph.get(concept_id, []):
                if prereq in concept_map:
                    visit(prereq)
            
            temp_visited.remove(concept_id)
            visited.add(concept_id)
            
            if concept_id in concept_map:
                ordered.append(concept_map[concept_id])
        
        for concept in concepts:
            if concept.concept_id not in visited:
                visit(concept.concept_id)
        
        return ordered
    
    def _calculate_difficulty_progression(self, concepts: List[ConceptNode], 
                                        profile: LearningProfile) -> List[float]:
        """Calculate difficulty progression based on user profile"""
        base_difficulties = [concept.difficulty_level for concept in concepts]
        
        # Adjust based on user preferences
        adjustment_factor = profile.preferred_difficulty - 0.5  # -0.5 to 0.5
        
        adjusted_difficulties = []
        for i, base_diff in enumerate(base_difficulties):
            # Gradual increase with user preference adjustment
            progression_factor = i / len(base_difficulties) * 0.3  # Max 30% increase
            adjusted_diff = base_diff + adjustment_factor + progression_factor
            adjusted_diff = max(0.1, min(1.0, adjusted_diff))  # Clamp to valid range
            adjusted_difficulties.append(adjusted_diff)
        
        return adjusted_difficulties
    
    def _estimate_completion_time(self, concepts: List[ConceptNode], 
                                profile: LearningProfile) -> str:
        """Estimate completion time based on concepts and user profile"""
        total_minutes = sum(concept.estimated_time for concept in concepts)
        
        # Adjust based on study pace
        pace_multipliers = {'slow': 1.5, 'normal': 1.0, 'fast': 0.7}
        multiplier = pace_multipliers.get(profile.study_pace, 1.0)
        
        adjusted_minutes = total_minutes * multiplier
        days = adjusted_minutes / (profile.attention_span * 2)  # Assume 2 sessions per day
        
        completion_date = datetime.now() + timedelta(days=days)
        return completion_date.isoformat()
    
    async def get_next_learning_activity(self, user_id: str, path_id: str) -> Dict[str, Any]:
        """Get the next recommended learning activity"""
        try:
            path = self.learning_paths.get(path_id)
            profile = self.learning_profiles.get(user_id)
            
            if not path or not profile:
                raise ValueError("Path or profile not found")
            
            if path.current_position >= len(path.concepts):
                return {"status": "completed", "message": "Learning path completed!"}
            
            current_concept = path.concepts[path.current_position]
            
            # Check if prerequisites are met
            if not self._prerequisites_met(current_concept, user_id):
                return {
                    "status": "blocked",
                    "message": "Prerequisites not met",
                    "missing_prerequisites": self._get_missing_prerequisites(current_concept, user_id)
                }
            
            # Get performance metrics for adaptive questioning
            metrics_key = f"{user_id}_{current_concept.concept_id}"
            metrics = self.performance_metrics.get(metrics_key)
            
            # Determine activity type based on learning style and progress
            activity = await self._select_optimal_activity(current_concept, profile, metrics)
            
            return {
                "status": "ready",
                "concept": asdict(current_concept),
                "activity": activity,
                "progress": {
                    "current": path.current_position + 1,
                    "total": len(path.concepts),
                    "percentage": ((path.current_position + 1) / len(path.concepts)) * 100
                }
            }
            
        except Exception as e:
            self.logger.error(f"Error getting next activity: {e}")
            raise
    
    def _prerequisites_met(self, concept: ConceptNode, user_id: str) -> bool:
        """Check if all prerequisites for a concept are met"""
        for prereq_id in concept.prerequisites:
            metrics_key = f"{user_id}_{prereq_id}"
            metrics = self.performance_metrics.get(metrics_key)
            
            if not metrics or metrics.mastery_level < 0.7:
                return False
        
        return True
    
    def _get_missing_prerequisites(self, concept: ConceptNode, user_id: str) -> List[str]:
        """Get list of missing prerequisites"""
        missing = []
        for prereq_id in concept.prerequisites:
            metrics_key = f"{user_id}_{prereq_id}"
            metrics = self.performance_metrics.get(metrics_key)
            
            if not metrics or metrics.mastery_level < 0.7:
                prereq_concept = self.concept_graph.get(prereq_id)
                if prereq_concept:
                    missing.append(prereq_concept.name)
        
        return missing
    
    async def _select_optimal_activity(self, concept: ConceptNode, 
                                     profile: LearningProfile, 
                                     metrics: Optional[PerformanceMetrics]) -> Dict[str, Any]:
        """Select optimal learning activity based on profile and performance"""
        # Determine activity type based on learning style
        style_preferences = {
            'visual': ['video', 'diagram', 'infographic'],
            'auditory': ['podcast', 'lecture', 'discussion'],
            'kinesthetic': ['practice', 'simulation', 'hands_on'],
            'reading': ['article', 'textbook', 'documentation']
        }
        
        preferred_types = style_preferences.get(profile.learning_style, ['video'])
        
        # Select activity type that matches both concept and preference
        available_types = concept.content_types
        activity_type = next((t for t in preferred_types if t in available_types), available_types[0])
        
        # Adjust difficulty based on performance
        difficulty = concept.difficulty_level
        if metrics:
            if metrics.avg_score < 0.6:
                difficulty = max(0.1, difficulty - 0.2)  # Make easier
            elif metrics.avg_score > 0.9:
                difficulty = min(1.0, difficulty + 0.2)  # Make harder
        
        return {
            "type": activity_type,
            "concept_id": concept.concept_id,
            "concept_name": concept.name,
            "description": concept.description,
            "difficulty": difficulty,
            "estimated_time": concept.estimated_time,
            "mastery_threshold": concept.mastery_threshold
        }
    
    def record_performance(self, user_id: str, concept_id: str, 
                          score: float, time_spent: int, success: bool):
        """Record user performance for analytics and adaptation"""
        metrics_key = f"{user_id}_{concept_id}"
        
        if metrics_key in self.performance_metrics:
            metrics = self.performance_metrics[metrics_key]
            metrics.attempts += 1
            if success:
                metrics.successes += 1
            
            # Update running averages
            metrics.avg_score = (metrics.avg_score * (metrics.attempts - 1) + score) / metrics.attempts
            metrics.time_spent += time_spent
            metrics.last_attempt = datetime.now().isoformat()
            
            # Calculate mastery level
            metrics.mastery_level = min(1.0, (metrics.successes / metrics.attempts) * (score / 100))
            
        else:
            # Create new metrics
            metrics = PerformanceMetrics(
                user_id=user_id,
                concept_id=concept_id,
                attempts=1,
                successes=1 if success else 0,
                avg_score=score,
                time_spent=time_spent,
                last_attempt=datetime.now().isoformat(),
                mastery_level=score / 100 if success else 0.0,
                retention_rate=1.0,
                learning_velocity=1.0
            )
            
            self.performance_metrics[metrics_key] = metrics
        
        self.save_data()
    
    def get_learning_analytics(self, user_id: str) -> Dict[str, Any]:
        """Get comprehensive learning analytics for a user"""
        try:
            profile = self.learning_profiles.get(user_id)
            if not profile:
                return {"error": "User profile not found"}
            
            # Get all user metrics
            user_metrics = [
                metrics for key, metrics in self.performance_metrics.items()
                if key.startswith(f"{user_id}_")
            ]
            
            if not user_metrics:
                return {"message": "No learning data available yet"}
            
            # Calculate analytics
            total_concepts = len(user_metrics)
            mastered_concepts = len([m for m in user_metrics if m.mastery_level >= 0.8])
            avg_score = sum(m.avg_score for m in user_metrics) / total_concepts
            total_time = sum(m.time_spent for m in user_metrics)
            
            # Learning velocity (concepts mastered per day)
            if user_metrics:
                first_attempt = min(datetime.fromisoformat(m.last_attempt) for m in user_metrics)
                days_learning = (datetime.now() - first_attempt).days or 1
                learning_velocity = mastered_concepts / days_learning
            else:
                learning_velocity = 0
            
            # Identify strengths and weaknesses
            strengths = []
            weaknesses = []
            
            for metrics in user_metrics:
                concept = self.concept_graph.get(metrics.concept_id)
                if concept:
                    if metrics.mastery_level >= 0.8:
                        strengths.append(concept.name)
                    elif metrics.mastery_level < 0.5:
                        weaknesses.append(concept.name)
            
            return {
                "user_id": user_id,
                "learning_profile": asdict(profile),
                "progress_summary": {
                    "total_concepts": total_concepts,
                    "mastered_concepts": mastered_concepts,
                    "mastery_percentage": (mastered_concepts / total_concepts) * 100 if total_concepts > 0 else 0,
                    "average_score": avg_score,
                    "total_study_time": total_time,
                    "learning_velocity": learning_velocity
                },
                "strengths": strengths[:5],  # Top 5
                "weaknesses": weaknesses[:5],  # Top 5
                "recommendations": self._generate_recommendations(user_metrics, profile)
            }
            
        except Exception as e:
            self.logger.error(f"Error generating analytics: {e}")
            return {"error": str(e)}
    
    def _generate_recommendations(self, metrics: List[PerformanceMetrics], 
                                profile: LearningProfile) -> List[str]:
        """Generate personalized learning recommendations"""
        recommendations = []
        
        # Analyze performance patterns
        weak_areas = [m for m in metrics if m.mastery_level < 0.5]
        strong_areas = [m for m in metrics if m.mastery_level >= 0.8]
        
        if weak_areas:
            recommendations.append(f"Focus on reviewing {len(weak_areas)} concepts with low mastery")
        
        if len(strong_areas) > len(weak_areas):
            recommendations.append("Consider advancing to more challenging topics")
        
        # Time-based recommendations
        avg_time_per_concept = sum(m.time_spent for m in metrics) / len(metrics) if metrics else 0
        if avg_time_per_concept > profile.attention_span:
            recommendations.append("Consider breaking study sessions into smaller chunks")
        
        # Learning style recommendations
        if profile.learning_style == 'visual':
            recommendations.append("Seek out more visual learning materials like diagrams and videos")
        elif profile.learning_style == 'kinesthetic':
            recommendations.append("Look for hands-on practice opportunities and interactive exercises")
        
        return recommendations[:5]  # Limit to top 5 recommendations
    
    async def predict_performance(self, user_id: str, concept_id: str) -> Dict[str, Any]:
        """Predict user performance on a concept using ML-like analysis"""
        try:
            profile = self.learning_profiles.get(user_id)
            concept = self.concept_graph.get(concept_id)
            
            if not profile or not concept:
                return {"error": "Profile or concept not found"}
            
            # Get historical performance
            user_metrics = [
                metrics for key, metrics in self.performance_metrics.items()
                if key.startswith(f"{user_id}_")
            ]
            
            if not user_metrics:
                # No history, use profile-based prediction
                base_score = 70 if profile.current_level == 'beginner' else 80 if profile.current_level == 'intermediate' else 90
                difficulty_adjustment = (1 - concept.difficulty_level) * 20
                predicted_score = base_score + difficulty_adjustment
                
                return {
                    "predicted_score": max(0, min(100, predicted_score)),
                    "confidence": 0.3,  # Low confidence without history
                    "estimated_time": concept.estimated_time,
                    "success_probability": predicted_score / 100,
                    "difficulty_rating": concept.difficulty_level
                }
            
            # Calculate prediction based on historical performance
            avg_performance = sum(m.avg_score for m in user_metrics) / len(user_metrics)
            
            # Adjust for concept difficulty
            difficulty_factor = 1 - (concept.difficulty_level - 0.5) * 0.4
            predicted_score = avg_performance * difficulty_factor
            
            # Check prerequisite mastery
            prereq_mastery = 1.0
            for prereq_id in concept.prerequisites:
                metrics_key = f"{user_id}_{prereq_id}"
                prereq_metrics = self.performance_metrics.get(metrics_key)
                if prereq_metrics:
                    prereq_mastery *= prereq_metrics.mastery_level
            
            predicted_score *= (0.7 + 0.3 * prereq_mastery)  # Prerequisite impact
            
            # Estimate time based on user's historical pace
            avg_time_per_concept = sum(m.time_spent for m in user_metrics) / len(user_metrics)
            time_adjustment = concept.difficulty_level * 1.5
            estimated_time = int(avg_time_per_concept * time_adjustment)
            
            return {
                "predicted_score": max(0, min(100, predicted_score)),
                "confidence": min(0.9, len(user_metrics) / 10),  # Higher confidence with more data
                "estimated_time": estimated_time,
                "success_probability": predicted_score / 100,
                "difficulty_rating": concept.difficulty_level,
                "prerequisite_readiness": prereq_mastery
            }
            
        except Exception as e:
            self.logger.error(f"Error predicting performance: {e}")
            return {"error": str(e)}