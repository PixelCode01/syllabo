import json
import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict
import time

@dataclass
class ReviewItem:
    """Represents a topic for spaced repetition review"""
    topic_name: str
    description: str
    last_review: str
    next_review: str
    interval_index: int
    review_count: int
    success_streak: int
    total_successes: int
    total_reviews: int
    created_at: str
    
    def to_dict(self) -> Dict:
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'ReviewItem':
        return cls(**data)

class SpacedRepetitionEngine:
    """Implements spaced repetition using the Leitner system"""
    
    # Intervals in days - based on cognitive science research
    INTERVALS = [1, 3, 5, 11, 25, 44, 88]
    
    def __init__(self, data_file: str = "data/spaced_repetition.json"):
        self.data_file = data_file
        self.items: Dict[str, ReviewItem] = {}
        self.load_data()
    
    def load_data(self):
        """Load review items from JSON file"""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.items = {
                        name: ReviewItem.from_dict(item_data) 
                        for name, item_data in data.items()
                    }
            except Exception as e:
                print(f"Error loading spaced repetition data: {e}")
                self.items = {}
        else:
            self.items = {}
    
    def save_data(self):
        """Save review items to JSON file"""
        try:
            data = {name: item.to_dict() for name, item in self.items.items()}
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error saving spaced repetition data: {e}")
    
    def add_topic(self, topic_name: str, description: str = "") -> bool:
        """Add a new topic for spaced repetition"""
        # Check if topic already exists
        if topic_name in self.items:
            return False
        
        # Ensure topic_name is not None or empty
        if topic_name is None or topic_name.strip() == "":
            print("Error: Cannot add topic with empty name")
            return False
        
        try:
            now = datetime.now()
            # Calculate next review date using the first interval
            next_review = now + timedelta(days=self.INTERVALS[0])
            
            # Create the review item
            self.items[topic_name] = ReviewItem(
                topic_name=topic_name,
                description=description if description is not None else "",
                last_review="",
                next_review=next_review.isoformat(),
                interval_index=0,
                review_count=0,
                success_streak=0,
                total_successes=0,
                total_reviews=0,
                created_at=now.isoformat()
            )
            
            # Save to file
            self.save_data()
            return True
        except Exception as e:
            print(f"Error adding topic: {e}")
            return False
    
    def mark_review(self, topic_name: str, success: bool) -> bool:
        """Mark a topic as reviewed with success/failure"""
        if topic_name not in self.items:
            return False
        
        item = self.items[topic_name]
        now = datetime.now()
        
        # Update review statistics
        item.last_review = now.isoformat()
        item.review_count += 1
        item.total_reviews += 1
        
        if success:
            item.total_successes += 1
            item.success_streak += 1
            
            # Move to next interval if not at maximum
            if item.interval_index < len(self.INTERVALS) - 1:
                item.interval_index += 1
        else:
            item.success_streak = 0
            
            # Move back one interval on failure, but not below 0
            item.interval_index = max(0, item.interval_index - 1)
        
        # Calculate next review date
        interval_days = self.INTERVALS[item.interval_index]
        item.next_review = (now + timedelta(days=interval_days)).isoformat()
        
        self.save_data()
        return True
    
    def get_due_topics(self) -> List[ReviewItem]:
        """Get topics that are due for review"""
        now = datetime.now()
        due_items = []
        
        for item in self.items.values():
            next_review = datetime.fromisoformat(item.next_review)
            if next_review <= now:
                due_items.append(item)
        
        # Sort by next review date (most overdue first)
        due_items.sort(key=lambda x: datetime.fromisoformat(x.next_review))
        return due_items
    
    def get_upcoming_topics(self, days_ahead: int = 7) -> List[ReviewItem]:
        """Get topics due within the next N days"""
        now = datetime.now()
        cutoff = now + timedelta(days=days_ahead)
        upcoming = []
        
        for item in self.items.values():
            next_review = datetime.fromisoformat(item.next_review)
            if now < next_review <= cutoff:
                upcoming.append(item)
        
        upcoming.sort(key=lambda x: datetime.fromisoformat(x.next_review))
        return upcoming
    
    def get_topic_stats(self, topic_name: str) -> Optional[Dict]:
        """Get statistics for a specific topic"""
        if topic_name not in self.items:
            return None
        
        item = self.items[topic_name]
        success_rate = (item.total_successes / item.total_reviews * 100) if item.total_reviews > 0 else 0
        
        next_review = datetime.fromisoformat(item.next_review)
        # Calculate days until review and ensure it's an integer
        time_delta = (next_review - datetime.now())
        days_until_review = time_delta.days if time_delta.days is not None else 0
        
        # Ensure days_until_review is never negative
        days_until_review = max(0, days_until_review)
        
        return {
            'topic_name': item.topic_name,
            'description': item.description,
            'success_rate': round(success_rate, 1),
            'success_streak': item.success_streak,
            'total_reviews': item.total_reviews,
            'current_interval': self.INTERVALS[item.interval_index],
            'days_until_review': days_until_review,
            'next_review_date': next_review.strftime('%Y-%m-%d'),
            'mastery_level': self._get_mastery_level(item)
        }
    
    def _get_mastery_level(self, item: ReviewItem) -> str:
        """Determine mastery level based on interval and success rate"""
        success_rate = (item.total_successes / item.total_reviews * 100) if item.total_reviews > 0 else 0
        
        if item.interval_index >= 5 and success_rate >= 80:
            return "Mastered"
        elif item.interval_index >= 3 and success_rate >= 70:
            return "Advanced"
        elif item.interval_index >= 2 and success_rate >= 60:
            return "Intermediate"
        elif item.interval_index >= 1:
            return "Beginner"
        else:
            return "Learning"
    
    def get_all_topics(self) -> List[Dict]:
        """Get all topics with their statistics"""
        topics = []
        for name in self.items.keys():
            stats = self.get_topic_stats(name)
            if stats is not None:
                topics.append(stats)
        return topics
    
    def remove_topic(self, topic_name: str) -> bool:
        """Remove a topic from spaced repetition"""
        if topic_name in self.items:
            del self.items[topic_name]
            self.save_data()
            return True
        return False
    
    def get_study_summary(self) -> Dict:
        """Get overall study summary statistics"""
        if not self.items:
            return {
                'total_topics': 0,
                'due_now': 0,
                'due_today': 0,
                'mastered_topics': 0,
                'average_success_rate': 0
            }
        
        now = datetime.now()
        today_end = now.replace(hour=23, minute=59, second=59)
        
        due_now = len(self.get_due_topics())
        due_today = len([
            item for item in self.items.values()
            if datetime.fromisoformat(item.next_review) <= today_end
        ])
        
        mastered_topics = len([
            item for item in self.items.values()
            if self._get_mastery_level(item) == "Mastered"
        ])
        
        total_reviews = sum(item.total_reviews for item in self.items.values())
        total_successes = sum(item.total_successes for item in self.items.values())
        average_success_rate = (total_successes / total_reviews * 100) if total_reviews > 0 else 0
        
        return {
            'total_topics': len(self.items),
            'due_now': due_now,
            'due_today': due_today,
            'mastered_topics': mastered_topics,
            'average_success_rate': round(average_success_rate, 1)
        }