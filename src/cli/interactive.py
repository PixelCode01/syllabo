import os
from typing import List, Dict

from src.youtube_client import YouTubeClient
from src.video_analyzer import VideoAnalyzer
from src.syllabus_parser import SyllabusParser
from rich.console import Console
from rich.panel import Panel

class InteractiveMode:
    def __init__(self):
        self.console = Console()
        self.youtube_client = YouTubeClient()
        self.video_analyzer = VideoAnalyzer(None)  # AI client not needed for this mode
        self.syllabus_parser = SyllabusParser()

    def run(self):
        self.console.print(Panel.fit("[bold cyan]Interactive Syllabus Processor[/bold cyan]"))
        while True:
            self.console.print("\nChoose an option:")
            self.console.print("1. Enter syllabus text")
            self.console.print("2. Load syllabus from file")
            self.console.print("3. Exit")
            choice = input("> ")

            if choice == '1':
                self.process_text_input()
            elif choice == '2':
                self.process_file_input()
            elif choice == '3':
                break
            else:
                self.console.print("Invalid choice.", style="bold red")
import os
import sys
from typing import Dict, List, Any, Optional
from prompt_toolkit import PromptSession
from prompt_toolkit.completion import Completer, Completion
from prompt_toolkit.history import FileHistory
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.formatted_text import HTML
from prompt_toolkit.styles import Style

from src.cli.formatting import OutputFormatter
from src.cli.keyboard_shortcuts import KeyboardShortcutManager

class SyllaboCommandCompleter(Completer):
    """Command completer for interactive mode"""

    def __init__(self):
        """Initialize with command structure for auto-completion"""
        self.commands = {
            'analyze': {
                'args': ['--file', '--text', '--search-videos', '--max-videos', 
                         '--print-results', '--save', '--export-format', '--add-to-review',
                         '--preview'],
                'help': 'Analyze syllabus and extract topics'
            },
            'search': {
                'args': ['--topic', '--max-videos', '--save', '--export-format', '--enhanced', '--preview'],
                'help': 'Search for educational videos on a specific topic'
            },
            'history': {
                'args': ['--limit', '--export-session', '--preview'],
                'help': 'Show recent syllabi and searches'
            },
            'export': {
                'args': ['--syllabus-id', '--format', '--preview'],
                'help': 'Export analysis results to a file'
            },
            'review': {
                'subcommands': {
                    'add': {
                        'args': ['--topic', '--description'],
                        'help': 'Add a topic to your review schedule'
                    },
                    'list': {
                        'args': ['--format'],
                        'help': 'List all topics in your review schedule'
                    },
                    'due': {
                        'args': ['--notify', '--format'],
                        'help': 'Show topics due for review today'
                    },
                    'mark': {
                        'args': ['--topic', '--success', '--failure'],
                        'help': 'Mark a topic as reviewed'
                    },
                    'stats': {
                        'args': ['--topic', '--format'],
                        'help': 'Show review statistics'
                    },
                    'remove': {
                        'args': ['--topic'],
                        'help': 'Remove a topic from your review schedule'
                    },
                    'help': {
                        'args': [],
                        'help': 'Show detailed help for the review system'
                    }
                },
                'help': 'Spaced repetition review system'
            },
            'help': {
                'args': [],
                'help': 'Show help information'
            },
            'exit': {
                'args': [],
                'help': 'Exit interactive mode'
            },
            'clear': {
                'args': [],
                'help': 'Clear the screen'
            }
        }

        # Common argument values
        self.arg_values = {
            '--export-format': ['json', 'csv', 'markdown', 'html'],
            '--format': ['json', 'csv', 'markdown', 'html', 'table'],
            '--max-videos': ['5', '10', '15', '20'],
            '--limit': ['5', '10', '15', '20']
        }

    def get_completions(self, document, complete_event):
        """Get completions based on current input"""
        text = document.text_before_cursor.lstrip()

        # Split by spaces, but keep quoted strings together
        words = []
        current_word = ''
        in_quotes = False
        quote_char = None

        for char in text:
            if char in ['"', "'"] and (not in_quotes or char == quote_char):
                in_quotes = not in_quotes
                quote_char = char if in_quotes else None
                current_word += char
            elif char == ' ' and not in_quotes:
                if current_word:
                    words.append(current_word)
                    current_word = ''
            else:
                current_word += char

        if current_word:
            words.append(current_word)

        # No text yet, suggest commands
        if not words:
            for cmd in self.commands:
                yield Completion(
                    cmd,
                    start_position=0,
                    display_meta=self.commands[cmd]['help']
                )
            return

        # First word is the command
        cmd = words[0]

        # Command is partial, suggest matching commands
        if len(words) == 1 and not text.endswith(' '):
            for command in self.commands:
                if command.startswith(cmd):
                    yield Completion(
                        command,
                        start_position=-len(cmd),
                        display_meta=self.commands[command]['help']
                    )
            return

        # Command is complete, suggest subcommands or arguments
        if cmd in self.commands:
            # Check if it's a command with subcommands (like review)
            if 'subcommands' in self.commands[cmd]:
                # If we have only the command, suggest subcommands
                if len(words) == 1 or (len(words) == 2 and not text.endswith(' ')):
                    subcmd = words[1] if len(words) > 1 else ''
                    for subcommand, details in self.commands[cmd]['subcommands'].items():
                        if subcommand.startswith(subcmd):
                            yield Completion(
                                subcommand,
                                start_position=-len(subcmd) if subcmd else 0,
                                display_meta=details['help']
                            )
                    return

                # If we have the subcommand, suggest its arguments
                if len(words) >= 2:
                    subcmd = words[1]
                    if subcmd in self.commands[cmd]['subcommands']:
                        last_word = words[-1] if not text.endswith(' ') else ''
                        all_args = self.commands[cmd]['subcommands'][subcmd]['args']

                        # Check what arguments have already been used
                        used_args = set()
                        for w in words[2:]:
                            if w.startswith('--'):
                                used_args.add(w.split('=')[0] if '=' in w else w)

                        # Suggest unused arguments
                        for arg in all_args:
                            if arg not in used_args and arg.startswith(last_word):
                                yield Completion(
                                    arg,
                                    start_position=-len(last_word),
                                    display_meta='Argument for ' + subcmd
                                )

                        # If the last word is a complete argument that takes values, suggest values
                        if last_word in self.arg_values and text.endswith(' '):
                            for value in self.arg_values[last_word]:
                                yield Completion(value, start_position=0)
            else:
                # Regular command, suggest its arguments
                last_word = words[-1] if not text.endswith(' ') else ''

                # Check what arguments have already been used
                used_args = set()
                for w in words[1:]:
                    if w.startswith('--'):
                        used_args.add(w.split('=')[0] if '=' in w else w)

                # Suggest unused arguments
                if last_word.startswith('--') or text.endswith(' '):
                    for arg in self.commands[cmd]['args']:
                        if arg not in used_args and arg.startswith(last_word):
                            yield Completion(
                                arg,
                                start_position=-len(last_word),
                                display_meta='Argument for ' + cmd
                            )

                    # If the last word is a complete argument that takes values, suggest values
                    if last_word in self.arg_values and text.endswith(' '):
                        for value in self.arg_values[last_word]:
                            yield Completion(value, start_position=0)


