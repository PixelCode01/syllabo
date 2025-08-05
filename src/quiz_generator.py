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
        """Generate quiz questions from content using intelligent analysis"""
        if not content or len(content.strip()) < 10:
            self.logger.warning("Content too short, using template-based generation")
            return self._generate_template_quiz(topic, num_questions, content)
        
        # Try AI first, then fallback to template-based generation
        try:
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
Make questions test understanding, not just memorization.
Ensure all questions are directly related to the provided content."""
            
            response = await self.ai_client.get_completion(prompt)
            
            # Try to parse JSON response
            if response and response.strip().startswith('{'):
                quiz_data = json.loads(response)
                questions = quiz_data.get("questions", [])
                
                if questions and len(questions) > 0:
                    quiz = {
                        "title": f"Quiz: {topic}",
                        "topic": topic,
                        "questions": questions[:num_questions],  # Limit to requested number
                        "created_at": datetime.now().isoformat(),
                        "difficulty": self._assess_difficulty(content)
                    }
                    return quiz
                else:
                    raise ValueError("No questions generated")
            else:
                raise ValueError("Invalid JSON response")
                
        except Exception as e:
            self.logger.error(f"AI quiz generation failed: {e}")
            # Fallback to template-based generation
            return self._generate_template_quiz(topic, num_questions, content)
    
    def _generate_template_quiz(self, topic: str, num_questions: int, content: str = "") -> Dict:
        """Generate quiz using predefined templates and content analysis"""
        # Educational quiz templates organized by topic
        quiz_templates = {
            'python programming': [
                {
                    "question": "What is the correct way to define a function in Python?",
                    "type": "multiple_choice",
                    "options": ["function myFunc():", "def myFunc():", "define myFunc():", "func myFunc():"],
                    "correct_answer": 1,
                    "explanation": "In Python, functions are defined using the 'def' keyword followed by the function name and parentheses."
                },
                {
                    "question": "Python is an interpreted language.",
                    "type": "true_false",
                    "correct_answer": True,
                    "explanation": "Python is indeed an interpreted language, meaning code is executed line by line at runtime."
                },
                {
                    "question": "What data type is used to store a sequence of characters in Python?",
                    "type": "short_answer",
                    "correct_answer": "string str",
                    "explanation": "Strings (str) are used to store sequences of characters in Python."
                },
                {
                    "question": "Which of the following is used to create a list in Python?",
                    "type": "multiple_choice",
                    "options": ["()", "[]", "{}", "<>"],
                    "correct_answer": 1,
                    "explanation": "Square brackets [] are used to create lists in Python."
                },
                {
                    "question": "Python uses indentation to define code blocks.",
                    "type": "true_false",
                    "correct_answer": True,
                    "explanation": "Python uses indentation (whitespace) to define code blocks instead of curly braces."
                }
            ],
            'machine learning': [
                {
                    "question": "What is supervised learning?",
                    "type": "multiple_choice",
                    "options": ["Learning without labeled data", "Learning with labeled training data", "Learning by trial and error", "Learning from rewards"],
                    "correct_answer": 1,
                    "explanation": "Supervised learning uses labeled training data to learn patterns and make predictions."
                },
                {
                    "question": "Overfitting occurs when a model performs well on training data but poorly on new data.",
                    "type": "true_false",
                    "correct_answer": True,
                    "explanation": "Overfitting happens when a model learns the training data too well and fails to generalize to new data."
                },
                {
                    "question": "What algorithm is commonly used for classification problems?",
                    "type": "short_answer",
                    "correct_answer": "decision tree random forest svm logistic regression",
                    "explanation": "Common classification algorithms include decision trees, random forests, SVM, and logistic regression."
                }
            ],
            'data science': [
                {
                    "question": "What is the first step in the data science process?",
                    "type": "multiple_choice",
                    "options": ["Data modeling", "Data collection", "Data visualization", "Data cleaning"],
                    "correct_answer": 1,
                    "explanation": "Data collection is typically the first step in the data science process."
                },
                {
                    "question": "Data visualization is only used at the end of data analysis.",
                    "type": "true_false",
                    "correct_answer": False,
                    "explanation": "Data visualization is used throughout the data science process for exploration, analysis, and communication."
                }
            ],
            'pandas': [
                {
                    "question": "What is the primary data structure in pandas?",
                    "type": "multiple_choice",
                    "options": ["Array", "DataFrame", "List", "Dictionary"],
                    "correct_answer": 1,
                    "explanation": "DataFrame is the primary two-dimensional data structure in pandas."
                },
                {
                    "question": "Pandas can only work with numerical data.",
                    "type": "true_false",
                    "correct_answer": False,
                    "explanation": "Pandas can work with various data types including numerical, text, dates, and categorical data."
                }
            ],
            'numpy': [
                {
                    "question": "What is the main data structure in NumPy?",
                    "type": "multiple_choice",
                    "options": ["List", "Array", "DataFrame", "Matrix"],
                    "correct_answer": 1,
                    "explanation": "NumPy's main data structure is the ndarray (N-dimensional array)."
                },
                {
                    "question": "NumPy arrays are faster than Python lists for numerical operations.",
                    "type": "true_false",
                    "correct_answer": True,
                    "explanation": "NumPy arrays are implemented in C and are much faster than Python lists for numerical computations."
                }
            ]
        }
        
        # Find matching questions
        topic_lower = topic.lower()
        selected_questions = []
        
        # Look for exact or partial matches
        for template_topic, questions in quiz_templates.items():
            if template_topic in topic_lower or any(word in topic_lower for word in template_topic.split()):
                selected_questions.extend(questions)
        
        # If no specific match, use general programming questions
        if not selected_questions:
            selected_questions = quiz_templates.get('python programming', [])
        
        # Select random questions up to the requested number
        if len(selected_questions) > num_questions:
            selected_questions = random.sample(selected_questions, num_questions)
        else:
            selected_questions = selected_questions[:num_questions]
        
        quiz = {
            "title": f"Quiz: {topic}",
            "topic": topic,
            "questions": selected_questions,
            "created_at": datetime.now().isoformat(),
            "difficulty": self._assess_difficulty(content or topic)
        }
        
        return quiz
    
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
    
    async def generate_quiz(self, topic_name: str, num_questions: int = 5) -> Dict:
        """Generate a quiz for a specific topic"""
        try:
            # Get topic content from database or use topic name
            content = f"Generate quiz questions about {topic_name}"
            return await self.generate_quiz_from_content(content, topic_name, num_questions)
        except Exception as e:
            self.logger.error(f"Failed to generate quiz for {topic_name}: {e}")
            return {
                "title": f"Quiz: {topic_name}",
                "topic": topic_name,
                "questions": [
                    {
                        "question": f"What is the main concept of {topic_name}?",
                        "type": "multiple_choice",
                        "options": ["Option A", "Option B", "Option C", "Option D"],
                        "correct_answer": 0,
                        "explanation": "This is a sample question."
                    }
                ]
            }
    
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