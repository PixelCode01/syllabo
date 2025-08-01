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
        
        # If we have good text-based results, use them
        if len(text_topics) >= 3:
            return text_topics
        
        # Otherwise, try AI enhancement
        try:
            prompt = f"""Extract main topics from this syllabus as JSON array:
[{{"name": "Topic Name", "subtopics": ["subtopic1", "subtopic2"]}}]

Syllabus:
{syllabus_text[:2000]}"""
            
            response = await ai_client.get_completion(prompt)
            
            import json
            ai_topics = json.loads(response)
            
            # Validate and merge with text-based topics
            if isinstance(ai_topics, list) and len(ai_topics) > 0:
                # Merge unique topics
                all_topics = text_topics.copy()
                existing_names = {t['name'].lower() for t in text_topics}
                
                for ai_topic in ai_topics:
                    if ai_topic.get('name', '').lower() not in existing_names:
                        all_topics.append(ai_topic)
                
                return all_topics[:8]  # Limit to 8 topics
            else:
                return text_topics
                
        except Exception:
            return text_topics
    
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
            'Python Programming': ['python', 'programming', 'coding', 'script', 'interpreter'],
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