#!/usr/bin/env python3
"""
Syllabo - AI-Powered Learning Assistant
Main entry point for all features

"""

import os
import sys
import asyncio
import time
from datetime import datetime
from typing import Dict, List
from dotenv import load_dotenv
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.rule import Rule
from rich.prompt import Prompt
from rich.text import Text
from rich.align import Align

load_dotenv()
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

# Import components
from src.database import SyllaboDatabase
from src.logger import SyllaboLogger
from src.ai_client import AIClient
from src.syllabus_parser import SyllabusParser
from src.quiz_generator import QuizGenerator
from src.progress_dashboard import ProgressDashboard
from src.goals_manager import GoalsManager
from src.platform_integrator import PlatformIntegrator
from src.bookmark_manager import BookmarkManager
from src.study_session_manager import StudySessionManager
from src.spaced_repetition import SpacedRepetitionEngine
from src.notes_generator import NotesGenerator
from src.video_analyzer import VideoAnalyzer
from src.resource_finder import ResourceFinder
from src.youtube_client import YouTubeClient
from src.config_manager import ConfigManager
from src.resource_manager import ResourceManager
from src.persistent_quiz_manager import PersistentQuizManager
from src.enhanced_video_search import EnhancedVideoSearch
from src.ai_learning_engine import AILearningEngine
from src.adaptive_quiz_engine import AdaptiveQuizEngine
from src.learning_analytics_dashboard import LearningAnalyticsDashboard
from src.predictive_learning_intelligence import PredictiveLearningIntelligence

