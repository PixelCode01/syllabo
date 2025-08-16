"""
Predictive Learning Intelligence
Advanced ML-like predictions for learning outcomes, time estimation, and success probability
"""

import json
import os
import math
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, asdict
import statistics
from .ai_client import AIClient
from .database import SyllaboDatabase
from .logger import SyllaboLogger

@dataclass
class LearningPrediction:
    """Learning outcome prediction"""
    user_id: str
    concept_id: str
    prediction_type: str  # performance, time, success, difficulty
    predicted_value: float
    confidence_score: float  # 0.0 to 1.0
    factors_considered: List[str]
    prediction_date: str
    actual_outcome: Optional[float] = None
    accuracy_score: Optional[float] = None

@dataclass
class UserLearningModel:
    """User-specific learning model parameters"""
    user_id: str
    learning_rate: float  # How quickly user learns new concepts
    retention_factor: float  # How well user retains information
    difficulty_tolerance: float  # User's ability to handle difficult concepts
    consistency_factor: float  # How consistent user's performance is
    motivation_level: float  # Current motivation/engagement level
    cognitive_load_capacity: float  # How much information user can process
    preferred_learning_modalities: List[str]
    historical_accuracy: float  # How accurate our predictions have been
    model_confidence: float  # Overall confidence in this user's model
    last_updated: str

@dataclass
class ConceptDifficultyModel:
    """Model for concept difficulty and learning requirements"""
    concept_id: str
    base_difficulty: float  # Inherent difficulty of the concept
    prerequisite_complexity: float  # Complexity of prerequisites
    cognitive_load: float  # Mental effort required
    typical_learning_time: int  # Average time to master (minutes)
    success_rate: float  # Historical success rate across users
    common_misconceptions: List[str]
    effective_learning_strategies: List[str]
    difficulty_factors: Dict[str, float]

