#!/usr/bin/env python3
"""
Persistent Quiz Manager - Create and store quizzes based on actual resources
Addresses user feedback about quiz persistence and resource-based generation
"""

import os
import json
import uuid
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from pathlib import Path
from .logger import SyllaboLogger
from .ai_client import AIClient

class PersistentQuizManager:
    """Enhanced quiz manager with persistent storage and resource-based generation"""
    
    def __init__(self, ai_client: AIClient, data_dir: str = "data"):
        self.ai_client = ai_client
        self.data_dir = Path(data_dir)
        self.quizzes_dir = self.data_dir / "quizzes"
        self.results_dir = self.data_dir / "quiz_results"
        self.logger = SyllaboLogger("persistent_quiz_manager")
        
        # Create directories
        self.quizzes_dir.mkdir(parents=True, exist_ok=True)
        self.results_dir.mkdir(parents=True, exist_ok=True)
    
    async def create_quiz_from_resources(self, topic: str, resources: Dict, 
                                       num_questions: int = 10, 
                                       difficulty: str = 'mixed') -> Dict:
        """Create a quiz based on actual recommended resources"""
        quiz_id = str(uuid.uuid4())
        
        # Extract content from resources for quiz generation
        resource_content = self._extract_resource_content(resources)
        
        # Generate quiz using AI with resource-specific content
        quiz_data = await self._generate_resource_based_quiz(
            topic, resource_content, num_questions, difficulty
        )
        
        # Add metadata
        quiz_data.update({
            'id': quiz_id,
            'topic': topic,
            'created_at': datetime.now().isoformat(),
            'difficulty': difficulty,
            'source_resources': self._get_resource_summary(resources),
            'total_questions': len(quiz_data.get('questions', [])),
            'estimated_time': len(quiz_data.get('questions', [])) * 2,  # 2 minutes per question
            'attempts': [],
            'best_score': 0
        })
        
        # Save quiz persistently
        quiz_file = self.quizzes_dir / f"{quiz_id}.json"
        with open(quiz_file, 'w', encoding='utf-8') as f:
            json.dump(quiz_data, f, indent=2, ensure_ascii=False)
        
        self.logger.info(f"Created quiz '{quiz_data.get('title')}' with {len(quiz_data.get('questions', []))} questions")
        return quiz_data
    
    async def create_quiz_from_video_content(self, video_info: Dict, 
                                           num_questions: int = 5) -> Dict:
        """Create a quiz specifically from a YouTube video's content"""
        quiz_id = str(uuid.uuid4())
        
        # Use video title, description, and transcript if available
        video_content = f"""
        Video Title: {video_info.get('title', '')}
        Channel: {video_info.get('channel', '')}
        Description: {video_info.get('description', '')}
        Duration: {video_info.get('duration', '')}
        """
        
        # Add transcript if available
        if video_info.get('transcript'):
            video_content += f"\nTranscript: {video_info['transcript'][:2000]}..."
        
        quiz_data = await self._generate_video_based_quiz(
            video_info.get('title', 'Video Content'), 
            video_content, 
            num_questions
        )
        
        # Add metadata
        quiz_data.update({
            'id': quiz_id,
            'created_at': datetime.now().isoformat(),
            'source_video': {
                'title': video_info.get('title'),
                'channel': video_info.get('channel'),
                'url': video_info.get('direct_link'),
                'duration': video_info.get('duration')
            },
            'total_questions': len(quiz_data.get('questions', [])),
            'attempts': [],
            'best_score': 0
        })
        
        # Save quiz
        quiz_file = self.quizzes_dir / f"{quiz_id}.json"
        with open(quiz_file, 'w', encoding='utf-8') as f:
            json.dump(quiz_data, f, indent=2, ensure_ascii=False)
        
        return quiz_data
    
    def get_saved_quizzes(self, topic: Optional[str] = None) -> List[Dict]:
        """Get list of saved quizzes"""
        quizzes = []
        
        for quiz_file in self.quizzes_dir.glob("*.json"):
            try:
                with open(quiz_file, 'r', encoding='utf-8') as f:
                    quiz_data = json.load(f)
                
                if topic is None or topic.lower() in quiz_data.get('topic', '').lower():
                    # Create summary info
                    quiz_summary = {
                        'id': quiz_data.get('id'),
                        'title': quiz_data.get('title', 'Untitled Quiz'),
                        'topic': quiz_data.get('topic', 'Unknown'),
                        'created_at': quiz_data.get('created_at', ''),
                        'total_questions': quiz_data.get('total_questions', 0),
                        'difficulty': quiz_data.get('difficulty', 'mixed'),
                        'attempts': len(quiz_data.get('attempts', [])),
                        'best_score': quiz_data.get('best_score', 0),
                        'estimated_time': quiz_data.get('estimated_time', 0),
                        'source_type': 'resources' if 'source_resources' in quiz_data else 'video',
                        'file_path': str(quiz_file)
                    }
                    quizzes.append(quiz_summary)
            except Exception as e:
                self.logger.error(f"Error reading quiz {quiz_file}: {e}")
        
        return sorted(quizzes, key=lambda x: x['created_at'], reverse=True)
    
    def load_quiz(self, quiz_id: str) -> Optional[Dict]:
        """Load a specific quiz by ID"""
        quiz_file = self.quizzes_dir / f"{quiz_id}.json"
        
        if not quiz_file.exists():
            return None
        
        try:
            with open(quiz_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            self.logger.error(f"Error loading quiz {quiz_id}: {e}")
            return None
    
    def save_quiz_attempt(self, quiz_id: str, score: int, total_questions: int, 
                         answers: List[Dict], time_taken: int = 0) -> bool:
        """Save a quiz attempt result"""
        quiz_data = self.load_quiz(quiz_id)
        if not quiz_data:
            return False
        
        attempt = {
            'timestamp': datetime.now().isoformat(),
            'score': score,
            'total_questions': total_questions,
            'percentage': round((score / total_questions) * 100, 1),
            'time_taken_minutes': time_taken,
            'answers': answers
        }
        
        # Add attempt to quiz data
        if 'attempts' not in quiz_data:
            quiz_data['attempts'] = []
        
        quiz_data['attempts'].append(attempt)
        
        # Update best score
        current_percentage = attempt['percentage']
        if current_percentage > quiz_data.get('best_score', 0):
            quiz_data['best_score'] = current_percentage
        
        # Save updated quiz data
        quiz_file = self.quizzes_dir / f"{quiz_id}.json"
        try:
            with open(quiz_file, 'w', encoding='utf-8') as f:
                json.dump(quiz_data, f, indent=2, ensure_ascii=False)
            
            # Also save detailed results
            self._save_detailed_results(quiz_id, attempt)
            return True
        except Exception as e:
            self.logger.error(f"Error saving quiz attempt: {e}")
            return False
    
    def get_quiz_statistics(self, quiz_id: str) -> Optional[Dict]:
        """Get detailed statistics for a quiz"""
        quiz_data = self.load_quiz(quiz_id)
        if not quiz_data:
            return None
        
        attempts = quiz_data.get('attempts', [])
        if not attempts:
            return {
                'quiz_title': quiz_data.get('title', 'Unknown'),
                'total_attempts': 0,
                'best_score': 0,
                'average_score': 0,
                'improvement_trend': 'No attempts yet'
            }
        
        scores = [attempt['percentage'] for attempt in attempts]
        
        return {
            'quiz_title': quiz_data.get('title', 'Unknown'),
            'total_attempts': len(attempts),
            'best_score': max(scores),
            'average_score': round(sum(scores) / len(scores), 1),
            'latest_score': scores[-1],
            'improvement_trend': self._calculate_improvement_trend(scores),
            'attempts_history': attempts[-5:],  # Last 5 attempts
            'created_at': quiz_data.get('created_at', ''),
            'source_info': quiz_data.get('source_resources', quiz_data.get('source_video', {}))
        }
    
    def delete_quiz(self, quiz_id: str) -> bool:
        """Delete a saved quiz"""
        quiz_file = self.quizzes_dir / f"{quiz_id}.json"
        
        try:
            if quiz_file.exists():
                quiz_file.unlink()
                
                # Also delete results file if it exists
                results_file = self.results_dir / f"{quiz_id}_results.json"
                if results_file.exists():
                    results_file.unlink()
                
                return True
        except Exception as e:
            self.logger.error(f"Error deleting quiz {quiz_id}: {e}")
        
        return False
    
    async def _generate_resource_based_quiz(self, topic: str, resource_content: str, 
                                          num_questions: int, difficulty: str) -> Dict:
        """Generate quiz questions based on resource content"""
        difficulty_instructions = {
            'easy': "Focus on basic concepts and definitions. Use simple multiple choice questions.",
            'medium': "Include both conceptual and application questions. Mix question types.",
            'hard': "Focus on advanced concepts, analysis, and problem-solving. Include complex scenarios.",
            'mixed': "Include a mix of easy, medium, and hard questions covering various aspects."
        }
        
        prompt = f"""Create a comprehensive quiz about "{topic}" based on the following learning resources and content:

{resource_content[:3000]}

Requirements:
- Generate exactly {num_questions} questions
- Difficulty level: {difficulty} - {difficulty_instructions.get(difficulty, '')}
- Include a mix of question types: multiple choice, true/false, and short answer
- Base questions directly on the content and resources provided
- Make questions practical and applicable to real learning scenarios

For each question, provide:
1. Question text
2. Question type (multiple_choice, true_false, or short_answer)
3. Options (for multiple choice)
4. Correct answer
5. Explanation of why the answer is correct
6. Reference to which resource this relates to (if applicable)

Format as JSON with this structure:
{{
    "title": "Quiz title based on topic",
    "description": "Brief description of what this quiz covers",
    "questions": [
        {{
            "question": "Question text",
            "type": "multiple_choice|true_false|short_answer",
            "options": ["Option 1", "Option 2", "Option 3", "Option 4"],
            "correct_answer": "correct answer or index",
            "explanation": "Why this answer is correct",
            "resource_reference": "Which resource this relates to",
            "difficulty": "easy|medium|hard"
        }}
    ]
}}

Make sure questions test understanding of the actual content from the resources provided."""
        
        try:
            response = await self.ai_client.get_completion(prompt)
            
            # Try to parse JSON response
            import re
            json_match = re.search(r'\{.*\}', response, re.DOTALL)
            if json_match:
                quiz_data = json.loads(json_match.group())
                return quiz_data
            else:
                # Fallback: create basic quiz structure
                return self._create_fallback_quiz(topic, num_questions)
                
        except Exception as e:
            self.logger.error(f"Error generating resource-based quiz: {e}")
            return self._create_fallback_quiz(topic, num_questions)
    
    async def _generate_video_based_quiz(self, video_title: str, video_content: str, 
                                       num_questions: int) -> Dict:
        """Generate quiz specifically from video content"""
        prompt = f"""Create a quiz based on this YouTube video content:

Video: {video_title}
Content: {video_content[:2000]}

Generate {num_questions} questions that test understanding of the video content.
Include practical questions that someone would need to know after watching this video.

Format as JSON:
{{
    "title": "Quiz: {video_title}",
    "description": "Test your understanding of this video",
    "questions": [
        {{
            "question": "Question text",
            "type": "multiple_choice|true_false|short_answer",
            "options": ["Option 1", "Option 2", "Option 3", "Option 4"],
            "correct_answer": "correct answer",
            "explanation": "Explanation based on video content"
        }}
    ]
}}"""
        
        try:
            response = await self.ai_client.get_completion(prompt)
            
            import re
            json_match = re.search(r'\{.*\}', response, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
            else:
                return self._create_fallback_video_quiz(video_title, num_questions)
                
        except Exception as e:
            self.logger.error(f"Error generating video-based quiz: {e}")
            return self._create_fallback_video_quiz(video_title, num_questions)
    
    def _extract_resource_content(self, resources: Dict) -> str:
        """Extract relevant content from resources for quiz generation"""
        content_parts = []
        
        # Extract from videos
        if 'videos' in resources:
            content_parts.append("RECOMMENDED VIDEOS:")
            for video in resources['videos'][:3]:  # Top 3 videos
                content_parts.append(f"- {video.get('title', '')}")
                content_parts.append(f"  Channel: {video.get('channel', '')}")
                content_parts.append(f"  Description: {video.get('description', '')[:200]}")
                if video.get('transcript'):
                    content_parts.append(f"  Key content: {video['transcript'][:300]}")
        
        # Extract from playlists
        if 'playlists' in resources:
            content_parts.append("\nRECOMMENDED PLAYLISTS:")
            for playlist in resources['playlists'][:2]:  # Top 2 playlists
                content_parts.append(f"- {playlist.get('title', '')}")
                content_parts.append(f"  Channel: {playlist.get('channel', '')}")
                content_parts.append(f"  Videos: {playlist.get('video_count', 0)}")
        
        # Extract from books
        if 'books' in resources:
            content_parts.append("\nRECOMMENDED BOOKS:")
            for book in resources['books'][:3]:  # Top 3 books
                content_parts.append(f"- {book.get('title', '')} by {book.get('author', '')}")
                content_parts.append(f"  Topics: {', '.join(book.get('topics', []))}")
        
        # Extract from courses
        if 'courses' in resources:
            content_parts.append("\nRECOMMENDED COURSES:")
            for course in resources['courses'][:3]:  # Top 3 courses
                content_parts.append(f"- {course.get('title', '')} on {course.get('platform', '')}")
                content_parts.append(f"  Topics: {', '.join(course.get('topics', []))}")
        
        return "\n".join(content_parts)
    
    def _get_resource_summary(self, resources: Dict) -> Dict:
        """Create a summary of resources used for quiz generation"""
        summary = {}
        
        for resource_type in ['videos', 'playlists', 'books', 'courses']:
            if resource_type in resources and resources[resource_type]:
                summary[resource_type] = []
                for resource in resources[resource_type][:3]:  # Top 3 of each type
                    summary[resource_type].append({
                        'title': resource.get('title', ''),
                        'author_channel': resource.get('channel', resource.get('author', '')),
                        'link': resource.get('direct_link', resource.get('amazon_search', ''))
                    })
        
        return summary
    
    def _create_fallback_quiz(self, topic: str, num_questions: int) -> Dict:
        """Create a basic fallback quiz when AI generation fails"""
        questions = []
        
        for i in range(min(num_questions, 5)):  # Max 5 fallback questions
            questions.append({
                'question': f'What is an important concept to understand about {topic}?',
                'type': 'short_answer',
                'correct_answer': f'Key concepts related to {topic}',
                'explanation': f'This tests basic understanding of {topic}',
                'difficulty': 'medium'
            })
        
        return {
            'title': f'{topic} - Basic Quiz',
            'description': f'Basic quiz covering {topic} fundamentals',
            'questions': questions
        }
    
    def _create_fallback_video_quiz(self, video_title: str, num_questions: int) -> Dict:
        """Create fallback quiz for video content"""
        questions = []
        
        for i in range(min(num_questions, 3)):
            questions.append({
                'question': f'What was covered in the video "{video_title}"?',
                'type': 'short_answer',
                'correct_answer': 'Main concepts from the video',
                'explanation': 'This tests understanding of the video content'
            })
        
        return {
            'title': f'Quiz: {video_title}',
            'description': 'Test your understanding of this video',
            'questions': questions
        }
    
    def _save_detailed_results(self, quiz_id: str, attempt: Dict):
        """Save detailed quiz results for analysis"""
        results_file = self.results_dir / f"{quiz_id}_results.json"
        
        try:
            # Load existing results or create new
            if results_file.exists():
                with open(results_file, 'r', encoding='utf-8') as f:
                    results_data = json.load(f)
            else:
                results_data = {'quiz_id': quiz_id, 'attempts': []}
            
            results_data['attempts'].append(attempt)
            
            # Save updated results
            with open(results_file, 'w', encoding='utf-8') as f:
                json.dump(results_data, f, indent=2, ensure_ascii=False)
                
        except Exception as e:
            self.logger.error(f"Error saving detailed results: {e}")
    
    def _calculate_improvement_trend(self, scores: List[float]) -> str:
        """Calculate if scores are improving over time"""
        if len(scores) < 2:
            return "Not enough data"
        
        recent_avg = sum(scores[-3:]) / len(scores[-3:])  # Last 3 attempts
        early_avg = sum(scores[:3]) / len(scores[:3])     # First 3 attempts
        
        if recent_avg > early_avg + 5:
            return "Improving"
        elif recent_avg < early_avg - 5:
            return "Declining"
        else:
            return "Stable"