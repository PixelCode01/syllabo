from typing import Dict, List, Optional, Tuple
import json
import os
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict
from .logger import SyllaboLogger
from .spaced_repetition import SpacedRepetitionEngine
from .database import SyllaboDatabase

@dataclass
class Achievement:
    """Represents a learning achievement or badge"""
    id: str
    name: str
    description: str
    icon: str  # Icon identifier
    category: str  # Category of achievement (streak, mastery, exploration, etc.)
    unlocked: bool
    unlock_date: Optional[str]  # ISO format date when unlocked
    progress: int  # Current progress towards achievement
    target: int  # Target value to unlock achievement
    
    def to_dict(self) -> Dict:
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'Achievement':
        return cls(**data)

class AchievementSystem:
    """System for tracking achievements, badges, and learning streaks"""
    
    def __init__(self, db: SyllaboDatabase = None, 
                 spaced_repetition: SpacedRepetitionEngine = None):
        self.logger = SyllaboLogger("achievement_system")
        self.db = db or SyllaboDatabase()
        self.spaced_repetition = spaced_repetition or SpacedRepetitionEngine()
        self.data_file = "achievements.json"
        self.achievements = {}
        self.streaks = {}
        self._load_data()
        self._initialize_achievements()
    
    def _load_data(self):
        """Load achievements and streaks data"""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.achievements = {
                        id: Achievement.from_dict(achievement_data)
                        for id, achievement_data in data.get('achievements', {}).items()
                    }
                    self.streaks = data.get('streaks', {})
            except Exception as e:
                self.logger.error(f"Error loading achievements data: {e}")
                self.achievements = {}
                self.streaks = {}
        else:
            self.achievements = {}
            self.streaks = self._initialize_streaks()
    
    def _save_data(self):
        """Save achievements and streaks data"""
        try:
            data = {
                'achievements': {id: achievement.to_dict() for id, achievement in self.achievements.items()},
                'streaks': self.streaks
            }
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            self.logger.error(f"Error saving achievements data: {e}")
    
    def _initialize_streaks(self) -> Dict:
        """Initialize streak tracking data"""
        return {
            'current_streak': 0,
            'longest_streak': 0,
            'last_activity_date': '',
            'streak_history': [],
            'total_study_days': 0
        }
    
    def _initialize_achievements(self):
        """Initialize default achievements if not present"""
        default_achievements = [
            # Streak achievements
            Achievement(
                id="streak_3",
                name="3-Day Streak",
                description="Study for 3 consecutive days",
                icon="calendar-check",
                category="streak",
                unlocked=False,
                unlock_date=None,
                progress=self.streaks.get('current_streak', 0),
                target=3
            ),
            Achievement(
                id="streak_7",
                name="Weekly Warrior",
                description="Maintain a 7-day study streak",
                icon="calendar-week",
                category="streak",
                unlocked=False,
                unlock_date=None,
                progress=self.streaks.get('current_streak', 0),
                target=7
            ),
            Achievement(
                id="streak_30",
                name="Monthly Master",
                description="Maintain a 30-day study streak",
                icon="calendar-month",
                category="streak",
                unlocked=False,
                unlock_date=None,
                progress=self.streaks.get('current_streak', 0),
                target=30
            ),
            
            # Topic mastery achievements
            Achievement(
                id="mastery_1",
                name="First Mastery",
                description="Master your first topic",
                icon="star",
                category="mastery",
                unlocked=False,
                unlock_date=None,
                progress=0,
                target=1
            ),
            Achievement(
                id="mastery_5",
                name="Knowledge Collector",
                description="Master 5 different topics",
                icon="stars",
                category="mastery",
                unlocked=False,
                unlock_date=None,
                progress=0,
                target=5
            ),
            
            # Review achievements
            Achievement(
                id="reviews_10",
                name="Review Rookie",
                description="Complete 10 topic reviews",
                icon="check-circle",
                category="reviews",
                unlocked=False,
                unlock_date=None,
                progress=0,
                target=10
            ),
            Achievement(
                id="reviews_50",
                name="Review Pro",
                description="Complete 50 topic reviews",
                icon="check-double",
                category="reviews",
                unlocked=False,
                unlock_date=None,
                progress=0,
                target=50
            ),
            
            # Perfect score achievements
            Achievement(
                id="perfect_5",
                name="Perfect Recall",
                description="Get 5 perfect reviews in a row",
                icon="award",
                category="performance",
                unlocked=False,
                unlock_date=None,
                progress=0,
                target=5
            )
        ]
        
        # Add default achievements if they don't exist
        for achievement in default_achievements:
            if achievement.id not in self.achievements:
                self.achievements[achievement.id] = achievement
        
        # Save if any were added
        if len(self.achievements) >= len(default_achievements):
            self._save_data()

    def get_unlocked_achievements(self) -> List[Achievement]:
        """Get a list of all unlocked achievements"""
        return sorted([ach for ach in self.achievements.values() if ach.unlocked], key=lambda x: x.unlock_date, reverse=True)

    def get_in_progress_achievements(self) -> List[Achievement]:
        """Get a list of achievements that are not yet unlocked"""
        return sorted([ach for ach in self.achievements.values() if not ach.unlocked], key=lambda x: x.progress, reverse=True)
    
    def update_streak(self) -> Dict:
        """Update learning streak based on current activity"""
        today = datetime.now().date()
        today_str = today.isoformat()
        
        # Initialize if empty
        if not self.streaks:
            self.streaks = self._initialize_streaks()
        
        # Get last activity date
        last_date_str = self.streaks.get('last_activity_date', '')
        
        if last_date_str:
            try:
                last_date = datetime.fromisoformat(last_date_str).date()
                date_diff = (today - last_date).days
                
                if date_diff == 0:
                    # Already recorded activity today
                    pass
                elif date_diff == 1:
                    # Consecutive day, increment streak
                    self.streaks['current_streak'] += 1
                    self.streaks['total_study_days'] += 1
                    
                    # Update longest streak if needed
                    if self.streaks['current_streak'] > self.streaks['longest_streak']:
                        self.streaks['longest_streak'] = self.streaks['current_streak']
                    
                    # Add to history
                    self.streaks['streak_history'].append(today_str)
                else:
                    # Streak broken
                    self.streaks['current_streak'] = 1
                    self.streaks['total_study_days'] += 1
                    self.streaks['streak_history'] = [today_str]
            except ValueError:
                # Invalid date format, reset
                self.streaks['current_streak'] = 1
                self.streaks['total_study_days'] = 1
                self.streaks['streak_history'] = [today_str]
        else:
            # First activity
            self.streaks['current_streak'] = 1
            self.streaks['longest_streak'] = 1
            self.streaks['total_study_days'] = 1
            self.streaks['streak_history'] = [today_str]
        
        # Update last activity date
        self.streaks['last_activity_date'] = today_str
        
        # Check for streak achievements
        self._update_achievement_progress()
        
        # Save data
        self._save_data()
        
        return {
            'current_streak': self.streaks['current_streak'],
            'longest_streak': self.streaks['longest_streak'],
            'total_study_days': self.streaks['total_study_days']
        }
    
    def _update_achievement_progress(self):
        """Update progress for all achievements"""
        # Get current stats
        current_streak = self.streaks.get('current_streak', 0)
        mastered_topics = len(self._get_mastered_topics())
        total_reviews = self._get_total_reviews()
        perfect_streak = self._get_perfect_review_streak()
        
        # Update streak achievements
        for streak_id in ["streak_3", "streak_7", "streak_30"]:
            if streak_id in self.achievements:
                achievement = self.achievements[streak_id]
                achievement.progress = current_streak
                if current_streak >= achievement.target and not achievement.unlocked:
                    self._unlock_achievement(achievement.id)
        
        # Update mastery achievements
        for mastery_id in ["mastery_1", "mastery_5"]:
            if mastery_id in self.achievements:
                achievement = self.achievements[mastery_id]
                achievement.progress = mastered_topics
                if mastered_topics >= achievement.target and not achievement.unlocked:
                    self._unlock_achievement(achievement.id)
        
        # Update review achievements
        for review_id in ["reviews_10", "reviews_50"]:
            if review_id in self.achievements:
                achievement = self.achievements[review_id]
                achievement.progress = total_reviews
                if total_reviews >= achievement.target and not achievement.unlocked:
                    self._unlock_achievement(achievement.id)
        
        # Update perfect score achievements
        if "perfect_5" in self.achievements:
            achievement = self.achievements["perfect_5"]
            achievement.progress = perfect_streak
            if perfect_streak >= achievement.target and not achievement.unlocked:
                self._unlock_achievement(achievement.id)
    
    def _unlock_achievement(self, achievement_id: str) -> bool:
        """Unlock an achievement"""
        if achievement_id in self.achievements:
            achievement = self.achievements[achievement_id]
            if not achievement.unlocked:
                achievement.unlocked = True
                achievement.unlock_date = datetime.now().isoformat()
                self._save_data()
                return True
        return False
    
    def _get_mastered_topics(self) -> List[str]:
        """Get list of mastered topics"""
        topics = self.spaced_repetition.get_all_topics()
        return [topic['topic_name'] for topic in topics 
                if topic.get('mastery_level') == "Mastered"]
    
    def _get_total_reviews(self) -> int:
        """Get total number of reviews completed"""
        total = 0
        for topic in self.spaced_repetition.get_all_topics():
            total += topic.get('total_reviews', 0)
        return total
    
    def _get_perfect_review_streak(self) -> int:
        """Get current streak of perfect reviews"""
        # This would need to track review results in the spaced repetition system
        # For now, return a placeholder value
        return 0

    def get_mastered_topics_count(self) -> int:
        """Get the number of mastered topics"""
        return len(self._get_mastered_topics())
    
    def get_total_reviews_count(self) -> int:
        """Get the total number of reviews completed"""
        return self._get_total_reviews()
    
    def get_all_achievements(self) -> List[Dict]:
        """Get all achievements with their status"""
        return [achievement.to_dict() for achievement in self.achievements.values()]
    
    def get_unlocked_achievements(self) -> List[Dict]:
        """Get only unlocked achievements"""
        return [achievement.to_dict() for achievement in self.achievements.values() 
                if achievement.unlocked]
    
    def get_streak_info(self) -> Dict:
        """Get current streak information"""
        return self.streaks
    
    def get_recent_achievements(self, count: int = 5) -> List[Dict]:
        """Get recently unlocked achievements"""
        unlocked = [achievement for achievement in self.achievements.values() 
                   if achievement.unlocked and achievement.unlock_date]
        
        # Sort by unlock date (most recent first)
        sorted_achievements = sorted(
            unlocked,
            key=lambda a: datetime.fromisoformat(a.unlock_date) if a.unlock_date else datetime.min,
            reverse=True
        )
        
        return [achievement.to_dict() for achievement in sorted_achievements[:count]]