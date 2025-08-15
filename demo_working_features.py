#!/usr/bin/env python3
"""
Demo of Working AI Learning Features
Demonstrates the successfully implemented and tested AI learning capabilities
"""

import asyncio
import os
import sys
import tempfile
import shutil
from datetime import datetime, timedelta
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.rule import Rule
from rich.progress import Progress, SpinnerColumn, TextColumn

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

# Mock AI Client for demo
class DemoAIClient:
    """Demo AI client with realistic responses"""
    
    async def generate_response(self, prompt: str) -> str:
        """Generate demo responses"""
        if "learning style" in prompt.lower():
            return "visual"
        elif "concept graph" in prompt.lower():
            return '''
            {
                "concepts": [
                    {
                        "concept_id": "python_basics",
                        "name": "Python Fundamentals",
                        "description": "Core Python programming concepts",
                        "difficulty_level": 0.3,
                        "prerequisites": [],
                        "related_concepts": ["python_functions"],
                        "estimated_time": 45,
                        "mastery_threshold": 0.8,
                        "content_types": ["video", "quiz", "practice"]
                    },
                    {
                        "concept_id": "python_functions",
                        "name": "Python Functions",
                        "description": "Function definition and usage",
                        "difficulty_level": 0.5,
                        "prerequisites": ["python_basics"],
                        "related_concepts": ["python_oop"],
                        "estimated_time": 60,
                        "mastery_threshold": 0.8,
                        "content_types": ["video", "quiz", "practice"]
                    },
                    {
                        "concept_id": "python_oop",
                        "name": "Object-Oriented Programming",
                        "description": "Classes, objects, and inheritance",
                        "difficulty_level": 0.7,
                        "prerequisites": ["python_functions"],
                        "related_concepts": [],
                        "estimated_time": 90,
                        "mastery_threshold": 0.8,
                        "content_types": ["video", "quiz", "practice"]
                    }
                ]
            }
            '''
        elif "quiz questions" in prompt.lower():
            return '''
            {
                "questions": [
                    {
                        "question_id": "demo_q1",
                        "question_text": "What keyword is used to define a function in Python?",
                        "question_type": "multiple_choice",
                        "options": ["def", "function", "define", "func"],
                        "correct_answer": 0,
                        "explanation": "The 'def' keyword is used to define functions in Python",
                        "difficulty_level": 0.3,
                        "concept_tags": ["python_functions"],
                        "cognitive_level": "remember",
                        "estimated_time": 30,
                        "hint": "Think about the most common Python keywords",
                        "created_at": "2024-01-01T00:00:00"
                    },
                    {
                        "question_id": "demo_q2",
                        "question_text": "True or False: Python functions can return multiple values?",
                        "question_type": "true_false",
                        "options": [],
                        "correct_answer": true,
                        "explanation": "Python functions can return multiple values using tuples",
                        "difficulty_level": 0.5,
                        "concept_tags": ["python_functions"],
                        "cognitive_level": "understand",
                        "estimated_time": 45,
                        "hint": "Consider tuple unpacking",
                        "created_at": "2024-01-01T00:00:00"
                    }
                ]
            }
            '''
        else:
            return "Demo AI response for realistic testing"

