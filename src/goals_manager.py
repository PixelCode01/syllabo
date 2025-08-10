from typing import Dict, List, Optional
import json
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict
from .database import SyllaboDatabase
from .logger import SyllaboLogger

@dataclass
class StudyGoal:
    """Represents a study goal or milestone"""
    id: str
    title: str
    description: str
    goal_type: str  # daily, weekly, monthly, milestone
    target_value: int
    current_value: int
    unit: str  # minutes, topics, quizzes, etc.
    deadline: str
    created_at: str
    completed: bool = False
    completed_at: Optional[str] = None

class GoalsManager:
    """Manage study goals and milestones"""
    
    def __init__(self, db: SyllaboDatabase = None):
        self.db = db or SyllaboDatabase()
        self.logger = SyllaboLogger("goals_manager")
        self.goals_file = "data/study_goals.json"
        self.goals = self._load_goals()
    
    def _load_goals(self) -> Dict[str, StudyGoal]:
        """Load goals from file"""
        try:
            # Create data directory if it doesn't exist
            import os
            os.makedirs(os.path.dirname(self.goals_file), exist_ok=True)
            with open(self.goals_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return {
                    goal_id: StudyGoal(**goal_data) 
                    for goal_id, goal_data in data.items()
                }
        except (FileNotFoundError, UnicodeDecodeError, json.JSONDecodeError):
            # If file doesn't exist or has encoding issues, start fresh
            return {}
    
    def _save_goals(self):
        """Save goals to file"""
        data = {goal_id: asdict(goal) for goal_id, goal in self.goals.items()}
        with open(self.goals_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    
    def create_goal(self, title: str, description: str, goal_type: str,
                   target_value: int, unit: str, days_to_complete: int = 30) -> str:
        """Create a new study goal"""
        goal_id = f"goal_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        deadline = (datetime.now() + timedelta(days=days_to_complete)).isoformat()
        
        goal = StudyGoal(
            id=goal_id,
            title=title,
            description=description,
            goal_type=goal_type,
            target_value=target_value,
            current_value=0,
            unit=unit,
            deadline=deadline,
            created_at=datetime.now().isoformat()
        )
        
        self.goals[goal_id] = goal
        self._save_goals()
        
        self.logger.info(f"Created goal: {title}")
        return goal_id
    
    def update_goal_progress(self, goal_id: str, progress_increment: int) -> bool:
        """Update progress on a goal"""
        if goal_id not in self.goals:
            return False
        
        goal = self.goals[goal_id]
        goal.current_value += progress_increment
        
        # Check if goal is completed
        if goal.current_value >= goal.target_value and not goal.completed:
            goal.completed = True
            goal.completed_at = datetime.now().isoformat()
            self.logger.info(f"Goal completed: {goal.title}")
        
        self._save_goals()
        return True
    
    def get_active_goals(self) -> List[StudyGoal]:
        """Get all active (non-completed) goals"""
        return [goal for goal in self.goals.values() if not goal.completed]
    
    def get_completed_goals(self) -> List[StudyGoal]:
        """Get all completed goals"""
        return [goal for goal in self.goals.values() if goal.completed]
    
    def get_goals_by_type(self, goal_type: str) -> List[StudyGoal]:
        """Get goals by type"""
        return [goal for goal in self.goals.values() if goal.goal_type == goal_type]
    
    def check_daily_goals(self) -> Dict:
        """Check progress on daily goals"""
        daily_goals = self.get_goals_by_type("daily")
        today = datetime.now().date()
        
        results = {
            "total_daily_goals": len(daily_goals),
            "completed_today": 0,
            "progress": []
        }
        
        for goal in daily_goals:
            # Reset daily goals each day
            goal_date = datetime.fromisoformat(goal.created_at).date()
            if goal_date < today:
                goal.current_value = 0
                goal.completed = False
                goal.completed_at = None
            
            progress_percent = min((goal.current_value / goal.target_value) * 100, 100)
            
            results["progress"].append({
                "title": goal.title,
                "progress": progress_percent,
                "current": goal.current_value,
                "target": goal.target_value,
                "unit": goal.unit,
                "completed": goal.completed
            })
            
            if goal.completed:
                results["completed_today"] += 1
        
        self._save_goals()
        return results
    
    def suggest_goals(self, user_level: str = "beginner") -> List[Dict]:
        """Suggest appropriate goals based on user level"""
        suggestions = {
            "beginner": [
                {"title": "Study 15 minutes daily", "type": "daily", "target": 15, "unit": "minutes"},
                {"title": "Complete 1 topic this week", "type": "weekly", "target": 1, "unit": "topics"},
                {"title": "Take 2 quizzes this week", "type": "weekly", "target": 2, "unit": "quizzes"}
            ],
            "intermediate": [
                {"title": "Study 30 minutes daily", "type": "daily", "target": 30, "unit": "minutes"},
                {"title": "Complete 3 topics this week", "type": "weekly", "target": 3, "unit": "topics"},
                {"title": "Maintain 7-day study streak", "type": "milestone", "target": 7, "unit": "days"}
            ],
            "advanced": [
                {"title": "Study 60 minutes daily", "type": "daily", "target": 60, "unit": "minutes"},
                {"title": "Complete 5 topics this week", "type": "weekly", "target": 5, "unit": "topics"},
                {"title": "Achieve 90% quiz average", "type": "milestone", "target": 90, "unit": "percent"}
            ]
        }
        
        return suggestions.get(user_level, suggestions["beginner"])
    
    def get_goal_summary(self) -> Dict:
        """Get summary of all goals"""
        active_goals = self.get_active_goals()
        completed_goals = self.get_completed_goals()
        
        return {
            "total_goals": len(self.goals),
            "active_goals": len(active_goals),
            "completed_goals": len(completed_goals),
            "completion_rate": len(completed_goals) / len(self.goals) if self.goals else 0,
            "recent_completions": [
                goal.title for goal in completed_goals 
                if goal.completed_at and 
                datetime.fromisoformat(goal.completed_at) > datetime.now() - timedelta(days=7)
            ]
        }
    
    def get_all_goals(self) -> List[StudyGoal]:
        """Get all goals (active and completed)"""
        return list(self.goals.values())