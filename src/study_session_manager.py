from typing import Dict, List, Optional
import time
from datetime import datetime, timedelta
from dataclasses import dataclass
from .notification_system import NotificationSystem
from .spaced_repetition import SpacedRepetitionEngine
from .logger import SyllaboLogger

@dataclass
class StudySession:
    """Represents a study session"""
    topic: str
    start_time: datetime
    planned_duration: int  # minutes
    actual_duration: Optional[int] = None
    breaks_taken: int = 0
    focus_score: Optional[float] = None
    completion_status: str = "in_progress"  # in_progress, completed, interrupted
    notes: str = ""

class StudySessionManager:
    """Manages interactive study sessions with Pomodoro technique"""
    
    def __init__(self, spaced_repetition: SpacedRepetitionEngine = None):
        self.spaced_repetition = spaced_repetition or SpacedRepetitionEngine()
        self.notifications = NotificationSystem()
        self.logger = SyllaboLogger("study_session")
        self.current_session: Optional[StudySession] = None
        
        # Pomodoro settings
        self.work_duration = 25  # minutes
        self.short_break = 5     # minutes
        self.long_break = 15     # minutes
        self.sessions_until_long_break = 4
    
    def start_study_session(self, topic: str, planned_duration: int = 25) -> StudySession:
        """Start a new study session"""
        if self.current_session and self.current_session.completion_status == "in_progress":
            self.logger.warning("Another session is already in progress")
            return self.current_session
        
        self.current_session = StudySession(
            topic=topic,
            start_time=datetime.now(),
            planned_duration=planned_duration
        )
        
        self.logger.info(f"Started study session for: {topic}")
        self.notifications.send_notification(
            "Study Session Started",
            f"Focusing on: {topic} for {planned_duration} minutes"
        )
        
        return self.current_session
    
    def take_break(self, break_type: str = "short") -> bool:
        """Take a study break"""
        if not self.current_session:
            return False
        
        break_duration = self.short_break if break_type == "short" else self.long_break
        
        self.current_session.breaks_taken += 1
        self.notifications.send_notification(
            f"{break_type.title()} Break Time",
            f"Take a {break_duration} minute break. You've earned it!"
        )
        
        # Schedule break end notification
        self._schedule_break_end_notification(break_duration)
        
        return True
    
    def end_session(self, completion_status: str = "completed", notes: str = "") -> Dict:
        """End the current study session"""
        if not self.current_session:
            return {"error": "No active session"}
        
        self.current_session.actual_duration = int(
            (datetime.now() - self.current_session.start_time).total_seconds() / 60
        )
        self.current_session.completion_status = completion_status
        self.current_session.notes = notes
        
        # Calculate focus score based on planned vs actual duration
        focus_score = min(1.0, self.current_session.actual_duration / self.current_session.planned_duration)
        self.current_session.focus_score = focus_score
        
        session_summary = {
            "topic": self.current_session.topic,
            "duration": self.current_session.actual_duration,
            "focus_score": focus_score,
            "breaks_taken": self.current_session.breaks_taken,
            "status": completion_status
        }
        
        self.logger.info(f"Session completed: {session_summary}")
        
        # Reset current session
        self.current_session = None
        
        return session_summary
    
    def get_session_stats(self) -> Dict:
        """Get statistics for current or recent sessions"""
        if self.current_session:
            elapsed = (datetime.now() - self.current_session.start_time).total_seconds() / 60
            return {
                "current_session": {
                    "topic": self.current_session.topic,
                    "elapsed_minutes": int(elapsed),
                    "planned_duration": self.current_session.planned_duration,
                    "breaks_taken": self.current_session.breaks_taken
                }
            }
        
        return {"current_session": None}
    
    def suggest_next_topic(self) -> Optional[str]:
        """Suggest the next topic to study based on spaced repetition"""
        due_topics = self.spaced_repetition.get_due_topics()
        if due_topics:
            return due_topics[0]['topic_name']
        return None
    
    def _schedule_break_end_notification(self, break_duration: int):
        """Schedule notification for when break ends"""
        import threading
        
        def notify_break_end():
            time.sleep(break_duration * 60)
            self.notifications.send_notification(
                "Break Over",
                "Time to get back to studying!"
            )
        
        thread = threading.Thread(target=notify_break_end)
        thread.daemon = True
        thread.start()
    
    def get_pomodoro_stats(self) -> Dict:
        """Get Pomodoro technique statistics"""
        # This would typically load from database
        return {
            "sessions_today": 0,
            "total_focus_time": 0,
            "average_session_length": 0,
            "break_compliance": 0.0
        }