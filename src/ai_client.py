import os
import requests
import hashlib
import json
import time
import random
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
        
        # Multiple free AI services for fallback
        self.free_services = [
            {
                'name': 'HackClub AI',
                'url': 'https://ai.hackclub.com/chat/completions',
                'type': 'openai_format',
                'active': True
            },
            {
                'name': 'Free GPT',
                'url': 'https://api.pawan.krd/cosmosrp/v1/chat/completions',
                'type': 'openai_format',
                'active': True
            },
            {
                'name': 'GPT4Free',
                'url': 'https://api.g4f.icu/v1/chat/completions',
                'type': 'openai_format',
                'active': True
            }
        ]
        
        if self.use_gemini:
            self.base_url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent"
            self.logger.info("Using Gemini API")
        else:
            active_services = [s['name'] for s in self.free_services if s['active']]
            self.logger.info(f"Using free AI services: {', '.join(active_services)}")
            
        if not self.gemini_key or self.gemini_key == "your_gemini_api_key_here_optional":
            self.logger.info("No API key required - using free services")
    
    async def get_completion(self, prompt: str, use_cache: bool = True) -> str:
        if use_cache:
            cache_key = self._get_cache_key(prompt)
            cached_result = self._get_from_cache(cache_key)
            if cached_result:
                self.logger.debug("Using cached AI response")
                return cached_result
        
        # Try Gemini first if available
        if self.use_gemini:
            try:
                result = await self._get_gemini_completion(prompt)
                if use_cache and not result.startswith("Error:"):
                    self._save_to_cache(cache_key, result)
                return result
            except Exception as e:
                self.logger.warning(f"Gemini API failed, trying free services: {e}")
        
        # Try free services with fallback
        result = await self._try_free_services(prompt)
        
        if use_cache and not result.startswith("Error:"):
            self._save_to_cache(cache_key, result)
        
        return result
    
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
        
        # Enhanced pattern matching for different types of requests
        if "rate relevance" in prompt_lower or "relevance" in prompt_lower:
            return self._calculate_text_relevance(prompt)
        
        elif "sentiment" in prompt_lower or "comments" in prompt_lower:
            return self._analyze_text_sentiment(prompt)
        
        elif "extract" in prompt_lower and "topics" in prompt_lower:
            return self._extract_topics_from_text(prompt)
        
        elif "missing topics" in prompt_lower:
            return self._find_missing_topics(prompt)
        
        elif "summarize" in prompt_lower or "summary" in prompt_lower:
            return self._generate_summary(prompt)
        
        elif "difficulty" in prompt_lower or "level" in prompt_lower:
            return self._analyze_difficulty(prompt)
        
        elif "keywords" in prompt_lower or "key terms" in prompt_lower:
            return self._extract_keywords(prompt)
        
        elif "questions" in prompt_lower or "quiz" in prompt_lower:
            return self._generate_questions(prompt)
        
        else:
            return self._provide_general_analysis(prompt)
    
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
    
    def _generate_summary(self, prompt: str) -> str:
        """Generate a summary using text analysis"""
        content = prompt
        
        # Extract main content (remove prompt instructions)
        lines = content.split('\n')
        content_lines = []
        for line in lines:
            if not line.lower().startswith(('summarize', 'please', 'can you', 'generate')):
                content_lines.append(line.strip())
        
        text = ' '.join(content_lines)
        sentences = [s.strip() for s in text.split('.') if len(s.strip()) > 10]
        
        if len(sentences) <= 3:
            return text[:200] + "..." if len(text) > 200 else text
        
        # Simple extractive summarization
        # Score sentences by keyword frequency
        word_freq = {}
        words = text.lower().split()
        for word in words:
            if len(word) > 3 and word.isalpha():
                word_freq[word] = word_freq.get(word, 0) + 1
        
        sentence_scores = {}
        for i, sentence in enumerate(sentences):
            score = 0
            sentence_words = sentence.lower().split()
            for word in sentence_words:
                if word in word_freq:
                    score += word_freq[word]
            sentence_scores[i] = score / len(sentence_words) if sentence_words else 0
        
        # Get top sentences
        top_sentences = sorted(sentence_scores.items(), key=lambda x: x[1], reverse=True)
        summary_sentences = []
        
        for idx, _ in top_sentences[:3]:
            summary_sentences.append((idx, sentences[idx]))
        
        # Sort by original order
        summary_sentences.sort(key=lambda x: x[0])
        summary = '. '.join([s[1] for s in summary_sentences]) + '.'
        
        return summary
    
    def _analyze_difficulty(self, prompt: str) -> str:
        """Analyze content difficulty level"""
        content = prompt.lower()
        
        # Difficulty indicators
        beginner_terms = ['introduction', 'basic', 'fundamentals', 'getting started', 'overview', 'simple']
        intermediate_terms = ['implementation', 'practice', 'application', 'examples', 'methods']
        advanced_terms = ['optimization', 'advanced', 'complex', 'architecture', 'algorithms', 'performance']
        
        beginner_score = sum(1 for term in beginner_terms if term in content)
        intermediate_score = sum(1 for term in intermediate_terms if term in content)
        advanced_score = sum(1 for term in advanced_terms if term in content)
        
        # Technical complexity indicators
        tech_indicators = len([w for w in content.split() if len(w) > 8 and any(c.isupper() for c in w)])
        
        total_score = beginner_score * 1 + intermediate_score * 2 + advanced_score * 3 + tech_indicators * 0.5
        
        if total_score <= 3:
            return "Beginner (1-3)"
        elif total_score <= 7:
            return "Intermediate (4-7)"
        else:
            return "Advanced (8-10)"
    
    def _extract_keywords(self, prompt: str) -> str:
        """Extract key terms from content"""
        import re
        
        content = prompt.lower()
        
        # Remove common words
        stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should', 'may', 'might', 'can', 'this', 'that', 'these', 'those', 'you', 'your', 'we', 'our', 'they', 'their', 'it', 'its'}
        
        # Extract words
        words = re.findall(r'\b[a-zA-Z]{3,}\b', content)
        word_freq = {}
        
        for word in words:
            if word.lower() not in stop_words:
                word_freq[word.lower()] = word_freq.get(word.lower(), 0) + 1
        
        # Get top keywords
        top_keywords = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)[:10]
        keywords = [word.title() for word, _ in top_keywords]
        
        return ', '.join(keywords)
    
    def _generate_questions(self, prompt: str) -> str:
        """Generate study questions from content"""
        content = prompt
        
        # Extract key concepts
        lines = content.split('\n')
        concepts = []
        
        for line in lines:
            line = line.strip()
            if line and not line.lower().startswith(('generate', 'create', 'make')):
                # Look for definition patterns
                if ':' in line:
                    concept = line.split(':')[0].strip()
                    if len(concept.split()) <= 4:
                        concepts.append(concept)
                elif line.endswith('.') and len(line.split()) <= 8:
                    concepts.append(line[:-1])
        
        if not concepts:
            # Fallback: extract from text structure
            words = content.split()
            important_words = [w for w in words if len(w) > 5 and w[0].isupper()]
            concepts = important_words[:5]
        
        # Generate questions
        questions = []
        question_templates = [
            "What is {}?",
            "How does {} work?",
            "Why is {} important?",
            "What are the key features of {}?",
            "How can {} be applied?"
        ]
        
        for i, concept in enumerate(concepts[:5]):
            template = question_templates[i % len(question_templates)]
            questions.append(template.format(concept))
        
        return '\n'.join(questions)
    
    def _provide_general_analysis(self, prompt: str) -> str:
        """Provide general analysis when specific patterns don't match"""
        content = prompt
        
        # Basic content analysis
        word_count = len(content.split())
        sentence_count = len([s for s in content.split('.') if s.strip()])
        
        # Identify content type
        content_lower = content.lower()
        if any(term in content_lower for term in ['video', 'youtube', 'watch']):
            content_type = "video content"
        elif any(term in content_lower for term in ['article', 'blog', 'post']):
            content_type = "article content"
        elif any(term in content_lower for term in ['course', 'lesson', 'chapter']):
            content_type = "educational content"
        else:
            content_type = "text content"
        
        analysis = f"Analysis of {content_type}:\n"
        analysis += f"- Word count: {word_count}\n"
        analysis += f"- Sentences: {sentence_count}\n"
        
        # Extract main topics
        keywords = self._extract_keywords(content)
        if keywords:
            analysis += f"- Key terms: {keywords}\n"
        
        # Difficulty assessment
        difficulty = self._analyze_difficulty(content)
        analysis += f"- Difficulty level: {difficulty}\n"
        
        analysis += "- Status: Analysis complete using local processing"
        
        return analysis
    
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
    
    async def _try_free_services(self, prompt: str) -> str:
        """Try multiple free AI services with fallback"""
        # Shuffle services to distribute load
        services = [s for s in self.free_services if s['active']]
        random.shuffle(services)
        
        for service in services:
            try:
                self.logger.debug(f"Trying {service['name']}")
                result = await self._get_free_service_completion(service, prompt)
                if result and not result.startswith("Error:"):
                    self.logger.info(f"Success with {service['name']}")
                    return result
            except Exception as e:
                self.logger.warning(f"{service['name']} failed: {e}")
                continue
        
        # All services failed, use intelligent fallback
        self.logger.info("All free services failed, using intelligent completion")
        return self._get_intelligent_completion(prompt)
    
    async def test_services(self) -> Dict[str, bool]:
        """Test all available AI services"""
        results = {}
        test_prompt = "Hello, please respond with 'Service working'"
        
        if self.use_gemini:
            try:
                result = await self._get_gemini_completion(test_prompt)
                results['Gemini'] = not result.startswith("Error:")
            except:
                results['Gemini'] = False
        
        for service in self.free_services:
            try:
                result = await self._get_free_service_completion(service, test_prompt)
                results[service['name']] = not result.startswith("Error:")
            except:
                results[service['name']] = False
        
        # Always available
        results['Intelligent Fallback'] = True
        
        return results
    
    def get_service_status(self) -> str:
        """Get current service configuration status"""
        status = []
        
        if self.use_gemini:
            status.append("Gemini API: Configured")
        else:
            status.append("Gemini API: Not configured")
        
        active_free = [s['name'] for s in self.free_services if s['active']]
        status.append(f"Free services: {', '.join(active_free)}")
        status.append("Intelligent fallback: Always available")
        
        return "\n".join(status)
    
    async def _get_free_service_completion(self, service: Dict, prompt: str) -> str:
        """Get completion from a free AI service"""
        if service['type'] == 'openai_format':
            return await self._get_openai_format_completion(service, prompt)
        else:
            raise ValueError(f"Unknown service type: {service['type']}")
    
    async def _get_openai_format_completion(self, service: Dict, prompt: str) -> str:
        """Get completion from OpenAI-format API"""
        payload = {
            "model": "gpt-3.5-turbo",
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": 1000,
            "temperature": 0.7
        }
        
        headers = {"Content-Type": "application/json"}
        
        # Some services might need specific headers
        if service['name'] == 'Free GPT':
            headers["Authorization"] = "Bearer pk-this-is-a-real-free-pool-token-for-everyone"
        
        try:
            response = requests.post(
                service['url'],
                json=payload,
                headers=headers,
                timeout=20
            )
            
            if response.status_code == 200:
                result_data = response.json()
                if 'choices' in result_data and len(result_data['choices']) > 0:
                    content = result_data['choices'][0]['message']['content']
                    return content.strip()
            
            # If we get here, the response wasn't successful
            self.logger.warning(f"{service['name']} returned status {response.status_code}")
            return f"Error: Service unavailable"
            
        except requests.exceptions.Timeout:
            self.logger.warning(f"{service['name']} timeout")
            return "Error: Request timeout"
        except requests.exceptions.RequestException as e:
            self.logger.warning(f"{service['name']} request failed: {e}")
            return f"Error: {str(e)}"
        except (KeyError, IndexError, ValueError) as e:
            self.logger.warning(f"{service['name']} response format error: {e}")
            return "Error: Invalid response format"
    
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