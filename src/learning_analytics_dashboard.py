"""
Learning Analytics Dashboard
Provides comprehensive learning analytics, velocity tracking, and predictive insights
"""

import json
import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, asdict
import statistics
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress, BarColumn, TextColumn, SpinnerColumn
from rich.layout import Layout
from rich.text import Text
from rich.rule import Rule
from .ai_client import AIClient
from .database import SyllaboDatabase
from .logger import SyllaboLogger

@dataclass
class LearningSession:
    """Individual learning session data"""
    session_id: str
    user_id: str
    start_time: str
    end_time: str
    duration_minutes: int
    activities: List[str]  # quiz, video, reading, practice
    concepts_covered: List[str]
    performance_score: float
    engagement_level: float  # 0.0 to 1.0
    session_type: str  # study, review, assessment

@dataclass
class LearningVelocity:
    """Learning velocity metrics"""
    user_id: str
    time_period: str  # daily, weekly, monthly
    concepts_learned: int
    concepts_mastered: int
    study_time_minutes: int
    quiz_attempts: int
    average_score: float
    velocity_score: float  # concepts per hour
    acceleration: float  # change in velocity
    calculated_at: str

@dataclass
class RetentionMetrics:
    """Knowledge retention analysis"""
    user_id: str
    concept_id: str
    initial_score: float
    scores_over_time: List[Tuple[str, float]]  # (date, score)
    retention_rate: float  # 0.0 to 1.0
    forgetting_curve_fit: Dict[str, float]
    optimal_review_interval: int  # days
    last_review: str
    next_suggested_review: str

@dataclass
class StudyPattern:
    """User study pattern analysis"""
    user_id: str
    optimal_study_times: List[str]  # hour ranges
    optimal_session_length: int  # minutes
    preferred_break_intervals: int  # minutes
    peak_performance_hours: List[int]
    study_consistency_score: float
    weekly_pattern: Dict[str, float]  # day -> activity level
    monthly_trend: List[float]

