import re
import PyPDF2
from typing import List, Dict

class SyllabusParser:
    def __init__(self):
        pass
    
    def load_from_file(self, file_path: str) -> str:
        if file_path.endswith('.pdf'):
            return self._extract_from_pdf(file_path)
        else:
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
    
    def _extract_from_pdf(self, pdf_path: str) -> str:
        text = ""
        with open(pdf_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            for page in reader.pages:
                text += page.extract_text()
        return text
    
    async def extract_topics(self, syllabus_text: str, ai_client) -> List[Dict]:
        """Extract topics using advanced text analysis with AI enhancement"""
        # Use advanced text analysis as primary method for better accuracy
        text_topics = self._advanced_text_extraction(syllabus_text)
        
        # Also try the AI client's improved context analysis
        try:
            ai_context_result = ai_client._extract_topics_from_text(syllabus_text)
            import json
            ai_context_topics = json.loads(ai_context_result)
            if ai_context_topics and len(ai_context_topics) > 0:
                # Merge AI context topics with text topics, prioritizing AI context
                merged_topics = ai_context_topics.copy()
                existing_names = {t['name'].lower() for t in ai_context_topics}
                
                # Add unique text-based topics
                for text_topic in text_topics:
                    if text_topic['name'].lower() not in existing_names:
                        merged_topics.append(text_topic)
                
                text_topics = merged_topics[:8]  # Limit to 8 topics
        except Exception as e:
            print(f"AI context analysis failed: {e}")
        
        # Always try AI enhancement for better accuracy
        try:
            # Enhanced AI prompt for better topic extraction with fallback handling
            prompt = f"""Extract learning topics from this syllabus content and return ONLY a JSON array.

Content: {syllabus_text[:800]}

Return exactly this format: [{{"name": "Topic Name", "subtopics": ["subtopic1", "subtopic2"]}}]

Extract 3-5 main topics, each with 2-3 subtopics. No explanations, just the JSON array."""
            
            response = await ai_client.get_completion(prompt)
            
            # Check if response is empty or None
            if not response or response.strip() == "":
                print("AI response was empty, using text-based extraction")
                return text_topics if text_topics else self._create_fallback_topics(syllabus_text)
            
            # Clean the response to extract JSON - handle thinking tags
            response = response.strip()
            
            # Remove thinking tags if present
            if '<think>' in response:
                # Extract content after </think> tag
                think_end = response.find('</think>')
                if think_end != -1:
                    response = response[think_end + 8:].strip()
            
            # Remove code block markers
            if response.startswith('```json'):
                response = response[7:]
            elif response.startswith('```'):
                response = response[3:]
            if response.endswith('```'):
                response = response[:-3]
            response = response.strip()
            
            # Additional check for empty response after cleaning
            if not response:
                print("AI response was empty after cleaning, using text-based extraction")
                return text_topics if text_topics else self._create_fallback_topics(syllabus_text)
            
            import json
            
            # Try to parse JSON with better error handling
            try:
                ai_topics = json.loads(response)
            except json.JSONDecodeError as e:
                # Try to extract JSON from response if it's embedded in text
                import re
                # Look for JSON array pattern
                json_match = re.search(r'\[[\s\S]*?\]', response)
                if json_match:
                    try:
                        ai_topics = json.loads(json_match.group())
                    except:
                        # If still fails, use text-based extraction
                        return text_topics if text_topics else self._create_fallback_topics(syllabus_text)
                else:
                    # No JSON found, use text-based extraction
                    return text_topics if text_topics else self._create_fallback_topics(syllabus_text)
            
            # Validate AI topics
            if isinstance(ai_topics, list) and len(ai_topics) > 0:
                validated_topics = []
                for topic in ai_topics:
                    if (isinstance(topic, dict) and 
                        'name' in topic and 
                        isinstance(topic['name'], str) and 
                        len(topic['name'].strip()) > 2):
                        
                        # Ensure subtopics is a list
                        if 'subtopics' not in topic or not isinstance(topic['subtopics'], list):
                            topic['subtopics'] = []
                        
                        # Clean subtopics
                        topic['subtopics'] = [st for st in topic['subtopics'] 
                                            if isinstance(st, str) and len(st.strip()) > 2][:4]
                        
                        validated_topics.append(topic)
                
                if validated_topics:
                    # If AI extraction was successful, prioritize it and limit text-based additions
                    all_topics = validated_topics.copy()
                    existing_names = {t['name'].lower() for t in validated_topics}
                    
                    # Only add high-quality text-based topics that are significantly different
                    for text_topic in text_topics:
                        topic_name_lower = text_topic['name'].lower()
                        # Skip if too similar to existing topics or too generic
                        if (topic_name_lower not in existing_names and 
                            len(topic_name_lower) > 5 and
                            not any(existing in topic_name_lower or topic_name_lower in existing 
                                   for existing in existing_names) and
                            len(all_topics) < 6):  # Limit total topics
                            all_topics.append(text_topic)
                    
                    return all_topics[:6]  # Limit to 6 topics for better quality
            
            # Fallback to text-based extraction
            return text_topics if text_topics else self._create_fallback_topics(syllabus_text)
                
        except Exception as e:
            # Only print error if it's not the common empty response issue
            if "Expecting value: line 1 column 1" not in str(e):
                print(f"AI extraction failed: {e}")
            else:
                print("AI response was empty, using text-based extraction")
            return text_topics if text_topics else self._create_fallback_topics(syllabus_text)
    
    def _create_fallback_topics(self, syllabus_text: str) -> List[Dict]:
        """Create fallback topics when extraction fails"""
        # Try to find any meaningful content
        lines = [line.strip() for line in syllabus_text.split('\n') if line.strip()]
        
        if not lines:
            return [{"name": "Course Content", "subtopics": ["Fundamentals", "Applications", "Practice"]}]
        
        # For very short inputs, create a more specific topic
        text_lower = syllabus_text.lower().strip()
        if len(text_lower) < 30:
            # Handle common abbreviations and typos
            if any(term in text_lower for term in ['oop', 'oops', 'opps']) and 'py' in text_lower:
                return [{
                    "name": "Python Object-Oriented Programming",
                    "subtopics": ["Classes and Objects", "Inheritance", "Polymorphism", "Encapsulation"]
                }]
            elif 'python' in text_lower and any(term in text_lower for term in ['oop', 'oops', 'opps']):
                return [{
                    "name": "Python Object-Oriented Programming", 
                    "subtopics": ["Classes and Objects", "Inheritance", "Polymorphism", "Encapsulation"]
                }]
            elif 'python' in text_lower:
                return [{
                    "name": "Python Programming",
                    "subtopics": ["Syntax and Basics", "Data Types", "Functions", "Control Structures"]
                }]
            elif any(term in text_lower for term in ['ml', 'machine learning']):
                return [{
                    "name": "Machine Learning",
                    "subtopics": ["Supervised Learning", "Unsupervised Learning", "Model Training", "Evaluation"]
                }]
            elif 'data science' in text_lower:
                return [{
                    "name": "Data Science",
                    "subtopics": ["Data Analysis", "Visualization", "Statistical Methods", "Python Libraries"]
                }]
        
        # Look for any structured content
        topics = []
        for line in lines[:20]:  # Check first 20 lines
            if len(line) > 10 and len(line) < 100:  # Reasonable topic length
                # Clean the line
                clean_line = re.sub(r'^[-•*○]\s*|\d+[\.)]\s*', '', line).strip()
                if clean_line and not clean_line.lower().startswith(('course', 'syllabus', 'instructor')):
                    topics.append({
                        "name": clean_line[:50],  # Limit length
                        "subtopics": ["Key Concepts", "Applications", "Practice"]
                    })
                    if len(topics) >= 4:
                        break
        
        return topics if topics else [{"name": "Course Content", "subtopics": ["Fundamentals", "Applications", "Practice"]}]
    
    def _advanced_text_extraction(self, text: str) -> List[Dict]:
        """Advanced text-based topic extraction using multiple strategies"""
        topics = []
        
        # Strategy 1: Look for structured content (chapters, units, etc.)
        structured_topics = self._extract_structured_topics(text)
        if structured_topics:
            topics.extend(structured_topics)
        
        # Strategy 2: Look for bullet points and lists
        list_topics = self._extract_list_topics(text)
        if list_topics:
            topics.extend(list_topics)
        
        # Strategy 3: Look for educational keywords and patterns
        keyword_topics = self._extract_keyword_topics(text)
        if keyword_topics:
            topics.extend(keyword_topics)
        
        # Remove duplicates and merge similar topics
        topics = self._merge_similar_topics(topics)
        
        return topics if topics else [{"name": "Course Content", "subtopics": ["Fundamentals", "Applications", "Practice"]}]
    
    def _extract_structured_topics(self, text: str) -> List[Dict]:
        """Extract topics from structured content like chapters, units, etc."""
        topics = []
        lines = text.split('\n')
        current_topic = None
        
        # Enhanced patterns for structured content
        topic_patterns = [
            r'^(Chapter|Unit|Topic|Week|Module|Section|Part)\s*(\d+)[:.]?\s*(.+)',
            r'^(\d+)\.?\s+(.+)',  # Numbered items
            r'^([A-Z][A-Z\s]+)$',  # All caps headings
            r'^([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*):',  # Title Case with colon
            r'^\s*[-•*]\s*([A-Z][a-z]+(?:\s+[A-Za-z]+)*)',  # Bulleted items
        ]
        
        for line in lines:
            line = line.strip()
            if not line or len(line) < 3:
                continue
            
            # Check if this line matches a topic pattern
            is_topic = False
            for pattern in topic_patterns:
                match = re.match(pattern, line, re.IGNORECASE)
                if match:
                    # Save previous topic
                    if current_topic:
                        topics.append(current_topic)
                    
                    # Start new topic
                    if len(match.groups()) >= 3:
                        topic_name = match.group(3).strip()
                    elif len(match.groups()) >= 2:
                        topic_name = match.group(2).strip()
                    else:
                        topic_name = match.group(1).strip()
                    
                    # Clean up topic name
                    topic_name = re.sub(r'^[-•*○]\s*', '', topic_name)
                    
                    if len(topic_name) > 2:
                        current_topic = {"name": topic_name, "subtopics": []}
                        is_topic = True
                    break
            
            # If not a topic header, might be a subtopic
            if not is_topic and current_topic:
                if line.startswith(('-', '•', '*', '○')) or re.match(r'^\w+\)', line):
                    subtopic = re.sub(r'^[-•*○]\s*|\w+\)\s*', '', line).strip()
                    if subtopic and len(subtopic) > 2:
                        current_topic["subtopics"].append(subtopic)
        
        # Add the last topic
        if current_topic:
            topics.append(current_topic)
        
        return topics
    
    def _extract_list_topics(self, text: str) -> List[Dict]:
        """Extract topics from bulleted or numbered lists"""
        topics = []
        lines = text.split('\n')
        
        # Look for lists that might represent topics
        current_list = []
        in_list = False
        
        for line in lines:
            line = line.strip()
            if not line:
                if in_list and current_list:
                    # End of list, process it
                    if len(current_list) >= 2:  # At least 2 items to be considered a topic list
                        topic_name = self._infer_topic_name(current_list)
                        topics.append({
                            "name": topic_name,
                            "subtopics": current_list[:5]  # Limit subtopics
                        })
                    current_list = []
                    in_list = False
                continue
            
            # Check if this is a list item
            if re.match(r'^[-•*○]\s+|^\d+[\.)]\s+|^[a-zA-Z][\.)]\s+', line):
                in_list = True
                item = re.sub(r'^[-•*○]\s+|\d+[\.)]\s+|[a-zA-Z][\.)]\s+', '', line).strip()
                if item and len(item) > 2:
                    current_list.append(item)
            elif in_list:
                # End of list
                if current_list and len(current_list) >= 2:
                    topic_name = self._infer_topic_name(current_list)
                    topics.append({
                        "name": topic_name,
                        "subtopics": current_list[:5]
                    })
                current_list = []
                in_list = False
        
        return topics
    
    def _extract_keyword_topics(self, text: str) -> List[Dict]:
        """Extract topics based on educational keywords and patterns"""
        topics = []
        text_lower = text.lower()
        
        # Enhanced educational topic keywords with more specific detection
        topic_keywords = {
            'Python Object-Oriented Programming': ['python oop', 'python oops', 'python opps', 'python object oriented', 'oop in python', 'oops in python', 'opps in python'],
            'Python Programming': ['python', 'programming', 'coding', 'script', 'interpreter', 'py'],
            'Object-Oriented Programming': ['oop', 'oops', 'opps', 'object oriented', 'classes', 'objects', 'inheritance', 'polymorphism', 'encapsulation'],
            'Pandas': ['pandas', 'dataframe', 'data manipulation', 'csv', 'excel'],
            'NumPy': ['numpy', 'arrays', 'numerical', 'scientific computing', 'matrix'],
            'Matplotlib': ['matplotlib', 'visualization', 'plotting', 'charts', 'graphs'],
            'Machine Learning': ['machine learning', 'ml', 'algorithms', 'model', 'training', 'supervised', 'unsupervised'],
            'Statistical Analysis': ['statistical', 'statistics', 'analysis', 'probability', 'hypothesis', 'regression'],
            'Data Visualization': ['visualization', 'plotting', 'charts', 'graphs', 'visual', 'dashboard'],
            'Data Science': ['data science', 'data', 'analysis', 'analytics', 'insights', 'big data'],
            'Web Development': ['html', 'css', 'javascript', 'web', 'frontend', 'backend'],
            'Database': ['database', 'sql', 'mysql', 'postgresql', 'mongodb', 'query'],
            'Deep Learning': ['deep learning', 'neural networks', 'cnn', 'rnn', 'tensorflow', 'pytorch'],
            'Algorithms': ['algorithms', 'data structures', 'sorting', 'searching', 'complexity']
        }
        
        for topic_name, keywords in topic_keywords.items():
            # Calculate match score with exact matches getting higher weight
            score = 0
            matched_keywords = []
            
            for keyword in keywords:
                if keyword in text_lower:
                    if len(keyword.split()) > 1:  # Multi-word exact match
                        score += 3
                    else:
                        score += 1
                    matched_keywords.append(keyword)
            
            # Lower threshold for more granular detection
            if score >= 1:  # At least 1 keyword must match
                # Find related subtopics
                subtopics = []
                for keyword in matched_keywords:
                    subtopics.append(keyword.title())
                
                topics.append({
                    "name": topic_name,
                    "subtopics": subtopics[:4],  # Limit to 4 subtopics
                    "score": score
                })
        
        # Sort by score and return top matches
        topics.sort(key=lambda x: x.get('score', 0), reverse=True)
        return [{"name": t["name"], "subtopics": t["subtopics"]} for t in topics[:8]]
    
    def _infer_topic_name(self, items: List[str]) -> str:
        """Infer a topic name from a list of items"""
        # Look for common words or themes
        all_words = []
        for item in items:
            words = re.findall(r'\b[a-zA-Z]{3,}\b', item.lower())
            all_words.extend(words)
        
        # Count word frequency
        word_count = {}
        for word in all_words:
            word_count[word] = word_count.get(word, 0) + 1
        
        # Find most common meaningful word
        common_words = {'the', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by'}
        meaningful_words = [(word, count) for word, count in word_count.items() 
                           if word not in common_words and count > 1]
        
        if meaningful_words:
            most_common = max(meaningful_words, key=lambda x: x[1])
            return most_common[0].title() + " Topics"
        else:
            return "Course Topics"
    
    def _merge_similar_topics(self, topics: List[Dict]) -> List[Dict]:
        """Merge similar topics to avoid duplicates"""
        if not topics:
            return topics
        
        merged = []
        used_indices = set()
        
        for i, topic in enumerate(topics):
            if i in used_indices:
                continue
            
            current_topic = topic.copy()
            used_indices.add(i)
            
            # Look for similar topics
            for j, other_topic in enumerate(topics[i+1:], i+1):
                if j in used_indices:
                    continue
                
                # Check similarity
                if self._topics_similar(topic['name'], other_topic['name']):
                    # Merge subtopics
                    current_topic['subtopics'].extend(other_topic['subtopics'])
                    used_indices.add(j)
            
            # Remove duplicate subtopics
            current_topic['subtopics'] = list(set(current_topic['subtopics']))[:6]  # Limit to 6
            merged.append(current_topic)
        
        return merged[:8]  # Limit to 8 topics total
    
    def _topics_similar(self, name1: str, name2: str) -> bool:
        """Check if two topic names are similar"""
        name1_words = set(name1.lower().split())
        name2_words = set(name2.lower().split())
        
        # Remove common words
        common_words = {'the', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'topics', 'course'}
        name1_words -= common_words
        name2_words -= common_words
        
        if not name1_words or not name2_words:
            return False
        
        # Calculate overlap
        overlap = len(name1_words.intersection(name2_words))
        total = len(name1_words.union(name2_words))
        
        return overlap / total > 0.5  # 50% overlap threshold