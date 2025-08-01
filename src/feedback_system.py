import json
import os
from typing import Dict, List, Optional
from datetime import datetime
from .logger import SyllaboLogger

class FeedbackSystem:
    def __init__(self, feedback_file="feedback.json"):
        self.feedback_file = feedback_file
        self.feedback_data = self._load_feedback()
        self.logger = SyllaboLogger("feedback_system")
    
    def _load_feedback(self) -> Dict:
        if os.path.exists(self.feedback_file):
            with open(self.feedback_file, 'r') as f:
                return json.load(f)
        return {"videos": {}, "topics": {}}
    
    def _save_feedback(self):
        with open(self.feedback_file, 'w') as f:
            json.dump(self.feedback_data, f, indent=2)
    
    def add_video_feedback(self, video_id: str, topic: str, rating: int, comment: str = ""):
        if video_id not in self.feedback_data["videos"]:
            self.feedback_data["videos"][video_id] = []
        
        feedback_entry = {
            "topic": topic,
            "rating": rating,
            "comment": comment,
            "timestamp": datetime.now().isoformat()
        }
        
        self.feedback_data["videos"][video_id].append(feedback_entry)
        self._save_feedback()
    
    def get_video_feedback(self, video_id: str) -> List[Dict]:
        return self.feedback_data["videos"].get(video_id, [])
    
    def get_average_rating(self, video_id: str) -> float:
        feedback = self.get_video_feedback(video_id)
        if not feedback:
            return 0.0
        
        ratings = [f["rating"] for f in feedback]
        return sum(ratings) / len(ratings)
    
    def add_topic_feedback(self, topic: str, missing_subtopics: List[str]):
        if topic not in self.feedback_data["topics"]:
            self.feedback_data["topics"][topic] = {"missing_subtopics": []}
        
        self.feedback_data["topics"][topic]["missing_subtopics"].extend(missing_subtopics)
        self._save_feedback()
    
    def get_topic_feedback(self, topic: str) -> Dict:
        return self.feedback_data["topics"].get(topic, {})