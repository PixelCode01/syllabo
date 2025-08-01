from typing import Dict, List, Optional
import json
from datetime import datetime, timedelta
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress, BarColumn, TextColumn
from .database import SyllaboDatabase
from .spaced_repetition import SpacedRepetitionEngine
from .logger import SyllaboLogger

class ProgressDashboard:
    """Visual progress tracking and analytics dashboard"""
    
    def __init__(self, db: SyllaboDatabase = None, 
                 spaced_repetition: SpacedRepetitionEngine = None):
        self.db = db or SyllaboDatabase()
        self.spaced_repetition = spaced_repetition or SpacedRepetitionEngine()
        self.console = Console()
        self.logger = SyllaboLogger("progress_dashboard")
    
    def show_dashboard(self):
        """Display comprehensive progress dashboard"""
        self.console.clear()
        self.console.print(Panel.fit("LEARNING PROGRESS DASHBOARD", style="bold blue"))
        
        # Study streak
        streak_data = self._get_study_streak()
        self._display_study_streak(streak_data)
        
        # Topic progress
        topic_progress = self._get_topic_progress()
        self._display_topic_progress(topic_progress)
        
        # Weekly activity
        weekly_stats = self._get_weekly_stats()
        self._display_weekly_activity(weekly_stats)
        
        # Upcoming reviews
        upcoming = self._get_upcoming_reviews()
        self._display_upcoming_reviews(upcoming)
    
    def _get_study_streak(self) -> Dict:
        """Calculate current study streak"""
        # This would query database for daily study activity
        return {
            "current_streak": 7,
            "longest_streak": 15,
            "last_study_date": datetime.now().date(),
            "streak_active": True
        }
    
    def _display_study_streak(self, streak_data: Dict):
        """Display study streak information"""
        streak_panel = Panel(
            f"Current Streak: {streak_data['current_streak']} days\n"
            f"Longest Streak: {streak_data['longest_streak']} days\n"
            f"Status: {'Active' if streak_data['streak_active'] else 'Broken'}",
            title="Study Streak",
            style="green" if streak_data['streak_active'] else "red"
        )
        self.console.print(streak_panel)
    
    def _get_topic_progress(self) -> List[Dict]:
        """Get progress for all topics"""
        topics = self.spaced_repetition.get_all_topics()
        progress_data = []
        
        for topic in topics:
            mastery_level = self._calculate_mastery_level(topic)
            progress_data.append({
                "topic": topic.get("topic_name", "Unknown"),
                "mastery": mastery_level,
                "reviews": topic.get("total_reviews", 0),
                "success_rate": topic.get("success_rate", 0.0)
            })
        
        return progress_data
    
    def _display_topic_progress(self, topics: List[Dict]):
        """Display topic progress table"""
        table = Table(title="Topic Progress")
        table.add_column("Topic", style="cyan")
        table.add_column("Mastery", style="green")
        table.add_column("Reviews", justify="right")
        table.add_column("Success Rate", justify="right")
        
        for topic in topics[:10]:  # Show top 10
            mastery_bar = "█" * int(topic["mastery"] * 10) + "░" * (10 - int(topic["mastery"] * 10))
            table.add_row(
                topic["topic"][:30],
                f"{mastery_bar} {topic['mastery']:.1%}",
                str(topic["reviews"]),
                f"{topic['success_rate']:.1%}"
            )
        
        self.console.print(table)
    
    def _get_weekly_stats(self) -> Dict:
        """Get weekly study statistics"""
        return {
            "total_study_time": 420,  # minutes
            "sessions_completed": 12,
            "topics_reviewed": 8,
            "quizzes_taken": 3,
            "average_session_length": 35
        }
    
    def _display_weekly_activity(self, stats: Dict):
        """Display weekly activity summary"""
        activity_text = f"""
Study Time: {stats['total_study_time'] // 60}h {stats['total_study_time'] % 60}m
Sessions: {stats['sessions_completed']}
Topics Reviewed: {stats['topics_reviewed']}
Quizzes Taken: {stats['quizzes_taken']}
Avg Session: {stats['average_session_length']} min
        """.strip()
        
        activity_panel = Panel(activity_text, title="This Week", style="blue")
        self.console.print(activity_panel)
    
    def _get_upcoming_reviews(self) -> List[Dict]:
        """Get upcoming review schedule"""
        due_topics = self.spaced_repetition.get_due_topics()
        return due_topics[:5]  # Next 5 reviews
    
    def _display_upcoming_reviews(self, reviews: List):
        """Display upcoming reviews"""
        if not reviews:
            self.console.print(Panel("No reviews due", title="Upcoming Reviews"))
            return
        
        review_text = "\n".join([
            f"• {getattr(review, 'topic_name', 'Unknown')} - Due: {getattr(review, 'next_review', 'Now')}"
            for review in reviews
        ])
        
        review_panel = Panel(review_text, title="Upcoming Reviews", style="yellow")
        self.console.print(review_panel)
    
    def _calculate_mastery_level(self, topic: Dict) -> float:
        """Calculate mastery level for a topic"""
        success_streak = topic.get("success_streak", 0)
        total_reviews = topic.get("total_reviews", 1)
        
        # Simple mastery calculation
        base_mastery = min(success_streak / 5, 1.0)  # Max at 5 successful reviews
        review_bonus = min(total_reviews / 10, 0.2)  # Up to 20% bonus for experience
        
        return min(base_mastery + review_bonus, 1.0)
    
    def generate_progress_report(self) -> str:
        """Generate text-based progress report"""
        streak_data = self._get_study_streak()
        weekly_stats = self._get_weekly_stats()
        topic_progress = self._get_topic_progress()
        
        report = f"""
LEARNING PROGRESS REPORT
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}

STUDY STREAK
Current: {streak_data['current_streak']} days
Longest: {streak_data['longest_streak']} days

WEEKLY SUMMARY
Study Time: {weekly_stats['total_study_time'] // 60}h {weekly_stats['total_study_time'] % 60}m
Sessions: {weekly_stats['sessions_completed']}
Topics: {weekly_stats['topics_reviewed']}

TOP PERFORMING TOPICS
"""
        
        # Add top 5 topics by mastery
        sorted_topics = sorted(topic_progress, key=lambda x: x['mastery'], reverse=True)
        for i, topic in enumerate(sorted_topics[:5], 1):
            report += f"{i}. {topic['topic']} - {topic['mastery']:.1%} mastery\n"
        
        return report