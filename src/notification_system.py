import os
import platform
from typing import List
from datetime import datetime

class NotificationSystem:
    """Cross-platform desktop notification system"""
    
    def __init__(self):
        self.system = platform.system().lower()
        self.notifications_enabled = self._check_notification_support()
    
    def _check_notification_support(self) -> bool:
        """Check if notifications are supported on this system"""
        try:
            if self.system == "windows":
                import warnings
                with warnings.catch_warnings():
                    warnings.filterwarnings("ignore", category=UserWarning, module="win10toast")
                    import win10toast
                return True
            elif self.system == "darwin":  # macOS
                return os.system("which osascript > /dev/null 2>&1") == 0
            elif self.system == "linux":
                return os.system("which notify-send > /dev/null 2>&1") == 0
            else:
                return False
        except ImportError:
            return False
    
    def send_notification(self, title: str, message: str, duration: int = 5) -> bool:
        """Send a desktop notification"""
        if not self.notifications_enabled:
            return False
        
        try:
            if self.system == "windows":
                return self._send_windows_notification(title, message, duration)
            elif self.system == "darwin":
                return self._send_macos_notification(title, message)
            elif self.system == "linux":
                return self._send_linux_notification(title, message, duration)
            else:
                return False
        except Exception as e:
            print(f"Failed to send notification: {e}")
            return False
    
    def _send_windows_notification(self, title: str, message: str, duration: int) -> bool:
        """Send notification on Windows"""
        try:
            # Suppress the pkg_resources deprecation warning from win10toast
            import warnings
            with warnings.catch_warnings():
                warnings.filterwarnings("ignore", category=UserWarning, module="win10toast")
                from win10toast import ToastNotifier
            toaster = ToastNotifier()
            toaster.show_toast(
                title,
                message,
                duration=duration,
                icon_path=None,
                threaded=True
            )
            return True
        except ImportError:
            # Fallback to basic Windows notification
            os.system(f'msg * "{title}: {message}"')
            return True
        except Exception:
            return False
    
    def _send_macos_notification(self, title: str, message: str) -> bool:
        """Send notification on macOS"""
        try:
            script = f'''
            display notification "{message}" with title "{title}"
            '''
            os.system(f"osascript -e '{script}'")
            return True
        except Exception:
            return False
    
    def _send_linux_notification(self, title: str, message: str, duration: int) -> bool:
        """Send notification on Linux"""
        try:
            duration_ms = duration * 1000
            os.system(f'notify-send "{title}" "{message}" -t {duration_ms}')
            return True
        except Exception:
            return False
    
    def notify_due_reviews(self, due_count: int) -> bool:
        """Send notification about due reviews"""
        if due_count == 0:
            return False
        
        title = "Syllabo - Review Time"
        if due_count == 1:
            message = "You have 1 topic ready for review"
        else:
            message = f"You have {due_count} topics ready for review"
        
        return self.send_notification(title, message)
    
    def notify_study_reminder(self, topic_name: str) -> bool:
        """Send notification for a specific topic review"""
        title = "Syllabo - Study Reminder"
        message = f"Time to review: {topic_name}"
        
        return self.send_notification(title, message)
    
    def notify_milestone(self, milestone_type: str, details: str) -> bool:
        """Send notification for study milestones"""
        title = f"Syllabo - {milestone_type}"
        
        return self.send_notification(title, details)

def install_notification_dependencies():
    """Install notification dependencies if needed"""
    system = platform.system().lower()
    
    if system == "windows":
        try:
            import win10toast
            print("Windows notifications ready")
        except ImportError:
            print("Installing Windows notification support...")
            os.system("pip install win10toast")
    
    elif system == "darwin":
        # macOS uses built-in osascript
        if os.system("which osascript > /dev/null 2>&1") == 0:
            print("macOS notifications ready")
        else:
            print("macOS notifications not available")
    
    elif system == "linux":
        # Linux uses notify-send
        if os.system("which notify-send > /dev/null 2>&1") == 0:
            print("Linux notifications ready")
        else:
            print("Install libnotify-bin for notifications: sudo apt-get install libnotify-bin")
    
    else:
        print("Notifications not supported on this platform")