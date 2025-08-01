import json
import os
import time
from datetime import datetime
from typing import List, Dict, Any, Optional

class SessionHistory:
    """Tracks and manages CLI session history"""

    def __init__(self, export_dir: str = 'exports'):
        """Initialize session history tracker

        Args:
            export_dir: Directory for exporting session history
        """
        self.session_start = datetime.now()
        self.export_dir = export_dir
        self.commands = []

        # Create export directory if it doesn't exist
        os.makedirs(export_dir, exist_ok=True)

    def add_command(self, command: str, args: Dict[str, Any], result: Any) -> None:
        """Add a command to the session history

        Args:
            command: The command name
            args: Command arguments
            result: Command execution result summary
        """
        entry = {
            'timestamp': datetime.now().isoformat(),
            'command': command,
            'args': args,
            'result': str(result)[:200] + '...' if len(str(result)) > 200 else str(result)
        }
        self.commands.append(entry)

    def get_session_summary(self) -> Dict[str, Any]:
        """Get a summary of the current session

        Returns:
            Dictionary with session summary data
        """
        now = datetime.now()
        duration = (now - self.session_start).total_seconds() / 60  # minutes

        return {
            'session_start': self.session_start.isoformat(),
            'session_duration_minutes': round(duration, 2),
            'commands_executed': len(self.commands),
            'command_types': self._count_command_types()
        }

    def _count_command_types(self) -> Dict[str, int]:
        """Count frequency of each command type

        Returns:
            Dictionary mapping command names to execution counts
        """
        counts = {}
        for entry in self.commands:
            command = entry['command']
            counts[command] = counts.get(command, 0) + 1
        return counts

    def export_session(self, format_type: str = 'json') -> str:
        """Export the session history to a file

        Args:
            format_type: Export format (json, csv, markdown)

        Returns:
            Path to the exported file
        """
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"session_history_{timestamp}.{format_type}"
        filepath = os.path.join(self.export_dir, filename)

        session_data = {
            'summary': self.get_session_summary(),
            'commands': self.commands
        }

        with open(filepath, 'w') as f:
            if format_type == 'json':
                json.dump(session_data, f, indent=2)
            elif format_type == 'csv':
                f.write('timestamp,command,args,result\n')
                for cmd in self.commands:
                    f.write(f"{cmd['timestamp']},{cmd['command']},{str(cmd['args']).replace(',', ';')},{cmd['result'].replace(',', ';')}\n")
            elif format_type == 'markdown':
                f.write(f"# Syllabo Session History\n\n")
                f.write(f"Session start: {self.session_start.isoformat()}\n\n")
                f.write(f"Commands executed: {len(self.commands)}\n\n")
                f.write(f"## Command History\n\n")
                for cmd in self.commands:
                    f.write(f"### {cmd['command']} ({cmd['timestamp']})\n\n")
                    f.write(f"Arguments: {cmd['args']}\n\n")
                    f.write(f"Result: {cmd['result']}\n\n")
                    f.write(f"---\n\n")

        return filepath

    def get_session_preview(self) -> str:
        """Get a preview of the session history for display

        Returns:
            A string representation of the session history
        """
        summary = self.get_session_summary()
        preview = []

        preview.append(f"Session started: {summary['session_start']}")
        preview.append(f"Duration: {summary['session_duration_minutes']} minutes")
        preview.append(f"Commands executed: {summary['commands_executed']}")
        preview.append("")
        preview.append("Command types:")
        for cmd, count in summary['command_types'].items():
            preview.append(f"  {cmd}: {count}")
        preview.append("")
        preview.append("Recent commands:")

        # Show the last 5 commands
        for cmd in self.commands[-5:]:
            preview.append(f"  {cmd['timestamp']} - {cmd['command']}")

        return "\n".join(preview)
