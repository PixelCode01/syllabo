import os
import requests
import hashlib
import json
import time
from typing import Optional, Dict, List
from .logger import SyllaboLogger

class AIClient:
    def __init__(self):
        self.gemini_key = os.getenv('GEMINI_API_KEY')
        self.use_gemini = bool(self.gemini_key and self.gemini_key != "your_gemini_api_key_here_optional")
        self.logger = SyllaboLogger("ai_client")
        self.cache = {}
        self.cache_ttl = 3600  # 1 hour cache
        self.use_mock = False
        
        if self.use_gemini:
            self.base_url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent"
            self.logger.info("Using Gemini API")
        else:
            self.base_url = "https://ai.hackclub.com/chat/completions"
            self.logger.info("Using Hack Club AI API (fallback)")
            
        # Check if we have any working API
        if not self.gemini_key or self.gemini_key == "your_gemini_api_key_here_optional":
            self.logger.warning("No API keys configured - will use intelligent fallback responses")
    
    async def get_completion(self, prompt: str, use_cache: bool = True) -> str:
        if use_cache:
            cache_key = self._get_cache_key(prompt)
            cached_result = self._get_from_cache(cache_key)
            if cached_result:
                self.logger.debug("Using cached AI response")
                return cached_result
        
        try:
            if self.use_gemini:
                result = await self._get_gemini_completion(prompt)
            else:
                result = await self._get_hackclub_completion(prompt)
            
            if use_cache and not result.startswith("Error:"):
                self._save_to_cache(cache_key, result)
            
            return result
        except Exception as e:
            self.logger.error(f"AI completion failed: {e}")
            return self._get_intelligent_completion(prompt)
    
    def _get_cache_key(self, prompt: str) -> str:
        """Generate cache key from prompt"""
        return hashlib.md5(prompt.encode()).hexdigest()
    
    def _get_from_cache(self, cache_key: str) -> Optional[str]:
        """Get result from cache if not expired"""
        if cache_key in self.cache:
            cached_data = self.cache[cache_key]
            if time.time() - cached_data['timestamp'] < self.cache_ttl:
                return cached_data['result']
            else:
                del self.cache[cache_key]
        return None
    
    def _save_to_cache(self, cache_key: str, result: str):
        """Save result to cache"""
        self.cache[cache_key] = {
            'result': result,
            'timestamp': time.time()
        }
    
    def _get_intelligent_completion(self, prompt: str) -> str:
        """Generate intelligent responses using text analysis algorithms"""
        prompt_lower = prompt.lower()
        
        if "rate relevance" in prompt_lower or "relevance" in prompt_lower:
            return self._calculate_text_relevance(prompt)
        
        elif "sentiment" in prompt_lower or "comments" in prompt_lower:
            return self._analyze_text_sentiment(prompt)
        
        elif "extract" in prompt_lower and "topics" in prompt_lower:
            return self._extract_topics_from_text(prompt)
        
        elif "missing topics" in prompt_lower:
            return self._find_missing_topics(prompt)
        
        else:
            return "Text analysis complete - no API required"
    
    def _calculate_text_relevance(self, prompt: str) -> str:
        """Calculate relevance using keyword matching and text analysis"""
        # Extract the topic and content from the prompt
        lines = prompt.split('\n')
        topic = ""
        content = ""
        
        for line in lines:
            if 'topic "' in line:
                topic = line.split('topic "')[1].split('"')[0].lower()
            elif line.startswith(('Title:', 'Description:', 'Content:', 'Transcript')):
                content += line.lower() + " "
        
        if not topic or not content:
            return "6.0"
        
        # Calculate keyword overlap
        topic_words = set(topic.split())
        content_words = set(content.split())
        
        # Remove common words
        common_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should', 'may', 'might', 'can', 'this', 'that', 'these', 'those'}
        topic_words -= common_words
        content_words -= common_words
        
        if not topic_words:
            return "5.0"
        
        # Calculate overlap ratio
        overlap = len(topic_words.intersection(content_words))
        total_topic_words = len(topic_words)
        
        if total_topic_words == 0:
            return "5.0"
        
        overlap_ratio = overlap / total_topic_words
        
        # Convert to 1-10 scale
        if overlap_ratio >= 0.8:
            score = 9.0 + (overlap_ratio - 0.8) * 5
        elif overlap_ratio >= 0.6:
            score = 7.5 + (overlap_ratio - 0.6) * 7.5
        elif overlap_ratio >= 0.4:
            score = 6.0 + (overlap_ratio - 0.4) * 7.5
        elif overlap_ratio >= 0.2:
            score = 4.0 + (overlap_ratio - 0.2) * 10
        else:
            score = 2.0 + overlap_ratio * 10
        
        return str(min(10.0, max(1.0, round(score, 1))))
    
    def _analyze_text_sentiment(self, prompt: str) -> str:
        """Analyze sentiment using keyword-based approach"""
        content = prompt.lower()
        
        positive_words = {'good', 'great', 'excellent', 'amazing', 'helpful', 'useful', 'clear', 'perfect', 'love', 'best', 'awesome', 'fantastic', 'wonderful', 'brilliant', 'outstanding', 'superb', 'thanks', 'thank you', 'appreciate', 'recommend', 'easy', 'understand', 'learned', 'informative'}
        negative_words = {'bad', 'terrible', 'awful', 'hate', 'worst', 'confusing', 'unclear', 'boring', 'useless', 'waste', 'disappointed', 'poor', 'difficult', 'hard', 'complicated', 'wrong', 'error', 'mistake', 'problem', 'issue'}
        
        positive_count = sum(1 for word in positive_words if word in content)
        negative_count = sum(1 for word in negative_words if word in content)
        
        if positive_count == 0 and negative_count == 0:
            return "6.0"
        
        total_sentiment_words = positive_count + negative_count
        if total_sentiment_words == 0:
            return "6.0"
        
        positive_ratio = positive_count / total_sentiment_words
        
        # Convert to 1-10 scale
        score = 1.0 + (positive_ratio * 9.0)
        return str(round(score, 1))
    
    def _extract_topics_from_text(self, prompt: str) -> str:
        """Extract topics using advanced text analysis and keyword detection"""
        content = prompt.lower()
        
        # Enhanced educational topic patterns with more specific detection
        topic_patterns = {
            'python programming': ['python', 'programming', 'coding', 'software', 'development', 'script'],
            'pandas': ['pandas', 'dataframe', 'data manipulation', 'data analysis', 'csv', 'excel'],
            'numpy': ['numpy', 'numerical', 'arrays', 'scientific computing', 'linear algebra', 'matrix'],
            'matplotlib': ['matplotlib', 'visualization', 'plotting', 'charts', 'graphs', 'seaborn'],
            'machine learning': ['machine learning', 'ml', 'ai', 'artificial intelligence', 'algorithms', 'model', 'training', 'supervised', 'unsupervised'],
            'statistical analysis': ['statistical', 'statistics', 'analysis', 'probability', 'hypothesis', 'regression', 'correlation'],
            'data visualization': ['visualization', 'plotting', 'charts', 'graphs', 'visual', 'dashboard', 'infographic'],
            'data science': ['data science', 'data', 'analysis', 'analytics', 'insights', 'big data', 'data mining'],
            'web development': ['html', 'css', 'web', 'frontend', 'backend', 'react', 'angular', 'vue', 'node'],
            'database': ['sql', 'database', 'mysql', 'postgresql', 'mongodb', 'data storage', 'nosql'],
            'javascript': ['javascript', 'js', 'node', 'react', 'angular', 'vue', 'typescript'],
            'deep learning': ['deep learning', 'neural networks', 'cnn', 'rnn', 'tensorflow', 'pytorch', 'keras'],
            'algorithms': ['algorithms', 'data structures', 'sorting', 'searching', 'complexity', 'optimization'],
            'mathematics': ['math', 'calculus', 'algebra', 'geometry', 'linear algebra', 'discrete math'],
            'computer science': ['computer science', 'cs', 'programming', 'algorithms', 'data structures', 'software engineering']
        }
        
        detected_topics = []
        
        # First pass: Look for exact matches and multi-word terms
        for topic_name, keywords in topic_patterns.items():
            score = 0
            matched_keywords = []
            
            # Check for multi-word exact matches first
            for keyword in keywords:
                if len(keyword.split()) > 1 and keyword in content:
                    score += 3  # Higher weight for exact multi-word matches
                    matched_keywords.append(keyword)
                elif keyword in content:
                    score += 1
                    matched_keywords.append(keyword)
            
            # Lower threshold for more granular topic detection
            if score >= 2 or (score >= 1 and any(len(kw.split()) > 1 for kw in matched_keywords)):
                # Generate subtopics based on matched keywords
                subtopics = []
                for kw in matched_keywords[:4]:
                    if kw not in subtopics:
                        subtopics.append(kw.title())
                
                detected_topics.append({
                    "name": topic_name.title(),
                    "subtopics": subtopics,
                    "score": score
                })
        
        # Sort by score and remove overlapping topics
        detected_topics.sort(key=lambda x: x['score'], reverse=True)
        final_topics = []
        used_keywords = set()
        
        for topic in detected_topics:
            # Check if this topic overlaps significantly with already selected topics
            topic_keywords = set(kw.lower() for kw in topic['subtopics'])
            if len(topic_keywords.intersection(used_keywords)) < len(topic_keywords) * 0.5:
                final_topics.append({
                    "name": topic["name"],
                    "subtopics": topic["subtopics"]
                })
                used_keywords.update(topic_keywords)
                
                if len(final_topics) >= 6:  # Limit to 6 topics
                    break
        
        # If no specific topics found, try to extract from structure
        if not final_topics:
            final_topics = self._extract_from_structure(content)
        
        return json.dumps(final_topics)
    
    def _extract_from_structure(self, content: str) -> List[Dict]:
        """Extract topics from text structure when pattern matching fails"""
        import re
        
        # Look for structured content
        lines = content.split('\n')
        topics = []
        
        # Look for lists, bullet points, or numbered items
        list_items = []
        for line in lines:
            line = line.strip()
            if re.match(r'^[-•*]\s+|^\d+[\.)]\s+|^[a-zA-Z][\.)]\s+', line):
                item = re.sub(r'^[-•*]\s+|\d+[\.)]\s+|[a-zA-Z][\.)]\s+', '', line).strip()
                if len(item) > 3:
                    list_items.append(item)
        
        if list_items:
            # Group related items
            if len(list_items) >= 3:
                topics.append({
                    "name": "Course Topics",
                    "subtopics": list_items[:5]
                })
        
        # Look for technical terms and concepts
        tech_terms = re.findall(r'\b[A-Z][a-z]*(?:[A-Z][a-z]*)*\b', content)
        tech_terms = [term for term in tech_terms if len(term) > 3 and term not in ['The', 'This', 'That', 'With', 'From']]
        
        if tech_terms and not topics:
            topics.append({
                "name": "Technical Concepts",
                "subtopics": list(set(tech_terms))[:5]
            })
        
        # Fallback
        if not topics:
            topics.append({
                "name": "Course Content",
                "subtopics": ["Fundamentals", "Applications", "Practice"]
            })
        
        return topics
    
    def _find_missing_topics(self, prompt: str) -> str:
        """Find potentially missing topics using text analysis"""
        content = prompt.lower()
        found_topics_line = ""
        
        # Extract already found topics
        for line in prompt.split('\n'):
            if 'already found topics:' in line.lower():
                found_topics_line = line.lower()
                break
        
        # Common topic extensions
        topic_extensions = {
            'python': ['Django', 'Flask', 'Data Analysis', 'Web Scraping'],
            'javascript': ['Node.js', 'Express', 'APIs', 'Testing'],
            'programming': ['Version Control', 'Testing', 'Debugging', 'Documentation'],
            'web': ['Responsive Design', 'Accessibility', 'Performance', 'Security'],
            'data': ['Visualization', 'Cleaning', 'Mining', 'Ethics'],
            'machine learning': ['Ethics', 'Deployment', 'Monitoring', 'Bias']
        }
        
        missing_topics = []
        
        for base_topic, extensions in topic_extensions.items():
            if base_topic in content and base_topic not in found_topics_line:
                missing_topics.extend(extensions[:2])
        
        if missing_topics:
            return '\n'.join(missing_topics[:3])
        else:
            return "None"
    
    async def _get_hackclub_completion(self, prompt: str) -> str:
        payload = {
            "messages": [{"role": "user", "content": prompt}]
        }
        
        max_retries = 3
        for attempt in range(max_retries):
            try:
                self.logger.debug(f"Making Hack Club AI request (attempt {attempt + 1})")
                response = requests.post(self.base_url, json=payload, timeout=30)
                response.raise_for_status()
                result = response.json()['choices'][0]['message']['content']
                self.logger.debug("Hack Club AI request successful")
                return result
            except requests.exceptions.Timeout:
                self.logger.warning(f"Hack Club AI timeout (attempt {attempt + 1})")
                if attempt == max_retries - 1:
                    return "Error: Request timeout"
                time.sleep(2 ** attempt)  # Exponential backoff
            except requests.exceptions.RequestException as e:
                self.logger.error(f"Hack Club AI request failed: {e}")
                if attempt == max_retries - 1:
                    return f"Error: {str(e)}"
                time.sleep(2 ** attempt)
            except (KeyError, IndexError) as e:
                self.logger.error(f"Unexpected Hack Club AI response format: {e}")
                return "Error: Unexpected response format"
    
    async def _get_gemini_completion(self, prompt: str) -> str:
        headers = {"Content-Type": "application/json"}
        payload = {
            "contents": [{
                "parts": [{"text": prompt}]
            }]
        }
        
        max_retries = 3
        for attempt in range(max_retries):
            try:
                self.logger.debug(f"Making Gemini API request (attempt {attempt + 1})")
                url = f"{self.base_url}?key={self.gemini_key}"
                response = requests.post(url, json=payload, headers=headers, timeout=30)
                response.raise_for_status()
                result = response.json()['candidates'][0]['content']['parts'][0]['text']
                self.logger.debug("Gemini API request successful")
                return result
            except requests.exceptions.Timeout:
                self.logger.warning(f"Gemini API timeout (attempt {attempt + 1})")
                if attempt == max_retries - 1:
                    return "Error: Request timeout"
                time.sleep(2 ** attempt)
            except requests.exceptions.RequestException as e:
                self.logger.error(f"Gemini API request failed: {e}")
                if attempt == max_retries - 1:
                    return f"Error: {str(e)}"
                time.sleep(2 ** attempt)
            except (KeyError, IndexError) as e:
                self.logger.error(f"Unexpected Gemini response format: {e}")
                return "Error: Unexpected response format"