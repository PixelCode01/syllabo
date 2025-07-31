import asyncio
from typing import List, Dict, Optional
from .ai_client import AIClient

class NotesGenerator:
    def __init__(self, ai_client: AIClient):
        self.ai_client = ai_client
    
    async def generate_optimal_study_materials(self, learning_path: Dict) -> Dict:
        """Generate study materials using the optimal learning path"""
        topic = learning_path['topic']
        primary_video = learning_path['primary_video']
        supplementary_videos = learning_path['supplementary_videos']
        
        if not primary_video:
            return {
                'topic': topic,
                'error': 'No videos available for this topic',
                'materials': {}
            }
        
        primary_materials = await self.generate_study_notes(topic, primary_video, None)
        
        supplementary_materials = []
        for video in supplementary_videos:
            materials = await self.generate_study_notes(topic, video, None)
            materials['coverage_type'] = video.get('coverage_type', 'supplementary')
            supplementary_materials.append(materials)
        
        study_guide = await self._create_comprehensive_guide(
            topic, primary_materials, supplementary_materials, learning_path
        )
        
        return {
            'topic': topic,
            'learning_strategy': learning_path['learning_strategy'],
            'primary_materials': primary_materials,
            'supplementary_materials': supplementary_materials,
            'comprehensive_guide': study_guide,
            'coverage_analysis': learning_path['coverage_analysis']
        }
    
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
  async def _create_comprehensive_guide(self, topic: str, primary_materials: Dict, 
                                        supplementary_materials: List[Dict], learning_path: Dict) -> Dict:
        """Create a comprehensive study guide combining all materials"""
        
        # Combine all key concepts
        all_concepts = primary_materials.get('key_concepts', [])
        for materials in supplementary_materials:
            all_concepts.extend(materials.get('key_concepts', []))
        
        # Remove duplicates while preserving order
        unique_concepts = []
        seen = set()
        for concept in all_concepts:
            if concept.lower() not in seen:
                unique_concepts.append(concept)
                seen.add(concept.lower())
        
        # Create study plan
        study_plan = self._create_study_plan(learning_path)
        
        # Generate comprehensive questions
        comprehensive_questions = await self._generate_comprehensive_questions(
            topic, primary_materials, supplementary_materials
        )
        
        return {
            'study_plan': study_plan,
            'key_concepts_summary': unique_concepts[:10],
            'comprehensive_questions': comprehensive_questions,
            'learning_objectives': self._extract_learning_objectives(topic, primary_materials, supplementary_materials),
            'study_tips': self._generate_advanced_study_tips(topic, learning_path)
        }
    
    def _create_study_plan(self, learning_path: Dict) -> List[Dict]:
        """Create a structured study plan"""
        plan = []
        coverage = learning_path.get('coverage_analysis', {})
        
        for i, item in enumerate(coverage.get('recommended_study_order', []), 1):
            video = item['video']
            plan.append({
                'step': i,
                'video_title': video['title'],
                'video_id': video['id'],
                'purpose': item['purpose'],
                'duration_minutes': item['duration_minutes'],
                'focus_areas': self._get_focus_areas(video),
                'study_method': self._recommend_study_method(video, item['purpose'])
            })
        
        return plan
    
    def _get_focus_areas(self, video: Dict) -> List[str]:
        """Extract focus areas from video"""
        title_lower = video['title'].lower()
        focus_areas = []
        
        if any(word in title_lower for word in ['concept', 'theory', 'principle']):
            focus_areas.append('Understand core concepts')
        
        if any(word in title_lower for word in ['example', 'practice', 'problem']):
            focus_areas.append('Work through examples')
        
        if any(word in title_lower for word in ['application', 'real world', 'use case']):
            focus_areas.append('Learn practical applications')
        
        if any(word in title_lower for word in ['advanced', 'complex', 'detailed']):
            focus_areas.append('Master advanced topics')
        
        return focus_areas if focus_areas else ['General understanding']
    
    def _recommend_study_method(self, video: Dict, purpose: str) -> str:
        """Recommend study method based on video type"""
        if 'Foundation' in purpose:
            return 'Watch actively, take detailed notes, pause to reflect'
        elif 'Practice' in purpose:
            return 'Follow along, try examples yourself, practice similar problems'
        elif 'Review' in purpose:
            return 'Quick watch for reinforcement, focus on key points'
        elif 'Tutorial' in purpose:
            return 'Follow step-by-step, implement alongside the video'
        elif 'Advanced' in purpose:
            return 'Watch carefully, connect to foundation concepts, take notes'
        else:
            return 'Watch attentively, relate to main topic, note new insights'
    
    async def _generate_comprehensive_questions(self, topic: str, primary_materials: Dict, 
                                              supplementary_materials: List[Dict]) -> List[str]:
        """Generate questions that span all materials"""
        
        # Collect all existing questions
        all_questions = primary_materials.get('questions', [])
        for materials in supplementary_materials:
            all_questions.extend(materials.get('questions', []))
        
        # Generate synthesis questions
        synthesis_prompt = f"""Based on comprehensive study of "{topic}" from multiple sources, create 5 synthesis questions that:
- Connect concepts across different videos
- Test deep understanding
- Encourage critical thinking
- Help identify knowledge gaps

Topic: {topic}
Number of sources: {1 + len(supplementary_materials)}

Generate questions that go beyond individual video content."""

        try:
            response = await self.ai_client.get_completion(synthesis_prompt)
            synthesis_questions = []
            
            for line in response.split('\n'):
                line = line.strip()
                if line and ('?' in line or line.lower().startswith(('what', 'how', 'why', 'explain', 'compare', 'analyze'))):
                    clean_question = line.lstrip('•-*123456789. ')
                    if not clean_question.endswith('?') and not clean_question.lower().startswith(('explain', 'describe', 'compare', 'analyze')):
                        clean_question += '?'
                    synthesis_questions.append(clean_question)
            
            # Combine with best individual questions
            selected_individual = all_questions[:8]  # Top 8 individual questions
            comprehensive = synthesis_questions[:5] + selected_individual
            
            return comprehensive[:12]  # Limit total questions
            
        except Exception as e:
            return all_questions[:10]  # Fallback to existing questions
    
    def _extract_learning_objectives(self, topic: str, primary_materials: Dict, 
                                   supplementary_materials: List[Dict]) -> List[str]:
        """Extract comprehensive learning objectives"""
        objectives = [
            f"Master fundamental {topic} concepts through comprehensive video study",
            f"Apply {topic} knowledge through practical examples and exercises",
            f"Synthesize information from multiple sources for deeper understanding"
        ]
        
        # Add specific objectives based on coverage types
        coverage_types = set()
        for materials in supplementary_materials:
            coverage_type = materials.get('coverage_type', '')
            coverage_types.add(coverage_type)
        
        if 'practice_examples' in coverage_types:
            objectives.append(f"Solve {topic} problems using demonstrated techniques")
        
        if 'deep_dive' in coverage_types:
            objectives.append(f"Analyze advanced {topic} concepts in detail")
        
        if 'practical_tutorial' in coverage_types:
            objectives.append(f"Implement {topic} solutions step-by-step")
        
        return objectives[:5]
    
    def _generate_advanced_study_tips(self, topic: str, learning_path: Dict) -> List[str]:
        """Generate advanced study tips based on learning path"""
        base_tips = [
            f"Start with the primary video to build a solid {topic} foundation",
            "Take breaks between videos to process and consolidate information",
            "Use supplementary videos to fill knowledge gaps and reinforce learning"
        ]
        
        strategy = learning_path.get('learning_strategy', '')
        total_time = learning_path.get('coverage_analysis', {}).get('estimated_study_time', 0)
        
        if strategy == 'comprehensive_primary':
            base_tips.append("The primary video provides excellent coverage - focus on understanding it thoroughly")
        
        if total_time > 60:
            base_tips.append("Break study sessions into 30-45 minute chunks with breaks")
        
        if len(learning_path.get('supplementary_videos', [])) > 2:
            base_tips.append("Use supplementary videos strategically - don't try to watch everything at once")
        
        base_tips.extend([
            "Create connections between concepts from different videos",
            "Test your understanding with the provided questions after each video",
            "Review key concepts regularly to improve retention"
        ])
        
        return base_tips[:7]