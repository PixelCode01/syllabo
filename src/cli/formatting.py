from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress, TextColumn, BarColumn, TaskProgressColumn, TimeRemainingColumn
from rich.prompt import Confirm
from rich import box
from typing import List, Dict, Any, Optional

class OutputFormatter:
    """Handles consistent formatting for CLI output"""

    def __init__(self, theme: str = 'minimal'):
        """Initialize the formatter with a theme

        Args:
            theme: Either 'minimal' or 'high-contrast'
        """
        self.theme = theme
        self.console = Console()

        # Define theme colors
        if theme == 'minimal':
            self.colors = {
                'title': 'bold blue',
                'success': 'green',
                'error': 'red',
                'warning': 'yellow',
                'info': 'cyan',
                'heading': 'bold',
                'subheading': 'italic',
                'highlight': 'bold cyan',
            }
        else:  # high-contrast
            self.colors = {
                'title': 'bold white on blue',
                'success': 'bold white on green',
                'error': 'bold white on red',
                'warning': 'black on yellow',
                'info': 'white on cyan',
                'heading': 'bold white',
                'subheading': 'bold gray',
                'highlight': 'bold white on cyan',
            }

    def print_title(self, text: str) -> None:
        """Print a title with appropriate styling"""
        self.console.print(f"\n{text}", style=self.colors['title'])

    def print_error(self, text: str) -> None:
        """Print an error message"""
        self.console.print(f"Error: {text}", style=self.colors['error'])

    def print_warning(self, text: str) -> None:
        """Print a warning message"""
        self.console.print(f"Warning: {text}", style=self.colors['warning'])

    def print_success(self, text: str) -> None:
        """Print a success message"""
        self.console.print(f"Success: {text}", style=self.colors['success'])

    def print_info(self, text: str) -> None:
        """Print an informational message"""
        self.console.print(f"Info: {text}", style=self.colors['info'])

    def create_table(self, title: str, columns: List[str]) -> Table:
        """Create a rich table with consistent styling

        Args:
            title: The table title
            columns: List of column names

        Returns:
            A rich Table object ready to have rows added
        """
        table = Table(title=title, box=box.SIMPLE)

        for column in columns:
            table.add_column(column, style=self.colors['heading'])

        return table

    def create_panel(self, title: str, content: str) -> Panel:
        """Create a rich panel with consistent styling

        Args:
            title: The panel title
            content: The content to display in the panel

        Returns:
            A rich Panel object
        """
        return Panel(content, title=title, border_style=self.colors['heading'])

    def create_progress_bar(self) -> Progress:
        """Create a progress bar with consistent styling

        Returns:
            A rich Progress object
        """
        progress = Progress(
            TextColumn("[bold blue]{task.description}"),
            BarColumn(),
            TaskProgressColumn(),
            TimeRemainingColumn(),
        )
        
        # Add a dummy context manager for compatibility
        progress.dummy = lambda: DummyContextManager()
        return progress
        
class DummyContextManager:
    """A dummy context manager that does nothing"""
    def __enter__(self):
        return self
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def confirm_action(self, prompt: str) -> bool:
        """Ask for user confirmation

        Args:
            prompt: The confirmation prompt text

        Returns:
            True if user confirms, False otherwise
        """
        return Confirm.ask(prompt)

    def print_summary_panel(self, title: str, data: Dict[str, Any]) -> None:
        """Print a summary panel with key-value data

        Args:
            title: The panel title
            data: Dictionary of data to display
        """
        content = "\n".join([f"{k}: {v}" for k, v in data.items()])
        panel = self.create_panel(title, content)
        self.console.print(panel)

    def show_export_preview(self, data: Any, format_type: str) -> bool:
        """Show a preview of data to be exported and confirm

        Args:
            data: The data to be exported
            format_type: The export format (json, csv, etc.)

        Returns:
            True if user confirms export, False otherwise
        """
        preview_panel = self.create_panel(
            f"Export Preview ({format_type})", 
            str(data)[:500] + "..." if len(str(data)) > 500 else str(data)
        )
        self.console.print(preview_panel)
        return self.confirm_action("Proceed with export?")

    def print_tabular_data(self, title: str, headers: List[str], rows: List[List[Any]]) -> None:
        """Print data in a nicely formatted table

        Args:
            title: The table title
            headers: List of column headers
            rows: List of rows, each containing a list of values
        """
        table = self.create_table(title, headers)

        for row in rows:
            table.add_row(*[str(item) for item in row])

        self.console.print(table)
