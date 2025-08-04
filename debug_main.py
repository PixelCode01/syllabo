#!/usr/bin/env python3
import sys
import os
import asyncio

print(f"DEBUG: Starting script, sys.argv = {sys.argv}")

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

print("DEBUG: About to import modules")

try:
    from dotenv import load_dotenv
    load_dotenv()
    print("DEBUG: dotenv loaded")
    
    from rich.console import Console
    print("DEBUG: rich imported")
    
    # Try importing our modules one by one
    from src.database import SyllaboDatabase
    print("DEBUG: database imported")
    
    from src.ai_client import AIClient
    print("DEBUG: ai_client imported")
    
    from src.logger import SyllaboLogger
    print("DEBUG: logger imported")
    
    from src.cli.commands import create_parser
    print("DEBUG: cli.commands imported")
    
except Exception as e:
    print(f"DEBUG: Import error: {e}")
    sys.exit(1)

print("DEBUG: All imports successful")

# Test basic functionality
console = Console()
logger = SyllaboLogger("debug")

print("DEBUG: Basic objects created")

# Test argument parser
try:
    parser = create_parser()
    print("DEBUG: Argument parser created")
except Exception as e:
    print(f"DEBUG: Error creating parser: {e}")

# Test SyllaboMain import and creation
try:
    # Import all the components that SyllaboMain needs
    from src.syllabus_parser import SyllabusParser
    from src.youtube_client import YouTubeClient
    from src.video_analyzer import VideoAnalyzer
    from src.spaced_repetition import SpacedRepetitionEngine
    from src.notification_system import NotificationSystem
    from src.quiz_generator import QuizGenerator
    from src.progress_dashboard import ProgressDashboard
    from src.goals_manager import GoalsManager
    from src.platform_integrator import PlatformIntegrator
    from src.podcast_integrator import PodcastIntegrator
    from src.bookmark_manager import BookmarkManager
    from src.difficulty_analyzer import DifficultyAnalyzer
    from src.study_session_manager import StudySessionManager
    from src.export_system import ExportSystem
    print("DEBUG: All SyllaboMain dependencies imported")
    
    # Try creating a minimal version
    db = SyllaboDatabase()
    ai_client = AIClient()
    print("DEBUG: Core components created")
    
except Exception as e:
    print(f"DEBUG: Error with SyllaboMain dependencies: {e}")
    import traceback
    traceback.print_exc()

if len(sys.argv) == 1:
    print("DEBUG: No arguments - should show interactive mode")
    console.print("[green]Interactive mode would start here[/green]")
else:
    print(f"DEBUG: Arguments provided: {sys.argv[1:]}")

print("DEBUG: Script completed successfully")