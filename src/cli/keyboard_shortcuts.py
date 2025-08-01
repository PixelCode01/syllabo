import sys
from prompt_toolkit.keys import Keys
from prompt_toolkit.key_binding import KeyBindings
from typing import Dict, Any, Callable, List

class KeyboardShortcutManager:
    """Manages keyboard shortcuts for interactive CLI mode"""

    def __init__(self):
        """Initialize keyboard shortcut manager"""
        self.bindings = KeyBindings()
        self._setup_default_bindings()

    def _setup_default_bindings(self) -> None:
        """Set up default key bindings"""
        # Exit application
        @self.bindings.add('c-c')
        @self.bindings.add('c-d')
        def _(event):
            """Exit when Control-C or Control-D is pressed"""
            event.app.exit()

        # Show help
        @self.bindings.add('f1')
        def _(event):
            """Show help when F1 is pressed"""
            event.app.show_help = True

        # Clear screen
        @self.bindings.add('c-l')
        def _(event):
            """Clear screen when Control-L is pressed"""
            event.app.renderer.clear()
from prompt_toolkit.keys import Keys
from prompt_toolkit.key_binding import KeyBindings
from typing import Dict, Any, Callable, List, Optional

class KeyboardShortcutManager:
    """Manages keyboard shortcuts for interactive CLI mode"""

    def __init__(self):
        """Initialize keyboard shortcut manager"""
        self.bindings = KeyBindings()
        self._setup_default_bindings()

    def _setup_default_bindings(self) -> None:
        """Set up default key bindings"""
        # Exit application
        @self.bindings.add('c-c')
        def _(event):
            """Exit when Control-C is pressed"""
            event.app.exit(result=None)

        # Exit application (alternate)
        @self.bindings.add('c-d')
        def _(event):
            """Exit when Control-D is pressed"""
            event.app.exit(result=None)

        # Show help
        @self.bindings.add('f1')
        def _(event):
            """Show help when F1 is pressed"""
            # Set a flag that the main loop will check
            event.app.current_buffer.document = event.app.current_buffer.document.set_text('')
            event.app.exit(result='help')

        # Clear screen
        @self.bindings.add('c-l')
        def _(event):
            """Clear screen when Control-L is pressed"""
            event.app.renderer.clear()

        # Command history
        @self.bindings.add('c-r')
        def _(event):
            """Search command history when Control-R is pressed"""
            event.app.current_buffer.start_history_lines_completion()

    def add_binding(self, key: str, handler: Callable) -> None:
        """Add a custom key binding

        Args:
            key: Key combination (e.g., 'c-s', 'f5')
            handler: Function to call when key is pressed
        """
        @self.bindings.add(key)
        def _(event):
            handler(event)

    def get_bindings(self) -> KeyBindings:
        """Get the key bindings object

        Returns:
            KeyBindings object with all registered bindings
        """
        return self.bindings

    def get_help_text(self) -> str:
        """Get help text for all keyboard shortcuts

        Returns:
            Formatted string with keyboard shortcut help
        """
        shortcuts = [
            ("Ctrl+C or Ctrl+D", "Exit the application"),
            ("F1", "Show this help screen"),
            ("Ctrl+L", "Clear the screen"),
            ("Ctrl+R", "Search command history"),
            ("↑/↓", "Navigate command history"),
            ("Tab", "Auto-complete command"),
            ("Ctrl+A", "Move to beginning of line"),
            ("Ctrl+E", "Move to end of line"),
            ("Ctrl+K", "Delete from cursor to end of line"),
            ("Ctrl+U", "Delete from cursor to beginning of line"),
            ("Ctrl+W", "Delete word before cursor"),
            ("Alt+B", "Move back one word"),
            ("Alt+F", "Move forward one word"),
        ]

        # Format as a help screen
        lines = []
        max_key_length = max(len(key) for key, _ in shortcuts)

        for key, description in shortcuts:
            padding = " " * (max_key_length - len(key) + 2)
            lines.append(f"{key}{padding}{description}")

        return "\n".join(lines)
        # Command history
        @self.bindings.add('c-r')
        def _(event):
            """Search command history when Control-R is pressed"""
            event.app.show_history_search = True

    def add_binding(self, key: str, handler: Callable) -> None:
        """Add a custom key binding

        Args:
            key: Key combination (e.g., 'c-s', 'f5')
            handler: Function to call when key is pressed
        """
        @self.bindings.add(key)
        def _(event):
            handler(event)

    def get_bindings(self) -> KeyBindings:
        """Get the key bindings object

        Returns:
            KeyBindings object with all registered bindings
        """
        return self.bindings

    def get_help_text(self) -> str:
        """Get help text for all keyboard shortcuts

        Returns:
            Formatted string with keyboard shortcut help
        """
        shortcuts = [
            ("Ctrl+C or Ctrl+D", "Exit the application"),
            ("F1", "Show this help screen"),
            ("Ctrl+L", "Clear the screen"),
            ("Ctrl+R", "Search command history"),
            ("↑/↓", "Navigate command history"),
            ("Tab", "Auto-complete command"),
            ("Ctrl+A", "Move to beginning of line"),
            ("Ctrl+E", "Move to end of line"),
            ("Ctrl+K", "Delete from cursor to end of line"),
            ("Ctrl+U", "Delete from cursor to beginning of line"),
            ("Ctrl+W", "Delete word before cursor"),
            ("Alt+B", "Move back one word"),
            ("Alt+F", "Move forward one word"),
        ]

        # Format as a help screen
        lines = ["Keyboard Shortcuts:", "-" * 50]
        max_key_length = max(len(key) for key, _ in shortcuts)

        for key, description in shortcuts:
            padding = " " * (max_key_length - len(key) + 2)
            lines.append(f"{key}{padding}{description}")

        return "\n".join(lines)
