"""
Adaptive Quiz Intelligence Engine
Implements adaptive questioning, concept mastery tracking, and intelligent question generation
"""

import json
import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, asdict
import random
from .ai_client import AIClient
from .database import SyllaboDatabase
from .logger import SyllaboLogger

@dataclass
class QuizQuestion:
    """Enhanced quiz question with adaptive features"""
    question_id: str
    question_text: str
    question_type: str  # multiple_choice, true_false, short_answer, fill_blank
    options: List[str]
    correct_answer: Any
    explanation: str
    difficulty_level: float  # 0.0 to 1.0
    concept_tags: List[str]
    cognitive_level: str  # remember, understand, apply, analyze, evaluate, create
    estimated_time: int  # seconds
    hint: Optional[str]
    created_at: str

@dataclass
class QuizSession:
    """Adaptive quiz session tracking"""
    session_id: str
    user_id: str
    concept_id: str
    questions: List[QuizQuestion]
    responses: List[Dict[str, Any]]
    current_question: int
    difficulty_progression: List[float]
    start_time: str
    end_time: Optional[str]
    adaptive_adjustments: List[str]
    performance_metrics: Dict[str, float]

@dataclass
class ConceptMastery:
    """Track mastery of specific concepts"""
    user_id: str
    concept_id: str
    concept_name: str
    mastery_level: float  # 0.0 to 1.0
    confidence_interval: Tuple[float, float]
    question_history: List[Dict[str, Any]]
    last_assessment: str
    mastery_trend: List[float]  # Historical mastery levels
    weak_areas: List[str]
    strong_areas: List[str]
    next_review_date: str

