#!/usr/bin/env python3
"""
Syllabo - AI-Powered Learning Assistant
Main entry point for all features
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
from rich.text import Text
from rich.align import Align

load_dotenv()
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

# Import components
from src.database import SyllaboDatabase
from src.logger import SyllaboLogger
from src.ai_client import AIClient
from src.syllabus_parser import SyllabusParser

class SyllaboMain:
    """Main application class with all features"""
    
    def __init__(self):
        self.console = Console()
        self.logger = SyllaboLogger("main")
        
        # Initialize core components
        self.db = SyllaboDatabase()
        self.ai_client = AIClient()
        self.syllabus_parser = SyllabusParser()
    
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
            ("1", "analyze", "Analyze Syllabus", "Process syllabus and find learning resources"),
            ("2", "quiz", "Interactive Quizzes", "Generate and take quizzes from content"),
            ("3", "progress", "Progress Dashboard", "View learning progress and analytics"),
            ("4", "goals", "Study Goals", "Manage learning goals and milestones"),
            ("5", "platforms", "Multi-Platform Search", "Search across learning platforms"),
            ("6", "bookmarks", "Smart Bookmarks", "Manage video bookmarks and notes"),
            ("7", "session", "Study Sessions", "Pomodoro timer and focus sessions"),
            ("8", "review", "Spaced Repetition", "Review topics using spaced repetition"),
            ("9", "help", "Help & Documentation", "Get help and usage information"),
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
            else:
                self.console.print(f"[yellow]Feature '{command}' coming soon![/yellow]")
                self.console.print("[dim]This feature is being developed and will be available soon.[/dim]")
                
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
                    
                else:
                    self.console.print("[bright_yellow]No topics found[/bright_yellow]")
                    
            except Exception as e:
                self.console.print(f"[bright_red]Error: {e}[/bright_red]")
        
        else:  # text input
            content = Prompt.ask("[bright_cyan]Enter syllabus text content[/bright_cyan]")
            if not content:
                self.console.print("[bright_red]No content provided[/bright_red]")
                return
            
            try:
                with self.console.status("[bright_cyan]Extracting topics with AI..."):
                    topics = await self.syllabus_parser.extract_topics(content, self.ai_client)
                
                if topics:
                    self.console.print(f"[bright_green]Found {len(topics)} topics[/bright_green]")
                else:
                    self.console.print("[bright_yellow]No topics found[/bright_yellow]")
                    
            except Exception as e:
                self.console.print(f"[bright_red]Error: {e}[/bright_red]")

async def main():
    """Main application entry point"""
    
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
            await app._interactive_analyze()
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