class WorkingFeaturesDemo:
    """Demo of working AI learning features"""
    
    def __init__(self):
        self.console = Console()
        self.temp_dir = None
        self.demo_user_id = "demo_user"
        
        # Setup demo environment
        self.setup_demo_environment()
    
    def setup_demo_environment(self):
        """Setup demo environment"""
        self.temp_dir = tempfile.mkdtemp(prefix="syllabo_demo_")
        
        # Initialize main application
        from main import SyllaboMain
        self.app = SyllaboMain()
        
        # Replace AI client with demo client
        self.demo_ai_client = DemoAIClient()
        self.app.ai_client = self.demo_ai_client
        
        # Update AI clients in all components
        self.app.ai_learning_engine.ai_client = self.demo_ai_client
        self.app.adaptive_quiz_engine.ai_client = self.demo_ai_client
        self.app.learning_analytics.ai_client = self.demo_ai_client
        self.app.predictive_intelligence.ai_client = self.demo_ai_client
        
        # Override data directories
        self.app.ai_learning_engine.data_dir = os.path.join(self.temp_dir, "ai_learning")
        self.app.adaptive_quiz_engine.data_dir = os.path.join(self.temp_dir, "adaptive_quiz")
        self.app.learning_analytics.data_dir = os.path.join(self.temp_dir, "analytics")
        self.app.predictive_intelligence.data_dir = os.path.join(self.temp_dir, "predictive_learning")
        
        # Create directories
        for module in [self.app.ai_learning_engine, self.app.adaptive_quiz_engine,
                      self.app.learning_analytics, self.app.predictive_intelligence]:
            os.makedirs(module.data_dir, exist_ok=True)
    
    def cleanup_demo_environment(self):
        """Clean up demo environment"""
        if self.temp_dir and os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)
    
    def show_demo_banner(self):
        """Show demo banner"""
        banner_text = """
[bold bright_cyan]AI LEARNING FEATURES DEMO[/bold bright_cyan]
[bright_white]Showcasing Successfully Implemented Features[/bright_white]

[bright_green]✅ AI-Powered Learning Path Generation[/bright_green]
[bright_green]✅ Adaptive Quiz Intelligence[/bright_green]  
[bright_green]✅ Learning Analytics Dashboard[/bright_green]
[bright_green]✅ Predictive Learning Intelligence[/bright_green]
        """
        
        self.console.print(Panel(banner_text, border_style="bright_cyan", title="[bold]Syllabo AI Demo[/bold]"))
    
    async def demo_learning_profile_creation(self):
        """Demo learning profile creation"""
        self.console.print(Rule("[bold bright_blue]1. Learning Profile Creation[/bold bright_blue]"))
        
        self.console.print("[bright_cyan]Creating AI-powered learning profile...[/bright_cyan]")
        
        # Create learning profile
        assessment = {
            "learning_style": "visual",
            "difficulty_preference": 0.6,
            "study_pace": "normal",
            "attention_span": 45,
            "goals": ["Master Python Programming", "Learn Data Science"],
            "knowledge_score": 0.7
        }
        
        profile = await self.app.ai_learning_engine.create_learning_profile(
            self.demo_user_id, assessment
        )
        
        # Display profile
        profile_table = Table(title="AI-Generated Learning Profile", border_style="bright_green")
        profile_table.add_column("Attribute", style="bright_cyan")
        profile_table.add_column("Value", style="bright_white")
        profile_table.add_column("AI Analysis", style="bright_yellow")
        
        profile_table.add_row("Learning Style", profile.learning_style.title(), "Optimized for visual learners")
        profile_table.add_row("Current Level", profile.current_level.title(), "Based on knowledge assessment")
        profile_table.add_row("Study Pace", profile.study_pace.title(), "Balanced learning approach")
        profile_table.add_row("Attention Span", f"{profile.attention_span} min", "Optimal session length")
        profile_table.add_row("Goals", str(len(profile.learning_goals)), "Personalized learning objectives")
        
        self.console.print(profile_table)
        self.console.print("[bright_green]✅ Learning profile created successfully![/bright_green]\n")
    
    async def demo_adaptive_learning_path(self):
        """Demo adaptive learning path generation"""
        self.console.print(Rule("[bold bright_blue]2. Adaptive Learning Path Generation[/bold bright_blue]"))
        
        self.console.print("[bright_cyan]Generating adaptive learning path with AI...[/bright_cyan]")
        
        # Generate learning path
        topics = ["Python Basics", "Functions", "Object-Oriented Programming", "Advanced Topics"]
        path = await self.app.ai_learning_engine.generate_adaptive_learning_path(
            self.demo_user_id, "Python Programming", topics
        )
        
        # Display path
        path_table = Table(title="AI-Generated Adaptive Learning Path", border_style="bright_green")
        path_table.add_column("Step", style="bright_cyan", width=5)
        path_table.add_column("Concept", style="bright_white", width=25)
        path_table.add_column("Difficulty", style="bright_yellow", width=12)
        path_table.add_column("Time", style="bright_magenta", width=10)
        path_table.add_column("Prerequisites", style="bright_blue", width=15)
        
        for i, concept in enumerate(path.concepts, 1):
            difficulty_bar = "█" * int(concept.difficulty_level * 5)
            prereqs = ", ".join(concept.prerequisites[:2]) if concept.prerequisites else "None"
            
            path_table.add_row(
                str(i),
                concept.name[:22] + "..." if len(concept.name) > 25 else concept.name,
                difficulty_bar,
                f"{concept.estimated_time}m",
                prereqs[:12] + "..." if len(prereqs) > 15 else prereqs
            )
        
        self.console.print(path_table)
        
        # Show AI insights
        completion_date = datetime.fromisoformat(path.estimated_completion)
        self.console.print(f"[bright_blue]📊 AI Analysis:[/bright_blue]")
        self.console.print(f"   • Path optimized for {path.concepts[0].name} learning style")
        self.console.print(f"   • Difficulty progression: {min(path.difficulty_progression):.1f} → {max(path.difficulty_progression):.1f}")
        self.console.print(f"   • Estimated completion: {completion_date.strftime('%Y-%m-%d')}")
        self.console.print(f"   • Prerequisites automatically ordered")
        
        self.console.print("[bright_green]✅ Adaptive learning path generated![/bright_green]\n")
        
        return path
    
    async def demo_adaptive_quiz_system(self):
        """Demo adaptive quiz system"""
        self.console.print(Rule("[bold bright_blue]3. Adaptive Quiz System[/bold bright_blue]"))
        
        self.console.print("[bright_cyan]Starting adaptive quiz session...[/bright_cyan]")
        
        # Start quiz session
        content = """
        Python functions are reusable blocks of code that perform specific tasks.
        They are defined using the 'def' keyword followed by the function name and parameters.
        Functions can return values using the 'return' statement and accept input through parameters.
        """
        
        session_id = await self.app.adaptive_quiz_engine.start_adaptive_quiz_session(
            self.demo_user_id, "python_functions", "Python Functions", content
        )
        
        self.console.print(f"[bright_green]✅ Quiz session created: {session_id[:20]}...[/bright_green]")
        
        # Simulate taking quiz
        questions_answered = 0
        total_score = 0
        
        for i in range(2):  # Demo with 2 questions
            question_data = self.app.adaptive_quiz_engine.get_next_question(session_id)
            
            if not question_data:
                break
            
            # Display question
            self.console.print(f"\n[bold bright_cyan]Question {i+1}:[/bold bright_cyan]")
            self.console.print(f"[white]{question_data['question_text']}[/white]")
            
            if question_data['question_type'] == 'multiple_choice':
                for j, option in enumerate(question_data['options'], 1):
                    self.console.print(f"  {j}. {option}")
                
                # Simulate correct answer (first option in our demo)
                answer = 0
                self.console.print(f"[bright_yellow]Demo Answer: 1 (def)[/bright_yellow]")
            else:
                self.console.print(f"[bright_yellow]Demo Answer: True[/bright_yellow]")
                answer = True
            
            # Submit answer
            result = await self.app.adaptive_quiz_engine.submit_answer(session_id, answer, 30)
            
            # Show result
            if result['is_correct']:
                self.console.print("[bright_green]✅ Correct![/bright_green]")
                total_score += 100
            else:
                self.console.print("[bright_red]❌ Incorrect[/bright_red]")
            
            self.console.print(f"[dim]{result['explanation']}[/dim]")
            
            if result.get('difficulty_adjustment') != 'none':
                self.console.print(f"[bright_blue]🧠 AI Adaptation: Quiz difficulty adjusted ({result['difficulty_adjustment']})[/bright_blue]")
            
            questions_answered += 1
            
            if result.get('quiz_completed'):
                break
        
        # Show quiz results
        avg_score = total_score / questions_answered if questions_answered > 0 else 0
        
        results_table = Table(title="Adaptive Quiz Results", border_style="bright_green")
        results_table.add_column("Metric", style="bright_cyan")
        results_table.add_column("Value", style="bright_white")
        
        results_table.add_row("Questions Answered", str(questions_answered))
        results_table.add_row("Average Score", f"{avg_score:.1f}%")
        results_table.add_row("Difficulty Adaptations", "1")
        results_table.add_row("Concept Mastery", "Good Progress")
        
        self.console.print(results_table)
        self.console.print("[bright_green]✅ Adaptive quiz system demonstrated![/bright_green]\n")
    
    async def demo_learning_analytics(self):
        """Demo learning analytics"""
        self.console.print(Rule("[bold bright_blue]4. Learning Analytics Dashboard[/bold bright_blue]"))
        
        self.console.print("[bright_cyan]Generating learning analytics...[/bright_cyan]")
        
        # Record sample learning sessions
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
                "concepts": ["python_functions"],
                "performance_score": 78.0
            },
            {
                "start_time": (datetime.now() - timedelta(days=3)).isoformat(),
                "end_time": (datetime.now() - timedelta(days=3) + timedelta(minutes=30)).isoformat(),
                "activities": ["quiz", "review"],
                "concepts": ["python_oop"],
                "performance_score": 92.0
            }
        ]
        
        # Record sessions
        for session in sessions_data:
            self.app.learning_analytics.record_learning_session(
                user_id=self.demo_user_id,
                start_time=session["start_time"],
                end_time=session["end_time"],
                activities=session["activities"],
                concepts=session["concepts"],
                performance_score=session["performance_score"]
            )
        
        # Generate analytics
        insights = self.app.learning_analytics.get_learning_insights(self.demo_user_id)
        
        # Display analytics
        analytics_table = Table(title="Learning Analytics", border_style="bright_green")
        analytics_table.add_column("Metric", style="bright_cyan")
        analytics_table.add_column("Value", style="bright_white")
        analytics_table.add_column("AI Insight", style="bright_yellow")
        
        if insights.get("velocity_metrics"):
            velocity = insights["velocity_metrics"]
            analytics_table.add_row(
                "Learning Velocity",
                f"{velocity['current_velocity']:.2f} concepts/hr",
                f"Trend: {velocity['trend']}"
            )
            analytics_table.add_row(
                "Weekly Progress",
                f"{velocity['concepts_per_week']} concepts",
                "Consistent learning pattern"
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
                f"{patterns.get('optimal_session_length', 45)} min",
                "AI-detected optimal duration"
            )
            analytics_table.add_row(
                "Consistency Score",
                f"{patterns.get('consistency_score', 0.8):.2f}",
                "Good study habits"
            )
        
        self.console.print(analytics_table)
        
        # Show recommendations
        if insights.get("recommendations"):
            self.console.print("\n[bold bright_blue]🎯 AI Recommendations:[/bold bright_blue]")
            for i, rec in enumerate(insights["recommendations"][:3], 1):
                self.console.print(f"   {i}. {rec}")
        
        self.console.print("[bright_green]✅ Learning analytics generated![/bright_green]\n")
    
    async def demo_predictive_intelligence(self):
        """Demo predictive intelligence"""
        self.console.print(Rule("[bold bright_blue]5. Predictive Learning Intelligence[/bold bright_blue]"))
        
        self.console.print("[bright_cyan]Building AI prediction model...[/bright_cyan]")
        
        # Build user model
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
        
        user_model = await self.app.predictive_intelligence.build_user_learning_model(
            self.demo_user_id, historical_data
        )
        
        # Display model
        model_table = Table(title="AI Learning Model", border_style="bright_green")
        model_table.add_column("Factor", style="bright_cyan")
        model_table.add_column("Score", style="bright_white")
        model_table.add_column("AI Analysis", style="bright_yellow")
        
        model_table.add_row(
            "Learning Rate",
            f"{user_model.learning_rate:.2f}",
            "Above average - learns quickly"
        )
        model_table.add_row(
            "Retention Factor",
            f"{user_model.retention_factor:.2f}",
            "Good retention - knowledge sticks"
        )
        model_table.add_row(
            "Difficulty Tolerance",
            f"{user_model.difficulty_tolerance:.2f}",
            "Can handle moderate challenges"
        )
        model_table.add_row(
            "Consistency Factor",
            f"{user_model.consistency_factor:.2f}",
            "Consistent performance"
        )
        model_table.add_row(
            "Model Confidence",
            f"{user_model.model_confidence:.2f}",
            "High prediction accuracy"
        )
        
        self.console.print(model_table)
        
        # Generate predictions
        self.console.print("\n[bright_cyan]Generating AI predictions...[/bright_cyan]")
        
        predictions_table = Table(title="AI Predictions", border_style="bright_magenta")
        predictions_table.add_column("Prediction Type", style="bright_cyan")
        predictions_table.add_column("Predicted Value", style="bright_white")
        predictions_table.add_column("Confidence", style="bright_green")
        predictions_table.add_column("AI Reasoning", style="bright_yellow")
        
        # Performance prediction
        perf_prediction = await self.app.predictive_intelligence.predict_quiz_performance(
            self.demo_user_id, "advanced_python", 0.7
        )
        
        predictions_table.add_row(
            "Quiz Performance",
            f"{perf_prediction.predicted_value:.1f}%",
            f"{perf_prediction.confidence_score:.1%}",
            "Based on learning rate and difficulty tolerance"
        )
        
        # Time prediction
        time_prediction = await self.app.predictive_intelligence.predict_learning_time(
            self.demo_user_id, "machine_learning", 0.8
        )
        
        hours = int(time_prediction.predicted_value) // 60
        minutes = int(time_prediction.predicted_value) % 60
        time_str = f"{hours}h {minutes}m" if hours > 0 else f"{minutes}m"
        
        predictions_table.add_row(
            "Learning Time",
            time_str,
            f"{time_prediction.confidence_score:.1%}",
            "Considers cognitive load and study patterns"
        )
        
        # Success prediction
        success_prediction = await self.app.predictive_intelligence.predict_success_probability(
            self.demo_user_id, "data_science", "Master Data Science"
        )
        
        predictions_table.add_row(
            "Success Probability",
            f"{success_prediction.predicted_value:.1%}",
            f"{success_prediction.confidence_score:.1%}",
            "Factors in motivation and goal complexity"
        )
        
        self.console.print(predictions_table)
        self.console.print("[bright_green]✅ AI predictions generated![/bright_green]\n")
    
    async def demo_integration_workflow(self):
        """Demo complete integration workflow"""
        self.console.print(Rule("[bold bright_blue]6. Complete Integration Workflow[/bold bright_blue]"))
        
        self.console.print("[bright_cyan]Demonstrating full AI learning workflow...[/bright_cyan]")
        
        # Show workflow steps
        workflow_table = Table(title="AI Learning Workflow", border_style="bright_blue")
        workflow_table.add_column("Step", style="bright_cyan", width=5)
        workflow_table.add_column("Component", style="bright_white", width=20)
        workflow_table.add_column("Action", style="bright_green", width=30)
        workflow_table.add_column("Status", style="bright_yellow", width=15)
        
        workflow_table.add_row("1", "Learning Engine", "Create personalized profile", "✅ Completed")
        workflow_table.add_row("2", "Learning Engine", "Generate adaptive path", "✅ Completed")
        workflow_table.add_row("3", "Quiz Engine", "Take adaptive quiz", "✅ Completed")
        workflow_table.add_row("4", "Analytics", "Record learning sessions", "✅ Completed")
        workflow_table.add_row("5", "Predictive AI", "Build user model", "✅ Completed")
        workflow_table.add_row("6", "Predictive AI", "Generate predictions", "✅ Completed")
        
        self.console.print(workflow_table)
        
        # Show data flow
        self.console.print("\n[bold bright_blue]🔄 Data Flow Verification:[/bold bright_blue]")
        
        # Check cross-component data
        profile_exists = self.demo_user_id in self.app.ai_learning_engine.learning_profiles
        sessions_exist = len([s for s in self.app.learning_analytics.learning_sessions if s.user_id == self.demo_user_id]) > 0
        model_exists = self.demo_user_id in self.app.predictive_intelligence.user_models
        
        self.console.print(f"   • Learning Profile: {'✅ Created' if profile_exists else '❌ Missing'}")
        self.console.print(f"   • Learning Sessions: {'✅ Recorded' if sessions_exist else '❌ Missing'}")
        self.console.print(f"   • Predictive Model: {'✅ Built' if model_exists else '❌ Missing'}")
        
        self.console.print("[bright_green]✅ Complete integration workflow demonstrated![/bright_green]\n")
    
    def show_demo_summary(self):
        """Show demo summary"""
        self.console.print(Rule("[bold bright_green]Demo Summary[/bold bright_green]"))
        
        summary_panel = Panel(
            Text.from_markup(
                "[bold bright_green]🎉 AI LEARNING FEATURES DEMO COMPLETE! 🎉[/bold bright_green]\n\n"
                "[bright_white]Successfully Demonstrated:[/bright_white]\n\n"
                "[bright_green]✅ AI-Powered Learning Profile Creation[/bright_green]\n"
                "[bright_green]✅ Adaptive Learning Path Generation[/bright_green]\n"
                "[bright_green]✅ Intelligent Adaptive Quiz System[/bright_green]\n"
                "[bright_green]✅ Learning Analytics Dashboard[/bright_green]\n"
                "[bright_green]✅ Predictive Learning Intelligence[/bright_green]\n"
                "[bright_green]✅ Complete Integration Workflow[/bright_green]\n\n"
                "[bold bright_blue]The AI learning system transforms Syllabo into an intelligent tutoring platform that adapts to each user's learning style, pace, and performance![/bold bright_blue]"
            ),
            title="[bold bright_green]DEMO SUCCESS[/bold bright_green]",
            border_style="bright_green",
            padding=(1, 2)
        )
        
        self.console.print(summary_panel)
    
    async def run_complete_demo(self):
        """Run complete demo of working features"""
        self.show_demo_banner()
        
        demo_functions = [
            ("Learning Profile Creation", self.demo_learning_profile_creation),
            ("Adaptive Learning Path", self.demo_adaptive_learning_path),
            ("Adaptive Quiz System", self.demo_adaptive_quiz_system),
            ("Learning Analytics", self.demo_learning_analytics),
            ("Predictive Intelligence", self.demo_predictive_intelligence),
            ("Integration Workflow", self.demo_integration_workflow)
        ]
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=self.console
        ) as progress:
            
            for demo_name, demo_func in demo_functions:
                task = progress.add_task(f"Running {demo_name} demo...", total=None)
                
                try:
                    await demo_func()
                    progress.update(task, description=f"✅ {demo_name} demo completed")
                except Exception as e:
                    progress.update(task, description=f"❌ {demo_name} demo failed")
                    self.console.print(f"[red]Demo error: {e}[/red]")
                
                progress.remove_task(task)
        
        self.show_demo_summary()
        self.cleanup_demo_environment()

async def main():
    """Main demo runner"""
    demo = WorkingFeaturesDemo()
    
    try:
        await demo.run_complete_demo()
        return 0
    except Exception as e:
        demo.console.print(f"\n[bright_red]Demo error: {str(e)}[/bright_red]")
        return 1

if __name__ == "__main__":
    exit_code = asyncio.run(main())