from typing import Dict, List, Optional
import os
import json
from datetime import datetime, timedelta
import platform
import webbrowser
from .logger import SyllaboLogger
from .spaced_repetition import SpacedRepetitionEngine

class CalendarSync:
    """Calendar synchronization system for study schedules"""
    
    def __init__(self, spaced_repetition: SpacedRepetitionEngine = None):
        self.logger = SyllaboLogger("calendar_sync")
        self.spaced_repetition = spaced_repetition or SpacedRepetitionEngine()
        self.calendar_data_file = "calendar_sync.json"
        self.calendar_settings = self._load_settings()
        
    def _load_settings(self) -> Dict:
        """Load calendar sync settings"""
        if os.path.exists(self.calendar_data_file):
            try:
                with open(self.calendar_data_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                self.logger.error(f"Error loading calendar settings: {e}")
                return self._default_settings()
        else:
            return self._default_settings()
    
    def _default_settings(self) -> Dict:
        """Default calendar settings"""
        return {
            "enabled": False,
            "calendar_type": "none",  # none, google, outlook, ical
            "sync_frequency": "daily",  # daily, weekly, manual
            "last_sync": "",
            "reminder_minutes": 30,
            "calendar_id": "",
            "sync_topics": True,
            "sync_sessions": True
        }
    
    def _save_settings(self):
        """Save calendar sync settings"""
        try:
            with open(self.calendar_data_file, 'w', encoding='utf-8') as f:
                json.dump(self.calendar_settings, f, indent=2, ensure_ascii=False)
        except Exception as e:
            self.logger.error(f"Error saving calendar settings: {e}")
    
    def update_settings(self, settings: Dict) -> bool:
        """Update calendar sync settings"""
        try:
            # Update only provided settings
            for key, value in settings.items():
                if key in self.calendar_settings:
                    self.calendar_settings[key] = value
            
            self._save_settings()
            return True
        except Exception as e:
            self.logger.error(f"Error updating calendar settings: {e}")
            return False
    
    def get_settings(self) -> Dict:
        """Get current calendar sync settings"""
        return self.calendar_settings
    
    def generate_ical_file(self, filename: str = "syllabo_schedule.ics") -> str:
        """Generate iCalendar file for import into calendar apps"""
        try:
            # Get due topics
            due_topics = self.spaced_repetition.get_due_topics()
            upcoming_topics = self.spaced_repetition.get_upcoming_topics(days_ahead=14)
            
            # Combine all topi\cs to include in calendar
            all_topics = due_topics + [topic for topic in upcoming_topics if topic not in due_topics]
            
            if not all_topics:
                return ""
            
            # Generate iCalendar content
            ical_content = [
                "BEGIN:VCALENDAR",
                "VERSION:2.0",
                "PRODID:-//Syllabo//Study Schedule//EN",
                "CALSCALE:GREGORIAN",
                "METHOD:PUBLISH"
            ]
            
            # Add events for each topic
            for topic in all_topics:
                event_id = f"syllabo-{hash(topic.topic_name)}-{datetime.now().strftime('%Y%m%d')}"
                next_review = datetime.fromisoformat(topic.next_review)
                end_time = next_review + timedelta(minutes=30)  # Default 30 min study session
                
                ical_content.extend([
                    "BEGIN:VEVENT",
                    f"UID:{event_id}",
                    f"DTSTAMP:{datetime.now().strftime('%Y%m%dT%H%M%SZ')}",
                    f"DTSTART:{next_review.strftime('%Y%m%dT%H%M%SZ')}",
                    f"DTEND:{end_time.strftime('%Y%m%dT%H%M%SZ')}",
                    f"SUMMARY:Review: {topic.topic_name}",
                    f"DESCRIPTION:Study session for {topic.topic_name}\n{topic.description}",
                    "STATUS:CONFIRMED",
                    f"CATEGORIES:Syllabo,Study,{topic.topic_name}",
                    "END:VEVENT"
                ])
            
            ical_content.append("END:VCALENDAR")
            
            # Write to file
            with open(filename, 'w', encoding='utf-8') as f:
                f.write("\n".join(ical_content))
            
            return os.path.abspath(filename)
            
        except Exception as e:
            self.logger.error(f"Error generating iCalendar file: {e}")
            return ""
    
    def open_calendar_file(self, filename: str) -> bool:
        """Open the generated calendar file"""
        try:
            if os.path.exists(filename):
                webbrowser.open(filename)
                return True
            return False
        except Exception as e:
            self.logger.error(f"Error opening calendar file: {e}")
            return False
    
    def sync_calendar(self) -> Dict:
        """Synchronize study schedule with calendar"""
        result = {
            "success": False,
            "message": "",
            "synced_items": 0,
            "calendar_type": self.calendar_settings["calendar_type"]
        }
        
        if not self.calendar_settings["enabled"]:
            result["message"] = "Calendar sync is disabled"
            return result
        
        try:
            # For now, just generate iCal file
            calendar_file = self.generate_ical_file()
            
            if calendar_file:
                # Update last sync time
                self.calendar_settings["last_sync"] = datetime.now().isoformat()
                self._save_settings()
                
                result["success"] = True
                result["message"] = f"Generated calendar file: {calendar_file}"
                result["file_path"] = calendar_file
            else:
                result["message"] = "No topics to sync"
            
            return result
            
        except Exception as e:
            self.logger.error(f"Calendar sync failed: {e}")
            result["message"] = f"Sync failed: {str(e)}"
            return result