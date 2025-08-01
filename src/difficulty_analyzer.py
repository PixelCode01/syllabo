from typing import Dict, List, Optional
import re
from .ai_client import AIClient
from .logger import SyllaboLogger

class DifficultyAnalyzer:
    """AI-powered content difficulty assessment"""
    
    def __init__(self, ai_client: AIClient = None):
        self.ai_client = ai_client or AIClient()
        self.logger = SyllaboLogger("difficulty_analyzer")
        
        # Difficulty indicators
        self.beginner_keywords = [
            'introduction', 'basics', 'fundamentals', 'getting started',
            'beginner', 'tutorial', 'simple', 'easy', 'overview'
        ]
        
        self.advanced_keywords = [
            'advanced', 'expert', 'deep dive', 'complex', 'optimization',
            'architecture', 'implementation', 'research', 'theory'
        ]
        
        self.technical_terms = [
            'algorithm', 'framework', 'methodology', 'paradigm',
            'optimization', 'implementation', 'architecture'
        ]
    
    async def analyze_content_difficulty(self, content: Dict) -> Dict:
        """Analyze difficulty of video/article content"""
        title = content.get('title', '')
        description = content.get('description', '')
        duration = content.get('duration', '')
        
        # Multiple analysis methods
        keyword_score = self._analyze_keywords(title, description)
        length_score = self._analyze_length(duration, description)
        ai_score = await self._ai_difficulty_analysis(title, description)
        
        # Combine scores
        final_score = (keyword_score * 0.3 + length_score * 0.2 + ai_score * 0.5)
        difficulty_level = self._score_to_level(final_score)
        
        return {
            'difficulty_score': final_score,
            'difficulty_level': difficulty_level,
            'keyword_indicators': self._get_difficulty_indicators(title, description),
            'estimated_prerequisite_knowledge': await self._estimate_prerequisites(title, description),
            'recommended_for': self._get_audience_recommendation(difficulty_level),
            'analysis_breakdown': {
                'keyword_score': keyword_score,
                'length_score': length_score,
                'ai_score': ai_score
            }
        }
    
    def _analyze_keywords(self, title: str, description: str) -> float:
        """Analyze difficulty based on keywords"""
        text = f"{title} {description}".lower()
        
        beginner_count = sum(1 for keyword in self.beginner_keywords if keyword in text)
        advanced_count = sum(1 for keyword in self.advanced_keywords if keyword in text)
        technical_count = sum(1 for term in self.technical_terms if term in text)
        
        # Score calculation
        if beginner_count > advanced_count:
            base_score = 0.2 + (beginner_count * 0.1)
        else:
            base_score = 0.6 + (advanced_count * 0.1)
        
        # Technical terms increase difficulty
        technical_bonus = min(technical_count * 0.1, 0.3)
        
        return min(base_score + technical_bonus, 1.0)
    
    def _analyze_length(self, duration: str, description: str) -> float:
        """Analyze difficulty based on content length"""
        # Parse duration
        duration_minutes = self._parse_duration(duration)
        description_words = len(description.split()) if description else 0
        
        # Longer content often indicates more complexity
        duration_score = min(duration_minutes / 120, 1.0)  # Normalize to 2 hours
        description_score = min(description_words / 500, 1.0)  # Normalize to 500 words
        
        return (duration_score + description_score) / 2
    
    def _parse_duration(self, duration: str) -> int:
        """Parse duration string to minutes"""
        if not duration:
            return 0
        
        # Handle formats like "1:23:45" or "23:45" or "45"
        parts = duration.split(':')
        try:
            if len(parts) == 3:  # HH:MM:SS
                return int(parts[0]) * 60 + int(parts[1])
            elif len(parts) == 2:  # MM:SS
                return int(parts[0])
            else:  # Just minutes
                return int(parts[0])
        except ValueError:
            return 0
    
    async def _ai_difficulty_analysis(self, title: str, description: str) -> float:
        """Analyze content difficulty using algorithmic approach"""
        try:
            # Try AI first, then fallback to algorithmic analysis
            prompt = f"""Analyze the difficulty level of this educational content on a scale of 0.0 to 1.0:

Title: {title}
Description: {description[:500]}

Consider:
- Prerequisites needed
- Complexity of concepts
- Technical depth
- Target audience

Respond with just a number between 0.0 (beginner) and 1.0 (expert level)."""
            
            response = await self.ai_client.get_completion(prompt)
            
            # Try to extract a number from the response
            import re
            number_match = re.search(r'(\d+\.?\d*)', response.strip())
            if number_match:
                score = float(number_match.group(1))
                # If it's a whole number > 1, assume it's out of 10
                if score > 1:
                    score = score / 10
                return max(0.0, min(1.0, score))
            else:
                raise ValueError("No valid number found in response")
                
        except Exception as e:
            self.logger.error(f"AI difficulty analysis failed: {e}")
            # Fallback to algorithmic analysis
            return self._algorithmic_difficulty_analysis(title, description)
    
    def _algorithmic_difficulty_analysis(self, title: str, description: str) -> float:
        """Algorithmic difficulty analysis without AI"""
        text = f"{title} {description}".lower()
        score = 0.5  # Start with intermediate
        
        # Advanced indicators
        advanced_patterns = [
            r'\b(advanced|expert|professional|enterprise|production)\b',
            r'\b(architecture|optimization|performance|scalability)\b',
            r'\b(deep dive|comprehensive|complete guide|mastery)\b',
            r'\b(implementation|algorithm|framework|methodology)\b'
        ]
        
        # Beginner indicators
        beginner_patterns = [
            r'\b(beginner|intro|introduction|basics|fundamentals)\b',
            r'\b(getting started|first steps|tutorial|guide)\b',
            r'\b(simple|easy|quick|basic)\b',
            r'\b(for beginners|step by step|from scratch)\b'
        ]
        
        # Count pattern matches
        advanced_matches = sum(1 for pattern in advanced_patterns if re.search(pattern, text))
        beginner_matches = sum(1 for pattern in beginner_patterns if re.search(pattern, text))
        
        # Adjust score based on matches
        if beginner_matches > advanced_matches:
            score = 0.2 + (beginner_matches * 0.05)
        elif advanced_matches > beginner_matches:
            score = 0.7 + (advanced_matches * 0.05)
        
        # Technical complexity indicators
        technical_indicators = [
            'api', 'framework', 'library', 'database', 'server',
            'deployment', 'testing', 'debugging', 'optimization'
        ]
        
        tech_count = sum(1 for indicator in technical_indicators if indicator in text)
        score += min(tech_count * 0.03, 0.2)  # Add up to 0.2 for technical content
        
        return max(0.0, min(1.0, score))
    
    def _score_to_level(self, score: float) -> str:
        """Convert numerical score to difficulty level"""
        if score < 0.3:
            return "beginner"
        elif score < 0.7:
            return "intermediate"
        else:
            return "advanced"
    
    def _get_difficulty_indicators(self, title: str, description: str) -> List[str]:
        """Get specific indicators that influenced difficulty rating"""
        text = f"{title} {description}".lower()
        indicators = []
        
        for keyword in self.beginner_keywords:
            if keyword in text:
                indicators.append(f"Beginner indicator: '{keyword}'")
        
        for keyword in self.advanced_keywords:
            if keyword in text:
                indicators.append(f"Advanced indicator: '{keyword}'")
        
        for term in self.technical_terms:
            if term in text:
                indicators.append(f"Technical term: '{term}'")
        
        return indicators
    
    async def _estimate_prerequisites(self, title: str, description: str) -> List[str]:
        """Estimate prerequisite knowledge needed"""
        try:
            prompt = f"""List the prerequisite knowledge needed for this educational content:

Title: {title}
Description: {description[:300]}

List 3-5 specific prerequisites a learner should have. Be concise."""
            
            response = await self.ai_client.get_completion(prompt)
            prerequisites = [line.strip() for line in response.split('\n') if line.strip()]
            if prerequisites and len(prerequisites) > 0:
                return prerequisites[:5]  # Limit to 5
            else:
                raise ValueError("No valid prerequisites found")
                
        except Exception as e:
            self.logger.error(f"Prerequisites estimation failed: {e}")
            # Fallback to algorithmic prerequisite estimation
            return self._algorithmic_prerequisites(title, description)
    
    def _algorithmic_prerequisites(self, title: str, description: str) -> List[str]:
        """Estimate prerequisites using algorithmic approach"""
        text = f"{title} {description}".lower()
        prerequisites = []
        
        # Topic-specific prerequisites
        if any(term in text for term in ['python', 'programming']):
            prerequisites.extend(['Basic programming concepts', 'Python syntax'])
        
        if any(term in text for term in ['machine learning', 'ml', 'ai']):
            prerequisites.extend(['Statistics basics', 'Python programming', 'Mathematics fundamentals'])
        
        if any(term in text for term in ['data science', 'data analysis']):
            prerequisites.extend(['Python programming', 'Statistics knowledge', 'Basic mathematics'])
        
        if any(term in text for term in ['web development', 'html', 'css', 'javascript']):
            prerequisites.extend(['Basic computer skills', 'Text editor usage'])
        
        if any(term in text for term in ['advanced', 'expert', 'professional']):
            prerequisites.extend(['Solid foundation in the topic', 'Previous experience recommended'])
        
        if any(term in text for term in ['database', 'sql']):
            prerequisites.extend(['Basic programming knowledge', 'Understanding of data concepts'])
        
        # Default prerequisites if none found
        if not prerequisites:
            if 'beginner' in text or 'introduction' in text:
                prerequisites = ['Basic computer skills', 'Willingness to learn']
            else:
                prerequisites = ['Basic understanding of the topic', 'Some prior experience helpful']
        
        return prerequisites[:5]
    
    def _get_audience_recommendation(self, difficulty_level: str) -> str:
        """Get audience recommendation based on difficulty"""
        recommendations = {
            "beginner": "Perfect for newcomers to the topic. No prior experience required.",
            "intermediate": "Best for learners with some background knowledge. Basic concepts should be familiar.",
            "advanced": "Designed for experienced learners. Requires solid foundation in the subject area."
        }
        
        return recommendations.get(difficulty_level, "Suitable for general audience")
    
    def batch_analyze_difficulty(self, content_list: List[Dict]) -> List[Dict]:
        """Analyze difficulty for multiple pieces of content"""
        results = []
        
        for content in content_list:
            try:
                # For batch processing, use simpler analysis to avoid API limits
                title = content.get('title', '')
                description = content.get('description', '')
                
                keyword_score = self._analyze_keywords(title, description)
                length_score = self._analyze_length(content.get('duration', ''), description)
                
                # Simple combined score without AI
                final_score = (keyword_score * 0.6 + length_score * 0.4)
                difficulty_level = self._score_to_level(final_score)
                
                content['difficulty_score'] = final_score
                content['difficulty_level'] = difficulty_level
                content['difficulty_indicators'] = self._get_difficulty_indicators(title, description)
                
                results.append(content)
                
            except Exception as e:
                self.logger.error(f"Failed to analyze content difficulty: {e}")
                content['difficulty_level'] = 'intermediate'  # Default
                results.append(content)
        
        return results
    
    def filter_by_difficulty(self, content_list: List[Dict], 
                           target_level: str) -> List[Dict]:
        """Filter content by difficulty level"""
        return [
            content for content in content_list 
            if content.get('difficulty_level', 'intermediate') == target_level
        ]
    
    def get_difficulty_distribution(self, content_list: List[Dict]) -> Dict:
        """Get distribution of difficulty levels in content list"""
        distribution = {'beginner': 0, 'intermediate': 0, 'advanced': 0}
        
        for content in content_list:
            level = content.get('difficulty_level', 'intermediate')
            if level in distribution:
                distribution[level] += 1
        
        total = len(content_list)
        if total > 0:
            distribution = {
                level: {'count': count, 'percentage': (count / total) * 100}
                for level, count in distribution.items()
            }
        
        return distribution