class SyllaboMain:
    """Main application class with all features"""
    
    async def _safe_execute_command(self, command_func, *args, **kwargs):
        """Safely execute a command with proper error handling"""
        try:
            return await command_func(*args, **kwargs)
        except KeyboardInterrupt:
            self.console.print("\n[yellow]Operation cancelled by user[/yellow]")
            return False
        except FileNotFoundError as e:
            self.console.print(f"[red]File not found: {e}[/red]")
            return False
        except PermissionError as e:
            self.console.print(f"[red]Permission denied: {e}[/red]")
            return False
        except Exception as e:
            self.console.print(f"[red]Unexpected error: {e}[/red]")
            self.logger.error(f"Command execution error: {e}")
            return False

    def __init__(self):
        self.console = Console()
        self.logger = SyllaboLogger("main")
        
        # Initialize core components
        self.db = SyllaboDatabase()
        self.ai_client = AIClient()
        self.syllabus_parser = SyllabusParser()
        
        # Initialize feature modules
        self.spaced_repetition = SpacedRepetitionEngine()
        self.quiz_generator = QuizGenerator(self.ai_client, self.db)
        self.progress_dashboard = ProgressDashboard(self.db, self.spaced_repetition)
        self.goals_manager = GoalsManager(self.db)
        self.platform_integrator = PlatformIntegrator()
        self.bookmark_manager = BookmarkManager()
        self.study_session_manager = StudySessionManager(self.spaced_repetition)
        
        # Initialize new enhanced modules
        self.notes_generator = NotesGenerator(self.ai_client)
        self.youtube_client = YouTubeClient()
        self.video_analyzer = VideoAnalyzer(self.ai_client)
        self.resource_finder = ResourceFinder(self.ai_client)
        self.config_manager = ConfigManager()
        
        # Initialize enhanced resource and quiz management
        self.resource_manager = ResourceManager()
        self.persistent_quiz_manager = PersistentQuizManager(self.ai_client)
        self.enhanced_video_search = EnhancedVideoSearch()
        
        # Initialize AI-powered learning features
        self.ai_learning_engine = AILearningEngine(self.ai_client, self.db)
        self.adaptive_quiz_engine = AdaptiveQuizEngine(self.ai_client, self.db)
        self.learning_analytics = LearningAnalyticsDashboard(self.ai_client, self.db)
        self.predictive_intelligence = PredictiveLearningIntelligence(self.ai_client, self.db)
    
    def reload_ai_client(self):
        """Reload AI client after configuration changes"""
        self.ai_client.reload_config()
        # Update components that use AI client
        self.quiz_generator.ai_client = self.ai_client
        self.notes_generator.ai_client = self.ai_client
        self.video_analyzer.ai_client = self.ai_client
        self.resource_finder.ai_client = self.ai_client
    
    def print_banner(self):
        """Print enhanced application banner"""
        banner_text = Text()
        banner_text.append("SYLLABO", style="bold cyan")
        banner_text.append("\n")
        banner_text.append("AI-Powered Learning Assistant", style="bold white")
        banner_text.append("\n")
        banner_text.append("Your comprehensive educational resource manager", style="dim")
        
        banner_panel = Panel(
            Align.center(banner_text),
            border_style="bright_cyan",
            padding=(1, 2),
            title="[bold bright_blue]Welcome[/bold bright_blue]",
            title_align="center"
        )
        
        self.console.print(banner_panel)
        self.console.print("[dim]Ready to start learning![/dim]")
        self.console.print()
    
    def show_interactive_menu(self):
        """Show interactive main menu with all options"""
        self.console.print(Rule("[bold bright_cyan]Main Menu[/bold bright_cyan]", style="bright_cyan"))
        
        menu_options = [
            ("1", "analyze", "Analyze Syllabus", "Process syllabus and find learning resources with direct links"),
            ("2", "quiz", "Interactive Quizzes", "Generate quizzes from topics, syllabus, or text"),
            ("3", "saved_quizzes", "Saved Quizzes", "View and retake your saved quizzes"),
            ("4", "progress", "Progress Dashboard", "View learning progress and analytics"),
            ("5", "goals", "Study Goals", "Manage learning goals and milestones"),
            ("6", "bookmarks", "Smart Bookmarks", "Manage video bookmarks and notes"),
            ("7", "session", "Study Sessions", "Pomodoro timer and focus sessions"),
            ("8", "review", "Spaced Repetition", "Review topics using spaced repetition"),

            ("9", "saved_resources", "Saved Resources", "View and manage your saved learning resources"),
            ("10", "notes", "Generate Study Notes", "Create notes and questions from content"),
            ("11", "ai_learning", "AI Learning Paths", "Generate adaptive learning paths with AI"),
            ("12", "adaptive_quiz", "Adaptive Quizzes", "Take intelligent adaptive quizzes"),
            ("13", "learning_analytics", "Learning Analytics", "View comprehensive learning analytics"),
            ("14", "predictions", "Learning Predictions", "Get AI predictions for learning outcomes"),
            ("15", "demo", "🎯 Features Demo", "Comprehensive demo of all app features for testing"),
            ("16", "config", "Configuration", "Manage API keys and application settings"),
            ("17", "help", "Help & Documentation", "Get help and usage information"),
            ("0", "exit", "Exit", "Exit the application")
        ]
        
        # Create menu table
        menu_table = Table(
            show_header=True, 
            header_style="bold bright_magenta",
            border_style="bright_blue",
            title="[bold bright_white]Choose Your Action[/bold bright_white]",
            title_style="bold bright_white"
        )
        menu_table.add_column("Option", style="bright_cyan", width=8, justify="center")
        menu_table.add_column("Feature", style="bright_green", width=22)
        menu_table.add_column("Description", style="bright_white", width=45)
        
        for option, cmd, feature, desc in menu_options:
            menu_table.add_row(option, feature, desc)
        
        self.console.print(menu_table)
        self.console.print()
        
        return self._get_user_choice(menu_options)
    
    def _get_user_choice(self, menu_options):
        """Get user menu choice with validation"""
        valid_choices = [option[0] for option in menu_options]
        
        while True:
            try:
                choice = Prompt.ask(
                    "[bold bright_yellow]Select an option[/bold bright_yellow]",
                    choices=valid_choices,
                    default="1",
                    show_choices=False
                )
                
                for option, cmd, feature, desc in menu_options:
                    if choice == option:
                        self.console.print(f"[bright_green]Selected:[/bright_green] {feature}")
                        return cmd
                        
            except KeyboardInterrupt:
                self.console.print("\n[yellow]Operation cancelled[/yellow]")
                return "exit"
            except Exception as e:
                self.console.print(f"[red]Error: {e}[/red]")
                continue
    
    async def _handle_interactive_command(self, command):
        """Handle interactive command execution"""
        try:
            if command == 'analyze':
                await self._interactive_analyze()
            elif command == 'quiz':
                await self._interactive_quiz()
            elif command == 'saved_quizzes':
                await self._interactive_saved_quizzes()
            elif command == 'progress':
                await self._interactive_progress()
            elif command == 'goals':
                await self._interactive_goals()
            elif command == 'bookmarks':
                await self._interactive_bookmarks()
            elif command == 'session':
                await self._interactive_session()
            elif command == 'review':
                await self._interactive_review()
            elif command == 'enhanced_videos':
                await self._interactive_enhanced_videos()
            elif command == 'resources':
                await self._interactive_enhanced_resources()
            elif command == 'saved_resources':
                await self._interactive_saved_resources()
            elif command == 'notes':
                await self._interactive_notes()
            elif command == 'ai_learning':
                await self._interactive_ai_learning()
            elif command == 'adaptive_quiz':
                await self._interactive_adaptive_quiz()
            elif command == 'learning_analytics':
                await self._interactive_learning_analytics()
            elif command == 'predictions':
                await self._interactive_predictions()
            elif command == 'demo':
                await self._interactive_demo()

            elif command == 'config':
                self._interactive_config()
            else:
                self.console.print(f"[yellow]Unknown command: {command}[/yellow]")
                
        except Exception as e:
            self.console.print(f"[red]Error executing command: {e}[/red]")
            self.logger.error(f"Interactive command error: {e}")

    
    async def _interactive_analyze(self):
        """Interactive syllabus analysis"""
        self.console.print(Rule("[bold bright_blue]Syllabus Analysis Setup[/bold bright_blue]"))
        
        # Get input method
        input_choice = Prompt.ask(
            "[bright_yellow]How would you like to provide your syllabus?[/bright_yellow]",
            choices=["file", "text"],
            default="file"
        )
        
        if input_choice == "file":
            file_path = Prompt.ask("[bright_cyan]Enter syllabus file path[/bright_cyan]")
            if not file_path or not os.path.exists(file_path):
                self.console.print("[bright_red]File not found. Please check the path.[/bright_red]")
                return
            
            # Load and analyze file
            try:
                with self.console.status("[bright_cyan]Loading syllabus..."):
                    content = self.syllabus_parser.load_from_file(file_path)
                    title = os.path.basename(file_path)
                
                self.console.print(f"[bright_green]Loaded:[/bright_green] {title}")
                
                # Extract topics
                with self.console.status("[bright_cyan]Extracting topics with AI..."):
                    topics = await self.syllabus_parser.extract_topics(content, self.ai_client)
                
                if topics:
                    self.console.print(f"[bright_green]Found {len(topics)} topics[/bright_green]")
                    
                    # Show topics
                    topics_table = Table(title="Extracted Topics", border_style="bright_green")
                    topics_table.add_column("Topic", style="bright_cyan")
                    topics_table.add_column("Description", style="bright_white")
                    
                    for topic in topics[:5]:  # Show first 5
                        desc = topic.get('description', 'No description')
                        if len(desc) > 50:
                            desc = desc[:50] + "..."
                        topics_table.add_row(topic['name'], desc)
                    
                    if len(topics) > 5:
                        topics_table.add_row(f"... and {len(topics)-5} more", "[dim]Topics extracted[/dim]")
                    
                    self.console.print(topics_table)
                    
                    # Save to database
                    syllabus_id = self.db.save_syllabus(title, content)
                    self.db.save_topics(syllabus_id, topics)
                    self.console.print("[bright_green]Saved to database[/bright_green]")
                    
                    # Enhanced analysis workflow - integrate new features
                    await self._comprehensive_analysis_workflow(topics, title)
                    
                else:
                    self.console.print("[bright_yellow]No topics found[/bright_yellow]")
                    
            except Exception as e:
                self.console.print(f"[bright_red]Error: {e}[/bright_red]")
        
        else:  # text input
            self.console.print("[bright_cyan]Enter your syllabus content (press Enter twice when done):[/bright_cyan]")
            
            lines = []
            empty_lines = 0
            
            while empty_lines < 2:
                try:
                    line = input()
                    if line.strip() == "":
                        empty_lines += 1
                    else:
                        empty_lines = 0
                    lines.append(line)
                except KeyboardInterrupt:
                    self.console.print("\n[yellow]Input cancelled[/yellow]")
                    return
            
            content = "\n".join(lines).strip()
            
            if not content:
                self.console.print("[bright_red]No content provided[/bright_red]")
                return
            
            try:
                # Get syllabus title
                title = Prompt.ask("[bright_cyan]Syllabus title/subject[/bright_cyan]", default="Custom Syllabus")
                
                with self.console.status("[bright_cyan]Extracting topics with AI..."):
                    topics = await self.syllabus_parser.extract_topics(content, self.ai_client)
                
                if topics:
                    self.console.print(f"[bright_green]Found {len(topics)} topics[/bright_green]")
                    
                    # Show topics
                    topics_table = Table(title="Extracted Topics", border_style="bright_green")
                    topics_table.add_column("Topic", style="bright_cyan")
                    topics_table.add_column("Description", style="bright_white")
                    
                    for topic in topics[:5]:  # Show first 5
                        desc = topic.get('description', 'No description')
                        if len(desc) > 50:
                            desc = desc[:50] + "..."
                        topics_table.add_row(topic['name'], desc)
                    
                    if len(topics) > 5:
                        topics_table.add_row(f"... and {len(topics)-5} more", "[dim]Topics extracted[/dim]")
                    
                    self.console.print(topics_table)
                    
                    # Save to database
                    syllabus_id = self.db.save_syllabus(title, content)
                    self.db.save_topics(syllabus_id, topics)
                    self.console.print("[bright_green]Saved to database[/bright_green]")
                    
                    # Enhanced analysis workflow for text input
                    await self._comprehensive_analysis_workflow(topics, title)
                else:
                    self.console.print("[bright_yellow]No topics found[/bright_yellow]")
                    
            except Exception as e:
                self.console.print(f"[bright_red]Error: {e}[/bright_red]")
    
    async def _interactive_quiz(self):
        """Interactive quiz generation and taking"""
        self.console.print(Rule("[bold bright_blue]Interactive Quizzes[/bold bright_blue]"))
        
        # Give user options for quiz generation
        quiz_source = Prompt.ask(
            "[bright_yellow]How would you like to generate the quiz?[/bright_yellow]",
            choices=["topics", "syllabus", "text"],
            default="topics"
        )
        
        if quiz_source == "topics":
            await self._quiz_from_topics()
        elif quiz_source == "syllabus":
            await self._quiz_from_syllabus()
        else:  # text
            await self._quiz_from_text()
    
    async def _quiz_from_topics(self):
        """Generate quiz from existing database topics"""
        # Get available topics from database
        topics = self.db.get_all_topics()
        if not topics:
            self.console.print("[yellow]No topics found. Please analyze a syllabus first or use syllabus/text option.[/yellow]")
            return
        
        # Show available topics
        topics_table = Table(title="Available Topics", border_style="bright_green")
        topics_table.add_column("ID", style="bright_cyan", width=5)
        topics_table.add_column("Topic", style="bright_white")
        
        for i, topic in enumerate(topics[:10], 1):
            topics_table.add_row(str(i), topic.get('name', 'Unknown'))
        
        self.console.print(topics_table)
        
        try:
            choice = int(Prompt.ask("[bright_yellow]Select topic number[/bright_yellow]", default="1"))
            if 1 <= choice <= len(topics):
                selected_topic = topics[choice - 1]
                
                # Ask for number of questions
                num_questions = int(Prompt.ask("[bright_yellow]Number of questions[/bright_yellow]", default="5"))
                
                with self.console.status("[bright_cyan]Generating quiz..."):
                    quiz_data = await self.quiz_generator.generate_quiz(selected_topic['name'], num_questions)
                
                if quiz_data:
                    await self._take_quiz(quiz_data)
                else:
                    self.console.print("[yellow]Could not generate quiz for this topic[/yellow]")
            else:
                self.console.print("[red]Invalid selection[/red]")
        except ValueError:
            self.console.print("[red]Please enter a valid number[/red]")
    
    async def _quiz_from_syllabus(self):
        """Generate quiz from syllabus file"""
        file_path = Prompt.ask("[bright_cyan]Enter syllabus file path[/bright_cyan]")
        if not file_path or not os.path.exists(file_path):
            self.console.print("[bright_red]File not found. Please check the path.[/bright_red]")
            return
        
        try:
            # Load syllabus content
            with self.console.status("[bright_cyan]Loading syllabus..."):
                content = self.syllabus_parser.load_from_file(file_path)
                title = os.path.basename(file_path)
            
            self.console.print(f"[bright_green]Loaded:[/bright_green] {title}")
            
            # Get quiz parameters
            topic_name = Prompt.ask("[bright_cyan]Quiz topic/subject[/bright_cyan]", default=title)
            num_questions = int(Prompt.ask("[bright_yellow]Number of questions[/bright_yellow]", default="5"))
            
            # Generate quiz from content
            with self.console.status("[bright_cyan]Generating quiz from syllabus..."):
                quiz_data = await self.quiz_generator.generate_quiz_from_content(content, topic_name, num_questions)
            
            if quiz_data:
                await self._take_quiz(quiz_data)
            else:
                self.console.print("[yellow]Could not generate quiz from this syllabus[/yellow]")
                
        except Exception as e:
            self.console.print(f"[bright_red]Error: {e}[/bright_red]")
    
    async def _quiz_from_text(self):
        """Generate quiz from direct text input"""
        self.console.print("[bright_cyan]Enter your study content (press Enter twice when done):[/bright_cyan]")
        
        lines = []
        empty_lines = 0
        
        while empty_lines < 2:
            try:
                line = input()
                if line.strip() == "":
                    empty_lines += 1
                else:
                    empty_lines = 0
                lines.append(line)
            except KeyboardInterrupt:
                self.console.print("\n[yellow]Input cancelled[/yellow]")
                return
        
        content = "\n".join(lines).strip()
        
        if not content:
            self.console.print("[bright_red]No content provided[/bright_red]")
            return
        
        try:
            # Get quiz parameters
            topic_name = Prompt.ask("[bright_cyan]Quiz topic/subject[/bright_cyan]", default="Study Material")
            num_questions = int(Prompt.ask("[bright_yellow]Number of questions[/bright_yellow]", default="5"))
            
            # Generate quiz from content
            with self.console.status("[bright_cyan]Generating quiz from your content..."):
                quiz_data = await self.quiz_generator.generate_quiz_from_content(content, topic_name, num_questions)
            
            if quiz_data:
                await self._take_quiz(quiz_data)
            else:
                self.console.print("[yellow]Could not generate quiz from this content[/yellow]")
                
        except ValueError:
            self.console.print("[red]Please enter a valid number for questions[/red]")
        except Exception as e:
            self.console.print(f"[bright_red]Error: {e}[/bright_red]")
    
    async def _take_quiz(self, quiz_data):
        """Take an interactive quiz"""
        self.console.print(f"\n[bold bright_green]Quiz: {quiz_data.get('title', 'Topic Quiz')}[/bold bright_green]")
        
        questions = quiz_data.get('questions', [])
        if not questions:
            self.console.print("[yellow]No questions available[/yellow]")
            return
        
        score = 0
        total = len(questions)
        
        for i, question in enumerate(questions, 1):
            self.console.print(f"\n[bold bright_cyan]Question {i}/{total}:[/bold bright_cyan]")
            self.console.print(question.get('question', ''))
            
            question_type = question.get('type', 'multiple_choice')
            is_correct = False
            
            if question_type == 'multiple_choice':
                options = question.get('options', [])
                if options:
                    for j, option in enumerate(options, 1):
                        self.console.print(f"  {j}. {option}")
                    
                    try:
                        answer = int(Prompt.ask("[bright_yellow]Your answer[/bright_yellow]"))
                        correct_index = question.get('correct_answer', 0)  # 0-based index
                        correct_display = correct_index + 1  # Convert to 1-based for display
                        
                        if answer == correct_display:
                            self.console.print("[bright_green]Correct![/bright_green]")
                            is_correct = True
                        else:
                            correct_option = options[correct_index] if correct_index < len(options) else "Unknown"
                            self.console.print(f"[bright_red]Incorrect. The correct answer was {correct_display}: {correct_option}[/bright_red]")
                            
                    except ValueError:
                        self.console.print("[red]Invalid answer[/red]")
                        
            elif question_type == 'true_false':
                answer = Prompt.ask("[bright_yellow]True or False (T/F)[/bright_yellow]").upper().strip()
                correct_answer = question.get('correct_answer', True)
                
                if (answer == 'T' and correct_answer) or (answer == 'F' and not correct_answer):
                    self.console.print("[bright_green]Correct![/bright_green]")
                    is_correct = True
                else:
                    correct_text = "True" if correct_answer else "False"
                    self.console.print(f"[bright_red]Incorrect. The correct answer was {correct_text}[/bright_red]")
                    
            elif question_type == 'short_answer':
                answer = Prompt.ask("[bright_yellow]Your answer[/bright_yellow]").strip()
                correct_answer = question.get('correct_answer', '')
                
                # Simple keyword matching for short answers
                if self._check_short_answer_match(answer, correct_answer):
                    self.console.print("[bright_green]Correct![/bright_green]")
                    is_correct = True
                else:
                    self.console.print(f"[bright_red]Incorrect. Expected: {correct_answer}[/bright_red]")
            
            # Show explanation if available
            explanation = question.get('explanation', '')
            if explanation:
                self.console.print(f"[dim]{explanation}[/dim]")
            
            if is_correct:
                score += 1
        
        # Show final score
        percentage = (score / total) * 100
        self.console.print(f"\n[bold bright_green]Quiz Complete![/bold bright_green]")
        self.console.print(f"Score: {score}/{total} ({percentage:.1f}%)")
    
    def _check_short_answer_match(self, user_answer: str, correct_answer: str) -> bool:
        """Check if short answer matches expected answer"""
        user_words = set(user_answer.lower().split())
        correct_words = set(correct_answer.lower().split())
        
        # Check for exact match first
        if user_answer.lower().strip() == correct_answer.lower().strip():
            return True
        
        # Check for keyword overlap (60% threshold)
        if correct_words:
            overlap = len(user_words.intersection(correct_words))
            return overlap >= len(correct_words) * 0.6
        
        return False
    
    async def _interactive_progress(self):
        """Interactive progress dashboard"""
        self.console.print(Rule("[bold bright_blue]Progress Dashboard[/bold bright_blue]"))
        
        try:
            progress_data = self.progress_dashboard.get_progress_summary()
            
            # Display progress summary
            progress_table = Table(title="Learning Progress", border_style="bright_green")
            progress_table.add_column("Metric", style="bright_cyan")
            progress_table.add_column("Value", style="bright_white")
            
            progress_table.add_row("Topics Studied", str(progress_data.get('topics_studied', 0)))
            progress_table.add_row("Quizzes Taken", str(progress_data.get('quizzes_taken', 0)))
            progress_table.add_row("Study Sessions", str(progress_data.get('study_sessions', 0)))
            progress_table.add_row("Average Score", f"{progress_data.get('average_score', 0):.1f}%")
            
            self.console.print(progress_table)
            
            # Show recent activity
            recent_activity = progress_data.get('recent_activity', [])
            if recent_activity:
                activity_table = Table(title="Recent Activity", border_style="bright_blue")
                activity_table.add_column("Date", style="bright_cyan")
                activity_table.add_column("Activity", style="bright_white")
                
                for activity in recent_activity[:5]:
                    activity_table.add_row(
                        activity.get('date', 'Unknown'),
                        activity.get('description', 'No description')
                    )
                
                self.console.print(activity_table)
            
        except Exception as e:
            self.console.print(f"[red]Error loading progress: {e}[/red]")
    
    async def _interactive_goals(self):
        """Interactive goals management"""
        self.console.print(Rule("[bold bright_blue]Study Goals[/bold bright_blue]"))
        
        action = Prompt.ask(
            "[bright_yellow]What would you like to do?[/bright_yellow]",
            choices=["view", "add", "update", "delete"],
            default="view"
        )
        
        if action == "view":
            goals = self.goals_manager.get_all_goals()
            if goals:
                goals_table = Table(title="Your Study Goals", border_style="bright_green")
                goals_table.add_column("Goal", style="bright_cyan")
                goals_table.add_column("Target", style="bright_white")
                goals_table.add_column("Progress", style="bright_yellow")
                goals_table.add_column("Status", style="bright_green")
                
                for goal in goals:
                    status = "✓ Complete" if goal.completed else "In Progress"
                    deadline = goal.deadline if hasattr(goal, 'deadline') else 'No deadline'
                    progress = int((goal.current_value / goal.target_value) * 100) if goal.target_value > 0 else 0
                    goals_table.add_row(
                        goal.title,
                        deadline,
                        f"{progress}%",
                        status
                    )
                
                self.console.print(goals_table)
            else:
                self.console.print("[yellow]No goals set yet[/yellow]")
        
        elif action == "add":
            title = Prompt.ask("[bright_cyan]Goal title[/bright_cyan]")
            description = Prompt.ask("[bright_cyan]Goal description[/bright_cyan]")
            goal_type = Prompt.ask("[bright_cyan]Goal type[/bright_cyan]", choices=["daily", "weekly", "monthly", "milestone"], default="weekly")
            target_value = int(Prompt.ask("[bright_cyan]Target value[/bright_cyan]", default="1"))
            unit = Prompt.ask("[bright_cyan]Unit (minutes/topics/quizzes)[/bright_cyan]", default="topics")
            days_to_complete = int(Prompt.ask("[bright_cyan]Days to complete[/bright_cyan]", default="30"))
            
            goal_id = self.goals_manager.create_goal(title, description, goal_type, target_value, unit, days_to_complete)
            self.console.print(f"[bright_green]Goal created with ID: {goal_id}[/bright_green]")
    

    async def _interactive_bookmarks(self):
        """Interactive bookmark management"""
        self.console.print(Rule("[bold bright_blue]Smart Bookmarks[/bold bright_blue]"))
        
        action = Prompt.ask(
            "[bright_yellow]What would you like to do?[/bright_yellow]",
            choices=["view", "add", "delete"],
            default="view"
        )
        
        if action == "view":
            bookmarks = self.bookmark_manager.get_all_bookmarks()
            if bookmarks:
                bookmarks_table = Table(title="Your Bookmarks", border_style="bright_green")
                bookmarks_table.add_column("Title", style="bright_cyan")
                bookmarks_table.add_column("URL", style="bright_white")
                bookmarks_table.add_column("Notes", style="bright_yellow")
                
                for bookmark in bookmarks[:10]:
                    notes = bookmark.get('notes', 'No notes')
                    if len(notes) > 30:
                        notes = notes[:30] + "..."
                    
                    bookmarks_table.add_row(
                        bookmark.get('title', 'Unknown'),
                        bookmark.get('url', 'No URL')[:40],
                        notes
                    )
                
                self.console.print(bookmarks_table)
            else:
                self.console.print("[yellow]No bookmarks saved yet[/yellow]")
        
        elif action == "add":
            title = Prompt.ask("[bright_cyan]Bookmark title[/bright_cyan]")
            url = Prompt.ask("[bright_cyan]URL[/bright_cyan]")
            notes = Prompt.ask("[bright_cyan]Notes (optional)[/bright_cyan]", default="")
            topic = Prompt.ask("[bright_cyan]Topic[/bright_cyan]", default="General")
            
            # For bookmark manager, we need video_id, video_title, timestamp, note, topic
            bookmark_id = self.bookmark_manager.add_bookmark(
                video_id=url,  # Using URL as video_id for general bookmarks
                video_title=title,
                timestamp="0:00",  # Default timestamp
                note=notes,
                topic=topic
            )
            self.console.print(f"[bright_green]Bookmark saved with ID: {bookmark_id}[/bright_green]")
    
    async def _interactive_session(self):
        """Interactive study session with Pomodoro timer"""
        self.console.print(Rule("[bold bright_blue]Study Sessions[/bold bright_blue]"))
        
        topic = Prompt.ask("[bright_cyan]Study topic[/bright_cyan]")
        duration = int(Prompt.ask("[bright_yellow]Session duration (minutes)[/bright_yellow]", default="25"))
        
        session = self.study_session_manager.start_study_session(topic, duration)
        
        self.console.print(f"[bright_green]Starting {duration}-minute study session for: {topic}[/bright_green]")
        self.console.print("[dim]Press Ctrl+C to end session early[/dim]")
        
        try:
            import time
            start_time = time.time()
            end_time = start_time + (duration * 60)
            
            while time.time() < end_time:
                remaining = int(end_time - time.time())
                mins, secs = divmod(remaining, 60)
                
                self.console.print(f"\r[bright_yellow]Time remaining: {mins:02d}:{secs:02d}[/bright_yellow]", end="")
                time.sleep(1)
            
            self.console.print(f"\n[bright_green]Session complete![/bright_green]")
            self.study_session_manager.end_session("completed")
            
        except KeyboardInterrupt:
            self.console.print(f"\n[yellow]Session ended early[/yellow]")
            self.study_session_manager.end_session("interrupted")
    
    async def _interactive_review(self):
        """Interactive spaced repetition review"""
        self.console.print(Rule("[bold bright_blue]Spaced Repetition Review[/bold bright_blue]"))
        
        # Get items due for review
        review_items = self.spaced_repetition.get_due_topics()
        
        if not review_items:
            self.console.print("[yellow]No items due for review today![/yellow]")
            self.console.print("[dim]Check back tomorrow or add new topics to review.[/dim]")
            return
        
        self.console.print(f"[bright_green]You have {len(review_items)} items to review[/bright_green]")
        
        for i, item in enumerate(review_items, 1):
            self.console.print(f"\n[bold bright_cyan]Review {i}/{len(review_items)}:[/bold bright_cyan]")
            self.console.print(f"Topic: {item.topic_name}")
            
            if item.description:
                self.console.print(f"Description: {item.description}")
            
            Prompt.ask("[dim]Press Enter when ready to mark your review[/dim]", default="")
            
            # Get user feedback
            difficulty = Prompt.ask(
                "[bright_yellow]How difficult was this? (1=Easy, 2=Medium, 3=Hard)[/bright_yellow]",
                choices=["1", "2", "3"],
                default="2"
            )
            
            # Update the spaced repetition schedule
            success = int(difficulty) <= 2  # Easy and Medium are considered success
            self.spaced_repetition.mark_review(item.topic_name, success)
        
        self.console.print(f"\n[bright_green]Review session complete![/bright_green]")
        self.console.print("[dim]Great job! Keep up the consistent practice.[/dim]")
    
    async def _handle_analyze_command(self, args):
        """Handle analyze command from CLI"""
        await self._interactive_analyze()
    
    async def _handle_search_command(self, args):
        """Handle search command from CLI"""
        if not args.topic:
            self.console.print("[red]Error: Topic is required for search[/red]")
            return
        
        self.console.print(f"[bright_cyan]Searching for videos on: {args.topic}[/bright_cyan]")
        
        try:
            # Use the video analyzer to find relevant videos
            videos = await self.video_analyzer.find_videos(args.topic, max_results=args.max_videos)
            
            if videos:
                self.console.print(f"[bright_green]Found {len(videos)} videos[/bright_green]")
                
                # Display results in a table
                videos_table = Table(title=f"Search Results for '{args.topic}'", border_style="bright_green")
                videos_table.add_column("Title", style="bright_cyan", width=40)
                videos_table.add_column("Channel", style="bright_white", width=20)
                videos_table.add_column("Duration", style="bright_yellow", width=10)
                videos_table.add_column("Views", style="bright_blue", width=10)
                
                for video in videos:
                    videos_table.add_row(
                        video.get('title', 'Unknown')[:37] + "..." if len(video.get('title', '')) > 40 else video.get('title', 'Unknown'),
                        video.get('channel', 'Unknown')[:17] + "..." if len(video.get('channel', '')) > 20 else video.get('channel', 'Unknown'),
                        video.get('duration', 'Unknown'),
                        video.get('view_count', 'Unknown')
                    )
                
                self.console.print(videos_table)
                
                if args.save:
                    # Save results to file
                    import json
                    import os
                    os.makedirs('exports', exist_ok=True)
                    filename = f"exports/search_{args.topic.replace(' ', '_')}.{args.export_format}"
                    
                    if args.export_format == 'json':
                        with open(filename, 'w') as f:
                            json.dump(videos, f, indent=2)
                    
                    self.console.print(f"[bright_green]Results saved to {filename}[/bright_green]")
            else:
                self.console.print("[yellow]No videos found for this topic[/yellow]")
                
        except Exception as e:
            self.console.print(f"[red]Search error: {e}[/red]")
    
    async def _handle_review_command(self, args):
        """Handle review command from CLI"""
        if not args.review_action:
            self.console.print("[red]Error: Review action is required[/red]")
            return
        
        if args.review_action == 'add':
            if not args.topic:
                self.console.print("[red]Error: Topic is required for adding to review[/red]")
                return
            
            success = self.spaced_repetition.add_topic(args.topic, args.description or "")
            if success:
                self.console.print(f"[bright_green]Added '{args.topic}' to review schedule[/bright_green]")
            else:
                self.console.print(f"[yellow]Topic '{args.topic}' is already in your review schedule[/yellow]")
        
        elif args.review_action == 'list':
            topics = self.spaced_repetition.get_all_topics()
            if not topics:
                self.console.print("[yellow]No topics in your review schedule[/yellow]")
                return
            
            topics_table = Table(title="Your Review Schedule", border_style="bright_green")
            topics_table.add_column("Topic", style="bright_cyan", width=30)
            topics_table.add_column("Mastery", style="bright_white", width=12)
            topics_table.add_column("Success Rate", style="bright_yellow", width=12)
            topics_table.add_column("Next Review", style="bright_blue", width=12)
            
            for topic in topics:
                mastery_color = {
                    'Learning': 'red', 'Beginner': 'yellow', 'Intermediate': 'blue', 
                    'Advanced': 'green', 'Mastered': 'bright_green'
                }.get(topic['mastery_level'], 'white')
                
                next_review_text = "Due now" if topic['days_until_review'] <= 0 else f"{topic['days_until_review']} days"
                
                topics_table.add_row(
                    topic['topic_name'][:27] + "..." if len(topic['topic_name']) > 30 else topic['topic_name'],
                    f"[{mastery_color}]{topic['mastery_level']}[/{mastery_color}]",
                    f"{topic['success_rate']}%",
                    next_review_text
                )
            
            self.console.print(topics_table)
            
            summary = self.spaced_repetition.get_study_summary()
            self.console.print(f"[bright_green]Summary: {summary['total_topics']} topics, {summary['due_now']} due now, {summary['mastered_topics']} mastered[/bright_green]")
        
        elif args.review_action == 'due':
            due_topics = self.spaced_repetition.get_due_topics()
            if not due_topics:
                self.console.print("[bright_green]No topics are due for review right now[/bright_green]")
                return
            
            self.console.print(f"[bright_yellow]You have {len(due_topics)} topic{'s' if len(due_topics) != 1 else ''} due for review[/bright_yellow]")
            
            due_table = Table(title="Topics Due for Review", border_style="bright_red")
            due_table.add_column("No.", style="dim", width=4)
            due_table.add_column("Topic", style="bright_cyan")
            due_table.add_column("Description", style="bright_white")
            
            for i, item in enumerate(due_topics, 1):
                due_table.add_row(
                    str(i),
                    item.topic_name,
                    item.description or "No description"
                )
            
            self.console.print(due_table)
        
        elif args.review_action == 'mark':
            if not args.topic:
                self.console.print("[red]Error: Topic is required for marking review[/red]")
                return
            
            success = self.spaced_repetition.mark_review(args.topic, args.success)
            if success:
                result_text = "successful" if args.success else "failed"
                self.console.print(f"[bright_green]Marked '{args.topic}' as {result_text} review[/bright_green]")
            else:
                self.console.print(f"[yellow]Topic '{args.topic}' not found in review schedule[/yellow]")
        
        elif args.review_action == 'stats':
            if args.topic:
                stats = self.spaced_repetition.get_topic_stats(args.topic)
                if not stats:
                    self.console.print(f"[yellow]Topic '{args.topic}' not found[/yellow]")
                    return
                
                stats_panel = Panel(
                    f"Mastery Level: {stats['mastery_level']}\n"
                    f"Success Rate: {stats['success_rate']}%\n"
                    f"Total Reviews: {stats['total_reviews']}\n"
                    f"Success Streak: {stats['success_streak']}\n"
                    f"Next Review: {stats['next_review_date']}\n"
                    f"Current Interval: {stats['current_interval']} days",
                    title=f"Stats for {stats['topic_name']}",
                    border_style="bright_blue"
                )
                self.console.print(stats_panel)
            else:
                summary = self.spaced_repetition.get_study_summary()
                analytics = self.spaced_repetition.get_learning_analytics()
                
                stats_table = Table(title="Review Statistics", border_style="bright_blue")
                stats_table.add_column("Metric", style="bright_cyan")
                stats_table.add_column("Value", style="bright_white")
                
                stats_table.add_row("Total Topics", str(summary['total_topics']))
                stats_table.add_row("Due Now", str(summary['due_now']))
                stats_table.add_row("Due Today", str(summary['due_today']))
                stats_table.add_row("Mastered Topics", str(summary['mastered_topics']))
                stats_table.add_row("Average Success Rate", f"{summary['average_success_rate']}%")
                stats_table.add_row("Total Reviews", str(analytics['total_reviews']))
                stats_table.add_row("Retention Rate", f"{analytics['retention_rate']}%")
                
                self.console.print(stats_table)
        
        elif args.review_action == 'remove':
            if not args.topic:
                self.console.print("[red]Error: Topic is required for removal[/red]")
                return
            
            success = self.spaced_repetition.remove_topic(args.topic)
            if success:
                self.console.print(f"[bright_green]Removed '{args.topic}' from review schedule[/bright_green]")
            else:
                self.console.print(f"[yellow]Topic '{args.topic}' not found in review schedule[/yellow]")
    
    async def _handle_goals_command(self, args):
        """Handle goals command from CLI"""
        if not args.action:
            self.console.print("[red]Error: Goals action is required[/red]")
            return
        
        if args.action == 'create':
            if not all([args.title, args.type, args.target, args.unit]):
                self.console.print("[red]Error: Title, type, target, and unit are required for creating goals[/red]")
                return
            
            goal_id = self.goals_manager.create_goal(
                title=args.title,
                description=args.description or "",
                goal_type=args.type,
                target_value=args.target,
                unit=args.unit
            )
            self.console.print(f"[bright_green]Goal created with ID: {goal_id}[/bright_green]")
        
        elif args.action == 'list':
            goals = self.goals_manager.get_all_goals()
            if not goals:
                self.console.print("[yellow]No goals set yet[/yellow]")
                return
            
            goals_table = Table(title="Your Study Goals", border_style="bright_green")
            goals_table.add_column("Goal", style="bright_cyan", width=25)
            goals_table.add_column("Type", style="bright_white", width=10)
            goals_table.add_column("Progress", style="bright_yellow", width=15)
            goals_table.add_column("Status", style="bright_blue", width=12)
            goals_table.add_column("Deadline", style="bright_magenta", width=12)
            
            for goal in goals:
                progress_percent = (goal.current_value / goal.target_value * 100) if goal.target_value > 0 else 0
                status = "✓ Complete" if goal.completed else "In Progress"
                status_color = "bright_green" if goal.completed else "bright_yellow"
                
                from datetime import datetime
                try:
                    deadline = datetime.fromisoformat(goal.deadline).strftime('%Y-%m-%d')
                except:
                    deadline = "No deadline"
                
                goals_table.add_row(
                    goal.title[:22] + "..." if len(goal.title) > 25 else goal.title,
                    goal.goal_type.capitalize(),
                    f"{goal.current_value}/{goal.target_value} {goal.unit} ({progress_percent:.1f}%)",
                    f"[{status_color}]{status}[/{status_color}]",
                    deadline
                )
            
            self.console.print(goals_table)
            
            summary = self.goals_manager.get_goal_summary()
            self.console.print(f"[bright_green]Summary: {summary['total_goals']} total, {summary['active_goals']} active, {summary['completed_goals']} completed[/bright_green]")
        
        elif args.action == 'suggest':
            suggestions = self.goals_manager.suggest_goals("beginner")  # Default to beginner
            
            suggestions_table = Table(title="Goal Suggestions", border_style="bright_blue")
            suggestions_table.add_column("Title", style="bright_cyan")
            suggestions_table.add_column("Type", style="bright_white")
            suggestions_table.add_column("Target", style="bright_yellow")
            
            for suggestion in suggestions:
                suggestions_table.add_row(
                    suggestion['title'],
                    suggestion['type'].capitalize(),
                    f"{suggestion['target']} {suggestion['unit']}"
                )
            
            self.console.print(suggestions_table)
            self.console.print("[dim]Use 'goals create' command to add any of these goals[/dim]")
    
    async def _handle_quiz_command(self, args):
        """Handle quiz command from CLI"""
        # If specific arguments provided, use them directly
        if hasattr(args, 'topic') and args.topic:
            # Generate quiz for specific topic
            num_questions = getattr(args, 'num_questions', 5)
            
            with self.console.status("[bright_cyan]Generating quiz..."):
                quiz_data = await self.quiz_generator.generate_quiz(args.topic, num_questions)
            
            if quiz_data:
                await self._take_quiz(quiz_data)
            else:
                self.console.print("[yellow]Could not generate quiz for this topic[/yellow]")
        
        elif hasattr(args, 'content_file') and args.content_file:
            # Generate quiz from content file
            if not os.path.exists(args.content_file):
                self.console.print(f"[bright_red]File not found: {args.content_file}[/bright_red]")
                return
            
            try:
                with self.console.status("[bright_cyan]Loading content..."):
                    content = self.syllabus_parser.load_from_file(args.content_file)
                    topic_name = os.path.basename(args.content_file)
                
                num_questions = getattr(args, 'num_questions', 5)
                
                with self.console.status("[bright_cyan]Generating quiz from file..."):
                    quiz_data = await self.quiz_generator.generate_quiz_from_content(content, topic_name, num_questions)
                
                if quiz_data:
                    await self._take_quiz(quiz_data)
                else:
                    self.console.print("[yellow]Could not generate quiz from this file[/yellow]")
                    
            except Exception as e:
                self.console.print(f"[bright_red]Error: {e}[/bright_red]")
        
        elif hasattr(args, 'source') and args.source:
            # Use specified source
            if args.source == "topics":
                await self._quiz_from_topics()
            elif args.source == "syllabus":
                await self._quiz_from_syllabus()
            else:  # text
                await self._quiz_from_text()
        
        else:
            # Default to interactive mode
            await self._interactive_quiz()
    
    async def _handle_progress_command(self, args):
        """Handle progress command from CLI"""
        await self._interactive_progress()
    
    async def _handle_session_command(self, args):
        """Handle session command from CLI"""
        await self._interactive_session()
    
    async def _handle_bookmarks_command(self, args):
        """Handle bookmarks command from CLI"""
        await self._interactive_bookmarks()
    
    async def _handle_platforms_command(self, args):
        """Handle platforms command from CLI - redirects to enhanced resources"""
        await self._interactive_enhanced_resources()
    
    async def _handle_config_command(self, args):
        """Handle config command from CLI"""
        if not hasattr(args, 'config_action') or not args.config_action:
            # No subcommand, show interactive config menu
            self.config_manager.show_config_menu()
            return
        
        if args.config_action == 'show':
            self.config_manager.show_current_config()
        
        elif args.config_action == 'youtube':
            if hasattr(args, 'key') and args.key:
                # Set YouTube API key directly
                if self.config_manager.update_env_key('YOUTUBE_API_KEY', args.key):
                    self.console.print("[bright_green]✅ YouTube API key updated successfully![/bright_green]")
                else:
                    self.console.print("[red]❌ Failed to update YouTube API key[/red]")
            else:
                # Interactive YouTube API configuration
                self.config_manager.configure_youtube_api()
        
        elif args.config_action == 'gemini':
            if hasattr(args, 'key') and args.key:
                # Set Gemini API key directly
                if self.config_manager.update_env_key('GEMINI_API_KEY', args.key):
                    self.console.print("[bright_green]✅ Gemini API key updated successfully![/bright_green]")
                else:
                    self.console.print("[red]❌ Failed to update Gemini API key[/red]")
            else:
                # Interactive Gemini API configuration
                self.config_manager.configure_gemini_api()
        
        elif args.config_action == 'test':
            service = getattr(args, 'service', 'all')
            if service == 'all':
                self.config_manager.test_api_connections()
            else:
                config = self.config_manager.load_config()
                if service == 'youtube':
                    youtube_key = config.get('YOUTUBE_API_KEY', '')
                    if youtube_key and youtube_key != 'your_youtube_api_key_here':
                        self.config_manager._test_youtube_api(youtube_key)
                    else:
                        self.console.print("[yellow]YouTube API key not configured[/yellow]")
                elif service == 'gemini':
                    gemini_key = config.get('GEMINI_API_KEY', '')
                    if gemini_key and gemini_key != 'your_gemini_api_key_here_optional':
                        self.config_manager._test_gemini_api(gemini_key)
                    else:
                        self.console.print("[yellow]Gemini API key not configured[/yellow]")
        
        elif args.config_action == 'reset':
            self.config_manager.reset_configuration()
        
        else:
            self.console.print(f"[yellow]Unknown config action: {args.config_action}[/yellow]")
    
    def _show_help(self):
        """Show comprehensive help information"""
        help_text = """
[bold bright_cyan]Syllabo - AI-Powered Learning Assistant[/bold bright_cyan]

[bright_white]Available Commands:[/bright_white]
• analyze    - Analyze syllabus and extract topics
• search     - Search for educational videos
• review     - Spaced repetition system
• goals      - Study goals management
• quiz       - Interactive quizzes from topics, syllabus, or text
• progress   - Learning progress dashboard
• session    - Study sessions with Pomodoro timer
• bookmarks  - Smart bookmarks management
• platforms  - Multi-platform search (redirects to enhanced resources)

[bright_white]Examples:[/bright_white]
  python main.py analyze --file syllabus.pdf
  python main.py search --topic "Machine Learning"
  python main.py review add --topic "Neural Networks"
  python main.py goals create --title "Daily Study" --type daily --target 30 --unit minutes

[bright_white]Interactive Mode:[/bright_white]
  python main.py interactive

For detailed help on any command, use:
  python main.py [command] --help
        """
        
        help_panel = Panel(
            help_text,
            title="[bold bright_blue]Help & Documentation[/bold bright_blue]",
            border_style="bright_blue",
            padding=(1, 2)
        )
        
        self.console.print(help_panel)
    
    async def _comprehensive_analysis_workflow(self, topics: List[Dict]):
        """Comprehensive analysis workflow integrating videos, resources, and notes generation"""
        self.console.print(Rule("[bold bright_magenta]Comprehensive Learning Analysis[/bold bright_magenta]"))
        
        # Ask user what they want to do with the extracted topics
        self.console.print(f"\n[bright_green]Great! I found {len(topics)} topics from your syllabus.[/bright_green]")
        self.console.print("[bright_white]Let me help you create a complete learning plan with:[/bright_white]")
        self.console.print("• Educational videos and playlists")
        self.console.print("• Books, courses, and learning resources")
        self.console.print("• Study notes and questions")
        self.console.print("• Spaced repetition schedule")
        
        proceed = Prompt.ask(
            "\n[bright_yellow]Would you like me to create a comprehensive learning plan? (y/n)[/bright_yellow]",
            default="y"
        ).lower() == 'y'
        
        if not proceed:
            self.console.print("[dim]You can always run individual features later from the main menu.[/dim]")
            return
        
        # Get user preferences for the analysis
        preferences = await self._get_analysis_preferences()
        
        # Initialize analysis results collection
        analysis_results = {
            'topics': [],
            'all_videos': [],
            'all_resources': [],
            'coverage_analysis': {},
            'notes_generated': 0,
            'questions_generated': 0
        }
        
        # Process each topic (limit to 3 for speed)
        topic_names = [topic.get('name', '') for topic in topics[:3]]  # Limit to first 3 topics for faster processing
        
        self.console.print(f"\n[bright_cyan]Processing {len(topic_names)} topics...[/bright_cyan]")
        
        for i, topic_name in enumerate(topic_names, 1):
            self.console.print(f"\n{'-'*60}")
            self.console.print(f"[bold bright_blue]Topic {i}/{len(topic_names)}: {topic_name}[/bold bright_blue]")
            self.console.print(f"{'-'*60}")
            
            topic_result = {'name': topic_name, 'videos': [], 'resources': [], 'coverage': {}}
            
            # 1. Find and analyze videos if requested
            if preferences.get('include_videos', True):
                video_analysis = await self._analyze_topic_videos(topic_name, preferences)
                if video_analysis:
                    topic_result['videos'] = video_analysis.get('all_content', [])
                    topic_result['coverage'] = video_analysis.get('topic_coverage_details', {})
                    analysis_results['all_videos'].extend(topic_result['videos'])
                    
                    # Count notes and questions generated
                    if video_analysis.get('notes_generated'):
                        analysis_results['notes_generated'] += video_analysis.get('notes_count', 0)
                        analysis_results['questions_generated'] += video_analysis.get('questions_count', 0)
            
            # 2. Find learning resources if requested
            if preferences.get('include_resources', True):
                resources = await self._find_topic_resources(topic_name, preferences)
                if resources:
                    topic_result['resources'] = resources
                    analysis_results['all_resources'].extend(resources.get('all_resources', []))
            
            # 3. Add to spaced repetition if requested
            if preferences.get('add_to_spaced_repetition', True):
                self._add_topic_to_spaced_repetition(topic_name, topics[i-1])
            
            analysis_results['topics'].append(topic_result)
            
            # Small delay between topics for better UX
            if i < len(topic_names):
                self.console.print("[dim]Moving to next topic...[/dim]")
                await asyncio.sleep(1)
        
        # Final comprehensive summary with all details
        await self._display_comprehensive_summary(analysis_results, preferences)
    
    async def _get_analysis_preferences(self) -> Dict:
        """Get user preferences for comprehensive analysis"""
        self.console.print("\n[bold bright_yellow]Analysis Preferences[/bold bright_yellow]")
        
        preferences = {}
        
        # Video analysis preferences
        preferences['include_videos'] = Prompt.ask(
            "[bright_cyan]Find and analyze educational videos? (y/n)[/bright_cyan]",
            default="y"
        ).lower() == 'y'
        
        if preferences['include_videos']:
            print("\nVideo learning preferences:")
            print("1. One comprehensive video per topic")
            print("2. Multiple focused videos per topic")
            print("3. Playlists and course series")
            print("4. Let AI decide based on available content")
            
            video_pref = Prompt.ask(
                "[bright_cyan]Choose video preference (1-4)[/bright_cyan]",
                choices=["1", "2", "3", "4"],
                default="4"
            )
            
            pref_map = {
                "1": "single_comprehensive",
                "2": "multiple_focused", 
                "3": "playlist_series",
                "4": "auto_decide"
            }
            preferences['video_preference'] = pref_map[video_pref]
            
            # Notes generation preferences
            preferences['generate_notes'] = Prompt.ask(
                "[bright_cyan]Generate study notes and questions from videos? (y/n)[/bright_cyan]",
                default="y"
            ).lower() == 'y'
        
        # Resource finder preferences
        preferences['include_resources'] = Prompt.ask(
            "[bright_cyan]Find books, courses, and learning materials? (y/n)[/bright_cyan]",
            default="y"
        ).lower() == 'y'
        
        if preferences['include_resources']:
            print("\nResource preferences:")
            print("1. Free resources only")
            print("2. Paid resources only")
            print("3. Both free and paid resources")
            
            resource_pref = Prompt.ask(
                "[bright_cyan]Choose resource preference (1-3)[/bright_cyan]",
                choices=["1", "2", "3"],
                default="3"
            )
            
            pref_map = {"1": "free", "2": "paid", "3": "both"}
            preferences['resource_preference'] = pref_map[resource_pref]
        
        # Spaced repetition preferences
        preferences['add_to_spaced_repetition'] = Prompt.ask(
            "[bright_cyan]Add topics to spaced repetition system? (y/n)[/bright_cyan]",
            default="y"
        ).lower() == 'y'
        
        return preferences
    
    async def _analyze_topic_videos(self, topic_name: str, preferences: Dict):
        """Analyze videos for a specific topic"""
        self.console.print(f"[bright_cyan]🎥 Finding videos for: {topic_name}[/bright_cyan]")
        
        try:
            with self.console.status(f"Searching for {topic_name} videos..."):
                # Search for videos and playlists (reduced for speed)
                videos = await self.youtube_client.search_videos(topic_name, 5)  # Reduced from 8 to 5
                playlists = await self.youtube_client.search_playlists(topic_name, 2)  # Reduced from 3 to 2
                
                if not videos and not playlists:
                    self.console.print(f"[yellow]No videos found for {topic_name}[/yellow]")
                    return None
                
                # Analyze content
                analysis = await self.video_analyzer.analyze_videos_and_playlists(videos, playlists, topic_name)
                
                # Display concise results
                self._display_topic_video_summary(analysis, topic_name)
                
                # Prepare detailed results for summary
                all_content = []
                
                # Add primary resource
                if analysis.get('primary_resource'):
                    primary = analysis['primary_resource']
                    primary['is_primary'] = True
                    all_content.append(primary)
                
                # Add supplementary content
                all_content.extend(analysis.get('supplementary_videos', []))
                all_content.extend(analysis.get('supplementary_playlists', []))
                
                # Generate notes if requested
                notes_count = 0
                questions_count = 0
                if preferences.get('generate_notes', False) and analysis.get('primary_resource'):
                    notes_result = await self._generate_topic_notes(analysis['primary_resource'], topic_name)
                    if notes_result:
                        notes_count = notes_result.get('notes_count', 0)
                        questions_count = notes_result.get('questions_count', 0)
                
                return {
                    'all_content': all_content,
                    'topic_coverage_details': analysis.get('topic_coverage_details', {}),
                    'notes_generated': notes_count > 0,
                    'notes_count': notes_count,
                    'questions_count': questions_count
                }
                
        except Exception as e:
            self.console.print(f"[red]Error analyzing videos for {topic_name}: {e}[/red]")
            return None
    
    def _display_topic_video_summary(self, analysis: Dict, topic_name: str):
        """Display concise video analysis summary"""
        primary = analysis.get('primary_resource')
        if primary:
            content_type = "Video" if primary.get('type') != 'playlist' else "Playlist"
            self.console.print(f"[bright_green]✓ Best {content_type}:[/bright_green] {primary['title']}")
            self.console.print(f"  Channel: {primary['channel']} | Score: {primary.get('composite_score', 0):.1f}/10")
            
            # Show topic coverage if available
            coverage = analysis.get('topic_coverage_details', {})
            if coverage:
                completeness = coverage.get('learning_completeness', 0)
                self.console.print(f"  Coverage: {completeness:.0f}% of expected topics")
                
                missing = coverage.get('missing_subtopics', [])
                if missing and len(missing) <= 3:
                    self.console.print(f"  [yellow]Missing: {', '.join(missing)}[/yellow]")
        
        # Show supplementary content count
        supp_videos = len(analysis.get('supplementary_videos', []))
        supp_playlists = len(analysis.get('supplementary_playlists', []))
        if supp_videos or supp_playlists:
            self.console.print(f"  [dim]+ {supp_videos} supplementary videos, {supp_playlists} playlists[/dim]")
    
    async def _generate_topic_notes(self, content: Dict, topic_name: str):
        """Generate notes for a topic's primary content"""
        try:
            # Set preferences for automatic generation
            self.notes_generator.set_user_preferences({
                'generate_notes': True,
                'generate_questions': True,
                'notes_style': 'concise'
            })
            
            # Generate notes without status display to avoid conflicts
            notes_data = await self.notes_generator.generate_study_notes(topic_name, content, None)
            
            # Display concise summary
            notes_count = len(notes_data.get('notes', []))
            questions_count = len(notes_data.get('questions', []))
            concepts_count = len(notes_data.get('key_concepts', []))
            
            self.console.print(f"[bright_green]✓ Generated:[/bright_green] {notes_count} notes, {questions_count} questions, {concepts_count} key concepts")
            
            return {
                'notes_count': notes_count,
                'questions_count': questions_count,
                'concepts_count': concepts_count,
                'notes_data': notes_data
            }
                
        except Exception as e:
            self.console.print(f"[red]Error generating notes: {e}[/red]")
            return None
    
    async def _find_topic_resources(self, topic_name: str, preferences: Dict):
        """Find learning resources for a specific topic"""
        self.console.print(f"[bright_cyan]📚 Finding resources for: {topic_name}[/bright_cyan]")
        
        try:
            resource_pref = preferences.get('resource_preference', 'both')
            topic_resources = await self.resource_finder._find_topic_resources(topic_name, resource_pref)
            
            # Display concise summary
            books_count = len(topic_resources.get('books', []))
            courses_count = len(topic_resources.get('courses', []))
            other_count = len(topic_resources.get('resources', []))
            
            if books_count or courses_count or other_count:
                self.console.print(f"[bright_green]✓ Found:[/bright_green] {books_count} books, {courses_count} courses, {other_count} other resources")
                
                # Show top resource
                all_resources = topic_resources.get('books', []) + topic_resources.get('courses', []) + topic_resources.get('resources', [])
                
                if all_resources:
                    top_resource = all_resources[0]
                    self.console.print(f"  [bright_white]Top recommendation:[/bright_white] {top_resource.get('title', 'Unknown')}")
                
                # Prepare detailed results for summary
                topic_resources['all_resources'] = all_resources
                return topic_resources
            else:
                self.console.print(f"[yellow]No resources found for {topic_name}[/yellow]")
                return None
                
        except Exception as e:
            self.console.print(f"[red]Error finding resources for {topic_name}: {e}[/red]")
            return None
            self.console.print(f"[red]Error finding resources for {topic_name}: {e}[/red]")
    
    def _add_topic_to_spaced_repetition(self, topic_name: str, topic_data: Dict):
        """Add topic to spaced repetition system"""
        try:
            description = topic_data.get('description', f'Study topic: {topic_name}')
            success = self.spaced_repetition.add_topic(topic_name, description)
            
            if success:
                self.console.print(f"[bright_green]✓ Added to spaced repetition:[/bright_green] {topic_name}")
            else:
                self.console.print(f"[dim]Already in spaced repetition: {topic_name}[/dim]")
                
        except Exception as e:
            self.console.print(f"[red]Error adding to spaced repetition: {e}[/red]")
    
    async def _display_comprehensive_summary(self, analysis_results: Dict, preferences: Dict):
        """Display comprehensive analysis summary with all videos, resources, and coverage details"""
        self.console.print(f"\n{'='*80}")
        self.console.print("[bold bright_green]📋 COMPREHENSIVE LEARNING ANALYSIS COMPLETE[/bold bright_green]")
        self.console.print(f"{'='*80}")
        
        # Overview statistics
        total_videos = len(analysis_results['all_videos'])
        total_resources = len(analysis_results['all_resources'])
        total_notes = analysis_results['notes_generated']
        total_questions = analysis_results['questions_generated']
        
        stats_table = Table(title="Analysis Overview", border_style="bright_cyan")
        stats_table.add_column("Metric", style="bright_white")
        stats_table.add_column("Count", style="bright_green")
        
        stats_table.add_row("Topics Analyzed", str(len(analysis_results['topics'])))
        stats_table.add_row("Videos Found", str(total_videos))
        stats_table.add_row("Learning Resources", str(total_resources))
        stats_table.add_row("Study Notes Generated", str(total_notes))
        stats_table.add_row("Practice Questions", str(total_questions))
        
        self.console.print(stats_table)
        
        # Detailed breakdown by topic
        self.console.print(f"\n[bold bright_magenta]📚 DETAILED TOPIC BREAKDOWN[/bold bright_magenta]")
        
        for topic_result in analysis_results['topics']:
            topic_name = topic_result['name']
            self.console.print(f"\n[bold bright_cyan]🎯 {topic_name}[/bold bright_cyan]")
            
            # Video analysis for this topic
            if topic_result['videos']:
                self.console.print(f"[bright_yellow]🎥 Videos ({len(topic_result['videos'])}):[/bright_yellow]")
                
                for i, video in enumerate(topic_result['videos'][:3], 1):  # Show top 3
                    is_primary = video.get('is_primary', False)
                    marker = "⭐ PRIMARY" if is_primary else f"  {i}."
                    title = video.get('title', 'Unknown Title')[:60]
                    channel = video.get('channel', 'Unknown Channel')
                    url = video.get('url', '#')
                    
                    self.console.print(f"    {marker} {title}")
                    self.console.print(f"        Channel: {channel}")
                    self.console.print(f"        Link: [link]{url}[/link]")
                    
                    # Show what's covered and missing
                    if is_primary and topic_result['coverage']:
                        coverage = topic_result['coverage']
                        completeness = coverage.get('learning_completeness', 0)
                        self.console.print(f"        Coverage: {completeness:.0f}% of expected topics")
                        
                        covered = coverage.get('covered_subtopics', [])
                        if covered:
                            covered_text = ', '.join(covered[:3])
                            if len(covered) > 3:
                                covered_text += f" + {len(covered)-3} more"
                            self.console.print(f"        ✅ Covers: {covered_text}")
                        
                        missing = coverage.get('missing_subtopics', [])
                        if missing:
                            missing_text = ', '.join(missing[:3])
                            if len(missing) > 3:
                                missing_text += f" + {len(missing)-3} more"
                            self.console.print(f"        ❌ Missing: {missing_text}")
                
                if len(topic_result['videos']) > 3:
                    self.console.print(f"    ... and {len(topic_result['videos'])-3} more videos")
            
            # Resources for this topic
            if topic_result['resources']:
                resources = topic_result['resources']
                books = resources.get('books', [])
                courses = resources.get('courses', [])
                other = resources.get('resources', [])
                
                self.console.print(f"[bright_yellow]📚 Learning Resources:[/bright_yellow]")
                
                # Show books
                if books:
                    self.console.print(f"    📖 Books ({len(books)}):")
                    for book in books[:2]:  # Show top 2
                        title = book.get('title', 'Unknown')[:50]
                        author = book.get('author', 'Unknown Author')
                        url = book.get('url', '#')
                        self.console.print(f"        • {title} by {author}")
                        self.console.print(f"          Link: [link]{url}[/link]")
                
                # Show courses
                if courses:
                    self.console.print(f"    🎓 Courses ({len(courses)}):")
                    for course in courses[:2]:  # Show top 2
                        title = course.get('title', 'Unknown')[:50]
                        provider = course.get('provider', 'Unknown Provider')
                        url = course.get('url', '#')
                        price = course.get('price', 'Unknown')
                        self.console.print(f"        • {title} - {provider}")
                        self.console.print(f"          Price: {price} | Link: [link]{url}[/link]")
                
                # Show other resources
                if other:
                    self.console.print(f"    🔗 Other Resources ({len(other)}):")
                    for resource in other[:2]:  # Show top 2
                        title = resource.get('title', 'Unknown')[:50]
                        url = resource.get('url', '#')
                        self.console.print(f"        • {title}")
                        self.console.print(f"          Link: [link]{url}[/link]")
            
            if not topic_result['videos'] and not topic_result['resources']:
                self.console.print("    [dim]No videos or resources found for this topic[/dim]")
        
        # Overall coverage analysis
        self.console.print(f"\n[bold bright_magenta]📊 OVERALL COVERAGE ANALYSIS[/bold bright_magenta]")
        
        total_topics = len(analysis_results['topics'])
        topics_with_videos = len([t for t in analysis_results['topics'] if t['videos']])
        topics_with_resources = len([t for t in analysis_results['topics'] if t['resources']])
        
        coverage_table = Table(title="Learning Coverage", border_style="bright_blue")
        coverage_table.add_column("Aspect", style="bright_white")
        coverage_table.add_column("Coverage", style="bright_green")
        coverage_table.add_column("Status", style="bright_yellow")
        
        video_coverage = (topics_with_videos / total_topics * 100) if total_topics > 0 else 0
        resource_coverage = (topics_with_resources / total_topics * 100) if total_topics > 0 else 0
        
        video_status = "Excellent" if video_coverage >= 80 else "Good" if video_coverage >= 60 else "Needs Improvement"
        resource_status = "Excellent" if resource_coverage >= 80 else "Good" if resource_coverage >= 60 else "Needs Improvement"
        
        coverage_table.add_row("Video Content", f"{video_coverage:.0f}% ({topics_with_videos}/{total_topics} topics)", video_status)
        coverage_table.add_row("Learning Resources", f"{resource_coverage:.0f}% ({topics_with_resources}/{total_topics} topics)", resource_status)
        
        self.console.print(coverage_table)
        
        # Recommendations based on gaps
        self.console.print(f"\n[bold bright_magenta]💡 RECOMMENDATIONS[/bold bright_magenta]")
        
        if video_coverage < 80:
            missing_video_topics = [t['name'] for t in analysis_results['topics'] if not t['videos']]
            if missing_video_topics:
                self.console.print(f"[yellow]📹 Consider searching for additional videos on:[/yellow]")
                for topic in missing_video_topics[:3]:
                    self.console.print(f"    • {topic}")
        
        if resource_coverage < 80:
            missing_resource_topics = [t['name'] for t in analysis_results['topics'] if not t['resources']]
            if missing_resource_topics:
                self.console.print(f"[yellow]📚 Look for additional books/courses on:[/yellow]")
                for topic in missing_resource_topics[:3]:
                    self.console.print(f"    • {topic}")
        
        # Next steps
        self.console.print(f"\n[bold bright_green]🚀 NEXT STEPS[/bold bright_green]")
        
        if preferences.get('add_to_spaced_repetition'):
            due_count = len(self.spaced_repetition.get_due_topics())
            if due_count > 0:
                self.console.print(f"• Review {due_count} topics due for spaced repetition (Menu option 8)")
            else:
                self.console.print("• Start reviewing topics tomorrow using spaced repetition (Menu option 8)")
        
        self.console.print("• Watch primary videos and take detailed notes")
        self.console.print("• Use generated study questions for self-assessment")
        self.console.print("• Explore recommended books and courses for deeper learning")
        self.console.print("• Set learning goals to track your progress (Menu option 4)")
        self.console.print("• Start focused study sessions with Pomodoro timer (Menu option 7)")
        
        self.console.print(f"\n[bright_green]🎉 Your comprehensive learning plan is ready![/bright_green]")
        self.console.print("[dim]All data has been saved and is accessible from the main menu.[/dim]")
    

    
    async def _interactive_resources(self):
        """Interactive resource finder"""
        self.console.print(Rule("[bold bright_blue]Resource Finder[/bold bright_blue]"))
        
        # Get topics from database or user input
        topics = self.db.get_all_topics()
        
        if topics:
            self.console.print("[bright_green]Found topics from your syllabus:[/bright_green]")
            for i, topic in enumerate(topics[:10], 1):
                self.console.print(f"{i}. {topic.get('name', 'Unknown')}")
            
            use_existing = Prompt.ask(
                "[bright_yellow]Use existing topics? (y/n)[/bright_yellow]",
                default="y"
            ).lower() == 'y'
            
            if use_existing:
                topic_names = [topic.get('name', '') for topic in topics[:10]]
            else:
                topic_input = Prompt.ask("[bright_cyan]Enter topics (comma-separated)[/bright_cyan]")
                topic_names = [t.strip() for t in topic_input.split(',') if t.strip()]
        else:
            topic_input = Prompt.ask("[bright_cyan]Enter topics to find resources for (comma-separated)[/bright_cyan]")
            topic_names = [t.strip() for t in topic_input.split(',') if t.strip()]
        
        if not topic_names:
            self.console.print("[red]No topics provided[/red]")
            return
        
        # Ask for resource preference
        preference = self.resource_finder._ask_user_preference()
        
        with self.console.status(f"[bright_cyan]Finding resources for {len(topic_names)} topics..."):
            try:
                resources = await self.resource_finder.find_resources_for_syllabus(topic_names, preference)
                
                # Display results using the built-in display method
                self.resource_finder.display_resources(resources)
                
            except Exception as e:
                self.console.print(f"[red]Resource search error: {e}[/red]")
    
    async def _interactive_notes(self):
        """Interactive notes generation"""
        self.console.print(Rule("[bold bright_blue]Generate Study Notes[/bold bright_blue]"))
        
        # Get user preferences
        preferences = self.notes_generator.ask_user_preferences()
        
        if not preferences.get('generate_notes') and not preferences.get('generate_questions'):
            self.console.print("[yellow]No content generation selected[/yellow]")
            return
        
        # Get topic and content
        topic = Prompt.ask("[bright_cyan]Enter topic for note generation[/bright_cyan]")
        if not topic:
            self.console.print("[red]No topic provided[/red]")
            return
        
        content_source = Prompt.ask(
            "[bright_yellow]Content source[/bright_yellow]",
            choices=["video_search", "manual_input"],
            default="video_search"
        )
        
        if content_source == "video_search":
            # Search for a video and generate notes
            with self.console.status(f"[bright_cyan]Searching for {topic} content..."):
                try:
                    videos = await self.youtube_client.search_videos(topic, 3)
                    if videos:
                        # Use the first video
                        video = videos[0]
                        self.console.print(f"[bright_green]Using video: {video['title']}[/bright_green]")
                        
                        notes_data = await self.notes_generator.generate_study_notes(topic, video, None)
                        self._display_generated_notes(notes_data, preferences)
                    else:
                        self.console.print("[yellow]No videos found for the topic[/yellow]")
                except Exception as e:
                    self.console.print(f"[red]Error: {e}[/red]")
        
        else:
            # Manual content input
            content_text = Prompt.ask("[bright_cyan]Enter content text or description[/bright_cyan]")
            if content_text:
                # Create a mock video object
                mock_video = {
                    'title': f"Manual content for {topic}",
                    'description': content_text,
                    'id': 'manual_input',
                    'channel': 'User Input'
                }
                
                notes_data = await self.notes_generator.generate_study_notes(topic, mock_video, content_text)
                self._display_generated_notes(notes_data, preferences)
    
    def _display_generated_notes(self, notes_data: Dict, preferences: Dict):
        """Display generated notes and questions"""
        self.console.print(f"\n[bold bright_green]Generated Study Materials for '{notes_data['topic']}'[/bold bright_green]")
        
        if notes_data.get('notes') and preferences.get('generate_notes'):
            self.console.print(f"\n[bold bright_cyan]Study Notes:[/bold bright_cyan]")
            for i, note in enumerate(notes_data['notes'], 1):
                self.console.print(f"{i}. {note}")
        
        if notes_data.get('questions') and preferences.get('generate_questions'):
            self.console.print(f"\n[bold bright_yellow]Study Questions:[/bold bright_yellow]")
            for i, question in enumerate(notes_data['questions'], 1):
                self.console.print(f"{i}. {question}")
        
        if notes_data.get('key_concepts'):
            self.console.print(f"\n[bold bright_magenta]Key Concepts:[/bold bright_magenta]")
            for concept in notes_data['key_concepts']:
                self.console.print(f"• {concept}")
        
        if notes_data.get('study_tips'):
            self.console.print(f"\n[bold bright_blue]Study Tips:[/bold bright_blue]")
            for tip in notes_data['study_tips']:
                self.console.print(f"• {tip}")
    
    async def _interactive_demo(self):
        """Launch comprehensive features demo"""
        self.console.print(Rule("[bold bright_green]🎯 Syllabo Features Demo[/bold bright_green]"))
        
        self.console.print("[bright_cyan]Welcome to the Syllabo Features Demo![/bright_cyan]")
        self.console.print("[bright_white]This comprehensive demo will showcase all features of the application.[/bright_white]\n")
        
        try:
            # Import and run the demo
            from demo_all_features import ComprehensiveFeaturesDemo
            
            demo = ComprehensiveFeaturesDemo()
            await demo.run_demo()
            
        except ImportError:
            self.console.print("[red]Demo module not found. Please ensure demo_all_features.py is available.[/red]")
        except Exception as e:
            self.console.print(f"[red]Demo error: {e}[/red]")
            self.logger.error(f"Demo execution error: {e}")
    
    def _interactive_config(self):
        """Interactive configuration management"""
        self.config_manager.show_config_menu()
    
    async def _comprehensive_analysis_workflow(self, topics: List[Dict], syllabus_title: str):
        """Enhanced comprehensive analysis workflow with resource saving"""
        if not topics:
            return
        
        self.console.print(Rule("[bold bright_green]Enhanced Resource Discovery[/bold bright_green]"))
        
        # Ask user if they want to find resources with direct links
        find_resources = Prompt.ask(
            "[bright_yellow]Find learning resources with direct links?[/bright_yellow]",
            choices=["yes", "no"],
            default="yes"
        )
        
        if find_resources == "yes":
            # Extract topic names for resource finding
            topic_names = [topic.get('name', '') for topic in topics if topic.get('name')]
            
            with self.console.status("[bright_cyan]Finding resources with direct links..."):
                # Find resources for all topics
                all_resources = await self.resource_finder.find_resources_for_syllabus(topic_names, 'both')
                
                # Use enhanced video search for comprehensive coverage
                youtube_resources = await self._enhanced_video_search_for_syllabus(syllabus_title, topic_names)
                
                # Combine resources
                combined_resources = self._combine_all_resources(all_resources, youtube_resources)
            
            if combined_resources:
                self.console.print(f"[bright_green]Found resources for {syllabus_title}![/bright_green]")
                
                # Display summary with enhanced video information
                self._display_resource_summary(combined_resources)
                
                # Show detailed video breakdown if enhanced search was used
                if 'study_order' in combined_resources:
                    self._display_enhanced_video_results(combined_resources)
                
                # Ask if user wants to save resources
                save_resources = Prompt.ask(
                    "[bright_yellow]Save these resources with direct links for future reference?[/bright_yellow]",
                    choices=["yes", "no"],
                    default="yes"
                )
                
                if save_resources == "yes":
                    # Save resources in multiple formats
                    saved_files = self.resource_manager.save_learning_resources(
                        syllabus_title, combined_resources, include_links=True
                    )
                    
                    self.console.print("[bright_green]Resources saved in multiple formats:[/bright_green]")
                    for format_type, file_path in saved_files.items():
                        self.console.print(f"  📄 {format_type.upper()}: {file_path}")
                    
                    self.console.print("\n[bright_cyan]💡 You can now:[/bright_cyan]")
                    self.console.print("  • Click links in the HTML file to go directly to resources")
                    self.console.print("  • Reference the text file anytime")
                    self.console.print("  • Import the CSV into spreadsheet apps")
                
                # Ask if user wants to create a quiz from these resources
                create_quiz = Prompt.ask(
                    "[bright_yellow]Create a quiz based on these resources?[/bright_yellow]",
                    choices=["yes", "no"],
                    default="yes"
                )
                
                if create_quiz == "yes":
                    await self._create_resource_based_quiz(syllabus_title, combined_resources)
    
    async def _find_youtube_resources_for_topics(self, topics: List[str]) -> Dict:
        """Find YouTube videos and playlists for topics"""
        youtube_resources = {'videos': [], 'playlists': []}
        
        for topic in topics[:2]:  # Limit to 2 topics for speed
            try:
                # Search for videos
                videos = await self.youtube_client.search_videos(topic, max_results=3)
                youtube_resources['videos'].extend(videos)
                
                # Search for playlists
                playlists = await self.youtube_client.search_playlists(topic, max_results=2)
                youtube_resources['playlists'].extend(playlists)
                
            except Exception as e:
                self.logger.error(f"Error finding YouTube resources for {topic}: {e}")
        
        return youtube_resources
    
    async def _enhanced_video_search_for_syllabus(self, syllabus_title: str, topic_names: List[str]) -> Dict:
        """Use enhanced video search for comprehensive syllabus coverage"""
        try:
            # Create syllabus text from topic names
            syllabus_text = f"{syllabus_title}. Topics: {', '.join(topic_names)}"
            
            # Use enhanced search
            search_results = await self.enhanced_video_search.comprehensive_topic_search(
                syllabus_text, max_videos_per_topic=4
            )
            
            # Convert to expected format
            youtube_resources = {
                'videos': search_results.get('comprehensive_videos', []),
                'playlists': [],  # Enhanced search focuses on videos
                'topic_coverage': search_results.get('topic_coverage', {}),
                'missing_topics': search_results.get('missing_topics', []),
                'study_order': search_results.get('recommended_study_order', []),
                'channel_diversity': search_results.get('channel_diversity', {})
            }
            
            self.logger.info(f"Enhanced search found {len(youtube_resources['videos'])} videos with {youtube_resources['channel_diversity'].get('total_channels', 0)} different channels")
            
            return youtube_resources
            
        except Exception as e:
            self.logger.error(f"Enhanced video search failed: {e}")
            # Fallback to original method
            return await self._find_youtube_resources_for_topics(topic_names[:3])
    
    def _combine_all_resources(self, general_resources: Dict, youtube_resources: Dict) -> Dict:
        """Combine general resources with YouTube resources"""
        combined = general_resources.copy()
        
        # Add YouTube videos
        if 'videos' not in combined:
            combined['videos'] = []
        combined['videos'].extend(youtube_resources.get('videos', []))
        
        # Add YouTube playlists
        if 'playlists' not in combined:
            combined['playlists'] = []
        combined['playlists'].extend(youtube_resources.get('playlists', []))
        
        return combined
    
    def _display_resource_summary(self, resources: Dict):
        """Display a summary of found resources with enhanced video information"""
        summary_table = Table(title="Resources Found", border_style="bright_green")
        summary_table.add_column("Type", style="bright_cyan")
        summary_table.add_column("Count", style="bright_white")
        summary_table.add_column("Examples", style="bright_yellow")
        
        # Only process actual resource lists, not metadata
        resource_types_to_display = ['videos', 'playlists', 'books', 'courses', 'free_resources', 'paid_resources']
        
        for resource_type, items in resources.items():
            if resource_type in resource_types_to_display and isinstance(items, list) and items:
                count = len(items)
                examples = []
                for item in items[:2]:
                    if isinstance(item, dict):
                        title = item.get('title', 'Unknown')
                    elif isinstance(item, str):
                        title = item
                    else:
                        title = str(item)
                    examples.append(title[:30] + "..." if len(title) > 30 else title)
                examples_str = ", ".join(examples)
                summary_table.add_row(resource_type.title(), str(count), examples_str)
        
        self.console.print(summary_table)
        
        # Show enhanced video information if available
        if 'channel_diversity' in resources:
            diversity = resources['channel_diversity']
            self.console.print(f"\n[bright_cyan]📺 Video Diversity:[/bright_cyan]")
            self.console.print(f"   Channels: {diversity.get('total_channels', 0)}")
            self.console.print(f"   Diversity Score: {diversity.get('diversity_score', 0):.2f}")
        
        if 'missing_topics' in resources and resources['missing_topics']:
            self.console.print(f"\n[bright_yellow]⚠️  Topics needing more coverage:[/bright_yellow]")
            for topic in resources['missing_topics'][:3]:
                self.console.print(f"   • {topic}")
        
        if 'topic_coverage' in resources:
            coverage = resources['topic_coverage']
            excellent_topics = [t for t, info in coverage.items() if info.get('coverage_quality') == 'Excellent']
            if excellent_topics:
                self.console.print(f"\n[bright_green]✅ Well-covered topics:[/bright_green]")
                for topic in excellent_topics[:3]:
                    self.console.print(f"   • {topic}")
    
    def _display_enhanced_video_results(self, resources: Dict):
        """Display enhanced video search results with study order and topic coverage"""
        if 'study_order' not in resources:
            return
        
        study_order = resources['study_order']
        if not study_order:
            return
        
        self.console.print(f"\n[bold bright_blue]📚 Recommended Study Order[/bold bright_blue]")
        
        study_table = Table(border_style="bright_blue")
        study_table.add_column("Order", style="bright_cyan", width=5)
        study_table.add_column("Video Title", style="bright_white", width=40)
        study_table.add_column("Channel", style="bright_green", width=20)
        study_table.add_column("Duration", style="bright_yellow", width=8)
        study_table.add_column("Views", style="bright_magenta", width=10)
        
        for i, video in enumerate(study_order[:8], 1):  # Show top 8 in study order
            title = video.get('title', 'Unknown')[:37] + "..." if len(video.get('title', '')) > 40 else video.get('title', 'Unknown')
            channel = video.get('channel', 'Unknown')[:17] + "..." if len(video.get('channel', '')) > 20 else video.get('channel', 'Unknown')
            duration = video.get('duration', 'Unknown')
            views = f"{video.get('view_count', 0):,}"
            
            study_table.add_row(str(i), title, channel, duration, views)
        
        self.console.print(study_table)
        
        # Show topic coverage breakdown
        if 'topic_coverage' in resources:
            self._display_topic_coverage_breakdown(resources['topic_coverage'])
    
    def _display_topic_coverage_breakdown(self, topic_coverage: Dict):
        """Display detailed topic coverage information"""
        if not topic_coverage:
            return
        
        self.console.print(f"\n[bold bright_green]📊 Topic Coverage Analysis[/bold bright_green]")
        
        coverage_table = Table(border_style="bright_green")
        coverage_table.add_column("Topic", style="bright_cyan", width=25)
        coverage_table.add_column("Videos", style="bright_white", width=8)
        coverage_table.add_column("Quality", style="bright_yellow", width=12)
        coverage_table.add_column("Best Video", style="bright_green", width=35)
        
        for topic, info in list(topic_coverage.items())[:6]:  # Show top 6 topics
            video_count = info.get('video_count', 0)
            quality = info.get('coverage_quality', 'Unknown')
            
            best_video = "No videos found"
            if info.get('videos'):
                best_video = info['videos'][0].get('title', 'Unknown')[:32] + "..." if len(info['videos'][0].get('title', '')) > 35 else info['videos'][0].get('title', 'Unknown')
            
            # Color code quality
            quality_color = {
                'Excellent': '[bright_green]Excellent[/bright_green]',
                'Good': '[bright_yellow]Good[/bright_yellow]',
                'Fair': '[bright_blue]Fair[/bright_blue]',
                'Limited': '[bright_red]Limited[/bright_red]',
                'No coverage': '[red]None[/red]'
            }.get(quality, quality)
            
            coverage_table.add_row(
                topic[:22] + "..." if len(topic) > 25 else topic,
                str(video_count),
                quality_color,
                best_video
            )
        
        self.console.print(coverage_table)
    
    async def _interactive_enhanced_videos(self):
        """Interactive enhanced video search with comprehensive topic coverage"""
        self.console.print(Rule("[bold bright_blue]Enhanced Video Search[/bold bright_blue]"))
        
        # Get input method
        input_choice = Prompt.ask(
            "[bright_yellow]How would you like to search for videos?[/bright_yellow]",
            choices=["syllabus", "topics"],
            default="topics"
        )
        
        if input_choice == "syllabus":
            # Get syllabus text
            self.console.print("[bright_cyan]Enter your syllabus content (press Enter twice when done):[/bright_cyan]")
            
            lines = []
            empty_lines = 0
            
            while empty_lines < 2:
                try:
                    line = input()
                    if line.strip() == "":
                        empty_lines += 1
                    else:
                        empty_lines = 0
                    lines.append(line)
                except KeyboardInterrupt:
                    self.console.print("\n[yellow]Input cancelled[/yellow]")
                    return
            
            syllabus_text = "\n".join(lines).strip()
            
            if not syllabus_text:
                self.console.print("[bright_red]No syllabus content provided[/bright_red]")
                return
            
            syllabus_title = Prompt.ask("[bright_cyan]Syllabus title/subject[/bright_cyan]", default="Course Syllabus")
            
        else:  # topics
            topic_input = Prompt.ask("[bright_cyan]Enter topics (comma-separated)[/bright_cyan]")
            if not topic_input:
                self.console.print("[bright_red]No topics provided[/bright_red]")
                return
            
            topics = [t.strip() for t in topic_input.split(',')]
            syllabus_title = Prompt.ask("[bright_cyan]Subject name[/bright_cyan]", default="Study Topics")
            syllabus_text = f"{syllabus_title}. Topics: {', '.join(topics)}"
        
        try:
            with self.console.status("[bright_cyan]Performing comprehensive video search..."):
                # Use enhanced video search
                search_results = await self.enhanced_video_search.comprehensive_topic_search(
                    syllabus_text, max_videos_per_topic=4
                )
            
            if not search_results.get('comprehensive_videos'):
                self.console.print("[yellow]No videos found for the given topics[/yellow]")
                return
            
            # Display results
            videos = search_results['comprehensive_videos']
            self.console.print(f"[bright_green]Found {len(videos)} videos from {search_results.get('channel_diversity', {}).get('total_channels', 0)} different channels![/bright_green]")
            
            # Show enhanced results
            youtube_resources = {
                'videos': videos,
                'topic_coverage': search_results.get('topic_coverage', {}),
                'missing_topics': search_results.get('missing_topics', []),
                'study_order': search_results.get('recommended_study_order', []),
                'channel_diversity': search_results.get('channel_diversity', {})
            }
            
            self._display_resource_summary(youtube_resources)
            self._display_enhanced_video_results(youtube_resources)
            
            # Ask if user wants to save results
            save_results = Prompt.ask(
                "[bright_yellow]Save these video results for future reference?[/bright_yellow]",
                choices=["yes", "no"],
                default="yes"
            )
            
            if save_results == "yes":
                # Convert to resource format and save
                resource_format = {
                    'videos': videos,
                    'playlists': [],
                    'books': [],
                    'courses': []
                }
                
                saved_files = self.resource_manager.save_learning_resources(
                    syllabus_title, resource_format, include_links=True
                )
                
                self.console.print("[bright_green]Video results saved![/bright_green]")
                for format_type, file_path in saved_files.items():
                    self.console.print(f"  📄 {format_type.upper()}: {file_path}")
            
            # Ask if user wants to create a quiz
            create_quiz = Prompt.ask(
                "[bright_yellow]Create a quiz based on these videos?[/bright_yellow]",
                choices=["yes", "no"],
                default="no"
            )
            
            if create_quiz == "yes":
                await self._create_resource_based_quiz(syllabus_title, youtube_resources)
                
        except Exception as e:
            self.console.print(f"[red]Error during enhanced video search: {e}[/red]")
            self.logger.error(f"Enhanced video search error: {e}")
    
    async def _create_resource_based_quiz(self, topic: str, resources: Dict):
        """Create a quiz based on the found resources"""
        try:
            num_questions = int(Prompt.ask(
                "[bright_yellow]How many questions for the quiz?[/bright_yellow]",
                default="10"
            ))
            
            difficulty = Prompt.ask(
                "[bright_yellow]Quiz difficulty?[/bright_yellow]",
                choices=["easy", "medium", "hard", "mixed"],
                default="mixed"
            )
            
            with self.console.status("[bright_cyan]Creating quiz from your resources..."):
                quiz_data = await self.persistent_quiz_manager.create_quiz_from_resources(
                    topic, resources, num_questions, difficulty
                )
            
            if quiz_data:
                self.console.print(f"[bright_green]Created quiz: {quiz_data.get('title')}[/bright_green]")
                self.console.print(f"Questions: {quiz_data.get('total_questions', 0)}")
                self.console.print(f"Estimated time: {quiz_data.get('estimated_time', 0)} minutes")
                
                # Ask if user wants to take the quiz now
                take_now = Prompt.ask(
                    "[bright_yellow]Take the quiz now?[/bright_yellow]",
                    choices=["yes", "no"],
                    default="yes"
                )
                
                if take_now == "yes":
                    await self._take_persistent_quiz(quiz_data)
                else:
                    self.console.print("[bright_cyan]Quiz saved! You can take it later from 'Saved Quizzes' menu.[/bright_cyan]")
            
        except ValueError:
            self.console.print("[red]Please enter a valid number for questions[/red]")
        except Exception as e:
            self.console.print(f"[red]Error creating quiz: {e}[/red]")
    
    async def _interactive_enhanced_resources(self):
        """Enhanced interactive resource finder with direct links"""
        self.console.print(Rule("[bold bright_blue]Enhanced Resource Finder[/bold bright_blue]"))
        
        topic = Prompt.ask("[bright_cyan]What topic would you like to find resources for?[/bright_cyan]")
        
        if not topic:
            self.console.print("[red]Please enter a topic[/red]")
            return
        
        try:
            with self.console.status("[bright_cyan]Finding resources with direct links..."):
                # Find general resources
                general_resources = await self.resource_finder.find_resources_for_syllabus([topic], 'both')
                
                # Find YouTube resources
                youtube_resources = await self._find_youtube_resources_for_topics([topic])
                
                # Combine resources
                combined_resources = self._combine_all_resources(general_resources, youtube_resources)
            
            if combined_resources:
                self.console.print(f"[bright_green]Found resources for '{topic}'![/bright_green]")
                
                # Display resources
                self._display_resource_summary(combined_resources)
                
                # Show some direct links
                self._show_sample_direct_links(combined_resources)
                
                # Ask to save
                save_resources = Prompt.ask(
                    "[bright_yellow]Save these resources with direct links?[/bright_yellow]",
                    choices=["yes", "no"],
                    default="yes"
                )
                
                if save_resources == "yes":
                    saved_files = self.resource_manager.save_learning_resources(
                        topic, combined_resources, include_links=True
                    )
                    
                    self.console.print("[bright_green]Resources saved![/bright_green]")
                    for format_type, file_path in saved_files.items():
                        self.console.print(f"  📄 {format_type.upper()}: {file_path}")
                
                # Ask to create quiz
                create_quiz = Prompt.ask(
                    "[bright_yellow]Create a quiz from these resources?[/bright_yellow]",
                    choices=["yes", "no"],
                    default="no"
                )
                
                if create_quiz == "yes":
                    await self._create_resource_based_quiz(topic, combined_resources)
            else:
                self.console.print("[yellow]No resources found for this topic[/yellow]")
                
        except Exception as e:
            self.console.print(f"[red]Error finding resources: {e}[/red]")
    
    def _show_sample_direct_links(self, resources: Dict):
        """Show sample direct links to demonstrate the feature"""
        self.console.print("\n[bright_cyan]📎 Sample Direct Links:[/bright_cyan]")
        
        # Show video links
        if 'videos' in resources and resources['videos']:
            video = resources['videos'][0]
            if isinstance(video, dict) and 'direct_link' in video:
                title = video.get('title', 'Video')[:40]
                self.console.print(f"🎥 {title}...")
                self.console.print(f"   🔗 {video['direct_link']}")
        
        # Show playlist links
        if 'playlists' in resources and resources['playlists']:
            playlist = resources['playlists'][0]
            if isinstance(playlist, dict) and 'direct_link' in playlist:
                title = playlist.get('title', 'Playlist')[:40]
                self.console.print(f"📚 {title}...")
                self.console.print(f"   🔗 {playlist['direct_link']}")
        
        self.console.print("[dim]All links will be saved in the files for easy access![/dim]\n")
    
    async def _interactive_saved_resources(self):
        """Interactive management of saved resources"""
        self.console.print(Rule("[bold bright_blue]Saved Resources[/bold bright_blue]"))
        
        # Get saved resources
        saved_resources = self.resource_manager.get_saved_resources()
        
        if not saved_resources:
            self.console.print("[yellow]No saved resources found[/yellow]")
            return
        
        # Display saved resources
        resources_table = Table(title="Your Saved Resources", border_style="bright_green")
        resources_table.add_column("ID", style="bright_cyan", width=3)
        resources_table.add_column("Topic", style="bright_white")
        resources_table.add_column("Generated", style="bright_yellow")
        resources_table.add_column("Resources", style="bright_green")
        
        for i, resource in enumerate(saved_resources, 1):
            generated_date = resource.get('generated_at', '')[:10]  # Just date part
            resources_table.add_row(
                str(i),
                resource.get('topic', 'Unknown'),
                generated_date,
                str(resource.get('total_count', 0))
            )
        
        self.console.print(resources_table)
        
        # Ask what to do
        action = Prompt.ask(
            "[bright_yellow]What would you like to do?[/bright_yellow]",
            choices=["view", "create_quiz", "back"],
            default="view"
        )
        
        if action == "view":
            try:
                choice = int(Prompt.ask("[bright_yellow]Select resource ID to view[/bright_yellow]"))
                if 1 <= choice <= len(saved_resources):
                    selected = saved_resources[choice - 1]
                    resource_data = self.resource_manager.load_saved_resources(selected['file'])
                    
                    if resource_data:
                        self.console.print(f"\n[bright_green]Resources for: {resource_data.get('topic')}[/bright_green]")
                        self._display_resource_summary(resource_data.get('resources', {}))
                        
                        # Show file locations
                        self.console.print(f"\n[bright_cyan]Saved files:[/bright_cyan]")
                        base_name = selected['file'].replace('.json', '')
                        self.console.print(f"📄 Text: {base_name.replace('data/resources/', 'exports/')}.txt")
                        self.console.print(f"📊 CSV: {base_name.replace('data/resources/', 'exports/')}.csv")
                        self.console.print(f"🌐 HTML: {base_name.replace('data/resources/', 'exports/')}.html")
                else:
                    self.console.print("[red]Invalid selection[/red]")
            except ValueError:
                self.console.print("[red]Please enter a valid number[/red]")
        
        elif action == "create_quiz":
            try:
                choice = int(Prompt.ask("[bright_yellow]Select resource ID to create quiz from[/bright_yellow]"))
                if 1 <= choice <= len(saved_resources):
                    selected = saved_resources[choice - 1]
                    resource_data = self.resource_manager.load_saved_resources(selected['file'])
                    
                    if resource_data:
                        await self._create_resource_based_quiz(
                            resource_data.get('topic', 'Unknown'),
                            resource_data.get('resources', {})
                        )
                else:
                    self.console.print("[red]Invalid selection[/red]")
            except ValueError:
                self.console.print("[red]Please enter a valid number[/red]")
    
    async def _interactive_saved_quizzes(self):
        """Interactive management of saved quizzes"""
        self.console.print(Rule("[bold bright_blue]Saved Quizzes[/bold bright_blue]"))
        
        # Get saved quizzes
        saved_quizzes = self.persistent_quiz_manager.get_saved_quizzes()
        
        if not saved_quizzes:
            self.console.print("[yellow]No saved quizzes found[/yellow]")
            self.console.print("[bright_cyan]💡 Create quizzes from the main menu or when analyzing syllabi![/bright_cyan]")
            return
        
        # Display saved quizzes
        quizzes_table = Table(title="Your Saved Quizzes", border_style="bright_green")
        quizzes_table.add_column("ID", style="bright_cyan", width=3)
        quizzes_table.add_column("Title", style="bright_white")
        quizzes_table.add_column("Questions", style="bright_yellow", width=10)
        quizzes_table.add_column("Attempts", style="bright_green", width=10)
        quizzes_table.add_column("Best Score", style="bright_magenta", width=12)
        quizzes_table.add_column("Source", style="bright_blue", width=10)
        
        for i, quiz in enumerate(saved_quizzes, 1):
            quizzes_table.add_row(
                str(i),
                quiz.get('title', 'Unknown')[:30] + ("..." if len(quiz.get('title', '')) > 30 else ""),
                str(quiz.get('total_questions', 0)),
                str(quiz.get('attempts', 0)),
                f"{quiz.get('best_score', 0):.1f}%",
                quiz.get('source_type', 'unknown')
            )
        
        self.console.print(quizzes_table)
        
        # Ask what to do
        action = Prompt.ask(
            "[bright_yellow]What would you like to do?[/bright_yellow]",
            choices=["take", "stats", "delete", "back"],
            default="take"
        )
        
        if action == "take":
            await self._select_and_take_quiz(saved_quizzes)
        elif action == "stats":
            await self._show_quiz_statistics(saved_quizzes)
        elif action == "delete":
            await self._delete_quiz(saved_quizzes)
    
    async def _select_and_take_quiz(self, saved_quizzes: List[Dict]):
        """Select and take a saved quiz"""
        try:
            choice = int(Prompt.ask("[bright_yellow]Select quiz ID to take[/bright_yellow]"))
            if 1 <= choice <= len(saved_quizzes):
                selected_quiz = saved_quizzes[choice - 1]
                quiz_data = self.persistent_quiz_manager.load_quiz(selected_quiz['id'])
                
                if quiz_data:
                    await self._take_persistent_quiz(quiz_data)
                else:
                    self.console.print("[red]Error loading quiz[/red]")
            else:
                self.console.print("[red]Invalid selection[/red]")
        except ValueError:
            self.console.print("[red]Please enter a valid number[/red]")
    
    async def _take_persistent_quiz(self, quiz_data: Dict):
        """Take a persistent quiz and save results"""
        self.console.print(f"\n[bold bright_green]Quiz: {quiz_data.get('title', 'Unknown Quiz')}[/bold bright_green]")
        self.console.print(f"Questions: {quiz_data.get('total_questions', 0)}")
        self.console.print(f"Estimated time: {quiz_data.get('estimated_time', 0)} minutes")
        
        if quiz_data.get('source_resources'):
            self.console.print("[bright_cyan]📚 Based on your saved learning resources[/bright_cyan]")
        
        questions = quiz_data.get('questions', [])
        if not questions:
            self.console.print("[yellow]No questions available[/yellow]")
            return
        
        score = 0
        total = len(questions)
        answers = []
        start_time = datetime.now()
        
        for i, question in enumerate(questions, 1):
            self.console.print(f"\n[bold bright_cyan]Question {i}/{total}:[/bold bright_cyan]")
            self.console.print(question.get('question', ''))
            
            question_type = question.get('type', 'multiple_choice')
            user_answer = None
            is_correct = False
            
            if question_type == 'multiple_choice':
                options = question.get('options', [])
                if options:
                    for j, option in enumerate(options, 1):
                        self.console.print(f"  {j}. {option}")
                    
                    try:
                        answer = int(Prompt.ask("[bright_yellow]Your answer[/bright_yellow]"))
                        user_answer = answer
                        correct_index = question.get('correct_answer', 0)
                        
                        if isinstance(correct_index, str):
                            # If correct_answer is the actual text, find its index
                            try:
                                correct_index = options.index(correct_index)
                            except ValueError:
                                correct_index = 0
                        
                        correct_display = correct_index + 1
                        
                        if answer == correct_display:
                            self.console.print("[bright_green]✓ Correct![/bright_green]")
                            is_correct = True
                        else:
                            correct_option = options[correct_index] if correct_index < len(options) else "Unknown"
                            self.console.print(f"[bright_red]✗ Incorrect. The correct answer was {correct_display}: {correct_option}[/bright_red]")
                            
                    except ValueError:
                        self.console.print("[red]Invalid answer[/red]")
                        user_answer = "invalid"
                        
            elif question_type == 'true_false':
                answer = Prompt.ask("[bright_yellow]True or False (T/F)[/bright_yellow]").upper().strip()
                user_answer = answer
                correct_answer = question.get('correct_answer', True)
                
                if (answer == 'T' and correct_answer) or (answer == 'F' and not correct_answer):
                    self.console.print("[bright_green]✓ Correct![/bright_green]")
                    is_correct = True
                else:
                    correct_text = "True" if correct_answer else "False"
                    self.console.print(f"[bright_red]✗ Incorrect. The correct answer was {correct_text}[/bright_red]")
                    
            elif question_type == 'short_answer':
                answer = Prompt.ask("[bright_yellow]Your answer[/bright_yellow]").strip()
                user_answer = answer
                correct_answer = question.get('correct_answer', '')
                
                if self._check_short_answer_match(answer, correct_answer):
                    self.console.print("[bright_green]✓ Correct![/bright_green]")
                    is_correct = True
                else:
                    self.console.print(f"[bright_red]✗ Incorrect. Expected: {correct_answer}[/bright_red]")
            
            # Show explanation if available
            explanation = question.get('explanation', '')
            if explanation:
                self.console.print(f"[dim]💡 {explanation}[/dim]")
            
            # Show resource reference if available
            resource_ref = question.get('resource_reference', '')
            if resource_ref:
                self.console.print(f"[dim]📚 Related to: {resource_ref}[/dim]")
            
            if is_correct:
                score += 1
            
            # Save answer details
            answers.append({
                'question_number': i,
                'question': question.get('question', ''),
                'user_answer': user_answer,
                'correct_answer': question.get('correct_answer'),
                'is_correct': is_correct,
                'explanation': explanation
            })
        
        # Calculate time taken
        end_time = datetime.now()
        time_taken = int((end_time - start_time).total_seconds() / 60)
        
        # Show final score
        percentage = (score / total) * 100
        self.console.print(f"\n[bold bright_green]Quiz Complete![/bold bright_green]")
        self.console.print(f"Score: {score}/{total} ({percentage:.1f}%)")
        self.console.print(f"Time taken: {time_taken} minutes")
        
        # Save quiz attempt
        quiz_id = quiz_data.get('id')
        if quiz_id:
            success = self.persistent_quiz_manager.save_quiz_attempt(
                quiz_id, score, total, answers, time_taken
            )
            
            if success:
                self.console.print("[bright_green]📊 Results saved![/bright_green]")
                
                # Show improvement if this isn't the first attempt
                stats = self.persistent_quiz_manager.get_quiz_statistics(quiz_id)
                if stats and stats.get('total_attempts', 0) > 1:
                    trend = stats.get('improvement_trend', '')
                    if trend == "Improving":
                        self.console.print("[bright_green]📈 You're improving! Keep it up![/bright_green]")
                    elif trend == "Stable":
                        self.console.print("[bright_yellow]📊 Consistent performance[/bright_yellow]")
            else:
                self.console.print("[yellow]Could not save results[/yellow]")
    
    async def _show_quiz_statistics(self, saved_quizzes: List[Dict]):
        """Show detailed statistics for a quiz"""
        try:
            choice = int(Prompt.ask("[bright_yellow]Select quiz ID to view stats[/bright_yellow]"))
            if 1 <= choice <= len(saved_quizzes):
                selected_quiz = saved_quizzes[choice - 1]
                stats = self.persistent_quiz_manager.get_quiz_statistics(selected_quiz['id'])
                
                if stats:
                    self.console.print(f"\n[bold bright_green]Statistics: {stats.get('quiz_title')}[/bold bright_green]")
                    
                    stats_table = Table(border_style="bright_blue")
                    stats_table.add_column("Metric", style="bright_cyan")
                    stats_table.add_column("Value", style="bright_white")
                    
                    stats_table.add_row("Total Attempts", str(stats.get('total_attempts', 0)))
                    stats_table.add_row("Best Score", f"{stats.get('best_score', 0):.1f}%")
                    stats_table.add_row("Average Score", f"{stats.get('average_score', 0):.1f}%")
                    stats_table.add_row("Latest Score", f"{stats.get('latest_score', 0):.1f}%")
                    stats_table.add_row("Trend", stats.get('improvement_trend', 'Unknown'))
                    
                    self.console.print(stats_table)
                    
                    # Show recent attempts
                    recent_attempts = stats.get('attempts_history', [])
                    if recent_attempts:
                        self.console.print("\n[bright_cyan]Recent Attempts:[/bright_cyan]")
                        for attempt in recent_attempts[-3:]:
                            date = attempt.get('timestamp', '')[:10]
                            score = attempt.get('percentage', 0)
                            self.console.print(f"  📅 {date}: {score:.1f}%")
                else:
                    self.console.print("[red]Could not load statistics[/red]")
            else:
                self.console.print("[red]Invalid selection[/red]")
        except ValueError:
            self.console.print("[red]Please enter a valid number[/red]")
    
    async def _delete_quiz(self, saved_quizzes: List[Dict]):
        """Delete a saved quiz"""
        try:
            choice = int(Prompt.ask("[bright_yellow]Select quiz ID to delete[/bright_yellow]"))
            if 1 <= choice <= len(saved_quizzes):
                selected_quiz = saved_quizzes[choice - 1]
                
                # Confirm deletion
                confirm = Prompt.ask(
                    f"[bright_red]Delete quiz '{selected_quiz.get('title', 'Unknown')}'? This cannot be undone.[/bright_red]",
                    choices=["yes", "no"],
                    default="no"
                )
                
                if confirm == "yes":
                    success = self.persistent_quiz_manager.delete_quiz(selected_quiz['id'])
                    if success:
                        self.console.print("[bright_green]Quiz deleted successfully[/bright_green]")
                    else:
                        self.console.print("[red]Error deleting quiz[/red]")
                else:
                    self.console.print("[yellow]Deletion cancelled[/yellow]")
            else:
                self.console.print("[red]Invalid selection[/red]")
        except ValueError:
            self.console.print("[red]Please enter a valid number[/red]")
    
    async def _interactive_ai_learning(self):
        """Interactive AI-powered learning paths"""
        self.console.print(Rule("[bold bright_blue]AI Learning Paths[/bold bright_blue]"))
        
        action = Prompt.ask(
            "[bright_yellow]What would you like to do?[/bright_yellow]",
            choices=["create_profile", "generate_path", "next_activity", "view_analytics"],
            default="create_profile"
        )
        
        user_id = Prompt.ask("[bright_cyan]Enter your user ID[/bright_cyan]", default="default_user")
        
        try:
            if action == "create_profile":
                await self._create_learning_profile(user_id)
            elif action == "generate_path":
                await self._generate_learning_path(user_id)
            elif action == "next_activity":
                await self._get_next_learning_activity(user_id)
            elif action == "view_analytics":
                await self._view_learning_analytics(user_id)
                
        except Exception as e:
            self.console.print(f"[red]Error: {e}[/red]")
    
    async def _interactive_adaptive_quiz(self):
        """Interactive adaptive quiz system"""
        self.console.print(Rule("[bold bright_blue]Adaptive Quiz System[/bold bright_blue]"))
        
        action = Prompt.ask(
            "[bright_yellow]What would you like to do?[/bright_yellow]",
            choices=["start_quiz", "view_mastery", "continue_session"],
            default="start_quiz"
        )
        
        user_id = Prompt.ask("[bright_cyan]Enter your user ID[/bright_cyan]", default="default_user")
        
        try:
            if action == "start_quiz":
                await self._start_adaptive_quiz(user_id)
            elif action == "view_mastery":
                await self._view_concept_mastery(user_id)
            elif action == "continue_session":
                await self._continue_quiz_session(user_id)
                
        except Exception as e:
            self.console.print(f"[red]Error: {e}[/red]")
    
    async def _interactive_learning_analytics(self):
        """Interactive learning analytics dashboard"""
        self.console.print(Rule("[bold bright_blue]Learning Analytics Dashboard[/bold bright_blue]"))
        
        action = Prompt.ask(
            "[bright_yellow]What would you like to view?[/bright_yellow]",
            choices=["dashboard", "insights", "patterns"],
            default="dashboard"
        )
        
        user_id = Prompt.ask("[bright_cyan]Enter your user ID[/bright_cyan]", default="default_user")
        
        try:
            if action == "dashboard":
                self.learning_analytics.show_comprehensive_dashboard(user_id)
                input("\nPress Enter to continue...")
            elif action == "insights":
                await self._show_learning_insights(user_id)
            elif action == "patterns":
                await self._show_study_patterns(user_id)
                
        except Exception as e:
            self.console.print(f"[red]Error: {e}[/red]")
    
    async def _interactive_predictions(self):
        """Interactive learning predictions"""
        self.console.print(Rule("[bold bright_blue]Learning Predictions[/bold bright_blue]"))
        
        action = Prompt.ask(
            "[bright_yellow]What would you like to predict?[/bright_yellow]",
            choices=["performance", "time", "success", "insights"],
            default="performance"
        )
        
        user_id = Prompt.ask("[bright_cyan]Enter your user ID[/bright_cyan]", default="default_user")
        
        try:
            if action == "performance":
                await self._predict_performance(user_id)
            elif action == "time":
                await self._predict_learning_time(user_id)
            elif action == "success":
                await self._predict_success(user_id)
            elif action == "insights":
                await self._show_prediction_insights(user_id)
                
        except Exception as e:
            self.console.print(f"[red]Error: {e}[/red]")
    
    # Helper methods for AI learning features
    async def _create_learning_profile(self, user_id: str):
        """Create a learning profile for the user"""
        try:
            profile_data = {
                'learning_style': Prompt.ask("[bright_cyan]Learning style[/bright_cyan]", 
                                           choices=["visual", "auditory", "kinesthetic", "reading"], 
                                           default="visual"),
                'experience_level': Prompt.ask("[bright_cyan]Experience level[/bright_cyan]", 
                                             choices=["beginner", "intermediate", "advanced"], 
                                             default="beginner"),
                'goals': [Prompt.ask("[bright_cyan]Primary learning goal[/bright_cyan]", default="general learning")],
                'time_availability': int(Prompt.ask("[bright_cyan]Daily study time (minutes)[/bright_cyan]", default="30"))
            }
            
            profile = await self.ai_learning_engine.create_learning_profile(user_id, profile_data)
            self.console.print(f"[bright_green]✅ Learning profile created for {user_id}[/bright_green]")
            
        except Exception as e:
            self.console.print(f"[red]Error creating profile: {e}[/red]")
    
    async def _generate_learning_path(self, user_id: str):
        """Generate an adaptive learning path"""
        try:
            subject = Prompt.ask("[bright_cyan]Subject[/bright_cyan]", default="Python Programming")
            topics_input = Prompt.ask("[bright_cyan]Topics (comma-separated)[/bright_cyan]", 
                                    default="variables,functions,loops,data structures")
            topics = [t.strip() for t in topics_input.split(',')]
            
            path = await self.ai_learning_engine.generate_adaptive_learning_path(user_id, subject, topics)
            self.console.print(f"[bright_green]✅ Learning path generated with {len(path.activities) if hasattr(path, 'activities') else 0} activities[/bright_green]")
            
        except Exception as e:
            self.console.print(f"[red]Error generating path: {e}[/red]")
    
    async def _get_next_learning_activity(self, user_id: str):
        """Get the next recommended learning activity"""
        try:
            activity = await self.ai_learning_engine.get_next_learning_activity(user_id)
            if activity:
                self.console.print(f"[bright_green]Next activity: {activity.title}[/bright_green]")
                self.console.print(f"[dim]{activity.description}[/dim]")
            else:
                self.console.print("[yellow]No activities available. Create a learning path first.[/yellow]")
                
        except Exception as e:
            self.console.print(f"[red]Error getting activity: {e}[/red]")
    
    async def _view_learning_analytics(self, user_id: str):
        """View learning analytics for the user"""
        try:
            self.learning_analytics.show_comprehensive_dashboard(user_id)
        except Exception as e:
            self.console.print(f"[red]Error showing analytics: {e}[/red]")
    
    async def _start_adaptive_quiz(self, user_id: str):
        """Start an adaptive quiz session"""
        try:
            concept_name = Prompt.ask("[bright_cyan]Concept to quiz on[/bright_cyan]", default="Python Basics")
            concept_id = concept_name.lower().replace(' ', '_')
            
            session_id = await self.adaptive_quiz_engine.start_adaptive_quiz_session(
                user_id, concept_id, concept_name, f"Quiz on {concept_name}"
            )
            self.console.print(f"[bright_green]✅ Quiz session started: {session_id}[/bright_green]")
            
            # Run the quiz loop
            await self._run_quiz_session(session_id)
            
        except Exception as e:
            self.console.print(f"[red]Error starting quiz: {e}[/red]")
    
    async def _run_quiz_session(self, session_id: str):
        """Run an interactive quiz session"""
        try:
            question_count = 0
            max_questions = 10
            
            self.console.print("\n[bold bright_blue]Starting Quiz...[/bold bright_blue]")
            
            while question_count < max_questions:
                # Get next question
                question_data = self.adaptive_quiz_engine.get_next_question(session_id)
                
                if not question_data:
                    self.console.print("[yellow]Quiz completed![/yellow]")
                    break
                
                question_count += 1
                
                # Display question
                self.console.print(f"\n[bold bright_cyan]Question {question_data['progress']['current']}/{question_data['progress']['total']}[/bold bright_cyan]")
                self.console.print(f"[bright_white]{question_data['question_text']}[/bright_white]")
                
                # Handle different question types
                if question_data['question_type'] == 'multiple_choice':
                    for i, option in enumerate(question_data['options']):
                        self.console.print(f"  {i + 1}. {option}")
                    
                    while True:
                        try:
                            answer_input = Prompt.ask("[bright_cyan]Your answer (1-4)[/bright_cyan]")
                            answer = int(answer_input) - 1
                            if 0 <= answer < len(question_data['options']):
                                break
                            else:
                                self.console.print("[red]Please enter a number between 1 and 4[/red]")
                        except ValueError:
                            self.console.print("[red]Please enter a valid number[/red]")
                
                elif question_data['question_type'] == 'true_false':
                    self.console.print("  1. True")
                    self.console.print("  2. False")
                    
                    while True:
                        try:
                            answer_input = Prompt.ask("[bright_cyan]Your answer (1-2)[/bright_cyan]")
                            answer = int(answer_input) - 1
                            if answer in [0, 1]:
                                break
                            else:
                                self.console.print("[red]Please enter 1 for True or 2 for False[/red]")
                        except ValueError:
                            self.console.print("[red]Please enter a valid number[/red]")
                
                elif question_data['question_type'] == 'short_answer':
                    answer = Prompt.ask("[bright_cyan]Your answer[/bright_cyan]")
                
                # Submit answer and get feedback
                import time
                start_time = time.time()
                result = await self.adaptive_quiz_engine.submit_answer(session_id, answer, int(time.time() - start_time))
                
                # Show feedback
                if result.get('is_correct'):
                    self.console.print("[bright_green]✅ Correct![/bright_green]")
                else:
                    self.console.print("[bright_red]❌ Incorrect[/bright_red]")
                    if question_data['question_type'] == 'multiple_choice':
                        correct_idx = result.get('correct_answer', 0)
                        if isinstance(correct_idx, int) and 0 <= correct_idx < len(question_data['options']):
                            self.console.print(f"[yellow]Correct answer: {question_data['options'][correct_idx]}[/yellow]")
                    else:
                        self.console.print(f"[yellow]Correct answer: {result.get('correct_answer', 'N/A')}[/yellow]")
                
                # Show explanation
                if result.get('explanation'):
                    self.console.print(f"[dim]{result['explanation']}[/dim]")
                
                # Check if quiz is completed
                if result.get('quiz_completed'):
                    final_results = result.get('final_results', {})
                    performance = final_results.get('performance', {})
                    
                    self.console.print("\n[bold bright_green]🎉 Quiz Completed![/bold bright_green]")
                    self.console.print(f"[bright_cyan]Final Score: {performance.get('final_score', 0):.1f}%[/bright_cyan]")
                    self.console.print(f"[bright_cyan]Accuracy: {performance.get('accuracy', 0):.1%}[/bright_cyan]")
                    self.console.print(f"[bright_cyan]Questions Answered: {performance.get('questions_answered', 0)}[/bright_cyan]")
                    break
                
                # Ask if user wants to continue
                if question_count < max_questions:
                    continue_quiz = Prompt.ask("\n[bright_cyan]Continue to next question? (y/n)[/bright_cyan]", default="y")
                    if continue_quiz.lower() != 'y':
                        break
            
        except Exception as e:
            self.console.print(f"[red]Error running quiz: {e}[/red]")

    async def _view_concept_mastery(self, user_id: str):
        """View concept mastery progress"""
        try:
            mastery_report = self.adaptive_quiz_engine.get_concept_mastery_report(user_id)
            if mastery_report and mastery_report.get('concepts'):
                self.console.print("[bright_green]Concept Mastery Progress:[/bright_green]")
                for concept_data in mastery_report['concepts']:
                    concept_name = concept_data.get('concept_name', 'Unknown')
                    mastery_level = concept_data.get('mastery_level', 0)
                    self.console.print(f"  {concept_name}: {mastery_level:.1%}")
            else:
                self.console.print("[yellow]No mastery data available yet.[/yellow]")
                
        except Exception as e:
            self.console.print(f"[red]Error viewing mastery: {e}[/red]")
    
    async def _continue_quiz_session(self, user_id: str):
        """Continue an existing quiz session"""
        try:
            # This would typically load an existing session
            self.console.print("[yellow]Continue quiz functionality not yet implemented.[/yellow]")
        except Exception as e:
            self.console.print(f"[red]Error continuing quiz: {e}[/red]")
    
    async def _show_learning_insights(self, user_id: str):
        """Show learning insights"""
        try:
            insights = await self.learning_analytics.generate_learning_insights(user_id)
            self.console.print("[bright_green]Learning Insights:[/bright_green]")
            for insight in insights:
                self.console.print(f"• {insight}")
        except Exception as e:
            self.console.print(f"[red]Error showing insights: {e}[/red]")
    
    async def _show_study_patterns(self, user_id: str):
        """Show study patterns analysis"""
        try:
            patterns = await self.learning_analytics.analyze_study_patterns(user_id)
            self.console.print("[bright_green]Study Patterns:[/bright_green]")
            self.console.print(f"• Best study time: {patterns.get('best_time', 'Unknown')}")
            self.console.print(f"• Average session length: {patterns.get('avg_session', 'Unknown')} minutes")
        except Exception as e:
            self.console.print(f"[red]Error showing patterns: {e}[/red]")
    
    async def _predict_performance(self, user_id: str):
        """Predict quiz performance"""
        try:
            concept_id = Prompt.ask("[bright_cyan]Concept ID[/bright_cyan]", default="python_basics")
            difficulty = float(Prompt.ask("[bright_cyan]Quiz difficulty (0.0-1.0)[/bright_cyan]", default="0.5"))
            
            prediction = await self.predictive_intelligence.predict_quiz_performance(user_id, concept_id, difficulty)
            self.console.print(f"[bright_green]Predicted performance: {prediction.predicted_value:.1%}[/bright_green]")
            self.console.print(f"[dim]Confidence: {prediction.confidence_score:.1%}[/dim]")
            
        except Exception as e:
            self.console.print(f"[red]Error predicting performance: {e}[/red]")
    
    async def _predict_learning_time(self, user_id: str):
        """Predict learning time"""
        try:
            concept_id = Prompt.ask("[bright_cyan]Concept ID[/bright_cyan]", default="python_basics")
            target_mastery = float(Prompt.ask("[bright_cyan]Target mastery (0.0-1.0)[/bright_cyan]", default="0.8"))
            
            prediction = await self.predictive_intelligence.predict_learning_time(user_id, concept_id, target_mastery)
            self.console.print(f"[bright_green]Estimated time: {prediction.predicted_value:.1f} hours[/bright_green]")
            
        except Exception as e:
            self.console.print(f"[red]Error predicting time: {e}[/red]")
    
    async def _predict_success(self, user_id: str):
        """Predict success probability"""
        try:
            concept_id = Prompt.ask("[bright_cyan]Concept ID[/bright_cyan]", default="python_basics")
            goal = Prompt.ask("[bright_cyan]Learning goal[/bright_cyan]", default="master the basics")
            
            prediction = await self.predictive_intelligence.predict_success_probability(user_id, concept_id, goal)
            self.console.print(f"[bright_green]Success probability: {prediction.predicted_value:.1%}[/bright_green]")
            
        except Exception as e:
            self.console.print(f"[red]Error predicting success: {e}[/red]")
    
    async def _show_prediction_insights(self, user_id: str):
        """Show prediction insights"""
        try:
            insights = await self.predictive_intelligence.generate_prediction_insights(user_id)
            self.console.print("[bright_green]Prediction Insights:[/bright_green]")
            for insight in insights:
                self.console.print(f"• {insight}")
        except Exception as e:
            self.console.print(f"[red]Error showing prediction insights: {e}[/red]")