class InteractiveShell:
    """Interactive command shell for Syllabo"""

    def __init__(self, cli_instance, theme: str = 'minimal'):
        """Initialize interactive shell

        Args:
            cli_instance: Instance of the main CLI class
            theme: Display theme (minimal or high-contrast)
        """
        self.cli = cli_instance
        self.formatter = OutputFormatter(theme)
        self.keyboard_manager = KeyboardShortcutManager()

        # Set up history file
        history_dir = os.path.join(os.path.expanduser('~'), '.syllabo')
        os.makedirs(history_dir, exist_ok=True)
        history_file = os.path.join(history_dir, 'history')

        # Create prompt session
        self.session = PromptSession(
            history=FileHistory(history_file),
            auto_suggest=AutoSuggestFromHistory(),
            completer=SyllaboCommandCompleter(),
            key_bindings=self.keyboard_manager.get_bindings(),
            style=self._get_prompt_style(theme)
        )

        # Flag for showing help
        self.show_help = False

    def _get_prompt_style(self, theme: str) -> Style:
        """Get the prompt style based on theme

        Args:
            theme: Theme name (minimal or high-contrast)

        Returns:
            Style object for prompt_toolkit
        """
        if theme == 'minimal':
            return Style.from_dict({
                'prompt': 'bold cyan',
                'continuation': 'gray'
            })
        else:  # high-contrast
            return Style.from_dict({
                'prompt': 'bold white on blue',
                'continuation': 'bold white on gray'
            })

    def _parse_interactive_command(self, text: str) -> List[str]:
        """Parse an interactive command into argv-style list

        Args:
            text: Command text entered by user

        Returns:
            List of command parts suitable for argparse
        """
        import shlex
        return ['syllabo.py'] + shlex.split(text)

    def _display_welcome(self) -> None:
        """Display welcome message and help"""
        self.formatter.print_title("Syllabo Enhanced Interactive Shell")
        self.formatter.print_info("Type commands directly or 'help' for assistance")
        self.formatter.print_info("Press F1 for keyboard shortcuts, Ctrl+C to exit")
        print()

    def _display_help(self) -> None:
        """Display help for interactive mode"""
        self.formatter.print_title("Available Commands")

        # Create table of commands
        table = self.formatter.create_table("Commands", ["Command", "Description"])

        # Add all command categories
        for cmd, details in sorted(SyllaboCommandCompleter().commands.items()):
            table.add_row(cmd, details['help'])

        self.formatter.console.print(table)

        # Show keyboard shortcuts
        self.formatter.print_title("Keyboard Shortcuts")
        print(self.keyboard_manager.get_help_text())

    def _handle_builtin_command(self, cmd: str) -> bool:
        """Handle built-in shell commands

        Args:
            cmd: Command string

        Returns:
            True if handled, False if should be passed to main CLI
        """
        if cmd.strip() == 'exit':
            return True

        if cmd.strip() == 'help':
            self._display_help()
            return True

        if cmd.strip() == 'clear':
            self.formatter.console.clear()
            return True

        return False

    async def run(self) -> None:
        """Run the interactive shell"""
        import argparse
        import asyncio

        self._display_welcome()

        while True:
            try:
                # Check if help was requested via keyboard shortcut
                if self.show_help:
                    self._display_help()
                    self.show_help = False

                # Get command with formatted prompt
                command = self.session.prompt(
                    HTML('<ansiblue>syllabo</ansiblue> <ansiyellow>»</ansiyellow> ')
                )

                # Skip empty commands
                if not command.strip():
                    continue

                # Handle built-in commands
                if self._handle_builtin_command(command):
                    if command.strip() == 'exit':
                        self.formatter.print_info("Exiting interactive mode")
                        break
                    continue

                # Parse the command and create args namespace
                try:
                    from src.cli.commands import create_parser
                    parser = create_parser()
                    args = parser.parse_args(self._parse_interactive_command(command)[1:])

                    # Execute the command
                    with self.formatter.console.status("Running command..."):
                        await self.cli.run(args)
                    print()

                except argparse.ArgumentError as e:
                    self.formatter.print_error(f"Argument error: {e}")
                except argparse.ArgumentTypeError as e:
                    self.formatter.print_error(f"Argument type error: {e}")
                except SystemExit:
                    # Argparse calls exit() on error, catch it to keep the shell running
                    pass

            except KeyboardInterrupt:
                # Ctrl+C, confirm exit
                if self.formatter.confirm_action("Exit interactive mode?"):
                    break
            except EOFError:
                # Ctrl+D, exit directly
                break
            except Exception as e:
                self.formatter.print_error(f"Error: {e}")

        self.formatter.print_success("Thanks for using Syllabo!")
    def process_text_input(self):
        self.console.print("Enter syllabus text (type 'END' on a new line to finish):")
        lines = []
        while True:
            line = input()
            if line.strip().upper() == 'END':
                break
            lines.append(line)
        syllabus_text = "\n".join(lines)
        self.process_syllabus(syllabus_text)

    def process_file_input(self):
        file_path = input("Enter file path: ")
        if not os.path.exists(file_path):
            self.console.print("File not found.", style="bold red")
            return
        try:
            syllabus_text = self.syllabus_parser.load_from_file(file_path)
            self.process_syllabus(syllabus_text)
        except Exception as e:
            self.console.print(f"Error reading file: {e}", style="bold red")

    def process_syllabus(self, syllabus_text: str):
        self.console.print("\nExtracting topics...")
        # This uses a simplified, non-AI topic extraction for speed
        topics = self.syllabus_parser._parse_topics(syllabus_text) 
        if not topics:
            self.console.print("Could not extract topics.", style="yellow")
            return

        for topic in topics:
            self.console.print(f"\n--- Processing Topic: {topic['name']} ---")
            self.find_and_display_videos(topic['name'])

    async def find_and_display_videos(self, topic_name: str):
        self.console.print(f"Searching for videos on '{topic_name}'...")
        videos = await self.youtube_client.search_videos(topic_name, max_results=5)
        if not videos:
            self.console.print("No videos found.", style="yellow")
            return

        self.console.print("Analyzing videos...")
        analyzed_videos = await self.video_analyzer.analyze_videos(videos, topic_name)

        self.console.print("\n[bold]Top Video Recommendations[/bold]")
        for i, video in enumerate(analyzed_videos, 1):
            self.console.print(f"{i}. {video['title']}")
            self.console.print(f"   Channel: {video['channel']}")
            self.console.print(f"   Score: {video['composite_score']:.1f}/10")
            self.console.print(f"   URL: https://youtube.com/watch?v={video['id']}")
