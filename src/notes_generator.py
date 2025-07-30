import asyncio
from typing import List, Dict, Optional
from .ai_client import AIClient

class NotesGenerator:
    def __init__(self, ai_client: AIClient):
        self.ai_client = ai_client
    
    async def generate_study_notes(self, topic: str, video_data: Dict, transcript: Optional[str] = None) -> Dict:
        """Generate comprehensive study notes for a topic and video"""
        
        # Create content summary for AI
        content_parts = [
            f"Topic: {topic}",
            f"Video Title: {video_data.get('title', '')}",
            f"Channel: {video_data.get('channel', '')}",
        ]
        
        if video_data.get('description'):
            content_parts.append(f"Description: {video_data['description'][:500]}")
        
        if transcript:
            # Use first part of transcript for better context
            transcript_sample = transcript[:1200] if len(transcript) > 1200 else transcript
            content_parts.append(f"Video Content: {transcript_sample}")
        
        content = "\n".join(content_parts)
        
        # Generate notes and questions concurrently
        notes_task = self._generate_notes(content, topic)
        questions_task = self._generate_questions(content, topic)
        key_concepts_task = self._extract_key_concepts(content, topic)
        
        notes, questions, key_concepts = await asyncio.gather(
            notes_task, questions_task, key_concepts_task
        )
        
        return {
            'topic': topic,
            'video_title': video_data.get('title', ''),
            'video_id': video_data.get('id', ''),
            'notes': notes,
            'questions': questions,
            'key_concepts': key_concepts,
            'study_tips': self._generate_study_tips(topic)
        }
    
    async def _generate_notes(self, content: str, topic: str) -> List[str]:
        """Generate structured study notes"""
        prompt = f"""Based on this educational content about "{topic}", create concise study notes.

Content:
{content}

Generate 5-8 key study notes that capture the most important information. Each note should be:
- One clear, complete sentence
- Focused on essential concepts
- Easy to remember and review

Format as a simple list, one note per line."""

        try:
            response = await self.ai_client.get_completion(prompt)
            
            # Parse response into list
            notes = []
            for line in response.split('\n'):
                line = line.strip()
                if line and not line.startswith('#') and len(line) > 10:
                    # Remove bullet points and numbering
                    clean_line = line.lstrip('•-*123456789. ')
                    if clean_line:
                        notes.append(clean_line)
            
            return notes[:8] if notes else [f"Key concepts related to {topic} are covered in this video."]
            
        except Exception as e:
            return [
                f"This video covers important concepts related to {topic}.",
                "Review the main points discussed in the video content.",
                "Practice applying the concepts shown in examples.",
                "Take notes on key terminology and definitions."
            ]
    
    async def _generate_questions(self, content: str, topic: str) -> List[str]:
        """Generate study questions for review"""
        prompt = f"""Based on this educational content about "{topic}", create study questions that help with learning and retention.

Content:
{content}

Generate 6-10 study questions that:
- Test understanding of key concepts
- Encourage critical thinking
- Help with memorization and review
- Range from basic recall to application

Format as questions, one per line."""

        try:
            response = await self.ai_client.get_completion(prompt)
            
            # Parse response into questions
            questions = []
            for line in response.split('\n'):
                line = line.strip()
                if line and ('?' in line or line.lower().startswith(('what', 'how', 'why', 'when', 'where', 'which', 'explain', 'describe', 'define'))):
                    # Clean up formatting
                    clean_question = line.lstrip('•-*123456789. ')
                    if not clean_question.endswith('?') and not clean_question.lower().startswith(('explain', 'describe', 'define')):
                        clean_question += '?'
                    questions.append(clean_question)
            
            return questions[:10] if questions else [
                f"What are the main concepts covered in this {topic} video?",
                f"How can you apply the {topic} principles shown?",
                f"What are the key benefits of understanding {topic}?",
                "Can you explain the main points in your own words?"
            ]
            
        except Exception as e:
            return [
                f"What are the main concepts covered in this {topic} video?",
                f"How does this relate to other {topic} concepts you've learned?",
                "What are the practical applications of this knowledge?",
                "Can you summarize the key points in your own words?",
                "What questions do you still have about this topic?"
            ]
    
    async def _extract_key_concepts(self, content: str, topic: str) -> List[str]:
        """Extract key concepts and terminology"""
        prompt = f"""From this educational content about "{topic}", identify the most important concepts and terms.

Content:
{content}

List 4-6 key concepts or terms that students should remember. Each should be:
- A specific concept, principle, or important term
- Essential for understanding {topic}
- Clearly defined or explained

Format as a simple list."""

        try:
            response = await self.ai_client.get_completion(prompt)
            
            concepts = []
            for line in response.split('\n'):
                line = line.strip()
                if line and len(line) > 3 and not line.startswith('#'):
                    clean_concept = line.lstrip('•-*123456789. ')
                    if clean_concept and len(clean_concept) < 100:
                        concepts.append(clean_concept)
            
            return concepts[:6] if concepts else [
                f"Core {topic} principles",
                f"Key {topic} terminology",
                f"Important {topic} applications",
                f"Fundamental {topic} concepts"
            ]
            
        except Exception as e:
            return [
                f"Core {topic} principles",
                f"Key {topic} terminology", 
                f"Practical {topic} applications"
            ]
    
    def _generate_study_tips(self, topic: str) -> List[str]:
        """Generate general study tips for the topic"""
        return [
            f"Review the {topic} concepts regularly to reinforce learning",
            "Practice explaining the concepts in your own words",
            "Look for real-world examples and applications",
            "Create connections between this topic and related subjects",
            "Test your understanding with the generated questions"
        ]
    
    async def generate_topic_summary(self, topic: str, videos: List[Dict]) -> Dict:
        """Generate a comprehensive summary for a topic based on multiple videos"""
        if not videos:
            return {
                'topic': topic,
                'summary': f"No videos found for {topic}",
                'learning_objectives': [],
                'recommended_order': []
            }
        
        # Create summary of all videos for this topic
        video_summaries = []
        for video in videos[:5]:  # Limit to top 5 videos
            video_summaries.append(f"- {video['title']} by {video['channel']}")
        
        videos_text = "\n".join(video_summaries)
        
        prompt = f"""Based on these educational videos about "{topic}", create a learning summary.

Videos:
{videos_text}

Provide:
1. A brief overview of what students will learn about {topic}
2. 3-4 key learning objectives
3. Suggested order for watching videos (if applicable)

Keep it concise and focused on learning outcomes."""

        try:
            response = await self.ai_client.get_completion(prompt)
            
            # Parse the response
            lines = response.split('\n')
            summary = ""
            objectives = []
            order = []
            
            current_section = "summary"
            for line in lines:
                line = line.strip()
                if not line:
                    continue
                
                if "objective" in line.lower() or "learn" in line.lower():
                    current_section = "objectives"
                elif "order" in line.lower() or "sequence" in line.lower():
                    current_section = "order"
                elif line.startswith('-') or line.startswith('•'):
                    clean_line = line.lstrip('-•').strip()
                    if current_section == "objectives":
                        objectives.append(clean_line)
                    elif current_section == "order":
                        order.append(clean_line)
                elif current_section == "summary" and len(line) > 20:
                    summary += line + " "
            
            return {
                'topic': topic,
                'summary': summary.strip() or f"Comprehensive learning materials for {topic}",
                'learning_objectives': objectives[:4] if objectives else [
                    f"Understand fundamental {topic} concepts",
                    f"Learn practical {topic} applications",
                    f"Develop {topic} problem-solving skills"
                ],
                'recommended_order': order[:3] if order else [
                    "Start with introductory videos",
                    "Progress to intermediate concepts", 
                    "Practice with advanced examples"
                ]
            }
            
        except Exception as e:
            return {
                'topic': topic,
                'summary': f"Comprehensive learning materials for {topic} with {len(videos)} educational videos",
                'learning_objectives': [
                    f"Understand fundamental {topic} concepts",
                    f"Learn practical {topic} applications", 
                    f"Develop {topic} problem-solving skills"
                ],
                'recommended_order': [
                    "Start with introductory videos",
                    "Progress to intermediate concepts",
                    "Practice with advanced examples"
                ]
            }