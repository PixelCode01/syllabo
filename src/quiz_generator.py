from typing import Dict, List, Optional
import json
import random
from datetime import datetime
from .ai_client import AIClient
from .database import SyllaboDatabase
from .logger import SyllaboLogger

class QuizGenerator:
    """Generate interactive quizzes from video content and notes"""
    
    def __init__(self, ai_client: AIClient = None, db: SyllaboDatabase = None):
        self.ai_client = ai_client or AIClient()
        self.db = db or SyllaboDatabase()
        self.logger = SyllaboLogger("quiz_generator")
    
    async def generate_quiz_from_content(self, content: str, topic: str, 
                                       num_questions: int = 5) -> Dict:
        """Generate quiz questions from content"""
        prompt = f"""Create {num_questions} quiz questions about {topic} based on this content:

{content[:2000]}

Generate questions in this JSON format:
{{
    "questions": [
        {{
            "question": "What is...",
            "type": "multiple_choice",
            "options": ["A", "B", "C", "D"],
            "correct_answer": 0,
            "explanation": "Brief explanation"
        }}
    ]
}}

Include different question types: multiple choice, true/false, and short answer.
Make questions test understanding, not just memorization."""
        
        try:
            response = await self.ai_client.get_completion(prompt)
            quiz_data = json.loads(response)
            
            quiz = {
                "topic": topic,
                "questions": quiz_data.get("questions", []),
                "created_at": datetime.now().isoformat(),
                "difficulty": self._assess_difficulty(content)
            }
            
            return quiz
            
        except Exception as e:
            self.logger.error(f"Failed to generate quiz: {e}")
            return {"error": str(e)}
    
    def take_quiz(self, quiz: Dict) -> Dict:
        """Interactive quiz taking session"""
        results = {
            "topic": quiz["topic"],
            "total_questions": len(quiz["questions"]),
            "correct_answers": 0,
            "answers": [],
            "score": 0.0,
            "completed_at": datetime.now().isoformat()
        }
        
        print(f"\nStarting quiz: {quiz['topic']}")
        print(f"Questions: {len(quiz['questions'])}")
        print("-" * 50)
        
        for i, question in enumerate(quiz["questions"], 1):
            print(f"\nQuestion {i}: {question['question']}")
            
            if question["type"] == "multiple_choice":
                for j, option in enumerate(question["options"]):
                    print(f"{chr(65+j)}. {option}")
                
                user_answer = input("Your answer (A/B/C/D): ").upper().strip()
                correct_index = question["correct_answer"]
                correct_letter = chr(65 + correct_index)
                
                is_correct = user_answer == correct_letter
                
            elif question["type"] == "true_false":
                user_answer = input("True or False (T/F): ").upper().strip()
                is_correct = (user_answer == "T" and question["correct_answer"]) or \
                           (user_answer == "F" and not question["correct_answer"])
                
            else:  # short_answer
                user_answer = input("Your answer: ").strip()
                is_correct = self._check_short_answer(user_answer, question["correct_answer"])
            
            if is_correct:
                print("Correct!")
                results["correct_answers"] += 1
            else:
                print(f"Incorrect. {question.get('explanation', '')}")
            
            results["answers"].append({
                "question": question["question"],
                "user_answer": user_answer,
                "correct": is_correct
            })
        
        results["score"] = (results["correct_answers"] / results["total_questions"]) * 100
        
        print(f"\nQuiz completed!")
        print(f"Score: {results['score']:.1f}% ({results['correct_answers']}/{results['total_questions']})")
        
        return results
    
    def _assess_difficulty(self, content: str) -> str:
        """Assess content difficulty level"""
        word_count = len(content.split())
        if word_count < 200:
            return "beginner"
        elif word_count < 500:
            return "intermediate"
        else:
            return "advanced"
    
    def _check_short_answer(self, user_answer: str, correct_answer: str) -> bool:
        """Check if short answer is approximately correct"""
        user_words = set(user_answer.lower().split())
        correct_words = set(correct_answer.lower().split())
        
        overlap = len(user_words.intersection(correct_words))
        return overlap >= len(correct_words) * 0.6  # 60% word overlap
    
    def save_quiz_results(self, results: Dict):
        """Save quiz results to database"""
        try:
            # Implementation would save to database
            self.logger.info(f"Quiz results saved: {results['score']:.1f}%")
        except Exception as e:
            self.logger.error(f"Failed to save quiz results: {e}")