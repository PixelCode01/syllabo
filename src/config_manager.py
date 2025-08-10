#!/usr/bin/env python3
"""
Configuration Manager for Syllabo
Handles API key configuration and management
"""

import os
import re
from pathlib import Path
from typing import Dict, Optional, Tuple
from rich.console import Console
from rich.prompt import Prompt, Confirm
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from .logger import SyllaboLogger

class ConfigManager:
    """Manage application configuration including API keys"""
    
    def __init__(self):
        self.console = Console()
        self.logger = SyllaboLogger("config_manager")
        self.env_file = Path('.env')
        self.env_example_file = Path('.env.example')
        
    def show_config_menu(self):
        """Show configuration management menu"""
        self.console.print(Panel(
            "[bold bright_cyan]Configuration Management[/bold bright_cyan]\n"
            "Manage your API keys and application settings",
            border_style="bright_cyan",
            title="[bold bright_white]Settings[/bold bright_white]"
        ))
        
        while True:
            self.console.print("\n[bold bright_yellow]Configuration Options:[/bold bright_yellow]")
            
            options_table = Table(show_header=False, border_style="bright_blue")
            options_table.add_column("Option", style="bright_cyan", width=8)
            options_table.add_column("Description", style="bright_white")
            
            options_table.add_row("1", "View current configuration")
            options_table.add_row("2", "Add/Update YouTube Data API key")
            options_table.add_row("3", "Add/Update Gemini API key")
            options_table.add_row("4", "Test API connections")
            options_table.add_row("5", "Reset configuration")
            options_table.add_row("6", "Export configuration")
            options_table.add_row("0", "Back to main menu")
            
            self.console.print(options_table)
            
            choice = Prompt.ask(
                "[bright_yellow]Select an option[/bright_yellow]",
                choices=["0", "1", "2", "3", "4", "5", "6"],
                default="1"
            )
            
            if choice == "0":
                break
            elif choice == "1":
                self.show_current_config()
            elif choice == "2":
                self.configure_youtube_api()
            elif choice == "3":
                self.configure_gemini_api()
            elif choice == "4":
                self.test_api_connections()
            elif choice == "5":
                self.reset_configuration()
            elif choice == "6":
                self.export_configuration()
    
    def show_current_config(self):
        """Display current configuration status"""
        self.console.print("\n[bold bright_blue]Current Configuration Status[/bold bright_blue]")
        
        config = self.load_config()
        
        config_table = Table(title="API Configuration", border_style="bright_green")
        config_table.add_column("Service", style="bright_cyan", width=20)
        config_table.add_column("Status", style="bright_white", width=15)
        config_table.add_column("Key Preview", style="dim", width=25)
        config_table.add_column("Description", style="bright_yellow")
        
        # YouTube API
        youtube_key = config.get('YOUTUBE_API_KEY', '')
        youtube_status = self._get_key_status(youtube_key)
        youtube_preview = self._get_key_preview(youtube_key)
        config_table.add_row(
            "YouTube Data API",
            youtube_status,
            youtube_preview,
            "Required for video search and analysis"
        )
        
        # Gemini API
        gemini_key = config.get('GEMINI_API_KEY', '')
        gemini_status = self._get_key_status(gemini_key)
        gemini_preview = self._get_key_preview(gemini_key)
        config_table.add_row(
            "Google Gemini API",
            gemini_status,
            gemini_preview,
            "Optional - Enhanced AI features"
        )
        
        self.console.print(config_table)
        
        # Show recommendations
        if youtube_status == "[red]Not Configured[/red]":
            self.console.print("\n[yellow]⚠️  YouTube API key is required for full video search functionality[/yellow]")
        
        if gemini_status == "[red]Not Configured[/red]":
            self.console.print("[dim]💡 Gemini API key is optional but provides enhanced AI features[/dim]")
    
    def configure_youtube_api(self):
        """Configure YouTube Data API key"""
        self.console.print("\n[bold bright_blue]YouTube Data API Configuration[/bold bright_blue]")
        
        # Show instructions
        instructions = Panel(
            "[bold bright_white]How to get YouTube Data API Key:[/bold bright_white]\n\n"
            "1. Go to [link=https://console.cloud.google.com/]Google Cloud Console[/link]\n"
            "2. Create a new project or select existing one\n"
            "3. Enable the YouTube Data API v3\n"
            "4. Go to 'Credentials' and create an API key\n"
            "5. Restrict the key to YouTube Data API v3 (recommended)\n\n"
            "[dim]The API key should look like: AIzaSyC-dK_N5TGz...[/dim]",
            border_style="bright_yellow",
            title="[bold bright_yellow]Setup Instructions[/bold bright_yellow]"
        )
        self.console.print(instructions)
        
        # Get current key
        current_config = self.load_config()
        current_key = current_config.get('YOUTUBE_API_KEY', '')
        
        if current_key and current_key != 'your_youtube_api_key_here':
            self.console.print(f"[dim]Current key: {self._get_key_preview(current_key)}[/dim]")
            
            if not Confirm.ask("[bright_yellow]Do you want to update the existing key?[/bright_yellow]"):
                return
        
        # Get new API key
        while True:
            api_key = Prompt.ask(
                "[bright_cyan]Enter your YouTube Data API key[/bright_cyan]",
                password=True
            )
            
            if not api_key:
                self.console.print("[red]API key cannot be empty[/red]")
                continue
            
            # Validate API key format
            if self._validate_youtube_api_key(api_key):
                break
            else:
                self.console.print("[red]Invalid API key format. YouTube API keys typically start with 'AIza'[/red]")
                if not Confirm.ask("[yellow]Continue anyway?[/yellow]"):
                    continue
                else:
                    break
        
        # Save the key
        if self.update_env_key('YOUTUBE_API_KEY', api_key):
            self.console.print("[bright_green]✅ YouTube API key saved successfully![/bright_green]")
            
            # Test the key
            if Confirm.ask("[bright_yellow]Would you like to test the API key now?[/bright_yellow]"):
                self._test_youtube_api(api_key)
        else:
            self.console.print("[red]❌ Failed to save API key[/red]")
    
    def configure_gemini_api(self):
        """Configure Gemini API key"""
        self.console.print("\n[bold bright_blue]Google Gemini API Configuration[/bold bright_blue]")
        
        # Show instructions
        instructions = Panel(
            "[bold bright_white]How to get Gemini API Key:[/bold bright_white]\n\n"
            "1. Go to [link=https://makersuite.google.com/app/apikey]Google AI Studio[/link]\n"
            "2. Sign in with your Google account\n"
            "3. Click 'Create API Key'\n"
            "4. Copy the generated API key\n\n"
            "[dim]The API key should look like: AIzaSyC-dK_N5TGz...[/dim]\n\n"
            "[bright_yellow]Note:[/bright_yellow] Gemini API is optional. The app works with free AI services if not configured.",
            border_style="bright_yellow",
            title="[bold bright_yellow]Setup Instructions[/bold bright_yellow]"
        )
        self.console.print(instructions)
        
        # Get current key
        current_config = self.load_config()
        current_key = current_config.get('GEMINI_API_KEY', '')
        
        if current_key and current_key != 'your_gemini_api_key_here_optional':
            self.console.print(f"[dim]Current key: {self._get_key_preview(current_key)}[/dim]")
            
            if not Confirm.ask("[bright_yellow]Do you want to update the existing key?[/bright_yellow]"):
                return
        
        # Option to skip
        if Confirm.ask("[bright_yellow]Do you want to skip Gemini API configuration? (App will use free AI services)[/bright_yellow]"):
            self.console.print("[dim]Skipping Gemini API configuration. Free AI services will be used.[/dim]")
            return
        
        # Get new API key
        while True:
            api_key = Prompt.ask(
                "[bright_cyan]Enter your Gemini API key[/bright_cyan]",
                password=True
            )
            
            if not api_key:
                if Confirm.ask("[yellow]Leave Gemini API unconfigured?[/yellow]"):
                    return
                continue
            
            # Validate API key format
            if self._validate_gemini_api_key(api_key):
                break
            else:
                self.console.print("[red]Invalid API key format. Gemini API keys typically start with 'AIza'[/red]")
                if not Confirm.ask("[yellow]Continue anyway?[/yellow]"):
                    continue
                else:
                    break
        
        # Save the key
        if self.update_env_key('GEMINI_API_KEY', api_key):
            self.console.print("[bright_green]✅ Gemini API key saved successfully![/bright_green]")
            
            # Test the key
            if Confirm.ask("[bright_yellow]Would you like to test the API key now?[/bright_yellow]"):
                self._test_gemini_api(api_key)
        else:
            self.console.print("[red]❌ Failed to save API key[/red]")
    
    def test_api_connections(self):
        """Test all configured API connections"""
        self.console.print("\n[bold bright_blue]Testing API Connections[/bold bright_blue]")
        
        config = self.load_config()
        
        # Test YouTube API
        youtube_key = config.get('YOUTUBE_API_KEY', '')
        if youtube_key and youtube_key != 'your_youtube_api_key_here':
            self.console.print("[bright_cyan]Testing YouTube Data API...[/bright_cyan]")
            self._test_youtube_api(youtube_key)
        else:
            self.console.print("[yellow]YouTube API key not configured - skipping test[/yellow]")
        
        # Test Gemini API
        gemini_key = config.get('GEMINI_API_KEY', '')
        if gemini_key and gemini_key != 'your_gemini_api_key_here_optional':
            self.console.print("\n[bright_cyan]Testing Gemini API...[/bright_cyan]")
            self._test_gemini_api(gemini_key)
        else:
            self.console.print("[yellow]Gemini API key not configured - skipping test[/yellow]")
        
        # Test free AI services
        self.console.print("\n[bright_cyan]Testing free AI services...[/bright_cyan]")
        self._test_free_ai_services()
    
    def reset_configuration(self):
        """Reset configuration to defaults"""
        if not Confirm.ask("[red]Are you sure you want to reset all configuration? This will remove all API keys.[/red]"):
            return
        
        try:
            # Create default .env from example
            if self.env_example_file.exists():
                with open(self.env_example_file, 'r', encoding='utf-8') as f:
                    example_content = f.read()
                
                with open(self.env_file, 'w', encoding='utf-8') as f:
                    f.write(example_content)
                
                self.console.print("[bright_green]✅ Configuration reset to defaults[/bright_green]")
            else:
                # Create minimal .env
                default_content = """YOUTUBE_API_KEY=your_youtube_api_key_here
GEMINI_API_KEY=your_gemini_api_key_here_optional"""
                
                with open(self.env_file, 'w', encoding='utf-8') as f:
                    f.write(default_content)
                
                self.console.print("[bright_green]✅ Configuration reset with default template[/bright_green]")
                
        except Exception as e:
            self.console.print(f"[red]❌ Failed to reset configuration: {e}[/red]")
    
    def export_configuration(self):
        """Export configuration (without sensitive data)"""
        config = self.load_config()
        
        export_data = {}
        for key, value in config.items():
            if 'API_KEY' in key:
                export_data[key] = "CONFIGURED" if value and not value.startswith('your_') else "NOT_CONFIGURED"
            else:
                export_data[key] = value
        
        export_table = Table(title="Configuration Export", border_style="bright_blue")
        export_table.add_column("Setting", style="bright_cyan")
        export_table.add_column("Status", style="bright_white")
        
        for key, value in export_data.items():
            export_table.add_row(key, str(value))
        
        self.console.print(export_table)
        
        if Confirm.ask("[bright_yellow]Save configuration status to file?[/bright_yellow]"):
            try:
                import json
                from datetime import datetime
                
                export_file = f"config_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
                with open(export_file, 'w', encoding='utf-8') as f:
                    json.dump({
                        'timestamp': datetime.now().isoformat(),
                        'configuration': export_data
                    }, f, indent=2)
                
                self.console.print(f"[bright_green]✅ Configuration exported to {export_file}[/bright_green]")
            except Exception as e:
                self.console.print(f"[red]❌ Failed to export configuration: {e}[/red]")
    
    def load_config(self) -> Dict[str, str]:
        """Load configuration from .env file"""
        config = {}
        
        if not self.env_file.exists():
            return config
        
        try:
            with open(self.env_file, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#') and '=' in line:
                        key, value = line.split('=', 1)
                        config[key.strip()] = value.strip()
        except Exception as e:
            self.logger.error(f"Failed to load config: {e}")
        
        return config
    
    def update_env_key(self, key: str, value: str) -> bool:
        """Update a specific key in the .env file"""
        try:
            # Ensure .env file exists
            if not self.env_file.exists():
                self.env_file.touch()
            
            # Read current content
            lines = []
            if self.env_file.stat().st_size > 0:
                with open(self.env_file, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
            
            # Update or add the key
            key_found = False
            for i, line in enumerate(lines):
                if line.strip().startswith(f"{key}="):
                    lines[i] = f"{key}={value}\n"
                    key_found = True
                    break
            
            if not key_found:
                lines.append(f"{key}={value}\n")
            
            # Write back to file
            with open(self.env_file, 'w', encoding='utf-8') as f:
                f.writelines(lines)
            
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to update env key {key}: {e}")
            return False
    
    def _get_key_status(self, key: str) -> str:
        """Get the status of an API key"""
        if not key or key.startswith('your_'):
            return "[red]Not Configured[/red]"
        elif len(key) < 10:
            return "[yellow]Invalid[/yellow]"
        else:
            return "[green]Configured[/green]"
    
    def _get_key_preview(self, key: str) -> str:
        """Get a preview of the API key (first 8 chars + ...)"""
        if not key or key.startswith('your_'):
            return "[dim]Not set[/dim]"
        elif len(key) < 8:
            return "[dim]Invalid key[/dim]"
        else:
            return f"{key[:8]}..."
    
    def _validate_youtube_api_key(self, key: str) -> bool:
        """Validate YouTube API key format"""
        # YouTube API keys typically start with 'AIza' and are 39 characters long
        return key.startswith('AIza') and len(key) == 39
    
    def _validate_gemini_api_key(self, key: str) -> bool:
        """Validate Gemini API key format"""
        # Gemini API keys also typically start with 'AIza'
        return key.startswith('AIza') and len(key) >= 35
    
    def _test_youtube_api(self, api_key: str):
        """Test YouTube API key"""
        try:
            import requests
            
            # Test with a simple API call
            url = "https://www.googleapis.com/youtube/v3/search"
            params = {
                'part': 'snippet',
                'q': 'test',
                'maxResults': 1,
                'key': api_key
            }
            
            with self.console.status("[bright_cyan]Testing YouTube API..."):
                response = requests.get(url, params=params, timeout=10)
            
            if response.status_code == 200:
                self.console.print("[bright_green]✅ YouTube API key is working![/bright_green]")
            elif response.status_code == 403:
                error_data = response.json()
                if 'quotaExceeded' in str(error_data):
                    self.console.print("[yellow]⚠️  YouTube API key is valid but quota exceeded[/yellow]")
                else:
                    self.console.print("[red]❌ YouTube API key is invalid or restricted[/red]")
            else:
                self.console.print(f"[red]❌ YouTube API test failed: HTTP {response.status_code}[/red]")
                
        except Exception as e:
            self.console.print(f"[red]❌ YouTube API test failed: {e}[/red]")
    
    def _test_gemini_api(self, api_key: str):
        """Test Gemini API key"""
        try:
            import requests
            
            # Test with a simple API call
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={api_key}"
            
            data = {
                "contents": [{
                    "parts": [{
                        "text": "Hello, please respond with 'API working'"
                    }]
                }]
            }
            
            with self.console.status("[bright_cyan]Testing Gemini API..."):
                response = requests.post(url, json=data, timeout=15)
            
            if response.status_code == 200:
                self.console.print("[bright_green]✅ Gemini API key is working![/bright_green]")
            elif response.status_code == 403:
                self.console.print("[red]❌ Gemini API key is invalid or access denied[/red]")
            elif response.status_code == 429:
                self.console.print("[yellow]⚠️  Gemini API key is valid but rate limited[/yellow]")
            else:
                self.console.print(f"[red]❌ Gemini API test failed: HTTP {response.status_code}[/red]")
                
        except Exception as e:
            self.console.print(f"[red]❌ Gemini API test failed: {e}[/red]")
    
    def _test_free_ai_services(self):
        """Test free AI services availability"""
        try:
            # Import AI client to test free services
            from .ai_client import AIClient
            
            ai_client = AIClient()
            
            with self.console.status("[bright_cyan]Testing free AI services..."):
                # This will test the free services
                test_result = ai_client._get_intelligent_completion("Test prompt")
            
            if test_result and not test_result.startswith("Error:"):
                self.console.print("[bright_green]✅ Free AI services are available![/bright_green]")
            else:
                self.console.print("[yellow]⚠️  Free AI services may have limited availability[/yellow]")
                
        except Exception as e:
            self.console.print(f"[red]❌ Free AI services test failed: {e}[/red]")