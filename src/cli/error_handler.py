import sys
import traceback
import asyncio
from typing import Optional, Callable, Any, TypeVar, Coroutine
from functools import wraps

from src.cli.formatting import OutputFormatter

T = TypeVar('T')

class CLIErrorHandler:
    """Handles errors in CLI commands with graceful fallback"""

    def __init__(self, formatter: Optional[OutputFormatter] = None):
        """Initialize error handler

        Args:
            formatter: Output formatter instance for displaying errors
        """
        self.formatter = formatter or OutputFormatter()
        self.debug_mode = False

    def set_debug_mode(self, enabled: bool) -> None:
        """Enable or disable debug mode

        Args:
            enabled: Whether debug mode should be enabled
        """
        self.debug_mode = enabled

    def handle_command_error(self, func: Callable) -> Callable:
        """Decorator to handle errors in CLI commands

        Args:
            func: The function to wrap with error handling

        Returns:
            Wrapped function with error handling
        """
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                self._display_error(e)
                return None
        return wrapper

    def handle_async_command_error(self, func: Callable[..., Coroutine[Any, Any, T]]) -> Callable[..., Coroutine[Any, Any, Optional[T]]]:
        """Decorator to handle errors in async CLI commands

        Args:
            func: The async function to wrap with error handling

        Returns:
            Wrapped async function with error handling
        """
        @wraps(func)
        async def wrapper(*args, **kwargs):
            try:
                return await func(*args, **kwargs)
            except asyncio.CancelledError:
                # Don't handle cancellation, let it propagate
                raise
            except Exception as e:
                self._display_error(e)
                return None
        return wrapper

    def _display_error(self, error: Exception) -> None:
        """Display a user-friendly error message

        Args:
            error: The exception that occurred
        """
        error_type = type(error).__name__
        error_message = str(error)

        # Special handling for common errors
        if error_type == 'FileNotFoundError':
            self.formatter.print_error(f"File not found: {error_message}")
            self.formatter.print_info("Check the file path and try again")
        elif error_type == 'PermissionError':
            self.formatter.print_error(f"Permission denied: {error_message}")
            self.formatter.print_info("Check file permissions or run with elevated privileges")
        elif error_type == 'ConnectionError':
            self.formatter.print_error(f"Connection error: {error_message}")
            self.formatter.print_info("Check your internet connection and try again")
        elif error_type == 'APIError':
            self.formatter.print_error(f"API error: {error_message}")
            self.formatter.print_info("Check your API keys in .env file or try again later")
        elif error_type == 'JSONDecodeError':
            self.formatter.print_error(f"JSON parsing error: {error_message}")
            self.formatter.print_info("The response data couldn't be parsed correctly")
        elif error_type == 'TimeoutError':
            self.formatter.print_error(f"Timeout error: {error_message}")
            self.formatter.print_info("The operation took too long to complete")
        else:
            # Generic error handling
            self.formatter.print_error(f"{error_type}: {error_message}")

            # Show traceback in debug mode
            if self.debug_mode:
                self.formatter.print_info("Stack trace (debug mode enabled):")
                traceback.print_exc()

        # Provide helpful suggestions based on error type
        self._suggest_recovery_action(error_type, error_message)

    def _suggest_recovery_action(self, error_type: str, error_message: str) -> None:
        """Suggest recovery actions based on error type

        Args:
            error_type: The type of exception that occurred
            error_message: The error message string
        """
        suggestions = {
            'FileNotFoundError': "Try using an absolute file path or check for typos",
            'PermissionError': "Try running the command with administrative privileges",
            'ConnectionError': "Check your internet connection or try again later",
            'APIError': "Verify your API keys in the .env file",
            'ValueError': "Check the format of your input values",
            'KeyError': "A required configuration key is missing",
            'JSONDecodeError': "The API returned invalid data. Try again later",
            'TimeoutError': "The operation timed out. Try using smaller input or check your connection",
            'YoutubeApiError': "There was a problem with the YouTube API. Check your API key"
        }

        if error_type in suggestions:
            self.formatter.print_info(f"Suggestion: {suggestions[error_type]}")
        else:
            self.formatter.print_info("Run with --help for usage information")


def exit_gracefully(formatter: OutputFormatter, message: Optional[str] = None, error: bool = False) -> None:
    """Exit the program gracefully with an optional message

    Args:
        formatter: Output formatter for displaying messages
        message: Optional message to display before exiting
        error: Whether this is an error exit (affects exit code)
    """
    if message:
        if error:
            formatter.print_error(message)
        else:
            formatter.print_info(message)

    sys.exit(1 if error else 0)


class SyllaboErrors:
    """Custom exception classes for Syllabo"""

    class YoutubeApiError(Exception):
        """Raised when there's an issue with YouTube API"""
        pass

    class AIServiceError(Exception):
        """Raised when there's an issue with AI service"""
        pass

    class SyllabusParsingError(Exception):
        """Raised when there's an issue parsing a syllabus"""
        pass

    class DatabaseError(Exception):
        """Raised when there's a database error"""
        pass

    class ValidationError(Exception):
        """Raised when input validation fails"""
        pass

    class ConfigurationError(Exception):
        """Raised when there's a configuration issue"""
        pass