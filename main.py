#!/usr/bin/env python3
"""
Simple working version of main.py with interactive mode
"""

import os
import sys
import asyncio
from dotenv import load_dotenv
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.rule import Rule
from rich.prompt import Prompt

load_dotenv()
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

# Import components
from src.syllabus_parser import SyllabusParser
from src.youtube_client import YouTubeClient
from src.ai_client import AIClient
from src.database import SyllaboDatabase
from src.logger import SyllaboLogger

class SimpleSyllabo:
    """Simple version of Syllabo with working interactive mode"""
    
    def __init__(self):
        self.console = Console()
        self.logger = SyllaboLogger("main")
        self.db = SyllaboDatabase()
        self.ai_client = AIClient()
        self.youtube_client = YouTubeClient()
        self.syllabus_parser = SyllabusParser()
    
    def print_banner(self):
        """Print banner"""
        banner = """
[bold cyan]SYLLABO[/bold cyan]
[bold white]AI-Powered Learning Assistant[/bold white]
[dim]Your comprehensive educational resource manager[/dim]
        """
        
        self.console.print(Panel(
            banner.strip(),
            border_style="bright_cyan",
            title="[bold bright_blue]Welcome[/bold bright_blue]"
        ))
    
    def show_interactive_menu(self):
        """Show interactive menu"""
        self.console.print(Rule("[bold bright_cyan]Main Menu[/bold bright_cyan]"))
        
        menu_table = Table(border_style="bright_blue")
        menu_table.add_column("Option", style="bright_cyan", width=8)
        menu_table.add_column("Feature", style="bright_green", width=20)
        menu_table.add_column("Description", style="bright_white", width=40)
        
        menu_table.add_row("1", "Analyze Syllabus", "Process syllabus and find resources")
        menu_table.add_row("2", "Quiz", "Generate interactive quizzes")
        menu_table.add_row("3", "Progress", "View learning progress")
        menu_table.add_row("0", "Exit", "Exit the application")
        
        self.console.print(menu_table)
        
        choice = Prompt.ask(
            "[bold bright_yellow]Select an option[/bold bright_yellow]",
            choices=["1", "2", "3", "0"],
            default="1"
        )
        
        if choice == "1":
            return "analyze"
        elif choice == "2":
            return "quiz"
        elif choice == "3":
            return "progress"
        else:
            return "exit"

async def main():
    """Main function"""
    # If no arguments, go to interactive mode
    if len(sys.argv) == 1:
        app = SimpleSyllabo()
        app.print_banner()
        
        while True:
            command = app.show_interactive_menu()
            
            if command == 'exit':
                app.console.print(Panel(
                    "[bold bright_cyan]Thank you for using Syllabo![/bold bright_cyan]",
                    border_style="bright_cyan"
                ))
                break
            else:
                app.console.print(f"[bright_green]You selected: {command}[/bright_green]")
                app.console.print("[dim]Feature coming soon![/dim]")
                Prompt.ask("\n[dim]Press Enter to continue[/dim]", default="")
                app.console.clear()
                app.print_banner()
    else:
        print("Command line mode not implemented in simple version")

if __name__ == "__main__":
    asyncio.run(main())