class AdaptiveQuizEngine:
    """Main adaptive quiz engine with intelligent questioning"""
    
    def __init__(self, ai_client: AIClient = None, db: SyllaboDatabase = None):
        self.ai_client = ai_client or AIClient()
        self.db = db or SyllaboDatabase()
        self.logger = SyllaboLogger("adaptive_quiz_engine")
        
        # Data storage
        self.data_dir = "data/adaptive_quiz"
        os.makedirs(self.data_dir, exist_ok=True)
        
        self.sessions_file = os.path.join(self.data_dir, "quiz_sessions.json")
        self.mastery_file = os.path.join(self.data_dir, "concept_mastery.json")
        self.questions_file = os.path.join(self.data_dir, "question_bank.json")
        
        # Load data
        self.quiz_sessions: Dict[str, QuizSession] = self._load_sessions()
        self.concept_mastery: Dict[str, ConceptMastery] = self._load_mastery()
        self.question_bank: Dict[str, List[QuizQuestion]] = self._load_questions()
        
        # Adaptive parameters
        self.difficulty_adjustment_rate = 0.15
        self.mastery_threshold = 0.8
        self.confidence_threshold = 0.7
    
    def _load_sessions(self) -> Dict[str, QuizSession]:
        """Load quiz sessions from file"""
        if os.path.exists(self.sessions_file):
            try:
                with open(self.sessions_file, 'r') as f:
                    data = json.load(f)
                    sessions = {}
                    for session_id, session_data in data.items():
                        # Convert question data back to QuizQuestion objects
                        questions = [QuizQuestion(**q) for q in session_data['questions']]
                        session_data['questions'] = questions
                        sessions[session_id] = QuizSession(**session_data)
                    return sessions
            except Exception as e:
                self.logger.error(f"Error loading sessions: {e}")
        return {}
    
    def _load_mastery(self) -> Dict[str, ConceptMastery]:
        """Load concept mastery data from file"""
        if os.path.exists(self.mastery_file):
            try:
                with open(self.mastery_file, 'r') as f:
                    data = json.load(f)
                    return {
                        key: ConceptMastery(**mastery_data)
                        for key, mastery_data in data.items()
                    }
            except Exception as e:
                self.logger.error(f"Error loading mastery data: {e}")
        return {}
    
    def _load_questions(self) -> Dict[str, List[QuizQuestion]]:
        """Load question bank from file"""
        if os.path.exists(self.questions_file):
            try:
                with open(self.questions_file, 'r') as f:
                    data = json.load(f)
                    question_bank = {}
                    for concept_id, questions_data in data.items():
                        questions = [QuizQuestion(**q) for q in questions_data]
                        question_bank[concept_id] = questions
                    return question_bank
            except Exception as e:
                self.logger.error(f"Error loading question bank: {e}")
        return {}
    
    def save_data(self):
        """Save all data to files"""
        try:
            # Save sessions
            with open(self.sessions_file, 'w') as f:
                sessions_data = {}
                for session_id, session in self.quiz_sessions.items():
                    session_dict = asdict(session)
                    # Convert QuizQuestion objects to dicts
                    session_dict['questions'] = [asdict(q) for q in session.questions]
                    sessions_data[session_id] = session_dict
                json.dump(sessions_data, f, indent=2)
            
            # Save mastery data
            with open(self.mastery_file, 'w') as f:
                json.dump({
                    key: asdict(mastery)
                    for key, mastery in self.concept_mastery.items()
                }, f, indent=2)
            
            # Save question bank
            with open(self.questions_file, 'w') as f:
                questions_data = {}
                for concept_id, questions in self.question_bank.items():
                    questions_data[concept_id] = [asdict(q) for q in questions]
                json.dump(questions_data, f, indent=2)
                
        except Exception as e:
            self.logger.error(f"Error saving data: {e}")
    
    async def generate_adaptive_questions(self, concept_id: str, concept_name: str, 
                                        content: str, user_id: str, 
                                        num_questions: int = 10) -> List[QuizQuestion]:
        """Generate adaptive questions based on user's current mastery level"""
        try:
            # Get user's current mastery level
            mastery_key = f"{user_id}_{concept_id}"
            mastery = self.concept_mastery.get(mastery_key)
            
            # Determine difficulty distribution based on mastery
            if mastery:
                current_level = mastery.mastery_level
                weak_areas = mastery.weak_areas
            else:
                current_level = 0.5  # Default for new users
                weak_areas = []
            
            # Calculate difficulty distribution
            difficulties = self._calculate_difficulty_distribution(current_level, num_questions)
            
            # Generate questions using AI
            questions = await self._generate_questions_with_ai(
                concept_name, content, difficulties, weak_areas
            )
            
            # Add to question bank
            if concept_id not in self.question_bank:
                self.question_bank[concept_id] = []
            
            self.question_bank[concept_id].extend(questions)
            self.save_data()
            
            return questions
            
        except Exception as e:
            self.logger.error(f"Error generating adaptive questions: {e}")
            return []
    
    def _calculate_difficulty_distribution(self, mastery_level: float, 
                                         num_questions: int) -> List[float]:
        """Calculate optimal difficulty distribution for questions"""
        difficulties = []
        
        if mastery_level < 0.3:  # Beginner
            # More easy questions, fewer hard ones
            easy_count = int(num_questions * 0.6)
            medium_count = int(num_questions * 0.3)
            hard_count = num_questions - easy_count - medium_count
            
            difficulties.extend([0.2 + random.uniform(0, 0.2) for _ in range(easy_count)])
            difficulties.extend([0.4 + random.uniform(0, 0.2) for _ in range(medium_count)])
            difficulties.extend([0.6 + random.uniform(0, 0.3) for _ in range(hard_count)])
            
        elif mastery_level < 0.7:  # Intermediate
            # Balanced distribution
            easy_count = int(num_questions * 0.3)
            medium_count = int(num_questions * 0.5)
            hard_count = num_questions - easy_count - medium_count
            
            difficulties.extend([0.3 + random.uniform(0, 0.2) for _ in range(easy_count)])
            difficulties.extend([0.5 + random.uniform(0, 0.2) for _ in range(medium_count)])
            difficulties.extend([0.7 + random.uniform(0, 0.2) for _ in range(hard_count)])
            
        else:  # Advanced
            # More challenging questions
            easy_count = int(num_questions * 0.2)
            medium_count = int(num_questions * 0.3)
            hard_count = num_questions - easy_count - medium_count
            
            difficulties.extend([0.4 + random.uniform(0, 0.2) for _ in range(easy_count)])
            difficulties.extend([0.6 + random.uniform(0, 0.2) for _ in range(medium_count)])
            difficulties.extend([0.8 + random.uniform(0, 0.2) for _ in range(hard_count)])
        
        random.shuffle(difficulties)
        return difficulties
    
    async def _generate_questions_with_ai(self, concept_name: str, content: str, 
                                        difficulties: List[float], 
                                        weak_areas: List[str]) -> List[QuizQuestion]:
        """Generate questions using AI with specific difficulty levels"""
        try:
            # Focus areas for questions
            focus_areas = weak_areas if weak_areas else [concept_name]
            
            prompt = f"""
            Generate {len(difficulties)} quiz questions about "{concept_name}" based on this content:
            
            Content: {content[:2000]}  # Limit content length
            
            Requirements:
            - Focus on these areas: {', '.join(focus_areas)}
            - Difficulty levels (0.0-1.0): {difficulties}
            - Include various question types: multiple_choice, true_false, short_answer
            - Include cognitive levels: remember, understand, apply, analyze
            - Provide explanations and hints
            - Estimate time needed for each question
            
            Respond with JSON in this exact format:
            {{
                "questions": [
                    {{
                        "question_id": "unique_id",
                        "question_text": "What is the main concept?",
                        "question_type": "multiple_choice",
                        "options": ["Option A", "Option B", "Option C", "Option D"],
                        "correct_answer": 0,
                        "explanation": "Detailed explanation of the answer",
                        "difficulty_level": 0.5,
                        "concept_tags": ["tag1", "tag2"],
                        "cognitive_level": "understand",
                        "estimated_time": 60,
                        "hint": "Think about the main principles",
                        "created_at": "{datetime.now().isoformat()}"
                    }}
                ]
            }}
            """
            
            response = await self.ai_client.get_completion(prompt)
            
            try:
                # Clean the response to extract JSON
                cleaned_response = self._extract_json_from_response(response)
                data = json.loads(cleaned_response)
                questions = []
                
                for i, q_data in enumerate(data.get('questions', [])):
                    # Assign the calculated difficulty if not provided
                    if i < len(difficulties):
                        q_data['difficulty_level'] = difficulties[i]
                    
                    question = QuizQuestion(
                        question_id=q_data.get('question_id', f"q_{datetime.now().timestamp()}_{i}"),
                        question_text=q_data.get('question_text', ''),
                        question_type=q_data.get('question_type', 'multiple_choice'),
                        options=q_data.get('options', []),
                        correct_answer=q_data.get('correct_answer', 0),
                        explanation=q_data.get('explanation', ''),
                        difficulty_level=q_data.get('difficulty_level', 0.5),
                        concept_tags=q_data.get('concept_tags', [concept_name]),
                        cognitive_level=q_data.get('cognitive_level', 'understand'),
                        estimated_time=q_data.get('estimated_time', 60),
                        hint=q_data.get('hint'),
                        created_at=q_data.get('created_at', datetime.now().isoformat())
                    )
                    questions.append(question)
                
                return questions
                
            except json.JSONDecodeError:
                self.logger.error("Failed to parse AI response for questions")
                return self._generate_fallback_questions(concept_name, len(difficulties))
                
        except Exception as e:
            self.logger.error(f"Error generating questions with AI: {e}")
            return self._generate_fallback_questions(concept_name, len(difficulties))
    
    def _extract_json_from_response(self, response: str) -> str:
        """Extract JSON from AI response that may contain thinking tags or markdown"""
        # Remove thinking tags if present
        if '<think>' in response and '</think>' in response:
            start = response.find('</think>') + 8
            response = response[start:].strip()
        
        # Remove markdown code blocks if present
        if '```json' in response:
            start = response.find('```json') + 7
            end = response.find('```', start)
            if end != -1:
                response = response[start:end].strip()
        elif '```' in response:
            # Handle generic code blocks
            start = response.find('```') + 3
            end = response.find('```', start)
            if end != -1:
                response = response[start:end].strip()
        
        # Find JSON object boundaries
        json_start = response.find('{')
        if json_start != -1:
            # Find the matching closing brace
            brace_count = 0
            json_end = -1
            for i in range(json_start, len(response)):
                if response[i] == '{':
                    brace_count += 1
                elif response[i] == '}':
                    brace_count -= 1
                    if brace_count == 0:
                        json_end = i + 1
                        break
            
            if json_end != -1:
                response = response[json_start:json_end]
        
        return response.strip()

    def _generate_fallback_questions(self, concept_name: str, count: int) -> List[QuizQuestion]:
        """Generate fallback questions when AI fails"""
        questions = []
        for i in range(count):
            question = QuizQuestion(
                question_id=f"fallback_{datetime.now().timestamp()}_{i}",
                question_text=f"What is an important aspect of {concept_name}?",
                question_type="short_answer",
                options=[],
                correct_answer=f"Key concepts related to {concept_name}",
                explanation=f"This question tests understanding of {concept_name}",
                difficulty_level=0.5,
                concept_tags=[concept_name],
                cognitive_level="understand",
                estimated_time=60,
                hint=f"Think about the main principles of {concept_name}",
                created_at=datetime.now().isoformat()
            )
            questions.append(question)
        
        return questions
    
    async def start_adaptive_quiz_session(self, user_id: str, concept_id: str, 
                                        concept_name: str, content: str = "") -> str:
        """Start a new adaptive quiz session"""
        try:
            session_id = f"{user_id}_{concept_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            
            # Generate adaptive questions
            questions = await self.generate_adaptive_questions(
                concept_id, concept_name, content, user_id
            )
            
            if not questions:
                raise ValueError("Failed to generate questions")
            
            # Create session
            session = QuizSession(
                session_id=session_id,
                user_id=user_id,
                concept_id=concept_id,
                questions=questions,
                responses=[],
                current_question=0,
                difficulty_progression=[q.difficulty_level for q in questions],
                start_time=datetime.now().isoformat(),
                end_time=None,
                adaptive_adjustments=[],
                performance_metrics={}
            )
            
            self.quiz_sessions[session_id] = session
            self.save_data()
            
            return session_id
            
        except Exception as e:
            self.logger.error(f"Error starting quiz session: {e}")
            raise
    
    def get_next_question(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Get the next adaptive question in the session"""
        try:
            session = self.quiz_sessions.get(session_id)
            if not session:
                return None
            
            if session.current_question >= len(session.questions):
                return None  # Quiz completed
            
            current_q = session.questions[session.current_question]
            
            return {
                "question_id": current_q.question_id,
                "question_text": current_q.question_text,
                "question_type": current_q.question_type,
                "options": current_q.options,
                "difficulty_level": current_q.difficulty_level,
                "estimated_time": current_q.estimated_time,
                "hint": current_q.hint,
                "progress": {
                    "current": session.current_question + 1,
                    "total": len(session.questions),
                    "percentage": ((session.current_question + 1) / len(session.questions)) * 100
                }
            }
            
        except Exception as e:
            self.logger.error(f"Error getting next question: {e}")
            return None
    
    async def submit_answer(self, session_id: str, answer: Any, 
                          time_taken: int) -> Dict[str, Any]:
        """Submit answer and get adaptive feedback"""
        try:
            session = self.quiz_sessions.get(session_id)
            if not session:
                return {"error": "Session not found"}
            
            if session.current_question >= len(session.questions):
                return {"error": "Quiz already completed"}
            
            current_q = session.questions[session.current_question]
            
            # Evaluate answer
            is_correct = self._evaluate_answer(current_q, answer)
            
            # Record response
            response = {
                "question_id": current_q.question_id,
                "user_answer": answer,
                "correct_answer": current_q.correct_answer,
                "is_correct": is_correct,
                "time_taken": time_taken,
                "difficulty_level": current_q.difficulty_level,
                "timestamp": datetime.now().isoformat()
            }
            
            session.responses.append(response)
            
            # Adaptive adjustment for next questions
            await self._make_adaptive_adjustment(session, is_correct, time_taken)
            
            # Move to next question
            session.current_question += 1
            
            # Prepare response
            result = {
                "is_correct": is_correct,
                "explanation": current_q.explanation,
                "correct_answer": current_q.correct_answer,
                "difficulty_adjustment": session.adaptive_adjustments[-1] if session.adaptive_adjustments else "none"
            }
            
            # Check if quiz is completed
            if session.current_question >= len(session.questions):
                result["quiz_completed"] = True
                result["final_results"] = await self._finalize_quiz_session(session)
            else:
                result["quiz_completed"] = False
                result["next_question"] = self.get_next_question(session_id)
            
            self.save_data()
            return result
            
        except Exception as e:
            self.logger.error(f"Error submitting answer: {e}")
            return {"error": str(e)}
    
    def _evaluate_answer(self, question: QuizQuestion, user_answer: Any) -> bool:
        """Evaluate if the user's answer is correct"""
        if question.question_type == "multiple_choice":
            return user_answer == question.correct_answer
        
        elif question.question_type == "true_false":
            return user_answer == question.correct_answer
        
        elif question.question_type == "short_answer":
            # Simple keyword matching for short answers
            correct = str(question.correct_answer).lower()
            user = str(user_answer).lower()
            
            # Check for exact match
            if user == correct:
                return True
            
            # Check for keyword overlap
            correct_words = set(correct.split())
            user_words = set(user.split())
            
            if correct_words and user_words:
                overlap = len(correct_words.intersection(user_words))
                return overlap >= len(correct_words) * 0.6
        
        return False
    
    async def _make_adaptive_adjustment(self, session: QuizSession, 
                                      is_correct: bool, time_taken: int):
        """Make adaptive adjustments to upcoming questions"""
        try:
            current_performance = self._calculate_current_performance(session)
            
            adjustment = "none"
            
            # Adjust difficulty based on performance
            if len(session.responses) >= 3:  # Need some history
                recent_correct = sum(1 for r in session.responses[-3:] if r['is_correct'])
                recent_accuracy = recent_correct / 3
                
                if recent_accuracy < 0.4:  # Struggling
                    adjustment = "easier"
                    self._adjust_remaining_questions(session, -self.difficulty_adjustment_rate)
                    
                elif recent_accuracy > 0.8:  # Doing well
                    adjustment = "harder"
                    self._adjust_remaining_questions(session, self.difficulty_adjustment_rate)
            
            # Time-based adjustments
            current_q = session.questions[session.current_question - 1]
            if time_taken > current_q.estimated_time * 2:  # Taking too long
                if adjustment == "none":
                    adjustment = "easier"
                    self._adjust_remaining_questions(session, -self.difficulty_adjustment_rate * 0.5)
            
            session.adaptive_adjustments.append(adjustment)
            
        except Exception as e:
            self.logger.error(f"Error making adaptive adjustment: {e}")
    
    def _calculate_current_performance(self, session: QuizSession) -> Dict[str, float]:
        """Calculate current performance metrics"""
        if not session.responses:
            return {"accuracy": 0.0, "avg_time": 0.0, "difficulty_handled": 0.5}
        
        correct_count = sum(1 for r in session.responses if r['is_correct'])
        accuracy = correct_count / len(session.responses)
        
        avg_time = sum(r['time_taken'] for r in session.responses) / len(session.responses)
        
        # Calculate average difficulty of correctly answered questions
        correct_difficulties = [
            r['difficulty_level'] for r in session.responses if r['is_correct']
        ]
        difficulty_handled = sum(correct_difficulties) / len(correct_difficulties) if correct_difficulties else 0.5
        
        return {
            "accuracy": accuracy,
            "avg_time": avg_time,
            "difficulty_handled": difficulty_handled
        }
    
    def _adjust_remaining_questions(self, session: QuizSession, adjustment: float):
        """Adjust difficulty of remaining questions"""
        for i in range(session.current_question, len(session.questions)):
            current_diff = session.questions[i].difficulty_level
            new_diff = max(0.1, min(1.0, current_diff + adjustment))
            session.questions[i].difficulty_level = new_diff
            session.difficulty_progression[i] = new_diff
    
    async def _finalize_quiz_session(self, session: QuizSession) -> Dict[str, Any]:
        """Finalize quiz session and update mastery tracking"""
        try:
            session.end_time = datetime.now().isoformat()
            
            # Calculate final metrics
            correct_count = sum(1 for r in session.responses if r['is_correct'])
            total_questions = len(session.responses)
            accuracy = correct_count / total_questions if total_questions > 0 else 0
            
            total_time = sum(r['time_taken'] for r in session.responses)
            avg_time = total_time / total_questions if total_questions > 0 else 0
            
            # Calculate difficulty-weighted score
            weighted_score = 0
            total_weight = 0
            
            for response in session.responses:
                weight = response['difficulty_level']
                score = 1 if response['is_correct'] else 0
                weighted_score += score * weight
                total_weight += weight
            
            final_score = (weighted_score / total_weight) * 100 if total_weight > 0 else 0
            
            session.performance_metrics = {
                "accuracy": accuracy,
                "final_score": final_score,
                "total_time": total_time,
                "avg_time_per_question": avg_time,
                "questions_answered": total_questions,
                "adaptive_adjustments_made": len([a for a in session.adaptive_adjustments if a != "none"])
            }
            
            # Update concept mastery
            await self._update_concept_mastery(session)
            
            return {
                "session_id": session.session_id,
                "performance": session.performance_metrics,
                "mastery_update": self._get_mastery_update(session.user_id, session.concept_id),
                "recommendations": await self._generate_session_recommendations(session)
            }
            
        except Exception as e:
            self.logger.error(f"Error finalizing session: {e}")
            return {"error": str(e)}
    
    async def _update_concept_mastery(self, session: QuizSession):
        """Update concept mastery based on quiz performance"""
        try:
            mastery_key = f"{session.user_id}_{session.concept_id}"
            
            # Calculate new mastery level
            performance = session.performance_metrics
            new_mastery_score = performance['final_score'] / 100
            
            if mastery_key in self.concept_mastery:
                mastery = self.concept_mastery[mastery_key]
                
                # Update with weighted average (recent performance has more weight)
                weight = 0.3  # Weight for new performance
                mastery.mastery_level = (1 - weight) * mastery.mastery_level + weight * new_mastery_score
                
                # Update trend
                mastery.mastery_trend.append(mastery.mastery_level)
                if len(mastery.mastery_trend) > 10:  # Keep last 10 assessments
                    mastery.mastery_trend = mastery.mastery_trend[-10:]
                
            else:
                # Create new mastery record
                mastery = ConceptMastery(
                    user_id=session.user_id,
                    concept_id=session.concept_id,
                    concept_name=session.concept_id,  # Would be better to get actual name
                    mastery_level=new_mastery_score,
                    confidence_interval=(max(0, new_mastery_score - 0.2), min(1, new_mastery_score + 0.2)),
                    question_history=[],
                    last_assessment=datetime.now().isoformat(),
                    mastery_trend=[new_mastery_score],
                    weak_areas=[],
                    strong_areas=[],
                    next_review_date=(datetime.now() + timedelta(days=7)).isoformat()
                )
                
                self.concept_mastery[mastery_key] = mastery
            
            # Analyze weak and strong areas
            self._analyze_performance_areas(mastery, session)
            
            mastery.last_assessment = datetime.now().isoformat()
            
            # Schedule next review based on mastery level
            if mastery.mastery_level >= 0.8:
                days_until_review = 14  # Review in 2 weeks if mastered
            elif mastery.mastery_level >= 0.6:
                days_until_review = 7   # Review in 1 week if good
            else:
                days_until_review = 3   # Review in 3 days if struggling
            
            mastery.next_review_date = (datetime.now() + timedelta(days=days_until_review)).isoformat()
            
        except Exception as e:
            self.logger.error(f"Error updating concept mastery: {e}")
    
    def _analyze_performance_areas(self, mastery: ConceptMastery, session: QuizSession):
        """Analyze performance to identify weak and strong areas"""
        weak_areas = []
        strong_areas = []
        
        # Group responses by concept tags
        tag_performance = {}
        
        for i, response in enumerate(session.responses):
            question = session.questions[i]
            for tag in question.concept_tags:
                if tag not in tag_performance:
                    tag_performance[tag] = {"correct": 0, "total": 0}
                
                tag_performance[tag]["total"] += 1
                if response["is_correct"]:
                    tag_performance[tag]["correct"] += 1
        
        # Classify areas
        for tag, perf in tag_performance.items():
            accuracy = perf["correct"] / perf["total"] if perf["total"] > 0 else 0
            
            if accuracy < 0.5:
                weak_areas.append(tag)
            elif accuracy >= 0.8:
                strong_areas.append(tag)
        
        mastery.weak_areas = weak_areas
        mastery.strong_areas = strong_areas
    
    def _get_mastery_update(self, user_id: str, concept_id: str) -> Dict[str, Any]:
        """Get mastery update information"""
        mastery_key = f"{user_id}_{concept_id}"
        mastery = self.concept_mastery.get(mastery_key)
        
        if not mastery:
            return {"status": "no_data"}
        
        # Determine mastery status
        if mastery.mastery_level >= 0.8:
            status = "mastered"
        elif mastery.mastery_level >= 0.6:
            status = "good_progress"
        elif mastery.mastery_level >= 0.4:
            status = "needs_practice"
        else:
            status = "struggling"
        
        return {
            "status": status,
            "mastery_level": mastery.mastery_level,
            "trend": "improving" if len(mastery.mastery_trend) > 1 and mastery.mastery_trend[-1] > mastery.mastery_trend[-2] else "stable",
            "weak_areas": mastery.weak_areas,
            "strong_areas": mastery.strong_areas,
            "next_review": mastery.next_review_date
        }
    
    async def _generate_session_recommendations(self, session: QuizSession) -> List[str]:
        """Generate recommendations based on session performance"""
        recommendations = []
        performance = session.performance_metrics
        
        if performance['accuracy'] < 0.5:
            recommendations.append("Consider reviewing the basic concepts before attempting more questions")
        
        if performance['avg_time_per_question'] > 120:  # More than 2 minutes per question
            recommendations.append("Try to work on answering questions more quickly")
        
        if performance['adaptive_adjustments_made'] > 3:
            recommendations.append("The quiz adapted significantly to your performance - consider more focused study")
        
        # Get mastery info for specific recommendations
        mastery_key = f"{session.user_id}_{session.concept_id}"
        mastery = self.concept_mastery.get(mastery_key)
        
        if mastery and mastery.weak_areas:
            recommendations.append(f"Focus on these areas: {', '.join(mastery.weak_areas[:3])}")
        
        if performance['final_score'] >= 80:
            recommendations.append("Great job! Consider moving to more advanced topics")
        
        return recommendations[:5]  # Limit to top 5 recommendations
    
    def get_concept_mastery_report(self, user_id: str) -> Dict[str, Any]:
        """Get comprehensive concept mastery report for a user"""
        try:
            user_masteries = {
                key: mastery for key, mastery in self.concept_mastery.items()
                if key.startswith(f"{user_id}_")
            }
            
            if not user_masteries:
                return {"message": "No mastery data available"}
            
            # Calculate overall statistics
            mastery_levels = [m.mastery_level for m in user_masteries.values()]
            avg_mastery = sum(mastery_levels) / len(mastery_levels)
            
            mastered_concepts = len([m for m in user_masteries.values() if m.mastery_level >= 0.8])
            total_concepts = len(user_masteries)
            
            # Identify concepts needing review
            needs_review = []
            for mastery in user_masteries.values():
                review_date = datetime.fromisoformat(mastery.next_review_date)
                if review_date <= datetime.now():
                    needs_review.append({
                        "concept": mastery.concept_name,
                        "mastery_level": mastery.mastery_level,
                        "weak_areas": mastery.weak_areas
                    })
            
            # Overall weak and strong areas
            all_weak_areas = []
            all_strong_areas = []
            
            for mastery in user_masteries.values():
                all_weak_areas.extend(mastery.weak_areas)
                all_strong_areas.extend(mastery.strong_areas)
            
            # Count frequency
            weak_area_counts = {}
            strong_area_counts = {}
            
            for area in all_weak_areas:
                weak_area_counts[area] = weak_area_counts.get(area, 0) + 1
            
            for area in all_strong_areas:
                strong_area_counts[area] = strong_area_counts.get(area, 0) + 1
            
            # Sort by frequency
            top_weak_areas = sorted(weak_area_counts.items(), key=lambda x: x[1], reverse=True)[:5]
            top_strong_areas = sorted(strong_area_counts.items(), key=lambda x: x[1], reverse=True)[:5]
            
            return {
                "user_id": user_id,
                "overall_mastery": avg_mastery,
                "mastered_concepts": mastered_concepts,
                "total_concepts": total_concepts,
                "mastery_percentage": (mastered_concepts / total_concepts) * 100,
                "concepts_needing_review": needs_review,
                "top_weak_areas": [area for area, count in top_weak_areas],
                "top_strong_areas": [area for area, count in top_strong_areas],
                "recommendations": self._generate_mastery_recommendations(user_masteries)
            }
            
        except Exception as e:
            self.logger.error(f"Error generating mastery report: {e}")
            return {"error": str(e)}
    
    def _generate_mastery_recommendations(self, masteries: Dict[str, ConceptMastery]) -> List[str]:
        """Generate recommendations based on overall mastery data"""
        recommendations = []
        
        mastery_levels = [m.mastery_level for m in masteries.values()]
        avg_mastery = sum(mastery_levels) / len(mastery_levels) if mastery_levels else 0
        
        if avg_mastery < 0.5:
            recommendations.append("Focus on building foundational knowledge before advancing")
        elif avg_mastery > 0.8:
            recommendations.append("Consider exploring more advanced topics in your strong areas")
        
        # Check for concepts that haven't been reviewed recently
        overdue_reviews = 0
        for mastery in masteries.values():
            review_date = datetime.fromisoformat(mastery.next_review_date)
            if review_date <= datetime.now():
                overdue_reviews += 1
        
        if overdue_reviews > 0:
            recommendations.append(f"You have {overdue_reviews} concepts due for review")
        
        return recommendations