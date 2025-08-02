import sys
import os
from typing import Any, Dict, List, Optional, Union, Tuple
import inquirer
from rich.console import Console
from src.cli.formatting import OutputFormatter

class CLIInputHandler:
    """Handles user input for CLI commands"""

    def __init__(self, formatter: Optional[OutputFormatter] = None):
        """Initialize input handler

        Args:
            formatter: Output formatter for messages
        """
        self.formatter = formatter or OutputFormatter()
        self.console = self.formatter.console

    def get_file_path(self, prompt: str, file_filter: Optional[str] = None) -> str:
        """Get a file path from the user with validation

        Args:
            prompt: Prompt text to display
            file_filter: Optional file extension filter (e.g., '.pdf')

        Returns:
            Validated file path
        """
        while True:
            path = input(f"{prompt}: ").strip()

            # Check if file exists
            if not os.path.exists(path):
                self.formatter.print_error(f"File not found: {path}")
                continue

            # Check if it's a file
            if not os.path.isfile(path):
                self.formatter.print_error(f"Not a file: {path}")
                continue

            # Check if it's readable
            if not os.access(path, os.R_OK):
                self.formatter.print_error(f"File not readable: {path}")
                continue

            # Check extension if filter provided
            if file_filter and not path.endswith(file_filter):
                self.formatter.print_error(f"File must have {file_filter} extension")
                continue

            return path

    def get_text_input(self, prompt: str, min_length: int = 0, max_length: Optional[int] = None) -> str:
        """Get text input from the user with validation

        Args:
            prompt: Prompt text to display
            min_length: Minimum required length
            max_length: Maximum allowed length

        Returns:
            Validated text input
        """
        while True:
            text = input(f"{prompt}: ").strip()

            # Check minimum length
            if len(text) < min_length:
                self.formatter.print_error(f"Input must be at least {min_length} characters")
                continue

            # Check maximum length
            if max_length and len(text) > max_length:
                self.formatter.print_error(f"Input must be at most {max_length} characters")
                continue

            return text

    def get_integer(self, prompt: str, min_value: Optional[int] = None, max_value: Optional[int] = None) -> int:
        """Get integer input from the user with validation

        Args:
            prompt: Prompt text to display
            min_value: Minimum allowed value
            max_value: Maximum allowed value

        Returns:
            Validated integer
        """
        while True:
            try:
                value = int(input(f"{prompt}: ").strip())

                # Check minimum value
                if min_value is not None and value < min_value:
                    self.formatter.print_error(f"Value must be at least {min_value}")
                    continue

                # Check maximum value
                if max_value is not None and value > max_value:
                    self.formatter.print_error(f"Value must be at most {max_value}")
                    continue

                return value
            except ValueError:
                self.formatter.print_error("Please enter a valid integer")

    def get_selection(self, prompt: str, options: List[str], default: Optional[str] = None) -> str:
        """Get a selection from a list of options

        Args:
            prompt: Prompt text to display
            options: List of options to choose from
            default: Default option

        Returns:
            Selected option
        """
        if not options:
            raise ValueError("No options provided for selection")

        # Use inquirer for better UX if available
        try:
            questions = [
                inquirer.List('selection',
                             message=prompt,
                             choices=options,
                             default=default or options[0])
            ]
            answers = inquirer.prompt(questions)
            return answers['selection']
        except (ImportError, Exception):
            # Fallback to simple console input
            self.formatter.print_info(prompt)
            for i, option in enumerate(options, 1):
                print(f"  {i}. {option}" + (" (default)" if option == default else ""))

            while True:
                try:
                    selection = input("Enter number: ").strip()

                    # Use default if empty
                    if not selection and default:
                        return default

                    idx = int(selection) - 1
                    if 0 <= idx < len(options):
                        return options[idx]
                    else:
                        self.formatter.print_error(f"Please enter a number between 1 and {len(options)}")
                except ValueError:
                    self.formatter.print_error("Please enter a valid number")

    def get_confirmation(self, prompt: str, default: bool = True) -> bool:
        """Get a yes/no confirmation from the user

        Args:
            prompt: Prompt text to display
            default: Default answer

        Returns:
            True for yes, False for no
        """
        return self.formatter.confirm_action(prompt)

    def get_key_press(self, prompt: str, valid_keys: List[str], default: Optional[str] = None) -> str:
        """Get a single key press from the user from a list of valid keys"""
        if self.interactive_mode:
            # In interactive mode, we might use a more advanced method
            # For now, fallback to simple input
            pass

        prompt_keys = []
        for k in valid_keys:
            if k == default:
                prompt_keys.append(k.upper())
            else:
                prompt_keys.append(k.lower())

        prompt_str = f"{prompt} ({'/'.join(prompt_keys)}): "

        while True:
            try:
                # Fallback to regular input
                if sys.stdin.isatty():
                    key = input(prompt_str).strip().lower()
                    if not key and default:
                        return default
                    if key in valid_keys:
                        return key
                    else:
                        self.formatter.print_error(f"Invalid input. Please enter one of {valid_keys}")
                else:
                    # Non-interactive mode, maybe read from a pipe
                    return default if default else valid_keys[0]  # Or handle differently
            except (EOFError, KeyboardInterrupt):
                self.formatter.print_error("\nInput cancelled.")
                return ""


