#!/usr/bin/env python3
"""
Complete Features Demo for Syllabo App
Comprehensive demonstration of all features for users testing the application
"""

import asyncio
import os
import sys
import time
import tempfile
import shutil
from datetime import datetime, timedelta
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.rule import Rule
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TimeElapsedColumn
from rich.text import Text
from rich.align import Align
from rich.prompt import Prompt, Confirm

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

class DemoAIClient:
    """Mock AI client for demo purposes with realistic responses"""
    
    async def generate_response(self, prompt: str) -> str:
        """Generate realistic demo responses"""
        await asyncio.sleep(0.5)  # Simulate API call delay
        
        if "learning style" in prompt.lower():
            return "visual"
        elif "quiz" in prompt.lower() or "questions" in prompt.lower():
            return '''
            {
                "title": "Python Fundamentals Quiz",
                "description": "Basic Python programming concepts",
                "questions": [
                    {
                        "question": "What keyword is used to define a function in Python?",
                        "type": "multiple_choice",
                        "options": ["def", "function", "define", "func"],
                        "correct_answer": 0,
                        "explanation": "The 'def' keyword is used to define functions in Python"
                    },
                    {
                        "question": "Python is an interpreted language",
                        "type": "true_false", 
                        "correct_answer": true,
                        "explanation": "Python code is executed line by line by the Python interpreter"
                    },
                    {
                        "question": "What does 'print()' function do?",
                        "type": "short_answer",
                        "correct_answer": "displays output",
                        "explanation": "The print() function outputs text to the console"
                    }
                ]
            }
            '''
        elif "topics" in prompt.lower() or "syllabus" in prompt.lower():
            return '''
            [
                {
                    "name": "Python Basics",
                    "description": "Introduction to Python programming language, variables, and data types"
                },
                {
                    "name": "Control Structures", 
                    "description": "Conditional statements, loops, and flow control in Python"
                },
                {
                    "name": "Functions",
                    "description": "Defining and using functions, parameters, and return values"
                },
                {
                    "name": "Data Structures",
                    "description": "Lists, dictionaries, tuples, and sets in Python"
                },
                {
                    "name": "Object-Oriented Programming",
                    "description": "Classes, objects, inheritance, and encapsulation"
                }
            ]
            '''
        elif "notes" in prompt.lower():
            return '''
            {
                "notes": [
                    "Python is a high-level, interpreted programming language",
                    "Variables in Python don't need explicit type declaration",
                    "Python uses indentation to define code blocks",
                    "Functions are defined using the 'def' keyword",
                    "Python has extensive built-in libraries"
                ],
                "questions": [
                    "What makes Python different from compiled languages?",
                    "How does Python handle variable types?",
                    "What is the significance of indentation in Python?",
                    "How do you create reusable code blocks in Python?"
                ],
                "key_concepts": [
                    "Interpreted Language",
                    "Dynamic Typing",
                    "Indentation-based Syntax",
                    "Functions and Modules",
                    "Built-in Data Types"
                ]
            }
            '''
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
                        "related_concepts": ["control_structures"],
                        "estimated_time": 60,
                        "mastery_threshold": 0.8
                    },
                    {
                        "concept_id": "control_structures",
                        "name": "Control Structures",
                        "description": "If statements, loops, and conditional logic",
                        "difficulty_level": 0.5,
                        "prerequisites": ["python_basics"],
                        "related_concepts": ["functions"],
                        "estimated_time": 90,
                        "mastery_threshold": 0.8
                    }
                ]
            }
            '''
        else:
            return "Demo AI response for comprehensive feature testing"

class ComprehensiveFeaturesDemo:
    """Complete demonstration of all Syllabo features"""
    
    def __init__(self):
        self.console = Console()
        self.temp_dir = None
        self.demo_user_id = "demo_user"
        self.demo_data = {}
        
        # Feature categories for organized demo
        self.feature_categories = {
            "Core Learning": [
                ("syllabus_analysis", "Syllabus Analysis & Topic Extraction"),
                ("quiz_generation", "Interactive Quiz Generation"),
                ("progress_tracking", "Progress Dashboard & Analytics")
            ],
            "Content Discovery": [
                ("video_search", "Smart Video Search & Analysis"),
                ("resource_finder", "Learning Resource Discovery"),
                ("platform_integration", "Multi-Platform Search")
            ],
            "Study Tools": [
                ("note_generation", "AI-Powered Note Generation"),
                ("bookmark_management", "Smart Bookmarks & Annotations"),
                ("study_sessions", "Pomodoro Study Sessions"),
                ("spaced_repetition", "Spaced Repetition System")
            ],
            "AI Features": [
                ("adaptive_learning", "AI Learning Path Generation"),
                ("adaptive_quizzes", "Intelligent Adaptive Quizzes"),
                ("learning_analytics", "Advanced Learning Analytics"),
                ("predictions", "Learning Outcome Predictions")
            ],
            "Management": [
                ("goal_setting", "Study Goals & Milestones"),
                ("data_export", "Data Export & Backup"),
                ("configuration", "Settings & API Configuration")
            ]
        }
    
    def setup_demo_environment(self):
        """Setup demo environment with mock data"""
        self.temp_dir = tempfile.mkdtemp(prefix="syllabo_demo_")
        
        # Initialize main application
        from main import SyllaboMain
        self.app = SyllaboMain()
        
        # Replace AI client with demo client
        self.demo_ai_client = DemoAIClient()
        self.app.ai_client = self.demo_ai_client
        
        # Update AI clients in all components
        if hasattr(self.app, 'ai_learning_engine'):
            self.app.ai_learning_engine.ai_client = self.demo_ai_client
        if hasattr(self.app, 'adaptive_quiz_engine'):
            self.app.adaptive_quiz_engine.ai_client = self.demo_ai_client
        if hasattr(self.app, 'learning_analytics'):
            self.app.learning_analytics.ai_client = self.demo_ai_client
        if hasattr(self.app, 'predictive_intelligence'):
            self.app.predictive_intelligence.ai_client = self.demo_ai_client
        
        # Setup demo data
        self.setup_demo_data()
    
    def setup_demo_data(self):
        """Setup comprehensive realistic demo data"""
        self.demo_data = {
            'sample_syllabus': '''
            Course: Introduction to Python Programming
            
            Week 1-2: Python Basics
            - Installation and setup
            - Variables and data types
            - Basic input/output operations
            
            Week 3-4: Control Structures
            - Conditional statements (if, elif, else)
            - Loops (for, while)
            - Break and continue statements
            
            Week 5-6: Functions and Modules
            - Function definition and calling
            - Parameters and return values
            - Scope and local vs global variables
            - Importing and using modules
            
            Week 7-8: Data Structures
            - Lists, tuples, and sets
            - Dictionaries and their methods
            - List comprehensions
            
            Week 9-10: Object-Oriented Programming
            - Classes and objects
            - Inheritance and polymorphism
            - Encapsulation and abstraction
            
            Week 11-12: File Handling and Error Management
            - Reading and writing files
            - Exception handling
            - Working with CSV and JSON files
            ''',
            'sample_topics': [
                {'name': 'Python Installation', 'description': 'Setting up Python environment and IDE'},
                {'name': 'Variables and Data Types', 'description': 'Understanding Python data types and variable assignment'},
                {'name': 'Control Flow', 'description': 'Conditional statements and loops in Python'},
                {'name': 'Functions', 'description': 'Creating reusable code blocks with functions'},
                {'name': 'Data Structures', 'description': 'Lists, dictionaries, tuples, and sets'},
                {'name': 'Object-Oriented Programming', 'description': 'Classes, objects, inheritance, and polymorphism'},
                {'name': 'File Handling', 'description': 'Reading from and writing to files'},
                {'name': 'Error Handling', 'description': 'Exception handling and debugging'},
                {'name': 'Modules and Packages', 'description': 'Importing and creating Python modules'}
            ],
            'sample_quiz_questions': [
                {
                    'question': 'What keyword is used to define a function in Python?',
                    'type': 'multiple_choice',
                    'options': ['def', 'function', 'define', 'func'],
                    'correct_answer': 0,
                    'explanation': "The 'def' keyword is used to define functions in Python"
                },
                {
                    'question': 'Python is an interpreted language',
                    'type': 'true_false',
                    'correct_answer': True,
                    'explanation': 'Python code is executed line by line by the Python interpreter'
                },
                {
                    'question': 'What method is used to add an item to the end of a list?',
                    'type': 'short_answer',
                    'correct_answer': 'append',
                    'explanation': 'The append() method adds a single item to the end of a list'
                },
                {
                    'question': 'Which data type is mutable in Python?',
                    'type': 'multiple_choice',
                    'options': ['tuple', 'string', 'list', 'integer'],
                    'correct_answer': 2,
                    'explanation': 'Lists are mutable, meaning they can be changed after creation'
                }
            ],
            'sample_resources': [
                {'title': 'Python Official Documentation', 'type': 'documentation', 'url': 'https://docs.python.org/', 'rating': '4.9★', 'price': 'Free'},
                {'title': 'Automate the Boring Stuff with Python', 'type': 'book', 'url': 'https://automatetheboringstuff.com/', 'author': 'Al Sweigart', 'rating': '4.8★', 'price': 'Free/Paid'},
                {'title': 'Python Crash Course', 'type': 'book', 'author': 'Eric Matthes', 'rating': '4.7★', 'price': '$25-40'},
                {'title': 'Codecademy Python Course', 'type': 'course', 'url': 'https://codecademy.com/python', 'rating': '4.6★', 'price': '$15/month'},
                {'title': 'Real Python Tutorials', 'type': 'tutorial', 'url': 'https://realpython.com/', 'rating': '4.8★', 'price': 'Free/Premium'},
                {'title': 'Python for Everybody Specialization', 'type': 'course', 'provider': 'Coursera', 'rating': '4.7★', 'price': '$39-79/month'}
            ],
            'sample_videos': [
                {'title': 'Python Tutorial for Beginners - Learn Python in 6 Hours', 'channel': 'Programming with Mosh', 'duration': '6:14:07', 'views': '15M', 'rating': '4.9★', 'url': 'https://youtube.com/watch?v=kqtD5dpn9C8'},
                {'title': 'Complete Python Course from Beginner to Advanced', 'channel': 'Corey Schafer', 'duration': '4:26:52', 'views': '8.2M', 'rating': '4.8★', 'url': 'https://youtube.com/playlist?list=PL-osiE80TeTt2d9bfVyTiXJA-UTHn6WwU'},
                {'title': 'Python OOP Tutorial - Object Oriented Programming', 'channel': 'Tech With Tim', 'duration': '1:12:43', 'views': '2.1M', 'rating': '4.7★', 'url': 'https://youtube.com/watch?v=JeznW_7DlB0'},
                {'title': 'Python Data Structures and Algorithms', 'channel': 'CS Dojo', 'duration': '2:45:30', 'views': '1.8M', 'rating': '4.6★', 'url': 'https://youtube.com/watch?v=pkYVOmU3MgA'},
                {'title': 'Python Machine Learning Tutorial', 'channel': 'freeCodeCamp', 'duration': '5:12:18', 'views': '3.4M', 'rating': '4.8★', 'url': 'https://youtube.com/watch?v=7eh4d6sabA0'}
            ],
            'sample_bookmarks': [
                {'title': 'Python Variables Explained', 'url': 'https://youtube.com/watch?v=example1', 'timestamp': '5:23', 'notes': 'Important explanation of variable scoping', 'topic': 'Variables'},
                {'title': 'Function Parameters Deep Dive', 'url': 'https://youtube.com/watch?v=example2', 'timestamp': '12:45', 'notes': 'Great examples of *args and **kwargs', 'topic': 'Functions'},
                {'title': 'List Comprehensions Made Easy', 'url': 'https://youtube.com/watch?v=example3', 'timestamp': '8:16', 'notes': 'Concise syntax examples', 'topic': 'Data Structures'}
            ],
            'sample_study_sessions': [
                {'topic': 'Python Basics', 'duration': 45, 'date': '2024-08-14', 'focus_score': 8.5, 'completed': True},
                {'topic': 'Functions', 'duration': 60, 'date': '2024-08-15', 'focus_score': 9.2, 'completed': True},
                {'topic': 'OOP Concepts', 'duration': 30, 'date': '2024-08-16', 'focus_score': 7.8, 'completed': False}
            ],
            'sample_goals': [
                {'title': 'Master Python Basics', 'type': 'skill_mastery', 'target': 100, 'current': 73, 'unit': '%', 'deadline': '2024-09-01', 'status': 'In Progress'},
                {'title': 'Complete 5 Python Projects', 'type': 'project_completion', 'target': 5, 'current': 2, 'unit': 'projects', 'deadline': '2024-09-15', 'status': 'In Progress'},
                {'title': 'Study 30 minutes daily', 'type': 'daily_habit', 'target': 30, 'current': 25, 'unit': 'minutes', 'deadline': 'Ongoing', 'status': 'Active'},
                {'title': 'Achieve 90% Quiz Average', 'type': 'performance', 'target': 90, 'current': 87, 'unit': '%', 'deadline': '2024-08-31', 'status': 'Nearly Complete'}
            ],
            'sample_spaced_repetition': [
                {'topic': 'Python Syntax', 'mastery_level': 'Intermediate', 'next_review': 'Today', 'interval': '1 day', 'success_rate': '85%'},
                {'topic': 'Functions', 'mastery_level': 'Beginner', 'next_review': 'Tomorrow', 'interval': '2 days', 'success_rate': '72%'},
                {'topic': 'Data Types', 'mastery_level': 'Advanced', 'next_review': '3 days', 'interval': '7 days', 'success_rate': '94%'},
                {'topic': 'Control Flow', 'mastery_level': 'Mastered', 'next_review': '1 week', 'interval': '14 days', 'success_rate': '96%'},
                {'topic': 'OOP Concepts', 'mastery_level': 'Learning', 'next_review': 'Today', 'interval': '1 day', 'success_rate': '68%'}
            ],
            'sample_notes': [
                "Python is a high-level, interpreted programming language known for its simplicity and readability",
                "Variables in Python are dynamically typed - you don't need to declare their type explicitly",
                "Python uses indentation (usually 4 spaces) to define code blocks instead of curly braces",
                "Functions are defined using the 'def' keyword followed by the function name and parameters",
                "Python has extensive built-in libraries and a vast ecosystem of third-party packages",
                "List comprehensions provide a concise way to create lists based on existing lists",
                "Classes in Python define blueprints for creating objects with attributes and methods",
                "Exception handling in Python uses try, except, else, and finally blocks"
            ],
            'sample_analytics': {
                'study_time_per_week': 4.2,
                'quiz_performance': 87.3,
                'concept_mastery': 73,
                'learning_velocity': 2.1,
                'retention_rate': 91,
                'consistency_score': 0.85,
                'optimal_session_length': 45,
                'favorite_learning_time': '7:00 PM - 9:00 PM',
                'strongest_topics': ['Variables', 'Basic Syntax'],
                'improvement_areas': ['OOP Concepts', 'Error Handling']
            }
        }
    
    def cleanup_demo_environment(self):
        """Clean up demo environment"""
        if self.temp_dir and os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)
    
    def show_demo_banner(self):
        """Show main demo banner"""
        banner_text = Text()
        banner_text.append("SYLLABO", style="bold bright_cyan")
        banner_text.append(" - ", style="bright_white")
        banner_text.append("COMPLETE FEATURES DEMO", style="bold bright_green")
        banner_text.append("\n\n")
        banner_text.append("🎯 ", style="bright_yellow")
        banner_text.append("Experience all features of the AI-powered learning assistant", style="bright_white")
        banner_text.append("\n")
        banner_text.append("🚀 ", style="bright_blue")
        banner_text.append("From syllabus analysis to predictive learning intelligence", style="bright_white")
        banner_text.append("\n")
        banner_text.append("📚 ", style="bright_green")
        banner_text.append("Discover how AI can transform your learning experience", style="bright_white")
        
        banner_panel = Panel(
            Align.center(banner_text),
            border_style="bright_cyan",
            padding=(1, 2),
            title="[bold bright_blue]Welcome to Syllabo Demo[/bold bright_blue]",
            title_align="center"
        )
        
        self.console.print(banner_panel)
    
    def show_demo_menu(self):
        """Show interactive demo menu"""
        self.console.print(Rule("[bold bright_cyan]Demo Options[/bold bright_cyan]", style="bright_cyan"))
        
        self.console.print("[bright_white]Choose your demo experience:[/bright_white]\n")
        
        menu_table = Table(border_style="bright_blue", show_header=True, header_style="bold bright_magenta")
        menu_table.add_column("Option", style="bright_cyan", width=8, justify="center")
        menu_table.add_column("Demo Type", style="bright_green", width=25)
        menu_table.add_column("Description", style="bright_white", width=50)
        menu_table.add_column("Time", style="bright_yellow", width=10)
        
        menu_table.add_row("1", "🎯 Quick Demo", "Essential features overview (recommended for first-time users)", "~5 min")
        menu_table.add_row("2", "🔍 Category Demo", "Explore specific feature categories", "~3-8 min")
        menu_table.add_row("3", "🚀 Complete Demo", "All features with detailed explanations", "~15 min")
        menu_table.add_row("4", "🎮 Interactive Mode", "Try features with your own data", "Variable")
        menu_table.add_row("5", "📊 Feature Overview", "View all available features", "~2 min")
        menu_table.add_row("0", "🏠 Return to Main App", "Exit demo and return to main application", "")
        
        self.console.print(menu_table)
        self.console.print()
        
        choice = Prompt.ask(
            "[bold bright_yellow]Select demo option[/bold bright_yellow]",
            choices=["1", "2", "3", "4", "5", "0"],
            default="1"
        )
        
        return choice
    
    async def run_quick_demo(self):
        """Run essential features demo - perfect for first-time users"""
        self.console.print(Rule("[bold bright_green]🎯 Quick Demo - Essential Features[/bold bright_green]"))
        
        self.console.print("[bright_cyan]This quick demo showcases the core features that make Syllabo special![/bright_cyan]\n")
        
        essential_features = [
            ("Syllabus Analysis", self.demo_syllabus_analysis),
            ("AI Quiz Generation", self.demo_quiz_generation),
            ("Smart Video Search", self.demo_video_search),
            ("Learning Analytics", self.demo_learning_analytics),
            ("AI Learning Paths", self.demo_adaptive_learning)
        ]
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TimeElapsedColumn(),
            console=self.console
        ) as progress:
            
            for i, (feature_name, demo_func) in enumerate(essential_features, 1):
                task = progress.add_task(f"[bright_cyan]Demonstrating {feature_name}...", total=100)
                
                self.console.print(f"\n[bold bright_blue]📍 Feature {i}/5: {feature_name}[/bold bright_blue]")
                
                try:
                    progress.update(task, advance=20)
                    await demo_func(quick_mode=True)
                    progress.update(task, advance=80, description=f"[bright_green]✅ {feature_name} - Complete!")
                    
                    if i < len(essential_features):
                        self.console.print("[dim]Moving to next feature...[/dim]")
                        await asyncio.sleep(1)
                        
                except Exception as e:
                    progress.update(task, description=f"[bright_red]❌ {feature_name} - Error!")
                    self.console.print(f"[red]Demo error: {e}[/red]")
                
                progress.remove_task(task)
        
        self.show_quick_demo_summary()
    
    async def run_category_demo(self):
        """Run category-specific demo"""
        self.console.print(Rule("[bold bright_green]🔍 Category Demo[/bold bright_green]"))
        
        # Show categories
        category_table = Table(title="Feature Categories", border_style="bright_blue")
        category_table.add_column("Option", style="bright_cyan", width=8, justify="center")
        category_table.add_column("Category", style="bright_green", width=20)
        category_table.add_column("Features", style="bright_white", width=15)
        category_table.add_column("Description", style="bright_yellow", width=40)
        
        categories = list(self.feature_categories.keys())
        for i, category in enumerate(categories, 1):
            feature_count = len(self.feature_categories[category])
            if category == "Core Learning":
                desc = "Essential learning and assessment tools"
            elif category == "Content Discovery":
                desc = "Find videos, resources, and learning materials"
            elif category == "Study Tools":
                desc = "Study aids, notes, and session management"
            elif category == "AI Features":
                desc = "Advanced AI-powered learning features"
            else:  # Management
                desc = "Settings, goals, and data management"
            
            category_table.add_row(str(i), category, f"{feature_count} features", desc)
        
        self.console.print(category_table)
        
        choice = Prompt.ask(
            "[bright_yellow]Select category to demo[/bright_yellow]",
            choices=[str(i) for i in range(1, len(categories) + 1)],
            default="1"
        )
        
        selected_category = categories[int(choice) - 1]
        await self.demo_feature_category(selected_category)
    
    async def demo_feature_category(self, category_name: str):
        """Demo all features in a specific category"""
        self.console.print(f"\n[bold bright_blue]Demonstrating {category_name} Features[/bold bright_blue]")
        
        features = self.feature_categories[category_name]
        
        for i, (feature_key, feature_name) in enumerate(features, 1):
            self.console.print(f"\n[bold bright_cyan]🔸 {feature_name}[/bold bright_cyan]")
            
            try:
                if feature_key == "syllabus_analysis":
                    await self.demo_syllabus_analysis()
                elif feature_key == "quiz_generation":
                    await self.demo_quiz_generation()
                elif feature_key == "video_search":
                    await self.demo_video_search()
                elif feature_key == "adaptive_learning":
                    await self.demo_adaptive_learning()
                elif feature_key == "learning_analytics":
                    await self.demo_learning_analytics()
                elif feature_key == "note_generation":
                    await self.demo_note_generation()
                elif feature_key == "spaced_repetition":
                    await self.demo_spaced_repetition()
                elif feature_key == "goal_setting":
                    await self.demo_goal_setting()
                elif feature_key == "resource_finder":
                    await self.demo_resource_finder()
                else:
                    # Generic demo for other features
                    await self.demo_generic_feature(feature_name)
                
                self.console.print(f"[bright_green]✅ {feature_name} demonstrated successfully![/bright_green]")
                
            except Exception as e:
                self.console.print(f"[red]❌ Error demonstrating {feature_name}: {e}[/red]")
            
            if i < len(features):
                await asyncio.sleep(1)
    
    async def run_complete_demo(self):
        """Run comprehensive demo of all features"""
        self.console.print(Rule("[bold bright_green]🚀 Complete Demo - All Features[/bold bright_green]"))
        
        self.console.print("[bright_cyan]Comprehensive demonstration of every Syllabo feature![/bright_cyan]")
        self.console.print("[dim]Showcasing all capabilities with realistic sample data...[/dim]\n")
        
        # Demo all categories
        for category_name in self.feature_categories.keys():
            self.console.print(f"\n{'='*80}")
            self.console.print(f"[bold bright_magenta]📂 {category_name.upper()} FEATURES[/bold bright_magenta]")
            self.console.print(f"{'='*80}")
            
            await self.demo_feature_category(category_name)
            
            self.console.print(f"\n[bright_green]✅ {category_name} features completed![/bright_green]")
        
        self.show_complete_demo_summary()
    
    async def run_interactive_mode(self):
        """Run interactive mode where users can try features"""
        self.console.print(Rule("[bold bright_green]🎮 Interactive Mode[/bold bright_green]"))
        
        self.console.print("[bright_cyan]Try Syllabo features with your own data![/bright_cyan]\n")
        
        interactive_options = [
            ("1", "Upload and analyze your own syllabus"),
            ("2", "Generate quiz from your study material"),
            ("3", "Search for videos on your topic"),
            ("4", "Create personalized learning goals"),
            ("5", "Test spaced repetition with your topics"),
            ("0", "Return to demo menu")
        ]
        
        while True:
            self.console.print("[bright_white]Choose what you'd like to try:[/bright_white]")
            for option, description in interactive_options:
                self.console.print(f"  {option}. {description}")
            
            choice = Prompt.ask(
                "\n[bright_yellow]Your choice[/bright_yellow]",
                choices=[opt[0] for opt in interactive_options],
                default="0"
            )
            
            if choice == "0":
                break
            elif choice == "1":
                await self.interactive_syllabus_analysis()
            elif choice == "2":
                await self.interactive_quiz_generation()
            elif choice == "3":
                await self.interactive_video_search()
            elif choice == "4":
                await self.interactive_goal_setting()
            elif choice == "5":
                await self.interactive_spaced_repetition()
            
            continue_demo = Confirm.ask("\n[bright_yellow]Try another feature?[/bright_yellow]", default=True)
            if not continue_demo:
                break
    
    def show_feature_overview(self):
        """Show comprehensive overview of all features"""
        self.console.print(Rule("[bold bright_green]📊 Complete Feature Overview[/bold bright_green]"))
        
        total_features = sum(len(features) for features in self.feature_categories.values())
        
        overview_text = f"""
[bold bright_cyan]SYLLABO - AI-POWERED LEARNING ASSISTANT[/bold bright_cyan]

[bright_white]Total Features: {total_features}[/bright_white]
[bright_white]Categories: {len(self.feature_categories)}[/bright_white]

[bright_green]🎯 What makes Syllabo special:[/bright_green]
• AI-powered content analysis and generation
• Adaptive learning that adjusts to your pace
• Comprehensive resource discovery across platforms
• Intelligent study tools and session management
• Advanced analytics and learning predictions
• Personalized goals and progress tracking
        """
        
        self.console.print(Panel(overview_text, border_style="bright_blue", title="[bold]Syllabo Overview[/bold]"))
        
        # Show detailed feature breakdown
        for category_name, features in self.feature_categories.items():
            self.console.print(f"\n[bold bright_blue]{category_name}:[/bold bright_blue]")
            
            for feature_key, feature_name in features:
                # Get feature description
                if feature_key == "syllabus_analysis":
                    desc = "Extract topics and create learning roadmaps from any syllabus"
                elif feature_key == "quiz_generation":
                    desc = "Generate intelligent quizzes from content with multiple question types"
                elif feature_key == "video_search":
                    desc = "Find and analyze educational videos with AI-powered recommendations"
                elif feature_key == "adaptive_learning":
                    desc = "Create personalized learning paths that adapt to your progress"
                elif feature_key == "learning_analytics":
                    desc = "Track progress with detailed analytics and learning insights"
                elif feature_key == "note_generation":
                    desc = "Generate study notes and questions from video content"
                elif feature_key == "spaced_repetition":
                    desc = "Optimize retention with scientifically-proven spaced repetition"
                elif feature_key == "goal_setting":
                    desc = "Set and track personalized learning goals and milestones"
                elif feature_key == "resource_finder":
                    desc = "Discover books, courses, and materials across multiple platforms"
                else:
                    desc = "Advanced feature for enhanced learning experience"
                
                self.console.print(f"  [bright_green]•[/bright_green] [bright_cyan]{feature_name}[/bright_cyan]")
                self.console.print(f"    [dim]{desc}[/dim]")
        
        # Show usage statistics (simulated)
        stats_table = Table(title="Demo Statistics", border_style="bright_green")
        stats_table.add_column("Metric", style="bright_cyan")
        stats_table.add_column("Value", style="bright_white")
        
        stats_table.add_row("Total Features Available", str(total_features))
        stats_table.add_row("AI-Powered Features", "12")
        stats_table.add_row("Content Sources Supported", "10+")
        stats_table.add_row("Export Formats", "5")
        stats_table.add_row("Learning Analytics Metrics", "20+")
        
        self.console.print(stats_table)
    
    # Individual feature demos
    async def demo_syllabus_analysis(self, quick_mode=False):
        """Demo syllabus analysis feature with comprehensive sample data"""
        if not quick_mode:
            self.console.print("[bright_cyan]📄 Analyzing sample syllabus with AI...[/bright_cyan]")
            
            # Show the sample syllabus being analyzed
            syllabus_panel = Panel(
                self.demo_data['sample_syllabus'].strip(),
                title="[bold bright_blue]Sample Syllabus: Introduction to Python Programming[/bold bright_blue]",
                border_style="bright_blue",
                padding=(1, 2)
            )
            self.console.print(syllabus_panel)
        
        # Simulate analysis
        await asyncio.sleep(1.5)
        
        # Extract topics using predefined data
        topics = self.demo_data['sample_topics']
        
        if not quick_mode:
            self.console.print(f"\n[bright_green]✅ Successfully extracted {len(topics)} topics from syllabus![/bright_green]")
            
            topics_table = Table(title="AI-Extracted Learning Topics", border_style="bright_green")
            topics_table.add_column("Week", style="bright_cyan", width=8)
            topics_table.add_column("Topic", style="bright_white", width=30)
            topics_table.add_column("Description", style="bright_yellow", width=45)
            topics_table.add_column("Difficulty", style="bright_magenta", width=12)
            
            difficulty_levels = ["Beginner", "Beginner", "Intermediate", "Intermediate", 
                               "Intermediate", "Advanced", "Advanced", "Intermediate", "Advanced"]
            
            for i, topic in enumerate(topics, 1):
                week = f"Week {((i-1)//1)+1}-{((i-1)//1)+2}" if i <= 6 else f"Week {i+5}-{i+6}"
                difficulty = difficulty_levels[i-1] if i <= len(difficulty_levels) else "Intermediate"
                
                # Add difficulty visual indicator
                diff_indicator = {
                    "Beginner": "🟢",
                    "Intermediate": "🟡", 
                    "Advanced": "🔴"
                }.get(difficulty, "🟡")
                
                topics_table.add_row(
                    week,
                    topic['name'],
                    topic['description'][:42] + "..." if len(topic['description']) > 45 else topic['description'],
                    f"{diff_indicator} {difficulty}"
                )
            
            self.console.print(topics_table)
            
            # Show AI analysis insights
            self.console.print(f"\n[bold bright_blue]🧠 AI Analysis Insights:[/bold bright_blue]")
            self.console.print("  📊 Course Structure: Well-organized progression from basics to advanced")
            self.console.print("  ⏱️  Estimated Completion: 10-12 weeks (3-4 hours/week)")
            self.console.print("  🎯 Learning Path: Scaffolded approach building on prerequisites")
            self.console.print("  📈 Difficulty Progression: Gradual increase from beginner to advanced")
            self.console.print("  💡 Recommendation: Add practical projects between weeks 6-8")
            
            # Show generated learning roadmap
            roadmap_table = Table(title="Generated Learning Roadmap", border_style="bright_magenta")
            roadmap_table.add_column("Phase", style="bright_cyan", width=15)
            roadmap_table.add_column("Focus Areas", style="bright_white", width=35)
            roadmap_table.add_column("Recommended Time", style="bright_green", width=18)
            
            roadmap_table.add_row("Foundation", "Python Basics, Variables, Control Flow", "Weeks 1-4 (20 hours)")
            roadmap_table.add_row("Core Skills", "Functions, Data Structures", "Weeks 5-8 (25 hours)")
            roadmap_table.add_row("Advanced", "OOP, File Handling, Error Management", "Weeks 9-12 (30 hours)")
            
            self.console.print(roadmap_table)
        else:
            self.console.print(f"[bright_green]✅ Extracted {len(topics)} topics with AI-powered difficulty analysis[/bright_green]")
    
    async def demo_quiz_generation(self, quick_mode=False):
        """Demo quiz generation feature with realistic questions"""
        if not quick_mode:
            self.console.print("[bright_cyan]🧠 Generating AI-powered quiz from 'Functions' topic...[/bright_cyan]")
        
        await asyncio.sleep(1.5)
        
        # Use predefined quiz questions
        quiz_questions = self.demo_data['sample_quiz_questions']
        
        if not quick_mode:
            self.console.print("[bright_green]✅ Generated adaptive quiz: 'Python Functions Assessment'[/bright_green]")
            
            # Show quiz metadata
            quiz_info_table = Table(title="Quiz Information", border_style="bright_yellow")
            quiz_info_table.add_column("Property", style="bright_cyan", width=20)
            quiz_info_table.add_column("Value", style="bright_white", width=40)
            
            quiz_info_table.add_row("Topic", "Python Functions")
            quiz_info_table.add_row("Question Count", f"{len(quiz_questions)} questions")
            quiz_info_table.add_row("Estimated Time", "8-12 minutes")
            quiz_info_table.add_row("Difficulty Level", "Adaptive (starts Medium)")
            quiz_info_table.add_row("Question Types", "Multiple Choice, True/False, Short Answer")
            quiz_info_table.add_row("AI Features", "Auto-grading, Explanations, Difficulty Adjustment")
            
            self.console.print(quiz_info_table)
            
            # Show sample questions
            self.console.print(f"\n[bold bright_blue]📝 Sample Quiz Questions:[/bold bright_blue]")
            
            for i, question in enumerate(quiz_questions, 1):
                self.console.print(f"\n[bold bright_cyan]Question {i}:[/bold bright_cyan] {question['type'].replace('_', ' ').title()}")
                self.console.print(f"[bright_white]{question['question']}[/bright_white]")
                
                if question['type'] == 'multiple_choice':
                    for j, option in enumerate(question['options'], 1):
                        marker = "✓" if j-1 == question['correct_answer'] else " "
                        color = "bright_green" if j-1 == question['correct_answer'] else "dim"
                        self.console.print(f"  [{color}]{marker} {j}. {option}[/{color}]")
                elif question['type'] == 'true_false':
                    correct = "True" if question['correct_answer'] else "False"
                    self.console.print(f"  [bright_green]✓ Answer: {correct}[/bright_green]")
                elif question['type'] == 'short_answer':
                    self.console.print(f"  [bright_green]✓ Expected: {question['correct_answer']}[/bright_green]")
                
                self.console.print(f"  [dim]💡 Explanation: {question['explanation']}[/dim]")
            
            # Show AI quiz features
            self.console.print(f"\n[bold bright_blue]🤖 AI Quiz Features:[/bold bright_blue]")
            self.console.print("  🎯 Adaptive Difficulty: Questions adjust based on performance")
            self.console.print("  📊 Real-time Analytics: Track response time and accuracy")
            self.console.print("  💡 Intelligent Explanations: Detailed feedback for each answer")
            self.console.print("  🔄 Spaced Repetition: Missed questions scheduled for review")
            self.console.print("  📈 Progress Tracking: Performance metrics and improvement areas")
        else:
            self.console.print(f"[bright_green]✅ Generated {len(quiz_questions)} adaptive questions with AI explanations[/bright_green]")
    
    async def demo_video_search(self, quick_mode=False):
        """Demo video search feature with comprehensive results"""
        if not quick_mode:
            self.console.print("[bright_cyan]🎥 Searching for 'Python Functions' educational videos...[/bright_cyan]")
        
        await asyncio.sleep(1.5)
        
        videos = self.demo_data['sample_videos']
        
        if not quick_mode:
            self.console.print(f"[bright_green]✅ Found {len(videos)} high-quality educational videos![/bright_green]")
            
            # Show search results with detailed information
            videos_table = Table(title="AI-Curated Video Results", border_style="bright_blue")
            videos_table.add_column("Rank", style="bright_cyan", width=6)
            videos_table.add_column("Title", style="bright_white", width=35)
            videos_table.add_column("Channel", style="bright_yellow", width=18)
            videos_table.add_column("Duration", style="bright_green", width=10)
            videos_table.add_column("Quality Score", style="bright_magenta", width=12)
            videos_table.add_column("Views", style="bright_blue", width=8)
            
            quality_scores = ["9.4/10", "9.1/10", "8.8/10", "8.5/10", "9.0/10"]
            
            for i, video in enumerate(videos, 1):
                score = quality_scores[i-1] if i <= len(quality_scores) else "8.7/10"
                title = video['title'][:32] + "..." if len(video['title']) > 35 else video['title']
                
                videos_table.add_row(
                    f"#{i}",
                    title,
                    video['channel'],
                    video['duration'],
                    f"⭐ {score}",
                    video.get('views', 'N/A')
                )
            
            self.console.print(videos_table)
            
            # Show AI analysis of best video
            best_video = videos[0]
            analysis_panel = Panel(
                f"[bold bright_white]🏆 TOP RECOMMENDATION[/bold bright_white]\n\n"
                f"[bright_cyan]Title:[/bright_cyan] {best_video['title']}\n"
                f"[bright_cyan]Channel:[/bright_cyan] {best_video['channel']}\n"
                f"[bright_cyan]Duration:[/bright_cyan] {best_video['duration']}\n"
                f"[bright_cyan]Rating:[/bright_cyan] {best_video.get('rating', '4.9★')}\n\n"
                f"[bold bright_blue]🧠 AI Analysis:[/bold bright_blue]\n"
                f"• Comprehensive coverage of Python functions\n"
                f"• Clear explanations with practical examples\n"
                f"• Progressive difficulty suitable for beginners\n"
                f"• High engagement and positive reviews\n"
                f"• Includes hands-on coding exercises",
                title="[bold bright_green]Best Match Analysis[/bold bright_green]",
                border_style="bright_green"
            )
            self.console.print(analysis_panel)
            
            # Show topic coverage analysis
            coverage_table = Table(title="Topic Coverage Analysis", border_style="bright_yellow")
            coverage_table.add_column("Concept", style="bright_cyan", width=25)
            coverage_table.add_column("Coverage", style="bright_green", width=15)
            coverage_table.add_column("Quality", style="bright_magenta", width=15)
            
            coverage_table.add_row("Function Definition", "✅ Excellent", "🟢 High")
            coverage_table.add_row("Parameters & Arguments", "✅ Excellent", "🟢 High")
            coverage_table.add_row("Return Values", "✅ Good", "🟡 Medium")
            coverage_table.add_row("Scope & Variables", "⚠️  Partial", "🟡 Medium")
            coverage_table.add_row("Advanced Concepts", "❌ Missing", "🔴 Low")
            
            self.console.print(coverage_table)
            
            self.console.print(f"\n[bold bright_blue]💡 AI Recommendations:[/bold bright_blue]")
            self.console.print("  📚 Watch the top 3 videos for comprehensive understanding")
            self.console.print("  🔍 Search for 'Python scope' to fill knowledge gaps")
            self.console.print("  🎯 Bookmark key moments for future reference")
            self.console.print("  📝 Take notes and create practice exercises")
        else:
            self.console.print(f"[bright_green]✅ Found {len(videos)} AI-curated videos with quality scoring[/bright_green]")
    
    async def demo_adaptive_learning(self, quick_mode=False):
        """Demo adaptive learning paths"""
        if not quick_mode:
            self.console.print("[bright_cyan]🧭 Generating personalized learning path...[/bright_cyan]")
        
        await asyncio.sleep(1.5)
        
        if not quick_mode:
            path_table = Table(title="AI-Generated Learning Path", border_style="bright_green")
            path_table.add_column("Step", style="bright_cyan", width=5)
            path_table.add_column("Concept", style="bright_white", width=25)
            path_table.add_column("Difficulty", style="bright_yellow", width=12)
            path_table.add_column("Time Est.", style="bright_magenta", width=10)
            
            learning_path = [
                ("1", "Python Fundamentals", "●○○○○", "60 min"),
                ("2", "Control Structures", "●●○○○", "90 min"),
                ("3", "Functions & Modules", "●●●○○", "120 min"),
                ("4", "Data Structures", "●●●●○", "150 min"),
                ("5", "OOP Concepts", "●●●●●", "180 min")
            ]
            
            for step, concept, difficulty, time_est in learning_path:
                path_table.add_row(step, concept, difficulty, time_est)
            
            self.console.print(path_table)
            
            self.console.print("[bright_blue]💡 Personalization Features:[/bright_blue]")
            self.console.print("  • Adapted to your learning style: Visual")
            self.console.print("  • Difficulty progression optimized")
            self.console.print("  • Prerequisites automatically ordered")
            self.console.print("  • Estimated completion: 8 weeks")
        else:
            self.console.print("[bright_green]✅ Created personalized 5-step learning path[/bright_green]")
    
    async def demo_learning_analytics(self, quick_mode=False):
        """Demo learning analytics with comprehensive data"""
        if not quick_mode:
            self.console.print("[bright_cyan]📊 Analyzing learning patterns and generating insights...[/bright_cyan]")
        
        await asyncio.sleep(1.5)
        
        analytics = self.demo_data['sample_analytics']
        
        if not quick_mode:
            self.console.print("[bright_green]✅ Learning analytics generated from 45 study sessions![/bright_green]")
            
            # Main analytics dashboard
            analytics_table = Table(title="Learning Analytics Dashboard", border_style="bright_magenta")
            analytics_table.add_column("Metric", style="bright_cyan", width=25)
            analytics_table.add_column("Current Value", style="bright_white", width=15)
            analytics_table.add_column("Trend", style="bright_green", width=10)
            analytics_table.add_column("AI Insight", style="bright_yellow", width=35)
            
            analytics_table.add_row(
                "Weekly Study Time", 
                f"{analytics['study_time_per_week']} hours", 
                "↗ +15%", 
                "Optimal for retention and progress"
            )
            analytics_table.add_row(
                "Quiz Performance", 
                f"{analytics['quiz_performance']}%", 
                "↗ +8%", 
                "Above average, showing improvement"
            )
            analytics_table.add_row(
                "Concept Mastery", 
                f"{analytics['concept_mastery']}%", 
                "↗ +12%", 
                "Strong understanding, keep progressing"
            )
            analytics_table.add_row(
                "Learning Velocity", 
                f"{analytics['learning_velocity']} topics/week", 
                "→ Stable", 
                "Consistent and sustainable pace"
            )
            analytics_table.add_row(
                "Retention Rate", 
                f"{analytics['retention_rate']}%", 
                "↗ +5%", 
                "Excellent long-term memory retention"
            )
            
            self.console.print(analytics_table)
            
            # Study patterns analysis
            patterns_table = Table(title="Study Patterns & Behavior Analysis", border_style="bright_blue")
            patterns_table.add_column("Pattern", style="bright_cyan", width=25)
            patterns_table.add_column("Analysis", style="bright_white", width=50)
            
            patterns_table.add_row(
                "Optimal Session Length",
                f"{analytics['optimal_session_length']} minutes - Perfect for focus and retention"
            )
            patterns_table.add_row(
                "Best Learning Time",
                f"{analytics['favorite_learning_time']} - Peak performance window"
            )
            patterns_table.add_row(
                "Consistency Score",
                f"{analytics['consistency_score']:.0%} - Very consistent study habits"
            )
            patterns_table.add_row(
                "Strongest Topics",
                f"{', '.join(analytics['strongest_topics'])} - Natural aptitudes"
            )
            patterns_table.add_row(
                "Improvement Areas",
                f"{', '.join(analytics['improvement_areas'])} - Focus needed"
            )
            
            self.console.print(patterns_table)
            
            # Progress visualization
            progress_panel = Panel(
                f"[bold bright_white]📈 LEARNING PROGRESS VISUALIZATION[/bold bright_white]\n\n"
                f"[bright_cyan]Week 1:[/bright_cyan] ████████░░ 80% (Foundation Building)\n"
                f"[bright_cyan]Week 2:[/bright_cyan] ██████████ 95% (Concepts Mastered)\n"
                f"[bright_cyan]Week 3:[/bright_cyan] ███████░░░ 70% (New Challenges)\n"
                f"[bright_cyan]Week 4:[/bright_cyan] █████████░ 85% (Strong Progress)\n\n"
                f"[bold bright_blue]🎯 Performance Trends:[/bold bright_blue]\n"
                f"• Quiz Scores: 75% → 82% → 89% → 94% (📈 Improving)\n"
                f"• Study Time: 2.5h → 3.2h → 4.1h → 4.5h (📈 Increasing)\n"
                f"• Topic Completion: 3 → 6 → 8 → 12 topics (🚀 Accelerating)",
                title="[bold bright_green]Progress Timeline[/bold bright_green]",
                border_style="bright_green"
            )
            self.console.print(progress_panel)
            
            # AI recommendations
            self.console.print(f"\n[bold bright_blue]🤖 AI-Powered Recommendations:[/bold bright_blue]")
            self.console.print("  🎯 Increase OOP practice - consider coding projects")
            self.console.print("  ⏰ Extend sessions to 50 minutes for optimal flow state")
            self.console.print("  📚 Add error handling exercises to weak areas")
            self.console.print("  🔄 Schedule review sessions for long-term retention")
            self.console.print("  🏆 You're ready for intermediate-level challenges!")
        else:
            self.console.print("[bright_green]✅ Generated comprehensive analytics from 45 sessions[/bright_green]")
    
    async def demo_note_generation(self, quick_mode=False):
        """Demo AI note generation"""
        if not quick_mode:
            self.console.print("[bright_cyan]📝 Generating study notes with AI...[/bright_cyan]")
        
        await asyncio.sleep(1)
        
        notes_response = await self.demo_ai_client.generate_response("generate notes")
        
        if not quick_mode:
            self.console.print("[bright_green]Generated comprehensive study materials:[/bright_green]")
            
            self.console.print("\n[bold bright_blue]📋 Key Notes:[/bold bright_blue]")
            notes = [
                "Python is a high-level, interpreted programming language",
                "Variables don't need explicit type declaration",
                "Indentation defines code blocks and structure",
                "Functions are reusable code blocks defined with 'def'"
            ]
            
            for i, note in enumerate(notes, 1):
                self.console.print(f"  {i}. {note}")
            
            self.console.print("\n[bold bright_yellow]❓ Study Questions:[/bold bright_yellow]")
            questions = [
                "What makes Python different from compiled languages?",
                "How does Python handle variable types?",
                "What is the significance of indentation in Python?"
            ]
            
            for i, question in enumerate(questions, 1):
                self.console.print(f"  {i}. {question}")
        else:
            self.console.print("[bright_green]✅ Generated 8 study notes and 6 review questions[/bright_green]")
    
    async def demo_spaced_repetition(self, quick_mode=False):
        """Demo spaced repetition system"""
        if not quick_mode:
            self.console.print("[bright_cyan]🔄 Setting up spaced repetition schedule...[/bright_cyan]")
        
        await asyncio.sleep(1)
        
        if not quick_mode:
            schedule_table = Table(title="Spaced Repetition Schedule", border_style="bright_blue")
            schedule_table.add_column("Topic", style="bright_cyan", width=25)
            schedule_table.add_column("Mastery Level", style="bright_white", width=15)
            schedule_table.add_column("Next Review", style="bright_yellow", width=12)
            schedule_table.add_column("Interval", style="bright_green", width=10)
            
            schedule_table.add_row("Python Basics", "Intermediate", "Today", "1 day")
            schedule_table.add_row("Functions", "Beginner", "Tomorrow", "2 days")
            schedule_table.add_row("Data Types", "Advanced", "3 days", "7 days")
            schedule_table.add_row("Control Flow", "Mastered", "1 week", "14 days")
            
            self.console.print(schedule_table)
            
            self.console.print("[bright_blue]💡 Science-Based Learning:[/bright_blue]")
            self.console.print("  • Optimized retention intervals")
            self.console.print("  • Adaptive difficulty adjustment")
            self.console.print("  • Progress tracking and analytics")
        else:
            self.console.print("[bright_green]✅ Added 8 topics to spaced repetition system[/bright_green]")
    
    async def demo_goal_setting(self, quick_mode=False):
        """Demo goal setting feature"""
        if not quick_mode:
            self.console.print("[bright_cyan]🎯 Creating personalized learning goals...[/bright_cyan]")
        
        await asyncio.sleep(1)
        
        if not quick_mode:
            goals_table = Table(title="Learning Goals", border_style="bright_green")
            goals_table.add_column("Goal", style="bright_cyan", width=25)
            goals_table.add_column("Target", style="bright_white", width=15)
            goals_table.add_column("Progress", style="bright_yellow", width=15)
            goals_table.add_column("Deadline", style="bright_magenta", width=12)
            
            goals_table.add_row("Master Python Basics", "100%", "73% (↗)", "2 weeks")
            goals_table.add_row("Complete 5 Projects", "5 projects", "2/5 (●●○○○)", "1 month")
            goals_table.add_row("Study 30 min/day", "Daily habit", "85% success", "Ongoing")
            goals_table.add_row("Quiz Score 90%+", "90% average", "87% current", "3 weeks")
            
            self.console.print(goals_table)
            
            self.console.print("[bright_blue]💡 Smart Goal Features:[/bright_blue]")
            self.console.print("  • SMART goal framework integration")
            self.console.print("  • Progress tracking and reminders")
            self.console.print("  • Adaptive timeline adjustment")
        else:
            self.console.print("[bright_green]✅ Created 4 personalized learning goals[/bright_green]")
    
    async def demo_resource_finder(self, quick_mode=False):
        """Demo resource finder feature"""
        if not quick_mode:
            self.console.print("[bright_cyan]🔍 Finding learning resources across platforms...[/bright_cyan]")
        
        await asyncio.sleep(1)
        
        if not quick_mode:
            resources_table = Table(title="Discovered Learning Resources", border_style="bright_blue")
            resources_table.add_column("Resource", style="bright_cyan", width=30)
            resources_table.add_column("Type", style="bright_white", width=12)
            resources_table.add_column("Rating", style="bright_yellow", width=8)
            resources_table.add_column("Price", style="bright_green", width=10)
            
            for resource in self.demo_data['sample_resources']:
                price = "Free" if resource['type'] in ['documentation'] else "Varies"
                rating = "4.8★" if 'book' in resource['type'] else "4.5★"
                resources_table.add_row(
                    resource['title'][:27] + "..." if len(resource['title']) > 30 else resource['title'],
                    resource['type'].title(),
                    rating,
                    price
                )
            
            self.console.print(resources_table)
            
            self.console.print("[bright_blue]💡 Multi-Platform Search:[/bright_blue]")
            self.console.print("  • Books, courses, documentation")
            self.console.print("  • Quality scoring and ranking")
            self.console.print("  • Direct links and availability")
        else:
            self.console.print("[bright_green]✅ Found 25 learning resources across 6 platforms[/bright_green]")
    
    async def demo_generic_feature(self, feature_name: str):
        """Demo generic feature placeholder"""
        self.console.print(f"[bright_cyan]⚙️ Demonstrating {feature_name}...[/bright_cyan]")
        
        await asyncio.sleep(0.5)
        
        self.console.print(f"[bright_green]✅ {feature_name} is fully functional and ready to use![/bright_green]")
        
        # Show some generic capabilities
        self.console.print("[bright_blue]💡 Key Features:[/bright_blue]")
        self.console.print("  • Intuitive user interface")
        self.console.print("  • Data export capabilities")
        self.console.print("  • Integration with other tools")
    
    # Interactive demos
    async def interactive_syllabus_analysis(self):
        """Interactive syllabus analysis"""
        self.console.print("[bold bright_blue]📄 Interactive Syllabus Analysis[/bold bright_blue]")
        
        content = Prompt.ask(
            "[bright_cyan]Enter your syllabus content or course description[/bright_cyan]",
            default="Introduction to Data Science course covering statistics, Python, machine learning basics"
        )
        
        self.console.print(f"\n[bright_cyan]Analyzing your content...[/bright_cyan]")
        await asyncio.sleep(2)
        
        # Simulate analysis
        topics = ["Statistics Fundamentals", "Python for Data Science", "Data Visualization", "Machine Learning Basics", "Data Cleaning"]
        
        self.console.print(f"[bright_green]✅ Extracted {len(topics)} topics from your content![/bright_green]")
        
        for i, topic in enumerate(topics, 1):
            self.console.print(f"  {i}. {topic}")
        
        self.console.print(f"\n[bright_blue]💡 Recommended next steps:[/bright_blue]")
        self.console.print("  • Generate quizzes for each topic")
        self.console.print("  • Find video tutorials and resources")
        self.console.print("  • Create a learning schedule")
    
    async def interactive_quiz_generation(self):
        """Interactive quiz generation"""
        self.console.print("[bold bright_blue]🧠 Interactive Quiz Generation[/bold bright_blue]")
        
        topic = Prompt.ask(
            "[bright_cyan]Enter the topic for your quiz[/bright_cyan]",
            default="Python Functions"
        )
        
        num_questions = int(Prompt.ask(
            "[bright_cyan]How many questions would you like?[/bright_cyan]",
            default="5"
        ))
        
        self.console.print(f"\n[bright_cyan]Generating {num_questions} questions about {topic}...[/bright_cyan]")
        await asyncio.sleep(2)
        
        self.console.print(f"[bright_green]✅ Generated quiz: '{topic} Assessment'[/bright_green]")
        self.console.print(f"Questions: {num_questions} (Mix of multiple choice, true/false, and short answer)")
        self.console.print(f"Estimated time: {num_questions * 2} minutes")
        self.console.print(f"Difficulty: Adaptive based on your responses")
    
    async def interactive_video_search(self):
        """Interactive video search"""
        self.console.print("[bold bright_blue]🎥 Interactive Video Search[/bold bright_blue]")
        
        topic = Prompt.ask(
            "[bright_cyan]What topic would you like to find videos for?[/bright_cyan]",
            default="Machine Learning Algorithms"
        )
        
        preference = Prompt.ask(
            "[bright_cyan]Video preference[/bright_cyan]",
            choices=["beginner", "intermediate", "advanced", "comprehensive"],
            default="intermediate"
        )
        
        self.console.print(f"\n[bright_cyan]Searching for {preference} level videos about {topic}...[/bright_cyan]")
        await asyncio.sleep(2)
        
        self.console.print(f"[bright_green]✅ Found 12 high-quality videos![/bright_green]")
        self.console.print(f"Average rating: 4.7/5 stars")
        self.console.print(f"Total duration: 8 hours 23 minutes")
        self.console.print(f"Best match: 'Complete Guide to {topic}' by Tech Academy")
    
    async def interactive_goal_setting(self):
        """Interactive goal setting"""
        self.console.print("[bold bright_blue]🎯 Interactive Goal Setting[/bold bright_blue]")
        
        goal_type = Prompt.ask(
            "[bright_cyan]What type of goal would you like to set?[/bright_cyan]",
            choices=["daily_study", "skill_mastery", "project_completion", "exam_prep"],
            default="skill_mastery"
        )
        
        title = Prompt.ask(
            "[bright_cyan]Goal title[/bright_cyan]",
            default="Master Python Programming"
        )
        
        timeline = Prompt.ask(
            "[bright_cyan]Target timeline[/bright_cyan]",
            default="8 weeks"
        )
        
        self.console.print(f"\n[bright_cyan]Creating your personalized goal...[/bright_cyan]")
        await asyncio.sleep(1)
        
        self.console.print(f"[bright_green]✅ Goal created: '{title}'[/bright_green]")
        self.console.print(f"Timeline: {timeline}")
        self.console.print(f"Type: {goal_type.replace('_', ' ').title()}")
        self.console.print(f"AI will track your progress and provide reminders!")
    
    async def interactive_spaced_repetition(self):
        """Interactive spaced repetition setup"""
        self.console.print("[bold bright_blue]🔄 Interactive Spaced Repetition[/bold bright_blue]")
        
        topics_input = Prompt.ask(
            "[bright_cyan]Enter topics to add to spaced repetition (comma-separated)[/bright_cyan]",
            default="Variables, Functions, Loops, Classes"
        )
        
        topics = [topic.strip() for topic in topics_input.split(',')]
        
        self.console.print(f"\n[bright_cyan]Setting up spaced repetition for {len(topics)} topics...[/bright_cyan]")
        await asyncio.sleep(1)
        
        self.console.print(f"[bright_green]✅ Added {len(topics)} topics to your review schedule![/bright_green]")
        
        for i, topic in enumerate(topics, 1):
            next_review = ["Today", "Tomorrow", "In 3 days", "In 1 week"][min(i-1, 3)]
            self.console.print(f"  {i}. {topic} - Next review: {next_review}")
        
        self.console.print(f"\n[bright_blue]💡 Your first review session is ready![/bright_blue]")
    
    # Summary methods
    def show_quick_demo_summary(self):
        """Show quick demo summary"""
        summary_text = """
[bold bright_green]🎉 QUICK DEMO COMPLETE! 🎉[/bold bright_green]

[bright_white]You've experienced Syllabo's core features:[/bright_white]

[bright_green]✅ AI Syllabus Analysis[/bright_green] - Extract topics and create learning roadmaps
[bright_green]✅ Smart Quiz Generation[/bright_green] - Adaptive quizzes that adjust to your level  
[bright_green]✅ Video Discovery[/bright_green] - Find the best educational content
[bright_green]✅ Learning Analytics[/bright_green] - Track your progress with AI insights
[bright_green]✅ Adaptive Learning Paths[/bright_green] - Personalized learning journeys

[bold bright_blue]Ready to transform your learning experience?[/bold bright_blue]
[bright_white]Try the full app or explore more features in the complete demo![/bright_white]
        """
        
        self.console.print(Panel(
            summary_text,
            title="[bold bright_green]Demo Summary[/bold bright_green]",
            border_style="bright_green",
            padding=(1, 2)
        ))
    
    def show_complete_demo_summary(self):
        """Show complete demo summary"""
        total_features = sum(len(features) for features in self.feature_categories.values())
        
        summary_text = f"""
[bold bright_green]🏆 COMPLETE DEMO FINISHED! 🏆[/bold bright_green]

[bright_white]Congratulations! You've experienced all {total_features} features across {len(self.feature_categories)} categories:[/bright_white]

[bright_cyan]📚 Core Learning Tools[/bright_cyan] - Analysis, quizzes, and progress tracking
[bright_blue]🔍 Content Discovery[/bright_blue] - Videos, resources, and multi-platform search  
[bright_yellow]⚡ Study Tools[/bright_yellow] - Notes, bookmarks, sessions, and spaced repetition
[bright_magenta]🤖 AI Features[/bright_magenta] - Adaptive learning, analytics, and predictions
[bright_green]⚙️ Management[/bright_green] - Goals, exports, and configuration

[bold bright_blue]Syllabo transforms traditional learning into an intelligent, adaptive experience![/bold bright_blue]

[bright_white]Key Benefits You've Seen:[/bright_white]
• AI-powered personalization for optimal learning
• Comprehensive content discovery across platforms
• Scientific study methods (spaced repetition, analytics)
• Seamless integration of all learning activities
• Detailed progress tracking and predictions

[bold bright_green]Ready to supercharge your learning journey? Start using Syllabo today![/bold bright_green]
        """
        
        self.console.print(Panel(
            summary_text,
            title="[bold bright_green]Complete Demo Summary[/bold bright_green]",
            border_style="bright_green", 
            padding=(1, 2)
        ))
    
    async def run_demo(self):
        """Main demo runner - runs complete demo by default"""
        self.setup_demo_environment()
        
        try:
            self.show_demo_banner()
            
            # Show a brief intro message
            self.console.print("[bright_cyan]Starting comprehensive demo of all Syllabo features...[/bright_cyan]")
            self.console.print("[dim]This will demonstrate every feature with realistic sample data.[/dim]\n")
            
            # Ask if user wants to continue or see options
            proceed = Confirm.ask("[bright_yellow]Continue with complete demo?[/bright_yellow]", default=True)
            
            if proceed:
                # Run complete demo directly
                await self.run_complete_demo()
            else:
                # Show menu options if user doesn't want complete demo
                while True:
                    choice = self.show_demo_menu()
                    
                    if choice == "0":
                        self.console.print("[bright_yellow]Returning to main application...[/bright_yellow]")
                        break
                    elif choice == "1":
                        await self.run_quick_demo()
                    elif choice == "2":
                        await self.run_category_demo()
                    elif choice == "3":
                        await self.run_complete_demo()
                    elif choice == "4":
                        await self.run_interactive_mode()
                    elif choice == "5":
                        self.show_feature_overview()
                    
                    if choice != "0":
                        continue_demo = Confirm.ask("\n[bright_yellow]Would you like to try another demo option?[/bright_yellow]", default=True)
                        if not continue_demo:
                            break
                        self.console.clear()
                        self.show_demo_banner()
        
        finally:
            self.cleanup_demo_environment()
    
def main():
    """Run the comprehensive features demo"""
    demo = ComprehensiveFeaturesDemo()
    return asyncio.run(demo.run_demo())

if __name__ == "__main__":
    main()
