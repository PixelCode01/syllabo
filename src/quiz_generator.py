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
            prompt = f"""Create {num_questions} quiz questions based on this specific content: "{content}"

IMPORTANT: Respond ONLY with valid JSON in this exact format:
{{
    "questions": [
        {{
            "question": "What is pandas in Python?",
            "type": "multiple_choice",
            "options": ["A data analysis library", "A web framework", "A game engine", "An image editor"],
            "correct_answer": 0,
            "explanation": "Pandas is a powerful data analysis and manipulation library for Python"
        }}
    ]
}}

Requirements:
- Generate exactly {num_questions} questions SPECIFICALLY about: {content}
- Base questions on the actual content provided, not generic topics
- Use types: multiple_choice, true_false, short_answer
- For multiple_choice: provide 4 options and correct_answer index (0-3)
- For true_false: set correct_answer to true or false
- For short_answer: provide expected answer as string
- Questions must be directly related to "{content}"
- NO extra text, ONLY JSON"""
            
            response = await self.ai_client.get_completion(prompt)
            
            # Try to parse JSON response with improved error handling
            if response and response.strip():
                # Clean up the response - sometimes AI adds extra text
                response = response.strip()
                
                # Multiple strategies to extract JSON
                json_content = self._extract_json_from_response(response)
                
                if json_content:
                    try:
                        quiz_data = json.loads(json_content)
                        questions = quiz_data.get("questions", [])
                        
                        if questions and len(questions) > 0:
                            # Validate and clean questions
                            valid_questions = []
                            for q in questions[:num_questions]:
                                if self._validate_question(q):
                                    valid_questions.append(q)
                            
                            if valid_questions:
                                quiz = {
                                    "title": f"Quiz: {topic}",
                                    "topic": topic,
                                    "questions": valid_questions,
                                    "created_at": datetime.now().isoformat(),
                                    "difficulty": self._assess_difficulty(content)
                                }
                                return quiz
                        
                    except json.JSONDecodeError as je:
                        self.logger.error(f"JSON parsing error: {je}")
                        self.logger.debug(f"Problematic JSON content: {json_content[:200]}...")
                
                # If JSON parsing fails, try to extract questions from text
                self.logger.warning("JSON parsing failed, attempting text extraction")
                extracted_quiz = self._extract_quiz_from_text(response, topic, num_questions)
                if extracted_quiz:
                    return extracted_quiz
                
                raise ValueError("Could not parse AI response")
                
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
                },
                {
                    "question": "Which type of learning uses rewards and punishments?",
                    "type": "multiple_choice",
                    "options": ["Supervised learning", "Unsupervised learning", "Reinforcement learning", "Semi-supervised learning"],
                    "correct_answer": 2,
                    "explanation": "Reinforcement learning uses rewards and punishments to learn optimal actions."
                },
                {
                    "question": "Feature engineering is important in machine learning.",
                    "type": "true_false",
                    "correct_answer": True,
                    "explanation": "Feature engineering helps improve model performance by creating better input features."
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
        
        # Find matching questions based on both content and topic
        content_lower = content.lower() if content else ""
        topic_lower = topic.lower()
        search_text = f"{content_lower} {topic_lower}".strip()
        selected_questions = []
        
        # Look for exact or partial matches in content first, then topic
        for template_topic, questions in quiz_templates.items():
            # Check if template topic matches the content or topic
            if (template_topic in search_text or 
                any(word in search_text for word in template_topic.split())):
                selected_questions.extend(questions)
                break  # Use first match to avoid mixing different topics
        
        # If no specific match, try broader keyword matching
        if not selected_questions:
            for template_topic, questions in quiz_templates.items():
                topic_keywords = template_topic.split()
                if any(keyword in search_text for keyword in topic_keywords):
                    selected_questions.extend(questions)
                    break
        
        # If still no match, create content-specific questions
        if not selected_questions:
            selected_questions = self._create_content_based_questions(content, topic, num_questions)
        
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
    
    def _validate_question(self, question: Dict) -> bool:
        """Validate that a question has all required fields"""
        required_fields = ['question', 'type']
        
        for field in required_fields:
            if field not in question or not question[field]:
                return False
        
        question_type = question.get('type', '')
        
        if question_type == 'multiple_choice':
            options = question.get('options', [])
            correct_answer = question.get('correct_answer')
            
            if not options or len(options) < 2:
                return False
            if correct_answer is None or correct_answer < 0 or correct_answer >= len(options):
                return False
                
        elif question_type == 'true_false':
            correct_answer = question.get('correct_answer')
            if correct_answer is None or not isinstance(correct_answer, bool):
                return False
                
        elif question_type == 'short_answer':
            correct_answer = question.get('correct_answer')
            if not correct_answer or not isinstance(correct_answer, str):
                return False
        else:
            return False
        
        return True
    
    def _extract_json_from_response(self, response: str) -> str:
        """Extract JSON content from AI response using multiple strategies"""
        # Strategy 1: Find complete JSON object
        start_idx = response.find('{')
        if start_idx != -1:
            brace_count = 0
            end_idx = start_idx
            
            for i, char in enumerate(response[start_idx:], start_idx):
                if char == '{':
                    brace_count += 1
                elif char == '}':
                    brace_count -= 1
                    if brace_count == 0:
                        end_idx = i + 1
                        break
            
            if brace_count == 0:
                json_content = response[start_idx:end_idx]
                # Basic validation
                if json_content.count('{') == json_content.count('}'):
                    return json_content
        
        # Strategy 2: Look for JSON between code blocks
        import re
        json_blocks = re.findall(r'```(?:json)?\s*(\{.*?\})\s*```', response, re.DOTALL)
        if json_blocks:
            return json_blocks[0]
        
        # Strategy 3: Clean up common AI response issues
        cleaned = response.replace('```json', '').replace('```', '').strip()
        if cleaned.startswith('{') and cleaned.endswith('}'):
            return cleaned
        
        return None
    
    def _extract_quiz_from_text(self, response: str, topic: str, num_questions: int) -> Dict:
        """Extract quiz questions from plain text response when JSON parsing fails"""
        import re
        
        questions = []
        
        # Look for question patterns in the text
        question_patterns = [
            r'(?:Question \d+:|Q\d+:|\d+\.)\s*(.+?)(?=Question \d+:|Q\d+:|\d+\.|$)',
            r'(.+\?)',  # Lines ending with question marks
        ]
        
        for pattern in question_patterns:
            matches = re.findall(pattern, response, re.DOTALL | re.IGNORECASE)
            for match in matches:
                question_text = match.strip()
                if len(question_text) > 10 and '?' in question_text:
                    # Create a simple multiple choice question
                    question = {
                        "question": question_text,
                        "type": "multiple_choice",
                        "options": ["Option A", "Option B", "Option C", "Option D"],
                        "correct_answer": 0,
                        "explanation": "This question was extracted from AI response text."
                    }
                    questions.append(question)
                    
                    if len(questions) >= num_questions:
                        break
            
            if questions:
                break
        
        # If no questions found, create template questions
        if not questions:
            self.logger.warning("No questions extracted from text, using template")
            return self._generate_template_quiz(topic, num_questions, response)
        
        return {
            "title": f"Quiz: {topic}",
            "topic": topic,
            "questions": questions[:num_questions],
            "created_at": datetime.now().isoformat(),
            "difficulty": self._assess_difficulty(response)
        }
    
    def _create_content_based_questions(self, content: str, topic: str, num_questions: int) -> List[Dict]:
        """Create questions based on the actual content provided"""
        questions = []
        content_lower = content.lower() if content else ""
        
        # Analyze content for specific technologies/concepts
        if "pandas" in content_lower:
            questions.extend([
                {
                    "question": "What is pandas primarily used for in Python?",
                    "type": "multiple_choice",
                    "options": ["Data analysis and manipulation", "Web development", "Game development", "Mobile app development"],
                    "correct_answer": 0,
                    "explanation": "Pandas is a powerful library for data analysis and manipulation in Python."
                },
                {
                    "question": "Pandas DataFrames can handle multiple data types in different columns.",
                    "type": "true_false",
                    "correct_answer": True,
                    "explanation": "DataFrames can store different data types (integers, floats, strings, etc.) in different columns."
                }
            ])
        elif "numpy" in content_lower:
            questions.extend([
                {
                    "question": "What does NumPy primarily provide for Python?",
                    "type": "multiple_choice",
                    "options": ["Web frameworks", "Numerical computing capabilities", "Database connections", "GUI development"],
                    "correct_answer": 1,
                    "explanation": "NumPy provides powerful numerical computing capabilities with efficient array operations."
                }
            ])
        elif "python" in content_lower:
            questions.extend([
                {
                    "question": "Python is known for its readability and simplicity.",
                    "type": "true_false",
                    "correct_answer": True,
                    "explanation": "Python's syntax is designed to be readable and straightforward, making it beginner-friendly."
                },
                {
                    "question": "What type of programming language is Python?",
                    "type": "multiple_choice",
                    "options": ["Compiled only", "Interpreted", "Assembly", "Machine code"],
                    "correct_answer": 1,
                    "explanation": "Python is an interpreted language, meaning code is executed line by line at runtime."
                }
            ])
        
        # If no specific content match, create generic but relevant questions
        if not questions:
            questions = [
                {
                    "question": f"What is the main focus when studying {content or topic}?",
                    "type": "multiple_choice",
                    "options": ["Understanding core concepts", "Memorizing syntax only", "Avoiding practice", "Skipping documentation"],
                    "correct_answer": 0,
                    "explanation": f"Understanding core concepts is essential when learning {content or topic}."
                },
                {
                    "question": f"Practical experience is important when learning {content or topic}.",
                    "type": "true_false",
                    "correct_answer": True,
                    "explanation": f"Hands-on practice helps solidify understanding of {content or topic}."
                }
            ]
        
        return questions[:num_questions]
    
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