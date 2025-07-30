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
        prompt = f"""Extract main topics from this syllabus as JSON array:
[{{"name": "Topic Name", "subtopics": ["subtopic1", "subtopic2"]}}]

Syllabus:
{syllabus_text[:2000]}"""
        
        response = await ai_client.get_completion(prompt)
        
        try:
            import json
            topics = json.loads(response)
            return topics
        except:
            return self._fallback_extraction(syllabus_text)
    
    def _fallback_extraction(self, text: str) -> List[Dict]:
        lines = text.split('\n')
        topics = []
        current_topic = None
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            if re.match(r'^(Chapter|Unit|Topic|Week)\s*\d+', line, re.IGNORECASE):
                if current_topic:
                    topics.append(current_topic)
                current_topic = {"name": line, "subtopics": []}
            elif current_topic and line.startswith('-'):
                current_topic["subtopics"].append(line[1:].strip())
        
        if current_topic:
            topics.append(current_topic)
        
        return topics if topics else [{"name": "General Course Content", "subtopics": []}]