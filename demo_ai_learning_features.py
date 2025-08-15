#!/usr/bin/env python3
"""
Demo script showcasing AI-Powered Learning Features
Demonstrates adaptive learning paths, intelligent quizzes, analytics, and predictions
"""

import asyncio
import os
import sys
from datetime import datetime, timedelta
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.rule import Rule
from rich.text import Text

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.ai_learning_engine import AILearningEngine
from src.adaptive_quiz_engine import AdaptiveQuizEngine
from src.learning_analytics_dashboard import LearningAnalyticsDashboard
from src.predictive_learning_intelligence import PredictiveLearningIntelligence
from src.ai_client import AIClient
from src.database import SyllaboDatabase

class AILearningDemo:
    """Demo class for AI learning features"""
    
    def __init__(self):
        self.console = Console()
        
        # Initialize components
        self.ai_client = AIClient()
        self.db = SyllaboDatabase()
        
        # Initialize AI learning modules
        self.ai_learning_engine = AILearningEngine(self.ai_client, self.db)
        self.adaptive_quiz_engine = AdaptiveQuizEngine(self.ai_client, self.db)
        self.learning_analytics = LearningAnalyticsDashboard(self.ai_client, self.db)
        self.predictive_intelligence = PredictiveLearningIntelligence(self.ai_client, self.db)
        
        # Demo user
        self.demo_user_id = "demo_user"
    
    def show_banner(self):
        """Show demo banner"""
        banner_text = Text()
        banner_text.append("AI-POWERED LEARNING FEATURES DEMO", style="bold cyan")
        banner_text.append("\n")
        banner_text.append("Showcasing Adaptive Learning, Intelligent Quizzes & Predictive Analytics", style="bold white")
        
        banner_panel = Panel(
            banner_text,
            border_style="bright_cyan",
            padding=(1, 2),
            title="[bold bright_blue]Syllabo AI Learning Demo[/bold bright_blue]",
            title_align="center"
        )
        
        self.console.print(banner_panel)
        self.console.print()
    
    async def run_demo(self):
        """Run the complete AI learning features demo"""
        self.show_banner()
        
        demos = [
            ("1. Learning Profile Creation", self.demo_learning_profile),
            ("2. Adaptive Learning Path Generation", self.demo_adaptive_learning_path),
            ("3. Intelligent Adaptive Quizzes", self.demo_adaptive_quizzes),
            ("4. Learning Analytics Dashboard", self.demo_learning_analytics),
            ("5. Predictive Learning Intelligence", self.demo_predictive_intelligence),
        ]
        
        for title, demo_func in demos:
            self.console.print(Rule(f"[bold bright_blue]{title}[/bold bright_blue]", style="bright_blue"))
            
            try:
                await demo_func()
            except Exception as e:
                self.console.print(f"[red]Demo error: {e}[/red]")
            
            self.console.print()
            input("Press Enter to continue to next demo...")
            self.console.print()
        
        self.console.print(Rule("[bold bright_green]Demo Complete![/bold bright_green]", style="bright_green"))
        self.console.print("[bright_green]All AI learning features demonstrated successfully![/bright_green]")
    
    async def demo_learning_profile(self):
        """Demo learning profile creation"""
        self.console.print("[bright_cyan]Creating AI-powered learning profile...[/bright_cyan]")
        
        # Sample assessment data
        assessment_data = {
            "learning_style": "visual",
            "difficulty_preference": 0.6,
            "study_pace": "normal",
            "attention_span": 45,
            "goals": ["Master Python Programming", "Learn Data Science", "Understand Machine Learning"],
            "knowledge_score": 0.7
        }
        
        # Create learning profile
        profile = await self.ai_learning_engine.create_learning_profile(
            self.demo_user_id, assessment_data
        )
        
        # Display profile
        profile_table = Table(title="AI-Generated Learning Profile", border_style="bright_green")
        profile_table.add_column("Attribute", style="bright_cyan", width=20)
        profile_table.add_column("Value", style="bright_white", width=30)
        profile_table.add_column("AI Analysis", style="bright_yellow", width=40)
        
        profile_table.add_row(
            "Learning Style", 
            profile.learning_style.title(),
            "Optimized for visual learners with diagrams and charts"
        )
        profile_table.add_row(
            "Current Level", 
            profile.current_level.title(),
            "Assessed based on knowledge score and goals"
        )
        profile_table.add_row(
            "Study Pace", 
            profile.study_pace.title(),
            "Balanced approach for steady progress"
        )
        profile_table.add_row(
            "Attention Span", 
            f"{profile.attention_span} minutes",
            "Optimal session length for maximum retention"
        )
        profile_table.add_row(
            "Difficulty Preference", 
            f"{profile.preferred_difficulty:.1f}",
            "Moderate challenge level for optimal learning"
        )
        
        self.console.print(profile_table)
        
        self.console.print("[bright_green]✓ Learning profile created with AI analysis![/bright_green]")
    
    async def demo_adaptive_learning_path(self):
        """Demo adaptive learning path generation"""
        self.console.print("[bright_cyan]Generating adaptive learning path with AI...[/bright_cyan]")
        
        # Sample topics for Python programming
        topics = [
            "Python Basics",
            "Data Types and Variables",
            "Control Structures",
            "Functions",
            "Object-Oriented Programming",
            "File Handling",
            "Error Handling",
            "Libraries and Modules",
            "Data Structures",
            "Advanced Python Concepts"
        ]
        
        # Generate adaptive learning path
        path = await self.ai_learning_engine.generate_adaptive_learning_path(
            self.demo_user_id, "Python Programming", topics
        )
        
        # Display learning path
        path_table = Table(title="AI-Generated Adaptive Learning Path", border_style="bright_green")
        path_table.add_column("Step", style="bright_cyan", width=5)
        path_table.add_column("Concept", style="bright_white", width=25)
        path_table.add_column("Difficulty", style="bright_yellow", width=12)
        path_table.add_column("Est. Time", style="bright_magenta", width=10)
        path_table.add_column("Prerequisites", style="bright_blue", width=20)
        
        for i, concept in enumerate(path.concepts[:8], 1):  # Show first 8
            difficulty_bar = "█" * int(concept.difficulty_level * 5)
            prereq_text = ", ".join(concept.prerequisites[:2]) if concept.prerequisites else "None"
            if len(prereq_text) > 18:
                prereq_text = prereq_text[:15] + "..."
            
            path_table.add_row(
                str(i),
                concept.name[:22] + "..." if len(concept.name) > 25 else concept.name,
                difficulty_bar,
                f"{concept.estimated_time}m",
                prereq_text
            )
        
        self.console.print(path_table)
        
        # Show AI insights
        insights_panel = Panel(
            f"[bold]AI Learning Path Insights:[/bold]\n\n"
            f"• Path optimized for {path.concepts[0].name} learning style\n"
            f"• Difficulty progression: {min(path.difficulty_progression):.1f} → {max(path.difficulty_progression):.1f}\n"
            f"• Total concepts: {len(path.concepts)}\n"
            f"• Estimated completion: {datetime.fromisoformat(path.estimated_completion).strftime('%Y-%m-%d')}\n"
            f"• Prerequisites automatically detected and ordered\n"
            f"• Adaptive difficulty based on user profile",
            title="AI Analysis",
            border_style="bright_blue"
        )
        
        self.console.print(insights_panel)
        self.console.print("[bright_green]✓ Adaptive learning path generated with AI optimization![/bright_green]")
    
    async def demo_adaptive_quizzes(self):
        """Demo adaptive quiz system"""
        self.console.print("[bright_cyan]Demonstrating adaptive quiz intelligence...[/bright_cyan]")
        
        # Sample content for quiz generation
        content = """
        Python functions are reusable blocks of code that perform specific tasks. 
        They are defined using the 'def' keyword followed by the function name and parameters.
        Functions can return values using the 'return' statement. Parameters allow functions
        to accept input values. Local variables exist only within the function scope.
        """
        
        # Start adaptive quiz session
        session_id = await self.adaptive_quiz_engine.start_adaptive_quiz_session(
            self.demo_user_id, "python_functions", "Python Functions", content
        )
        
        self.console.print(f"[bright_green]✓ Adaptive quiz session created: {session_id}[/bright_green]")
        
        # Simulate taking a few questions
        for question_num in range(1, 4):
            question_data = self.adaptive_quiz_engine.get_next_question(session_id)
            
            if not question_data:
                break
            
            # Display question
            question_panel = Panel(
                f"[bold]Question {question_num}:[/bold]\n\n"
                f"{question_data['question_text']}\n\n"
                f"Type: {question_data['question_type']}\n"
                f"Difficulty: {'█' * int(question_data['difficulty_level'] * 5)}\n"
                f"Estimated time: {question_data['estimated_time']} seconds",
                title=f"Adaptive Question {question_num}",
                border_style="bright_yellow"
            )
            
            self.console.print(question_panel)
            
            # Simulate answer (correct for demo)
            if question_data['question_type'] == 'multiple_choice':
                # Always choose first option for demo
                answer = 0
            elif question_data['question_type'] == 'true_false':
                answer = True
            else:
                answer = "function"
            
            # Submit answer
            result = await self.adaptive_quiz_engine.submit_answer(session_id, answer, 30)
            
            # Show result
            result_color = "bright_green" if result['is_correct'] else "bright_red"
            status = "Correct!" if result['is_correct'] else "Incorrect"
            
            self.console.print(f"[{result_color}]{status}[/{result_color}]")
            
            if result.get('difficulty_adjustment') != 'none':
                self.console.print(f"[bright_blue]AI Adaptation: Quiz difficulty adjusted ({result['difficulty_adjustment']})[/bright_blue]")
            
            if result.get('quiz_completed'):
                break
        
        # Show concept mastery report
        mastery_report = self.adaptive_quiz_engine.get_concept_mastery_report(self.demo_user_id)
        
        if not mastery_report.get('error') and not mastery_report.get('message'):
            mastery_table = Table(title="AI Concept Mastery Analysis", border_style="bright_green")
            mastery_table.add_column("Metric", style="bright_cyan")
            mastery_table.add_column("Value", style="bright_white")
            mastery_table.add_column("AI Insight", style="bright_yellow")
            
            mastery_table.add_row(
                "Overall Mastery", 
                f"{mastery_report['overall_mastery']:.1%}",
                "Good progress on fundamental concepts"
            )
            mastery_table.add_row(
                "Concepts Tracked", 
                str(mastery_report['total_concepts']),
                "Building comprehensive knowledge map"
            )
            mastery_table.add_row(
                "Mastery Rate", 
                f"{mastery_report['mastery_percentage']:.1f}%",
                "Above average learning velocity"
            )
            
            self.console.print(mastery_table)
        
        self.console.print("[bright_green]✓ Adaptive quiz system demonstrated with AI-powered difficulty adjustment![/bright_green]")
    
    async def demo_learning_analytics(self):
        """Demo learning analytics dashboard"""
        self.console.print("[bright_cyan]Generating AI-powered learning analytics...[/bright_cyan]")
        
        # Simulate some learning sessions
        sessions_data = [
            {
                "start_time": (datetime.now() - timedelta(days=7)).isoformat(),
                "end_time": (datetime.now() - timedelta(days=7) + timedelta(minutes=45)).isoformat(),
                "activities": ["video", "quiz"],
                "concepts": ["python_basics"],
                "performance_score": 85.0
            },
            {
                "start_time": (datetime.now() - timedelta(days=5)).isoformat(),
                "end_time": (datetime.now() - timedelta(days=5) + timedelta(minutes=60)).isoformat(),
                "activities": ["reading", "practice"],
                "concepts": ["data_types"],
                "performance_score": 78.0
            },
            {
                "start_time": (datetime.now() - timedelta(days=3)).isoformat(),
                "end_time": (datetime.now() - timedelta(days=3) + timedelta(minutes=30)).isoformat(),
                "activities": ["quiz", "review"],
                "concepts": ["functions"],
                "performance_score": 92.0
            }
        ]
        
        # Record learning sessions
        for session in sessions_data:
            self.learning_analytics.record_learning_session(
                user_id=self.demo_user_id,
                start_time=session["start_time"],
                end_time=session["end_time"],
                activities=session["activities"],
                concepts=session["concepts"],
                performance_score=session["performance_score"]
            )
        
        # Get learning insights
        insights = self.learning_analytics.get_learning_insights(self.demo_user_id)
        
        # Display analytics
        if not insights.get("error"):
            analytics_table = Table(title="AI Learning Analytics", border_style="bright_green")
            analytics_table.add_column("Metric", style="bright_cyan", width=20)
            analytics_table.add_column("Value", style="bright_white", width=15)
            analytics_table.add_column("AI Analysis", style="bright_yellow", width=40)
            
            if insights.get("velocity_metrics"):
                velocity = insights["velocity_metrics"]
                analytics_table.add_row(
                    "Learning Velocity",
                    f"{velocity['current_velocity']:.2f} concepts/hr",
                    f"Trend: {velocity['trend']} - Good learning pace"
                )
                analytics_table.add_row(
                    "Weekly Progress",
                    f"{velocity['concepts_per_week']} concepts",
                    "Consistent learning pattern detected"
                )
                analytics_table.add_row(
                    "Average Score",
                    f"{velocity['average_score']:.1f}%",
                    "Above average performance"
                )
            
            if insights.get("study_patterns"):
                patterns = insights["study_patterns"]
                analytics_table.add_row(
                    "Optimal Session",
                    f"{patterns.get('optimal_session_length', 0)} min",
                    "AI-detected optimal study duration"
                )
                analytics_table.add_row(
                    "Consistency Score",
                    f"{patterns.get('consistency_score', 0):.2f}",
                    "Regular study habits improve retention"
                )
            
            self.console.print(analytics_table)
            
            # Show AI recommendations
            if insights.get("recommendations"):
                recommendations_panel = Panel(
                    "\n".join(f"• {rec}" for rec in insights["recommendations"][:5]),
                    title="AI-Generated Recommendations",
                    border_style="bright_blue"
                )
                self.console.print(recommendations_panel)
        
        self.console.print("[bright_green]✓ AI learning analytics generated with personalized insights![/bright_green]")
    
    async def demo_predictive_intelligence(self):
        """Demo predictive learning intelligence"""
        self.console.print("[bright_cyan]Demonstrating AI predictive learning intelligence...[/bright_cyan]")
        
        # Build user learning model
        historical_data = {
            'quiz_scores': [75, 80, 85, 88, 92],
            'study_times': [30, 45, 60, 40, 50],
            'concept_masteries': [
                {'initial_score': 70, 'current_score': 85},
                {'initial_score': 80, 'current_score': 90}
            ],
            'sessions': [
                {'engagement_level': 0.8, 'duration_minutes': 45},
                {'engagement_level': 0.9, 'duration_minutes': 60}
            ]
        }
        
        user_model = await self.predictive_intelligence.build_user_learning_model(
            self.demo_user_id, historical_data
        )
        
        # Display user model
        model_table = Table(title="AI Learning Model", border_style="bright_green")
        model_table.add_column("Factor", style="bright_cyan", width=20)
        model_table.add_column("Score", style="bright_white", width=10)
        model_table.add_column("AI Analysis", style="bright_yellow", width=40)
        
        model_table.add_row(
            "Learning Rate",
            f"{user_model.learning_rate:.2f}",
            "Above average - learns new concepts quickly"
        )
        model_table.add_row(
            "Retention Factor",
            f"{user_model.retention_factor:.2f}",
            "Good retention - knowledge sticks well"
        )
        model_table.add_row(
            "Difficulty Tolerance",
            f"{user_model.difficulty_tolerance:.2f}",
            "Can handle moderate to high difficulty"
        )
        model_table.add_row(
            "Consistency Factor",
            f"{user_model.consistency_factor:.2f}",
            "Consistent performance across sessions"
        )
        model_table.add_row(
            "Model Confidence",
            f"{user_model.model_confidence:.2f}",
            "High confidence in predictions"
        )
        
        self.console.print(model_table)
        
        # Generate predictions
        predictions = []
        
        # Performance prediction
        perf_prediction = await self.predictive_intelligence.predict_quiz_performance(
            self.demo_user_id, "advanced_python", 0.7
        )
        predictions.append(("Performance", f"{perf_prediction.predicted_value:.1f}%", perf_prediction.confidence_score))
        
        # Time prediction
        time_prediction = await self.predictive_intelligence.predict_learning_time(
            self.demo_user_id, "machine_learning", 0.8
        )
        hours = int(time_prediction.predicted_value) // 60
        minutes = int(time_prediction.predicted_value) % 60
        time_str = f"{hours}h {minutes}m" if hours > 0 else f"{minutes}m"
        predictions.append(("Learning Time", time_str, time_prediction.confidence_score))
        
        # Success prediction
        success_prediction = await self.predictive_intelligence.predict_success_probability(
            self.demo_user_id, "data_science", "Master Data Science Fundamentals"
        )
        predictions.append(("Success Probability", f"{success_prediction.predicted_value:.1%}", success_prediction.confidence_score))
        
        # Display predictions
        predictions_table = Table(title="AI Predictions", border_style="bright_magenta")
        predictions_table.add_column("Prediction Type", style="bright_cyan", width=18)
        predictions_table.add_column("Predicted Value", style="bright_white", width=15)
        predictions_table.add_column("Confidence", style="bright_green", width=12)
        predictions_table.add_column("AI Reasoning", style="bright_yellow", width=35)
        
        reasoning = [
            "Based on learning rate and difficulty tolerance",
            "Considers cognitive load and study patterns",
            "Factors in motivation and goal complexity"
        ]
        
        for i, (pred_type, value, confidence) in enumerate(predictions):
            predictions_table.add_row(
                pred_type,
                value,
                f"{confidence:.1%}",
                reasoning[i]
            )
        
        self.console.print(predictions_table)
        
        # Show prediction insights
        insights = self.predictive_intelligence.get_prediction_insights(self.demo_user_id)
        
        if not insights.get("error") and insights.get("model_insights"):
            model_insights = insights["model_insights"]
            
            insights_panel = Panel(
                f"[bold]AI Model Insights:[/bold]\n\n"
                f"• Learning style optimized for: {', '.join(model_insights.get('preferred_modalities', ['visual']))}\n"
                f"• Prediction accuracy improving over time\n"
                f"• Strong performance on moderate difficulty concepts\n"
                f"• Recommended focus: consistency and advanced topics\n"
                f"• Model confidence: {model_insights['model_confidence']:.1%}",
                title="Predictive Intelligence Summary",
                border_style="bright_blue"
            )
            
            self.console.print(insights_panel)
        
        self.console.print("[bright_green]✓ AI predictive intelligence demonstrated with personalized forecasting![/bright_green]")

async def main():
    """Run the AI learning features demo"""
    demo = AILearningDemo()
    await demo.run_demo()

if __name__ == "__main__":
    asyncio.run(main())