class PredictiveLearningIntelligence:
    """Advanced predictive system for learning outcomes"""
    
    def __init__(self, ai_client: AIClient = None, db: SyllaboDatabase = None):
        self.ai_client = ai_client or AIClient()
        self.db = db or SyllaboDatabase()
        self.logger = SyllaboLogger("predictive_learning")
        
        # Data storage
        self.data_dir = "data/predictive_learning"
        os.makedirs(self.data_dir, exist_ok=True)
        
        self.predictions_file = os.path.join(self.data_dir, "predictions.json")
        self.user_models_file = os.path.join(self.data_dir, "user_models.json")
        self.concept_models_file = os.path.join(self.data_dir, "concept_models.json")
        
        # Load data
        self.predictions: List[LearningPrediction] = self._load_predictions()
        self.user_models: Dict[str, UserLearningModel] = self._load_user_models()
        self.concept_models: Dict[str, ConceptDifficultyModel] = self._load_concept_models()
        
        # Model parameters
        self.confidence_threshold = 0.7
        self.prediction_horizon_days = 30
        self.model_update_frequency = 5  # Update after every 5 predictions
    
    def _load_predictions(self) -> List[LearningPrediction]:
        """Load prediction history from file"""
        if os.path.exists(self.predictions_file):
            try:
                with open(self.predictions_file, 'r') as f:
                    data = json.load(f)
                    return [LearningPrediction(**pred_data) for pred_data in data]
            except Exception as e:
                self.logger.error(f"Error loading predictions: {e}")
        return []
    
    def _load_user_models(self) -> Dict[str, UserLearningModel]:
        """Load user learning models from file"""
        if os.path.exists(self.user_models_file):
            try:
                with open(self.user_models_file, 'r') as f:
                    data = json.load(f)
                    return {
                        user_id: UserLearningModel(**model_data)
                        for user_id, model_data in data.items()
                    }
            except Exception as e:
                self.logger.error(f"Error loading user models: {e}")
        return {}
    
    def _load_concept_models(self) -> Dict[str, ConceptDifficultyModel]:
        """Load concept difficulty models from file"""
        if os.path.exists(self.concept_models_file):
            try:
                with open(self.concept_models_file, 'r') as f:
                    data = json.load(f)
                    return {
                        concept_id: ConceptDifficultyModel(**model_data)
                        for concept_id, model_data in data.items()
                    }
            except Exception as e:
                self.logger.error(f"Error loading concept models: {e}")
        return {}
    
    def save_data(self):
        """Save all predictive data to files"""
        try:
            # Save predictions
            with open(self.predictions_file, 'w') as f:
                json.dump([asdict(pred) for pred in self.predictions], f, indent=2)
            
            # Save user models
            with open(self.user_models_file, 'w') as f:
                json.dump({
                    user_id: asdict(model)
                    for user_id, model in self.user_models.items()
                }, f, indent=2)
            
            # Save concept models
            with open(self.concept_models_file, 'w') as f:
                json.dump({
                    concept_id: asdict(model)
                    for concept_id, model in self.concept_models.items()
                }, f, indent=2)
                
        except Exception as e:
            self.logger.error(f"Error saving predictive data: {e}")
    
    async def build_user_learning_model(self, user_id: str, 
                                      historical_data: Dict[str, Any]) -> UserLearningModel:
        """Build or update a user's learning model based on historical data"""
        try:
            # Extract features from historical data
            quiz_scores = historical_data.get('quiz_scores', [])
            study_times = historical_data.get('study_times', [])
            concept_masteries = historical_data.get('concept_masteries', [])
            session_data = historical_data.get('sessions', [])
            
            # Calculate learning rate (improvement over time)
            learning_rate = self._calculate_learning_rate(quiz_scores)
            
            # Calculate retention factor (how well knowledge is retained)
            retention_factor = self._calculate_retention_factor(concept_masteries)
            
            # Calculate difficulty tolerance (performance on hard concepts)
            difficulty_tolerance = self._calculate_difficulty_tolerance(historical_data)
            
            # Calculate consistency factor (variance in performance)
            consistency_factor = self._calculate_consistency_factor(quiz_scores)
            
            # Estimate motivation level (engagement trends)
            motivation_level = self._estimate_motivation_level(session_data)
            
            # Estimate cognitive load capacity
            cognitive_load_capacity = self._estimate_cognitive_load_capacity(study_times, quiz_scores)
            
            # Determine preferred learning modalities
            preferred_modalities = self._analyze_learning_modalities(historical_data)
            
            # Calculate historical prediction accuracy if we have previous predictions
            historical_accuracy = self._calculate_prediction_accuracy(user_id)
            
            # Calculate overall model confidence
            data_points = len(quiz_scores) + len(study_times) + len(concept_masteries)
            model_confidence = min(1.0, data_points / 50)  # Full confidence at 50+ data points
            
            model = UserLearningModel(
                user_id=user_id,
                learning_rate=learning_rate,
                retention_factor=retention_factor,
                difficulty_tolerance=difficulty_tolerance,
                consistency_factor=consistency_factor,
                motivation_level=motivation_level,
                cognitive_load_capacity=cognitive_load_capacity,
                preferred_learning_modalities=preferred_modalities,
                historical_accuracy=historical_accuracy,
                model_confidence=model_confidence,
                last_updated=datetime.now().isoformat()
            )
            
            self.user_models[user_id] = model
            self.save_data()
            
            return model
            
        except Exception as e:
            self.logger.error(f"Error building user model: {e}")
            raise
    
    def _calculate_learning_rate(self, quiz_scores: List[float]) -> float:
        """Calculate how quickly the user learns (improvement rate)"""
        if len(quiz_scores) < 3:
            return 0.5  # Default moderate learning rate
        
        # Calculate trend in scores over time
        improvements = []
        for i in range(1, len(quiz_scores)):
            improvement = quiz_scores[i] - quiz_scores[i-1]
            improvements.append(improvement)
        
        avg_improvement = statistics.mean(improvements) if improvements else 0
        
        # Normalize to 0-1 scale
        # Positive improvements indicate faster learning
        learning_rate = 0.5 + (avg_improvement / 100)  # Assuming scores are 0-100
        return max(0.1, min(1.0, learning_rate))
    
    def _calculate_retention_factor(self, concept_masteries: List[Dict[str, Any]]) -> float:
        """Calculate how well the user retains learned information"""
        if not concept_masteries:
            return 0.7  # Default good retention
        
        retention_scores = []
        for mastery in concept_masteries:
            initial_score = mastery.get('initial_score', 0)
            current_score = mastery.get('current_score', 0)
            
            if initial_score > 0:
                retention = current_score / initial_score
                retention_scores.append(min(1.0, retention))  # Cap at 1.0
        
        return statistics.mean(retention_scores) if retention_scores else 0.7
    
    def _calculate_difficulty_tolerance(self, historical_data: Dict[str, Any]) -> float:
        """Calculate user's ability to handle difficult concepts"""
        difficult_concept_scores = []
        
        # Look for performance on concepts marked as difficult
        for concept_data in historical_data.get('concept_performances', []):
            difficulty = concept_data.get('difficulty_level', 0.5)
            score = concept_data.get('score', 0)
            
            if difficulty > 0.7:  # Consider concepts with difficulty > 0.7 as hard
                difficult_concept_scores.append(score)
        
        if not difficult_concept_scores:
            return 0.5  # Default moderate tolerance
        
        avg_difficult_score = statistics.mean(difficult_concept_scores)
        return avg_difficult_score / 100  # Normalize to 0-1
    
    def _calculate_consistency_factor(self, quiz_scores: List[float]) -> float:
        """Calculate how consistent the user's performance is"""
        if len(quiz_scores) < 3:
            return 0.5  # Default moderate consistency
        
        # Lower standard deviation indicates higher consistency
        std_dev = statistics.stdev(quiz_scores)
        
        # Normalize: lower std_dev = higher consistency
        # Assuming scores range 0-100, std_dev of 0 = perfect consistency (1.0)
        # std_dev of 50 = very inconsistent (0.0)
        consistency = 1.0 - (std_dev / 50)
        return max(0.0, min(1.0, consistency))
    
    def _estimate_motivation_level(self, session_data: List[Dict[str, Any]]) -> float:
        """Estimate current motivation level based on recent engagement"""
        if not session_data:
            return 0.7  # Default good motivation
        
        # Look at recent sessions (last 10)
        recent_sessions = session_data[-10:] if len(session_data) > 10 else session_data
        
        engagement_scores = []
        for session in recent_sessions:
            engagement = session.get('engagement_level', 0.7)
            duration = session.get('duration_minutes', 30)
            
            # Longer sessions with high engagement indicate higher motivation
            motivation_score = engagement * min(1.0, duration / 60)  # Cap at 1 hour
            engagement_scores.append(motivation_score)
        
        return statistics.mean(engagement_scores) if engagement_scores else 0.7
    
    def _estimate_cognitive_load_capacity(self, study_times: List[int], 
                                        quiz_scores: List[float]) -> float:
        """Estimate how much cognitive load the user can handle"""
        if not study_times or not quiz_scores:
            return 0.6  # Default moderate capacity
        
        # Users with higher cognitive load capacity can maintain performance
        # even with longer study sessions
        
        # Correlate study time with performance
        if len(study_times) != len(quiz_scores):
            return 0.6
        
        # Calculate performance efficiency (score per minute of study)
        efficiencies = []
        for time, score in zip(study_times, quiz_scores):
            if time > 0:
                efficiency = score / time
                efficiencies.append(efficiency)
        
        if not efficiencies:
            return 0.6
        
        avg_efficiency = statistics.mean(efficiencies)
        
        # Normalize efficiency to 0-1 scale
        # Higher efficiency suggests higher cognitive load capacity
        capacity = min(1.0, avg_efficiency * 10)  # Adjust scaling as needed
        return max(0.1, capacity)
    
    def _analyze_learning_modalities(self, historical_data: Dict[str, Any]) -> List[str]:
        """Analyze which learning modalities work best for the user"""
        modality_performance = {}
        
        for session in historical_data.get('sessions', []):
            activities = session.get('activities', [])
            performance = session.get('performance_score', 0)
            
            for activity in activities:
                if activity not in modality_performance:
                    modality_performance[activity] = []
                modality_performance[activity].append(performance)
        
        # Calculate average performance for each modality
        modality_averages = {}
        for modality, scores in modality_performance.items():
            modality_averages[modality] = statistics.mean(scores)
        
        # Return top 3 modalities
        sorted_modalities = sorted(modality_averages.items(), key=lambda x: x[1], reverse=True)
        return [modality for modality, _ in sorted_modalities[:3]]
    
    def _calculate_prediction_accuracy(self, user_id: str) -> float:
        """Calculate historical accuracy of predictions for this user"""
        user_predictions = [p for p in self.predictions if p.user_id == user_id and p.actual_outcome is not None]
        
        if not user_predictions:
            return 0.5  # Default moderate accuracy
        
        accuracies = [p.accuracy_score for p in user_predictions if p.accuracy_score is not None]
        return statistics.mean(accuracies) if accuracies else 0.5
    
    async def predict_quiz_performance(self, user_id: str, concept_id: str, 
                                     quiz_difficulty: float) -> LearningPrediction:
        """Predict user's performance on a quiz"""
        try:
            user_model = self.user_models.get(user_id)
            concept_model = self.concept_models.get(concept_id)
            
            if not user_model:
                # Create basic model if none exists
                user_model = await self.build_user_learning_model(user_id, {})
            
            # Base prediction on user's historical performance
            base_score = 70  # Default expectation
            
            # Adjust based on user factors
            difficulty_adjustment = (1 - quiz_difficulty) * user_model.difficulty_tolerance * 30
            learning_rate_adjustment = user_model.learning_rate * 20
            consistency_adjustment = user_model.consistency_factor * 10
            motivation_adjustment = user_model.motivation_level * 15
            
            predicted_score = (base_score + difficulty_adjustment + 
                             learning_rate_adjustment + consistency_adjustment + 
                             motivation_adjustment)
            
            # Apply concept-specific adjustments if we have the model
            if concept_model:
                concept_difficulty_adjustment = (1 - concept_model.base_difficulty) * 20
                predicted_score += concept_difficulty_adjustment
            
            # Clamp to valid range
            predicted_score = max(0, min(100, predicted_score))
            
            # Calculate confidence based on model quality and data availability
            confidence = user_model.model_confidence * user_model.historical_accuracy
            
            factors_considered = [
                "user_difficulty_tolerance",
                "learning_rate",
                "consistency_factor",
                "motivation_level",
                "quiz_difficulty"
            ]
            
            if concept_model:
                factors_considered.append("concept_difficulty")
            
            prediction = LearningPrediction(
                user_id=user_id,
                concept_id=concept_id,
                prediction_type="performance",
                predicted_value=predicted_score,
                confidence_score=confidence,
                factors_considered=factors_considered,
                prediction_date=datetime.now().isoformat()
            )
            
            self.predictions.append(prediction)
            self.save_data()
            
            return prediction
            
        except Exception as e:
            self.logger.error(f"Error predicting quiz performance: {e}")
            raise
    
    async def predict_learning_time(self, user_id: str, concept_id: str, 
                                  target_mastery: float = 0.8) -> LearningPrediction:
        """Predict time needed to reach target mastery level"""
        try:
            user_model = self.user_models.get(user_id)
            concept_model = self.concept_models.get(concept_id)
            
            if not user_model:
                user_model = await self.build_user_learning_model(user_id, {})
            
            # Base time estimate
            base_time = 120  # 2 hours default
            
            if concept_model:
                base_time = concept_model.typical_learning_time
            
            # Adjust based on user factors
            learning_rate_factor = 2.0 - user_model.learning_rate  # Faster learners need less time
            difficulty_factor = 1.0 + (1.0 - user_model.difficulty_tolerance) * 0.5
            cognitive_load_factor = 2.0 - user_model.cognitive_load_capacity
            motivation_factor = 2.0 - user_model.motivation_level
            
            # Adjust for target mastery level
            mastery_factor = target_mastery * 1.5  # Higher mastery requires more time
            
            predicted_time = (base_time * learning_rate_factor * difficulty_factor * 
                            cognitive_load_factor * motivation_factor * mastery_factor)
            
            # Apply concept difficulty if available
            if concept_model:
                concept_factor = 1.0 + concept_model.base_difficulty
                predicted_time *= concept_factor
            
            predicted_time = max(30, predicted_time)  # Minimum 30 minutes
            
            confidence = user_model.model_confidence * 0.8  # Time predictions are generally less certain
            
            prediction = LearningPrediction(
                user_id=user_id,
                concept_id=concept_id,
                prediction_type="time",
                predicted_value=predicted_time,
                confidence_score=confidence,
                factors_considered=[
                    "learning_rate", "difficulty_tolerance", "cognitive_load_capacity",
                    "motivation_level", "target_mastery", "concept_difficulty"
                ],
                prediction_date=datetime.now().isoformat()
            )
            
            self.predictions.append(prediction)
            self.save_data()
            
            return prediction
            
        except Exception as e:
            self.logger.error(f"Error predicting learning time: {e}")
            raise
    
    async def predict_success_probability(self, user_id: str, concept_id: str, 
                                        learning_goal: str) -> LearningPrediction:
        """Predict probability of successfully achieving a learning goal"""
        try:
            user_model = self.user_models.get(user_id)
            concept_model = self.concept_models.get(concept_id)
            
            if not user_model:
                user_model = await self.build_user_learning_model(user_id, {})
            
            # Base success probability
            base_probability = 0.7  # 70% default
            
            # Adjust based on user factors
            learning_rate_boost = user_model.learning_rate * 0.2
            consistency_boost = user_model.consistency_factor * 0.15
            motivation_boost = user_model.motivation_level * 0.1
            retention_boost = user_model.retention_factor * 0.1
            
            success_probability = (base_probability + learning_rate_boost + 
                                 consistency_boost + motivation_boost + retention_boost)
            
            # Adjust based on concept difficulty
            if concept_model:
                difficulty_penalty = concept_model.base_difficulty * 0.3
                success_rate_boost = concept_model.success_rate * 0.2
                success_probability = success_probability - difficulty_penalty + success_rate_boost
            
            # Adjust based on goal complexity
            goal_complexity = self._assess_goal_complexity(learning_goal)
            complexity_penalty = goal_complexity * 0.2
            success_probability -= complexity_penalty
            
            # Clamp to valid probability range
            success_probability = max(0.1, min(0.95, success_probability))
            
            confidence = user_model.model_confidence * user_model.historical_accuracy * 0.9
            
            prediction = LearningPrediction(
                user_id=user_id,
                concept_id=concept_id,
                prediction_type="success",
                predicted_value=success_probability,
                confidence_score=confidence,
                factors_considered=[
                    "learning_rate", "consistency_factor", "motivation_level",
                    "retention_factor", "concept_difficulty", "goal_complexity"
                ],
                prediction_date=datetime.now().isoformat()
            )
            
            self.predictions.append(prediction)
            self.save_data()
            
            return prediction
            
        except Exception as e:
            self.logger.error(f"Error predicting success probability: {e}")
            raise
    
    def _assess_goal_complexity(self, learning_goal: str) -> float:
        """Assess the complexity of a learning goal"""
        # Simple heuristic based on goal description
        complexity_keywords = {
            'master': 0.8,
            'understand': 0.4,
            'learn': 0.3,
            'apply': 0.6,
            'analyze': 0.7,
            'create': 0.9,
            'evaluate': 0.8,
            'advanced': 0.7,
            'basic': 0.2,
            'fundamental': 0.3
        }
        
        goal_lower = learning_goal.lower()
        complexity_score = 0.5  # Default moderate complexity
        
        for keyword, score in complexity_keywords.items():
            if keyword in goal_lower:
                complexity_score = max(complexity_score, score)
        
        return complexity_score
    
    async def predict_concept_difficulty(self, concept_id: str, concept_name: str, 
                                       concept_description: str) -> ConceptDifficultyModel:
        """Predict difficulty characteristics of a new concept"""
        try:
            # Use AI to analyze concept difficulty
            prompt = f"""
            Analyze the difficulty and learning characteristics of this concept:
            
            Concept: {concept_name}
            Description: {concept_description}
            
            Provide analysis in JSON format:
            {{
                "base_difficulty": 0.7,
                "prerequisite_complexity": 0.6,
                "cognitive_load": 0.8,
                "typical_learning_time": 90,
                "estimated_success_rate": 0.75,
                "common_misconceptions": ["misconception1", "misconception2"],
                "effective_strategies": ["strategy1", "strategy2"],
                "difficulty_factors": {{
                    "abstract_concepts": 0.8,
                    "mathematical_complexity": 0.6,
                    "memorization_required": 0.4
                }}
            }}
            
            Base difficulty: 0.0 (very easy) to 1.0 (very hard)
            Typical learning time: minutes to master
            Success rate: proportion of learners who typically succeed
            """
            
            response = await self.ai_client.get_completion(prompt)
            
            try:
                analysis = json.loads(response)
                
                model = ConceptDifficultyModel(
                    concept_id=concept_id,
                    base_difficulty=analysis.get('base_difficulty', 0.5),
                    prerequisite_complexity=analysis.get('prerequisite_complexity', 0.5),
                    cognitive_load=analysis.get('cognitive_load', 0.5),
                    typical_learning_time=analysis.get('typical_learning_time', 60),
                    success_rate=analysis.get('estimated_success_rate', 0.7),
                    common_misconceptions=analysis.get('common_misconceptions', []),
                    effective_learning_strategies=analysis.get('effective_strategies', []),
                    difficulty_factors=analysis.get('difficulty_factors', {})
                )
                
                self.concept_models[concept_id] = model
                self.save_data()
                
                return model
                
            except json.JSONDecodeError:
                # Fallback to heuristic analysis
                return self._create_heuristic_concept_model(concept_id, concept_name, concept_description)
                
        except Exception as e:
            self.logger.error(f"Error predicting concept difficulty: {e}")
            return self._create_heuristic_concept_model(concept_id, concept_name, concept_description)
    
    def _create_heuristic_concept_model(self, concept_id: str, concept_name: str, 
                                      concept_description: str) -> ConceptDifficultyModel:
        """Create concept model using heuristic analysis"""
        # Simple heuristics based on keywords
        difficulty_keywords = {
            'advanced': 0.8, 'complex': 0.7, 'difficult': 0.8,
            'basic': 0.2, 'simple': 0.3, 'fundamental': 0.4,
            'theory': 0.6, 'practical': 0.4, 'abstract': 0.7,
            'mathematical': 0.7, 'conceptual': 0.6
        }
        
        text = f"{concept_name} {concept_description}".lower()
        base_difficulty = 0.5
        
        for keyword, difficulty in difficulty_keywords.items():
            if keyword in text:
                base_difficulty = max(base_difficulty, difficulty)
        
        return ConceptDifficultyModel(
            concept_id=concept_id,
            base_difficulty=base_difficulty,
            prerequisite_complexity=base_difficulty * 0.8,
            cognitive_load=base_difficulty,
            typical_learning_time=int(60 + base_difficulty * 60),  # 60-120 minutes
            success_rate=1.0 - base_difficulty * 0.4,  # Harder concepts have lower success rates
            common_misconceptions=[],
            effective_learning_strategies=['practice', 'examples', 'repetition'],
            difficulty_factors={'complexity': base_difficulty}
        )
    
    def record_actual_outcome(self, prediction_id: str, actual_value: float):
        """Record actual outcome to improve prediction accuracy"""
        try:
            # Find the prediction
            prediction = None
            for pred in self.predictions:
                if hasattr(pred, 'prediction_id') and pred.prediction_id == prediction_id:
                    prediction = pred
                    break
            
            if not prediction:
                # Try to find by user_id and concept_id if prediction_id not found
                return
            
            prediction.actual_outcome = actual_value
            
            # Calculate accuracy
            predicted = prediction.predicted_value
            if prediction.prediction_type == "performance":
                # For performance predictions (0-100), calculate percentage error
                error = abs(predicted - actual_value) / 100
                accuracy = 1.0 - error
            elif prediction.prediction_type == "time":
                # For time predictions, calculate relative error
                error = abs(predicted - actual_value) / max(predicted, actual_value)
                accuracy = 1.0 - min(1.0, error)
            elif prediction.prediction_type == "success":
                # For success probability, check if prediction was correct
                success_threshold = 0.5
                predicted_success = predicted > success_threshold
                actual_success = actual_value > success_threshold
                accuracy = 1.0 if predicted_success == actual_success else 0.0
            else:
                accuracy = 0.5  # Default
            
            prediction.accuracy_score = max(0.0, accuracy)
            
            # Update user model confidence based on prediction accuracy
            user_model = self.user_models.get(prediction.user_id)
            if user_model:
                # Weighted update of historical accuracy
                weight = 0.1  # Weight for new accuracy
                user_model.historical_accuracy = (
                    (1 - weight) * user_model.historical_accuracy + 
                    weight * accuracy
                )
                user_model.last_updated = datetime.now().isoformat()
            
            self.save_data()
            
        except Exception as e:
            self.logger.error(f"Error recording actual outcome: {e}")
    
    def get_prediction_insights(self, user_id: str) -> Dict[str, Any]:
        """Get insights about prediction accuracy and model performance"""
        try:
            user_predictions = [p for p in self.predictions if p.user_id == user_id]
            user_model = self.user_models.get(user_id)
            
            if not user_predictions:
                return {"message": "No predictions available for this user"}
            
            # Calculate prediction statistics
            total_predictions = len(user_predictions)
            predictions_with_outcomes = [p for p in user_predictions if p.actual_outcome is not None]
            
            accuracy_stats = {}
            if predictions_with_outcomes:
                accuracies = [p.accuracy_score for p in predictions_with_outcomes if p.accuracy_score is not None]
                if accuracies:
                    accuracy_stats = {
                        "average_accuracy": statistics.mean(accuracies),
                        "accuracy_trend": "improving" if len(accuracies) > 1 and accuracies[-1] > accuracies[0] else "stable",
                        "predictions_validated": len(accuracies),
                        "best_prediction_type": self._get_best_prediction_type(predictions_with_outcomes)
                    }
            
            # Model insights
            model_insights = {}
            if user_model:
                model_insights = {
                    "model_confidence": user_model.model_confidence,
                    "learning_rate": user_model.learning_rate,
                    "difficulty_tolerance": user_model.difficulty_tolerance,
                    "consistency_factor": user_model.consistency_factor,
                    "preferred_modalities": user_model.preferred_learning_modalities
                }
            
            # Recent predictions
            recent_predictions = sorted(user_predictions, key=lambda x: x.prediction_date, reverse=True)[:5]
            recent_summary = []
            
            for pred in recent_predictions:
                summary = {
                    "type": pred.prediction_type,
                    "concept": pred.concept_id,
                    "predicted_value": pred.predicted_value,
                    "confidence": pred.confidence_score,
                    "date": pred.prediction_date
                }
                
                if pred.actual_outcome is not None:
                    summary["actual_outcome"] = pred.actual_outcome
                    summary["accuracy"] = pred.accuracy_score
                
                recent_summary.append(summary)
            
            return {
                "user_id": user_id,
                "total_predictions": total_predictions,
                "accuracy_statistics": accuracy_stats,
                "model_insights": model_insights,
                "recent_predictions": recent_summary,
                "recommendations": self._generate_prediction_recommendations(user_id)
            }
            
        except Exception as e:
            self.logger.error(f"Error getting prediction insights: {e}")
            return {"error": str(e)}
    
    def _get_best_prediction_type(self, predictions: List[LearningPrediction]) -> str:
        """Determine which type of prediction is most accurate for this user"""
        type_accuracies = {}
        
        for pred in predictions:
            if pred.accuracy_score is not None:
                pred_type = pred.prediction_type
                if pred_type not in type_accuracies:
                    type_accuracies[pred_type] = []
                type_accuracies[pred_type].append(pred.accuracy_score)
        
        # Calculate average accuracy for each type
        avg_accuracies = {}
        for pred_type, accuracies in type_accuracies.items():
            avg_accuracies[pred_type] = statistics.mean(accuracies)
        
        if avg_accuracies:
            return max(avg_accuracies.items(), key=lambda x: x[1])[0]
        
        return "unknown"
    
    def _generate_prediction_recommendations(self, user_id: str) -> List[str]:
        """Generate recommendations for improving prediction accuracy"""
        recommendations = []
        
        user_model = self.user_models.get(user_id)
        user_predictions = [p for p in self.predictions if p.user_id == user_id]
        
        if not user_model or not user_predictions:
            return ["More learning data needed to improve predictions"]
        
        # Check model confidence
        if user_model.model_confidence < 0.5:
            recommendations.append("Continue learning to improve prediction accuracy - more data needed")
        
        # Check prediction accuracy
        if user_model.historical_accuracy < 0.6:
            recommendations.append("Predictions may be less reliable - consider this when planning")
        
        # Check consistency
        if user_model.consistency_factor < 0.5:
            recommendations.append("Work on maintaining consistent performance for better predictions")
        
        # Check motivation
        if user_model.motivation_level < 0.6:
            recommendations.append("Improving engagement could lead to better learning outcomes")
        
        return recommendations[:5]
    
    def generate_prediction_insights(self, user_id: str) -> Dict[str, Any]:
        """Generate comprehensive prediction insights for a user"""
        try:
            return self.get_prediction_insights(user_id)
        except Exception as e:
            self.logger.error(f"Error generating prediction insights: {e}")
            return {"error": str(e)}