class LearningAnalyticsDashboard:
    """Comprehensive learning analytics and insights"""
    
    def __init__(self, ai_client: AIClient = None, db: SyllaboDatabase = None):
        self.ai_client = ai_client or AIClient()
        self.db = db or SyllaboDatabase()
        self.logger = SyllaboLogger("learning_analytics")
        self.console = Console()
        
        # Data storage
        self.data_dir = "data/analytics"
        os.makedirs(self.data_dir, exist_ok=True)
        
        self.sessions_file = os.path.join(self.data_dir, "learning_sessions.json")
        self.velocity_file = os.path.join(self.data_dir, "learning_velocity.json")
        self.retention_file = os.path.join(self.data_dir, "retention_metrics.json")
        self.patterns_file = os.path.join(self.data_dir, "study_patterns.json")
        
        # Load data
        self.learning_sessions: List[LearningSession] = self._load_sessions()
        self.velocity_metrics: Dict[str, List[LearningVelocity]] = self._load_velocity()
        self.retention_metrics: Dict[str, RetentionMetrics] = self._load_retention()
        self.study_patterns: Dict[str, StudyPattern] = self._load_patterns()
    
    def _load_sessions(self) -> List[LearningSession]:
        """Load learning sessions from file"""
        if os.path.exists(self.sessions_file):
            try:
                with open(self.sessions_file, 'r') as f:
                    data = json.load(f)
                    return [LearningSession(**session_data) for session_data in data]
            except Exception as e:
                self.logger.error(f"Error loading sessions: {e}")
        return []
    
    def _load_velocity(self) -> Dict[str, List[LearningVelocity]]:
        """Load velocity metrics from file"""
        if os.path.exists(self.velocity_file):
            try:
                with open(self.velocity_file, 'r') as f:
                    data = json.load(f)
                    velocity_data = {}
                    for user_id, velocities in data.items():
                        velocity_data[user_id] = [LearningVelocity(**v) for v in velocities]
                    return velocity_data
            except Exception as e:
                self.logger.error(f"Error loading velocity data: {e}")
        return {}
    
    def _load_retention(self) -> Dict[str, RetentionMetrics]:
        """Load retention metrics from file"""
        if os.path.exists(self.retention_file):
            try:
                with open(self.retention_file, 'r') as f:
                    data = json.load(f)
                    return {
                        key: RetentionMetrics(**retention_data)
                        for key, retention_data in data.items()
                    }
            except Exception as e:
                self.logger.error(f"Error loading retention data: {e}")
        return {}
    
    def _load_patterns(self) -> Dict[str, StudyPattern]:
        """Load study patterns from file"""
        if os.path.exists(self.patterns_file):
            try:
                with open(self.patterns_file, 'r') as f:
                    data = json.load(f)
                    return {
                        user_id: StudyPattern(**pattern_data)
                        for user_id, pattern_data in data.items()
                    }
            except Exception as e:
                self.logger.error(f"Error loading patterns: {e}")
        return {}
    
    def save_data(self):
        """Save all analytics data to files"""
        try:
            # Save sessions
            with open(self.sessions_file, 'w') as f:
                json.dump([asdict(session) for session in self.learning_sessions], f, indent=2)
            
            # Save velocity metrics
            with open(self.velocity_file, 'w') as f:
                velocity_data = {}
                for user_id, velocities in self.velocity_metrics.items():
                    velocity_data[user_id] = [asdict(v) for v in velocities]
                json.dump(velocity_data, f, indent=2)
            
            # Save retention metrics
            with open(self.retention_file, 'w') as f:
                json.dump({
                    key: asdict(retention)
                    for key, retention in self.retention_metrics.items()
                }, f, indent=2)
            
            # Save study patterns
            with open(self.patterns_file, 'w') as f:
                json.dump({
                    user_id: asdict(pattern)
                    for user_id, pattern in self.study_patterns.items()
                }, f, indent=2)
                
        except Exception as e:
            self.logger.error(f"Error saving analytics data: {e}")
    
    def record_learning_session(self, user_id: str, start_time: str, end_time: str,
                              activities: List[str], concepts: List[str],
                              performance_score: float, engagement_level: float = 0.8):
        """Record a new learning session"""
        try:
            start_dt = datetime.fromisoformat(start_time)
            end_dt = datetime.fromisoformat(end_time)
            duration = int((end_dt - start_dt).total_seconds() / 60)
            
            session = LearningSession(
                session_id=f"{user_id}_{start_dt.strftime('%Y%m%d_%H%M%S')}",
                user_id=user_id,
                start_time=start_time,
                end_time=end_time,
                duration_minutes=duration,
                activities=activities,
                concepts_covered=concepts,
                performance_score=performance_score,
                engagement_level=engagement_level,
                session_type=self._classify_session_type(activities, performance_score)
            )
            
            self.learning_sessions.append(session)
            
            # Update analytics
            self._update_velocity_metrics(user_id)
            self._update_study_patterns(user_id)
            
            self.save_data()
            
        except Exception as e:
            self.logger.error(f"Error recording learning session: {e}")
    
    def _classify_session_type(self, activities: List[str], performance_score: float) -> str:
        """Classify the type of learning session"""
        if 'quiz' in activities and performance_score < 60:
            return 'assessment'
        elif 'review' in activities or 'spaced_repetition' in activities:
            return 'review'
        else:
            return 'study'
    
    def _update_velocity_metrics(self, user_id: str):
        """Update learning velocity metrics for a user"""
        try:
            # Get user sessions from last 7 days
            week_ago = datetime.now() - timedelta(days=7)
            recent_sessions = [
                s for s in self.learning_sessions
                if s.user_id == user_id and datetime.fromisoformat(s.start_time) >= week_ago
            ]
            
            if not recent_sessions:
                return
            
            # Calculate metrics
            total_time = sum(s.duration_minutes for s in recent_sessions)
            unique_concepts = set()
            for session in recent_sessions:
                unique_concepts.update(session.concepts_covered)
            
            concepts_learned = len(unique_concepts)
            quiz_attempts = len([s for s in recent_sessions if 'quiz' in s.activities])
            avg_score = statistics.mean([s.performance_score for s in recent_sessions])
            
            # Calculate velocity (concepts per hour)
            velocity_score = (concepts_learned / (total_time / 60)) if total_time > 0 else 0
            
            # Calculate acceleration (change from previous week)
            if user_id in self.velocity_metrics and self.velocity_metrics[user_id]:
                previous_velocity = self.velocity_metrics[user_id][-1].velocity_score
                acceleration = velocity_score - previous_velocity
            else:
                acceleration = 0
            
            velocity = LearningVelocity(
                user_id=user_id,
                time_period="weekly",
                concepts_learned=concepts_learned,
                concepts_mastered=len([s for s in recent_sessions if s.performance_score >= 80]),
                study_time_minutes=total_time,
                quiz_attempts=quiz_attempts,
                average_score=avg_score,
                velocity_score=velocity_score,
                acceleration=acceleration,
                calculated_at=datetime.now().isoformat()
            )
            
            if user_id not in self.velocity_metrics:
                self.velocity_metrics[user_id] = []
            
            self.velocity_metrics[user_id].append(velocity)
            
            # Keep only last 12 weeks of data
            if len(self.velocity_metrics[user_id]) > 12:
                self.velocity_metrics[user_id] = self.velocity_metrics[user_id][-12:]
            
        except Exception as e:
            self.logger.error(f"Error updating velocity metrics: {e}")
    
    def _update_study_patterns(self, user_id: str):
        """Update study pattern analysis for a user"""
        try:
            user_sessions = [s for s in self.learning_sessions if s.user_id == user_id]
            
            if len(user_sessions) < 5:  # Need minimum data
                return
            
            # Analyze optimal study times
            hour_performance = {}
            for session in user_sessions:
                hour = datetime.fromisoformat(session.start_time).hour
                if hour not in hour_performance:
                    hour_performance[hour] = []
                hour_performance[hour].append(session.performance_score)
            
            # Find peak performance hours
            peak_hours = []
            for hour, scores in hour_performance.items():
                if statistics.mean(scores) >= 75:  # Good performance threshold
                    peak_hours.append(hour)
            
            # Analyze session lengths
            session_lengths = [s.duration_minutes for s in user_sessions]
            optimal_length = int(statistics.median(session_lengths))
            
            # Analyze weekly patterns
            weekly_pattern = {}
            for session in user_sessions:
                day = datetime.fromisoformat(session.start_time).strftime('%A')
                if day not in weekly_pattern:
                    weekly_pattern[day] = []
                weekly_pattern[day].append(session.performance_score)
            
            # Convert to average scores
            for day in weekly_pattern:
                weekly_pattern[day] = statistics.mean(weekly_pattern[day])
            
            # Calculate consistency score
            scores = [s.performance_score for s in user_sessions[-10:]]  # Last 10 sessions
            consistency = 1 - (statistics.stdev(scores) / 100) if len(scores) > 1 else 0.5
            
            pattern = StudyPattern(
                user_id=user_id,
                optimal_study_times=[f"{h}:00-{h+1}:00" for h in peak_hours],
                optimal_session_length=optimal_length,
                preferred_break_intervals=15,  # Default
                peak_performance_hours=peak_hours,
                study_consistency_score=consistency,
                weekly_pattern=weekly_pattern,
                monthly_trend=self._calculate_monthly_trend(user_sessions)
            )
            
            self.study_patterns[user_id] = pattern
            
        except Exception as e:
            self.logger.error(f"Error updating study patterns: {e}")
    
    def _calculate_monthly_trend(self, sessions: List[LearningSession]) -> List[float]:
        """Calculate monthly performance trend"""
        try:
            monthly_scores = {}
            
            for session in sessions:
                month_key = datetime.fromisoformat(session.start_time).strftime('%Y-%m')
                if month_key not in monthly_scores:
                    monthly_scores[month_key] = []
                monthly_scores[month_key].append(session.performance_score)
            
            # Calculate monthly averages
            trend = []
            for month in sorted(monthly_scores.keys()):
                avg_score = statistics.mean(monthly_scores[month])
                trend.append(avg_score)
            
            return trend[-6:]  # Last 6 months
            
        except Exception as e:
            self.logger.error(f"Error calculating monthly trend: {e}")
            return []
    
    def update_retention_metrics(self, user_id: str, concept_id: str, 
                               current_score: float):
        """Update retention metrics for a concept"""
        try:
            retention_key = f"{user_id}_{concept_id}"
            current_time = datetime.now().isoformat()
            
            if retention_key in self.retention_metrics:
                retention = self.retention_metrics[retention_key]
                retention.scores_over_time.append((current_time, current_score))
                
                # Calculate retention rate
                if len(retention.scores_over_time) > 1:
                    initial_score = retention.initial_score
                    retention.retention_rate = current_score / initial_score if initial_score > 0 else 0
                
                # Update optimal review interval based on forgetting curve
                retention.optimal_review_interval = self._calculate_optimal_review_interval(retention)
                retention.next_suggested_review = (
                    datetime.now() + timedelta(days=retention.optimal_review_interval)
                ).isoformat()
                
            else:
                # Create new retention record
                retention = RetentionMetrics(
                    user_id=user_id,
                    concept_id=concept_id,
                    initial_score=current_score,
                    scores_over_time=[(current_time, current_score)],
                    retention_rate=1.0,
                    forgetting_curve_fit={},
                    optimal_review_interval=7,  # Default 1 week
                    last_review=current_time,
                    next_suggested_review=(datetime.now() + timedelta(days=7)).isoformat()
                )
                
                self.retention_metrics[retention_key] = retention
            
            retention.last_review = current_time
            self.save_data()
            
        except Exception as e:
            self.logger.error(f"Error updating retention metrics: {e}")
    
    def _calculate_optimal_review_interval(self, retention: RetentionMetrics) -> int:
        """Calculate optimal review interval based on forgetting curve"""
        try:
            if len(retention.scores_over_time) < 3:
                return 7  # Default
            
            # Simple forgetting curve analysis
            scores = [score for _, score in retention.scores_over_time]
            
            # If scores are stable or improving, increase interval
            if len(scores) >= 2:
                recent_trend = scores[-1] - scores[-2]
                if recent_trend >= 0:  # Stable or improving
                    return min(21, retention.optimal_review_interval + 3)  # Max 3 weeks
                else:  # Declining
                    return max(3, retention.optimal_review_interval - 2)  # Min 3 days
            
            return retention.optimal_review_interval
            
        except Exception as e:
            self.logger.error(f"Error calculating review interval: {e}")
            return 7
    
    def show_comprehensive_dashboard(self, user_id: str):
        """Display comprehensive learning analytics dashboard"""
        try:
            self.console.clear()
            
            # Create layout
            layout = Layout()
            layout.split_column(
                Layout(name="header", size=3),
                Layout(name="main"),
                Layout(name="footer", size=3)
            )
            
            layout["main"].split_row(
                Layout(name="left"),
                Layout(name="right")
            )
            
            layout["left"].split_column(
                Layout(name="velocity", size=12),
                Layout(name="patterns", size=12)
            )
            
            layout["right"].split_column(
                Layout(name="retention", size=12),
                Layout(name="predictions", size=12)
            )
            
            # Header
            header_text = Text()
            header_text.append("LEARNING ANALYTICS DASHBOARD", style="bold cyan")
            header_text.append(f"\nUser: {user_id} | Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}", style="dim")
            layout["header"].update(Panel(header_text, border_style="bright_blue"))
            
            # Velocity metrics
            velocity_panel = self._create_velocity_panel(user_id)
            layout["velocity"].update(velocity_panel)
            
            # Study patterns
            patterns_panel = self._create_patterns_panel(user_id)
            layout["patterns"].update(patterns_panel)
            
            # Retention analysis
            retention_panel = self._create_retention_panel(user_id)
            layout["retention"].update(retention_panel)
            
            # Predictions
            predictions_panel = self._create_predictions_panel(user_id)
            layout["predictions"].update(predictions_panel)
            
            # Footer
            footer_text = Text("Press any key to continue...", style="dim italic")
            layout["footer"].update(Panel(footer_text, border_style="dim"))
            
            self.console.print(layout)
            
        except Exception as e:
            self.logger.error(f"Error showing dashboard: {e}")
            self.console.print(f"[red]Error displaying dashboard: {e}[/red]")
    
    def _create_velocity_panel(self, user_id: str) -> Panel:
        """Create learning velocity panel"""
        try:
            velocities = self.velocity_metrics.get(user_id, [])
            
            if not velocities:
                return Panel("No velocity data available", title="Learning Velocity", border_style="yellow")
            
            latest = velocities[-1]
            
            table = Table(show_header=True, header_style="bold magenta")
            table.add_column("Metric", style="cyan")
            table.add_column("Value", style="white")
            table.add_column("Trend", style="green")
            
            # Calculate trends
            velocity_trend = "↑" if latest.acceleration > 0 else "↓" if latest.acceleration < 0 else "→"
            
            table.add_row("Concepts/Week", str(latest.concepts_learned), velocity_trend)
            table.add_row("Study Time", f"{latest.study_time_minutes} min", "")
            table.add_row("Avg Score", f"{latest.average_score:.1f}%", "")
            table.add_row("Velocity", f"{latest.velocity_score:.2f} concepts/hr", velocity_trend)
            
            # Add velocity chart (simple text-based)
            if len(velocities) > 1:
                chart_data = [v.velocity_score for v in velocities[-8:]]  # Last 8 weeks
                chart = self._create_simple_chart(chart_data, "Velocity Trend")
                table.add_row("Trend", chart, "")
            
            return Panel(table, title="Learning Velocity", border_style="bright_green")
            
        except Exception as e:
            self.logger.error(f"Error creating velocity panel: {e}")
            return Panel("Error loading velocity data", title="Learning Velocity", border_style="red")
    
    def _create_patterns_panel(self, user_id: str) -> Panel:
        """Create study patterns panel"""
        try:
            pattern = self.study_patterns.get(user_id)
            
            if not pattern:
                return Panel("No pattern data available", title="Study Patterns", border_style="yellow")
            
            table = Table(show_header=True, header_style="bold magenta")
            table.add_column("Pattern", style="cyan")
            table.add_column("Value", style="white")
            
            table.add_row("Optimal Times", ", ".join(pattern.optimal_study_times[:3]))
            table.add_row("Session Length", f"{pattern.optimal_session_length} min")
            table.add_row("Consistency", f"{pattern.study_consistency_score:.2f}")
            
            # Best day of week
            if pattern.weekly_pattern:
                best_day = max(pattern.weekly_pattern.items(), key=lambda x: x[1])
                table.add_row("Best Day", f"{best_day[0]} ({best_day[1]:.1f}%)")
            
            # Monthly trend
            if pattern.monthly_trend:
                trend_direction = "↑" if pattern.monthly_trend[-1] > pattern.monthly_trend[0] else "↓"
                table.add_row("Monthly Trend", trend_direction)
            
            return Panel(table, title="Study Patterns", border_style="bright_blue")
            
        except Exception as e:
            self.logger.error(f"Error creating patterns panel: {e}")
            return Panel("Error loading pattern data", title="Study Patterns", border_style="red")
    
    def _create_retention_panel(self, user_id: str) -> Panel:
        """Create retention analysis panel"""
        try:
            user_retentions = {
                key: retention for key, retention in self.retention_metrics.items()
                if key.startswith(f"{user_id}_")
            }
            
            if not user_retentions:
                return Panel("No retention data available", title="Retention Analysis", border_style="yellow")
            
            table = Table(show_header=True, header_style="bold magenta")
            table.add_column("Metric", style="cyan")
            table.add_column("Value", style="white")
            
            # Calculate overall retention stats
            retention_rates = [r.retention_rate for r in user_retentions.values()]
            avg_retention = statistics.mean(retention_rates) if retention_rates else 0
            
            # Concepts due for review
            due_for_review = 0
            for retention in user_retentions.values():
                review_date = datetime.fromisoformat(retention.next_suggested_review)
                if review_date <= datetime.now():
                    due_for_review += 1
            
            table.add_row("Avg Retention", f"{avg_retention:.2f}")
            table.add_row("Concepts Tracked", str(len(user_retentions)))
            table.add_row("Due for Review", str(due_for_review))
            
            # Optimal review intervals
            intervals = [r.optimal_review_interval for r in user_retentions.values()]
            avg_interval = statistics.mean(intervals) if intervals else 7
            table.add_row("Avg Review Interval", f"{avg_interval:.1f} days")
            
            return Panel(table, title="Retention Analysis", border_style="bright_yellow")
            
        except Exception as e:
            self.logger.error(f"Error creating retention panel: {e}")
            return Panel("Error loading retention data", title="Retention Analysis", border_style="red")
    
    def _create_predictions_panel(self, user_id: str) -> Panel:
        """Create predictions and recommendations panel"""
        try:
            predictions = self._generate_predictions(user_id)
            
            table = Table(show_header=True, header_style="bold magenta")
            table.add_column("Prediction", style="cyan")
            table.add_column("Value", style="white")
            table.add_column("Confidence", style="green")
            
            for prediction in predictions:
                table.add_row(
                    prediction["type"],
                    prediction["value"],
                    f"{prediction['confidence']:.0%}"
                )
            
            return Panel(table, title="Predictions & Insights", border_style="bright_magenta")
            
        except Exception as e:
            self.logger.error(f"Error creating predictions panel: {e}")
            return Panel("Error generating predictions", title="Predictions", border_style="red")
    
    def _generate_predictions(self, user_id: str) -> List[Dict[str, Any]]:
        """Generate predictive insights for the user"""
        predictions = []
        
        try:
            # Learning velocity prediction
            velocities = self.velocity_metrics.get(user_id, [])
            if len(velocities) >= 2:
                recent_velocity = velocities[-1].velocity_score
                trend = velocities[-1].acceleration
                
                next_week_velocity = recent_velocity + trend
                predictions.append({
                    "type": "Next Week Velocity",
                    "value": f"{next_week_velocity:.2f} concepts/hr",
                    "confidence": 0.7
                })
            
            # Study pattern prediction
            pattern = self.study_patterns.get(user_id)
            if pattern and pattern.monthly_trend:
                if len(pattern.monthly_trend) >= 2:
                    trend = pattern.monthly_trend[-1] - pattern.monthly_trend[-2]
                    next_month_score = pattern.monthly_trend[-1] + trend
                    
                    predictions.append({
                        "type": "Next Month Score",
                        "value": f"{next_month_score:.1f}%",
                        "confidence": 0.6
                    })
            
            # Retention prediction
            user_retentions = {
                key: retention for key, retention in self.retention_metrics.items()
                if key.startswith(f"{user_id}_")
            }
            
            if user_retentions:
                at_risk_concepts = len([
                    r for r in user_retentions.values()
                    if r.retention_rate < 0.7
                ])
                
                predictions.append({
                    "type": "Concepts at Risk",
                    "value": str(at_risk_concepts),
                    "confidence": 0.8
                })
            
            # Time to mastery prediction
            if velocities:
                current_velocity = velocities[-1].velocity_score
                if current_velocity > 0:
                    concepts_to_master = 10  # Assume 10 concepts to master
                    weeks_to_mastery = concepts_to_master / (current_velocity * 7)  # Convert to weekly
                    
                    predictions.append({
                        "type": "Weeks to Mastery",
                        "value": f"{weeks_to_mastery:.1f} weeks",
                        "confidence": 0.5
                    })
            
        except Exception as e:
            self.logger.error(f"Error generating predictions: {e}")
        
        return predictions
    
    def _create_simple_chart(self, data: List[float], title: str) -> str:
        """Create a simple text-based chart"""
        if not data:
            return "No data"
        
        # Normalize data to 0-10 range for display
        min_val = min(data)
        max_val = max(data)
        
        if max_val == min_val:
            return "─" * len(data)
        
        normalized = [(val - min_val) / (max_val - min_val) * 10 for val in data]
        
        # Create simple bar chart
        bars = []
        for val in normalized:
            if val < 2:
                bars.append("▁")
            elif val < 4:
                bars.append("▃")
            elif val < 6:
                bars.append("▅")
            elif val < 8:
                bars.append("▇")
            else:
                bars.append("█")
        
        return "".join(bars)
    
    def get_learning_insights(self, user_id: str) -> Dict[str, Any]:
        """Get comprehensive learning insights for API/programmatic access"""
        try:
            insights = {
                "user_id": user_id,
                "generated_at": datetime.now().isoformat(),
                "velocity_metrics": {},
                "study_patterns": {},
                "retention_analysis": {},
                "predictions": [],
                "recommendations": []
            }
            
            # Velocity insights
            velocities = self.velocity_metrics.get(user_id, [])
            if velocities:
                latest = velocities[-1]
                insights["velocity_metrics"] = {
                    "current_velocity": latest.velocity_score,
                    "acceleration": latest.acceleration,
                    "concepts_per_week": latest.concepts_learned,
                    "study_time_per_week": latest.study_time_minutes,
                    "average_score": latest.average_score,
                    "trend": "improving" if latest.acceleration > 0 else "declining" if latest.acceleration < 0 else "stable"
                }
            
            # Pattern insights
            pattern = self.study_patterns.get(user_id)
            if pattern:
                insights["study_patterns"] = {
                    "optimal_study_times": pattern.optimal_study_times,
                    "optimal_session_length": pattern.optimal_session_length,
                    "consistency_score": pattern.study_consistency_score,
                    "peak_performance_hours": pattern.peak_performance_hours,
                    "best_day": max(pattern.weekly_pattern.items(), key=lambda x: x[1])[0] if pattern.weekly_pattern else None
                }
            
            # Retention insights
            user_retentions = {
                key: retention for key, retention in self.retention_metrics.items()
                if key.startswith(f"{user_id}_")
            }
            
            if user_retentions:
                retention_rates = [r.retention_rate for r in user_retentions.values()]
                due_for_review = sum(1 for r in user_retentions.values() 
                                   if datetime.fromisoformat(r.next_suggested_review) <= datetime.now())
                
                insights["retention_analysis"] = {
                    "average_retention_rate": statistics.mean(retention_rates),
                    "concepts_tracked": len(user_retentions),
                    "concepts_due_for_review": due_for_review,
                    "at_risk_concepts": len([r for r in user_retentions.values() if r.retention_rate < 0.7])
                }
            
            # Predictions
            insights["predictions"] = self._generate_predictions(user_id)
            
            # Recommendations
            insights["recommendations"] = self._generate_comprehensive_recommendations(user_id)
            
            return insights
            
        except Exception as e:
            self.logger.error(f"Error generating insights: {e}")
            return {"error": str(e)}
    
    def _generate_comprehensive_recommendations(self, user_id: str) -> List[str]:
        """Generate comprehensive learning recommendations"""
        recommendations = []
        
        try:
            # Velocity-based recommendations
            velocities = self.velocity_metrics.get(user_id, [])
            if velocities:
                latest = velocities[-1]
                if latest.velocity_score < 0.5:
                    recommendations.append("Consider shorter, more frequent study sessions to improve learning velocity")
                elif latest.velocity_score > 2.0:
                    recommendations.append("Great velocity! Consider tackling more challenging concepts")
            
            # Pattern-based recommendations
            pattern = self.study_patterns.get(user_id)
            if pattern:
                if pattern.study_consistency_score < 0.5:
                    recommendations.append("Try to maintain more consistent study schedules for better results")
                
                if pattern.optimal_session_length > 90:
                    recommendations.append("Consider breaking long study sessions into shorter chunks with breaks")
            
            # Retention-based recommendations
            user_retentions = {
                key: retention for key, retention in self.retention_metrics.items()
                if key.startswith(f"{user_id}_")
            }
            
            if user_retentions:
                due_count = sum(1 for r in user_retentions.values() 
                              if datetime.fromisoformat(r.next_suggested_review) <= datetime.now())
                
                if due_count > 0:
                    recommendations.append(f"You have {due_count} concepts due for review - prioritize spaced repetition")
                
                at_risk = len([r for r in user_retentions.values() if r.retention_rate < 0.7])
                if at_risk > 0:
                    recommendations.append(f"Focus on reinforcing {at_risk} concepts with declining retention")
            
            # Session-based recommendations
            recent_sessions = [
                s for s in self.learning_sessions
                if s.user_id == user_id and 
                datetime.fromisoformat(s.start_time) >= datetime.now() - timedelta(days=7)
            ]
            
            if recent_sessions:
                avg_engagement = statistics.mean([s.engagement_level for s in recent_sessions])
                if avg_engagement < 0.6:
                    recommendations.append("Try varying your study activities to improve engagement")
                
                avg_performance = statistics.mean([s.performance_score for s in recent_sessions])
                if avg_performance < 70:
                    recommendations.append("Consider reviewing foundational concepts before advancing")
            
        except Exception as e:
            self.logger.error(f"Error generating recommendations: {e}")
        
        return recommendations[:7]  # Limit to top 7 recommendations
    
    def generate_learning_insights(self, user_id: str) -> Dict[str, Any]:
        """Generate comprehensive learning insights for a user"""
        try:
            return self.get_learning_insights(user_id)
        except Exception as e:
            self.logger.error(f"Error generating learning insights: {e}")
            return {"error": str(e)}
    
    def analyze_study_patterns(self, user_id: str) -> Dict[str, Any]:
        """Analyze and return detailed study patterns for a user"""
        try:
            pattern = self.study_patterns.get(user_id)
            user_sessions = [s for s in self.learning_sessions if s.user_id == user_id]
            
            if not pattern and len(user_sessions) < 3:
                return {
                    "message": "Insufficient data for pattern analysis",
                    "sessions_analyzed": len(user_sessions),
                    "minimum_required": 3
                }
            
            # If no pattern exists but we have sessions, create one
            if not pattern and user_sessions:
                self._update_study_patterns(user_id)
                pattern = self.study_patterns.get(user_id)
            
            if not pattern:
                return {"error": "Could not analyze study patterns"}
            
            # Enhanced pattern analysis
            analysis = {
                "user_id": user_id,
                "pattern_summary": {
                    "optimal_study_times": pattern.optimal_study_times,
                    "optimal_session_length": pattern.optimal_session_length,
                    "peak_performance_hours": pattern.peak_performance_hours,
                    "study_consistency_score": pattern.study_consistency_score
                },
                "weekly_analysis": {
                    "pattern": pattern.weekly_pattern,
                    "best_day": max(pattern.weekly_pattern.items(), key=lambda x: x[1]) if pattern.weekly_pattern else None,
                    "worst_day": min(pattern.weekly_pattern.items(), key=lambda x: x[1]) if pattern.weekly_pattern else None
                },
                "trends": {
                    "monthly_trend": pattern.monthly_trend,
                    "trend_direction": self._analyze_trend_direction(pattern.monthly_trend)
                },
                "recommendations": self._generate_pattern_recommendations(pattern),
                "sessions_analyzed": len(user_sessions),
                "analysis_date": datetime.now().isoformat()
            }
            
            # Add session distribution analysis
            if user_sessions:
                hour_distribution = {}
                duration_stats = []
                
                for session in user_sessions:
                    hour = datetime.fromisoformat(session.start_time).hour
                    hour_distribution[hour] = hour_distribution.get(hour, 0) + 1
                    duration_stats.append(session.duration_minutes)
                
                analysis["session_distribution"] = {
                    "by_hour": hour_distribution,
                    "duration_stats": {
                        "average": statistics.mean(duration_stats),
                        "median": statistics.median(duration_stats),
                        "min": min(duration_stats),
                        "max": max(duration_stats)
                    }
                }
            
            return analysis
            
        except Exception as e:
            self.logger.error(f"Error analyzing study patterns: {e}")
            return {"error": str(e)}
    
    def _analyze_trend_direction(self, monthly_trend: List[float]) -> str:
        """Analyze the direction of monthly performance trend"""
        if not monthly_trend or len(monthly_trend) < 2:
            return "insufficient_data"
        
        if len(monthly_trend) == 2:
            return "improving" if monthly_trend[1] > monthly_trend[0] else "declining" if monthly_trend[1] < monthly_trend[0] else "stable"
        
        # Calculate trend over last 3 months
        recent_trend = monthly_trend[-3:] if len(monthly_trend) >= 3 else monthly_trend
        
        improvements = 0
        declines = 0
        
        for i in range(1, len(recent_trend)):
            if recent_trend[i] > recent_trend[i-1]:
                improvements += 1
            elif recent_trend[i] < recent_trend[i-1]:
                declines += 1
        
        if improvements > declines:
            return "improving"
        elif declines > improvements:
            return "declining"
        else:
            return "stable"
    
    def _generate_pattern_recommendations(self, pattern: StudyPattern) -> List[str]:
        """Generate recommendations based on study patterns"""
        recommendations = []
        
        # Session length recommendations
        if pattern.optimal_session_length > 90:
            recommendations.append("Consider shorter study sessions (60-90 minutes) with breaks to maintain focus")
        elif pattern.optimal_session_length < 30:
            recommendations.append("Try extending study sessions to 45-60 minutes for better learning retention")
        
        # Consistency recommendations
        if pattern.study_consistency_score < 0.5:
            recommendations.append("Work on maintaining consistent study schedules and performance")
        elif pattern.study_consistency_score > 0.8:
            recommendations.append("Excellent consistency! Consider gradually increasing study complexity")
        
        # Time-based recommendations
        if pattern.peak_performance_hours:
            peak_hours_str = ", ".join([f"{h}:00" for h in pattern.peak_performance_hours[:3]])
            recommendations.append(f"Schedule important study sessions during your peak hours: {peak_hours_str}")
        
        # Weekly pattern recommendations
        if pattern.weekly_pattern:
            worst_day = min(pattern.weekly_pattern.items(), key=lambda x: x[1])
            if worst_day[1] < 60:  # Less than 60% performance
                recommendations.append(f"Focus on improving {worst_day[0]} study sessions")
        
        return recommendations[:5]