async def main():
    """Main application entry point"""
    
    # Check for first-run setup
    from src.setup_manager import SetupManager
    setup_manager = SetupManager()
    
    if setup_manager.is_first_run():
        setup_success = await setup_manager.run_first_time_setup()
        if not setup_success:
            print("Setup was cancelled. You can run Syllabo again to retry setup.")
            return
        
        # Reload environment after setup
        from dotenv import load_dotenv
        load_dotenv(override=True)
    
    # If no arguments provided, go directly to interactive mode
    if len(sys.argv) == 1:
        app = SyllaboMain()
        app.print_banner()
        
        # Interactive menu loop
        while True:
            command = app.show_interactive_menu()
            
            if command == 'exit':
                app.console.print(Panel(
                    "[bold bright_cyan]Thank you for using Syllabo![/bold bright_cyan]\n[dim]Keep learning and growing![/dim]",
                    border_style="bright_cyan",
                    title="[bold bright_white]Goodbye[/bold bright_white]"
                ))
                break
            elif command == 'help':
                from src.cli.commands import create_parser
                parser = create_parser()
                app.console.print(Rule("[bold bright_yellow]Available Commands[/bold bright_yellow]"))
                parser.print_help()
                Prompt.ask("\n[dim]Press Enter to continue[/dim]", default="")
            else:
                await app._handle_interactive_command(command)
                Prompt.ask("\n[dim]Press Enter to continue[/dim]", default="")
                app.console.clear()
                app.print_banner()
        return
    
    # Handle command line arguments
    from src.cli.commands import create_parser
    parser = create_parser()
    args = parser.parse_args()
    app = SyllaboMain()
    
    try:
        # Handle different commands
        if args.command == 'analyze':
            await app._handle_analyze_command(args)
        elif args.command == 'search':
            await app._handle_search_command(args)
        elif args.command == 'review':
            await app._handle_review_command(args)
        elif args.command == 'goals':
            await app._handle_goals_command(args)
        elif args.command == 'quiz':
            await app._handle_quiz_command(args)
        elif args.command == 'progress':
            await app._handle_progress_command(args)
        elif args.command == 'session':
            await app._handle_session_command(args)
        elif args.command == 'bookmarks':
            await app._handle_bookmarks_command(args)
        elif args.command == 'platforms':
            await app._handle_platforms_command(args)
        elif args.command == 'config':
            await app._handle_config_command(args)
        elif args.command == 'interactive':
            # Interactive mode
            while True:
                try:
                    app.print_banner()
                    command = app.show_interactive_menu()
                    
                    if command == 'exit':
                        app.console.print("[bright_green]Thanks for using Syllabo![/bright_green]")
                        break
                    elif command == 'help':
                        app._show_help()
                        Prompt.ask("\n[dim]Press Enter to continue[/dim]", default="")
                    else:
                        await app._handle_interactive_command(command)
                        Prompt.ask("\n[dim]Press Enter to continue[/dim]", default="")
                        app.console.clear()
                except KeyboardInterrupt:
                    app.console.print("\n[bright_green]Thanks for using Syllabo![/bright_green]")
                    break
        else:
            parser.print_help()
    
    except KeyboardInterrupt:
        print("\nOperation cancelled by user")
    except Exception as e:
        print(f"ERROR: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main())
