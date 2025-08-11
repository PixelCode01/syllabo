#!/usr/bin/env python3
"""
Setup Manager for Syllabo - Handles first-run configuration
"""

import os
import sys
from pathlib import Path
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt, Confirm
from rich.text import Text
from rich.align import Align
from .logger import SyllaboLogger

class SetupManager:
    """Manages first-run setup and configuration"""
    
    def __init__(self):
        self.console = Console()
        self.logger = SyllaboLogger("setup_manager")
        self.setup_file = Path(".syllabo_setup_complete")
        self.env_file = Path(".env")
    
    def is_first_run(self) -> bool:
        """Check if this is the first run"""
        return not self.setup_file.exists()
    
    def mark_setup_complete(self):
        """Mark setup as completed"""
        try:
            self.setup_file.touch()
            self.logger.info("Setup marked as complete")
        except Exception as e:
            self.logger.error(f"Failed to mark setup complete: {e}")
    
    async def run_first_time_setup(self) -> bool:
        """Run first-time setup wizard"""
        try:
            self._show_welcome_banner()
            
            # Check if .env exists
            if not self.env_file.exists():
                self._create_env_file()
            
            # Setup Gemini API key
            await self._setup_gemini_api()
            
            # Show completion message
            self._show_setup_complete()
            
            # Mark setup as complete
            self.mark_setup_complete()
            
            return True
            
        except KeyboardInterrupt:
            self.console.print("\n[yellow]Setup cancelled by user[/yellow]")
            return False
        except Exception as e:
            self.console.print(f"\n[red]Setup error: {e}[/red]")
            self.logger.error(f"Setup failed: {e}")
            return False
    
    def _show_welcome_banner(self):
        """Show welcome banner for first-time setup"""
        welcome_text = Text()
        welcome_text.append("🎉 Welcome to Syllabo! 🎉", style="bold bright_cyan")
        welcome_text.append("\n\n")
        welcome_text.append("AI-Powered Learning Assistant", style="bold white")
        welcome_text.append("\n\n")
        welcome_text.append("Let's get you set up for the best experience!", style="bright_white")
        
        welcome_panel = Panel(
            Align.center(welcome_text),
            border_style="bright_cyan",
            padding=(1, 2),
            title="[bold bright_blue]First Time Setup[/bold bright_blue]",
            title_align="center"
        )
        
        self.console.print(welcome_panel)
        self.console.print()
    
    def _create_env_file(self):
        """Create .env file from .env.example"""
        try:
            env_example = Path(".env.example")
            if env_example.exists():
                # Copy .env.example to .env
                with open(env_example, 'r') as src:
                    content = src.read()
                
                with open(self.env_file, 'w') as dst:
                    dst.write(content)
                
                self.console.print("[green]✅ Created .env configuration file[/green]")
            else:
                # Create basic .env file
                basic_env = """GEMINI_API_KEY=your_gemini_api_key_here_optional
YOUTUBE_API_KEY=your_youtube_api_key_here
"""
                with open(self.env_file, 'w') as f:
                    f.write(basic_env)
                
                self.console.print("[green]✅ Created basic .env configuration file[/green]")
                
        except Exception as e:
            self.console.print(f"[yellow]Warning: Could not create .env file: {e}[/yellow]")
    
    async def _setup_gemini_api(self):
        """Setup Gemini API key with user interaction"""
        self.console.print()
        
        # Show Gemini API information
        gemini_info = Panel(
            """[bold bright_white]🤖 Gemini AI Setup (Recommended)[/bold bright_white]

[bright_white]Why use Gemini AI?[/bright_white]
• [green]Higher quality responses[/green] - More accurate and detailed
• [green]Better quiz generation[/green] - More relevant questions
• [green]Advanced analysis[/green] - Superior content understanding
• [green]Faster processing[/green] - Optimized for educational content

[bright_white]How to get your API key:[/bright_white]
1. Visit: [link]https://makersuite.google.com/app/apikey[/link]
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy the generated key

[dim]Note: Gemini API has a generous free tier. If you skip this, 
Syllabo will use free AI services (which work but are less reliable).[/dim]""",
            border_style="bright_blue",
            title="[bold bright_cyan]Gemini AI Configuration[/bold bright_cyan]",
            title_align="center"
        )
        
        self.console.print(gemini_info)
        self.console.print()
        
        # Ask if user wants to configure Gemini
        setup_gemini = Confirm.ask(
            "[bright_yellow]Would you like to set up Gemini AI now?[/bright_yellow]",
            default=True
        )
        
        if setup_gemini:
            await self._configure_gemini_key()
        else:
            self.console.print("[yellow]⏭️  Skipping Gemini setup - you can configure it later in .env file[/yellow]")
            self.console.print("[dim]Syllabo will use free AI services for now.[/dim]")
    
    async def _configure_gemini_key(self):
        """Configure Gemini API key"""
        self.console.print()
        
        while True:
            # Get API key from user
            api_key = Prompt.ask(
                "[bright_cyan]Please paste your Gemini API key[/bright_cyan]",
                password=True  # Hide the key while typing
            )
            
            if not api_key or api_key.strip() == "":
                skip = Confirm.ask("[yellow]No key entered. Skip Gemini setup?[/yellow]", default=False)
                if skip:
                    break
                continue
            
            api_key = api_key.strip()
            
            # Show the key (masked) for confirmation
            masked_key = self._mask_api_key(api_key)
            self.console.print(f"[bright_white]API Key entered:[/bright_white] [dim]{masked_key}[/dim]")
            
            # Confirm the key
            confirm = Confirm.ask("[bright_yellow]Is this correct?[/bright_yellow]", default=True)
            
            if confirm:
                # Test the API key
                self.console.print("[bright_cyan]🔍 Testing API key...[/bright_cyan]")
                
                if await self._test_gemini_key(api_key):
                    # Save to .env file
                    self._save_gemini_key(api_key)
                    self.console.print("[bright_green]✅ Gemini API key configured successfully![/bright_green]")
                    self.console.print("[dim]Syllabo will now use Gemini AI for better responses.[/dim]")
                    break
                else:
                    self.console.print("[bright_red]❌ API key test failed[/bright_red]")
                    retry = Confirm.ask("[yellow]Would you like to try a different key?[/yellow]", default=True)
                    if not retry:
                        self.console.print("[yellow]⏭️  Skipping Gemini setup[/yellow]")
                        break
            # If not confirmed, loop back to enter key again
    
    def _mask_api_key(self, api_key: str) -> str:
        """Mask API key for display"""
        if len(api_key) <= 8:
            return "*" * len(api_key)
        
        return api_key[:4] + "*" * (len(api_key) - 8) + api_key[-4:]
    
    async def _test_gemini_key(self, api_key: str) -> bool:
        """Test if Gemini API key works"""
        try:
            # Use requests instead of aiohttp for simplicity
            import requests
            
            url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent"
            
            headers = {
                'Content-Type': 'application/json',
            }
            
            data = {
                "contents": [{
                    "parts": [{
                        "text": "Hello, please respond with 'API key working'"
                    }]
                }]
            }
            
            response = requests.post(
                f"{url}?key={api_key}",
                headers=headers,
                json=data,
                timeout=10
            )
            
            if response.status_code == 200:
                result = response.json()
                if 'candidates' in result:
                    return True
            
            return False
            
        except Exception as e:
            self.logger.error(f"Gemini API test failed: {e}")
            return False
    
    def _save_gemini_key(self, api_key: str):
        """Save Gemini API key to .env file"""
        try:
            # Read current .env content
            env_content = ""
            if self.env_file.exists():
                with open(self.env_file, 'r') as f:
                    env_content = f.read()
            
            # Update or add GEMINI_API_KEY
            lines = env_content.split('\n')
            updated = False
            
            for i, line in enumerate(lines):
                if line.startswith('GEMINI_API_KEY='):
                    lines[i] = f'GEMINI_API_KEY={api_key}'
                    updated = True
                    break
            
            if not updated:
                lines.append(f'GEMINI_API_KEY={api_key}')
            
            # Write back to file
            with open(self.env_file, 'w') as f:
                f.write('\n'.join(lines))
            
            self.logger.info("Gemini API key saved to .env file")
            
        except Exception as e:
            self.console.print(f"[red]Error saving API key: {e}[/red]")
            self.logger.error(f"Failed to save API key: {e}")
    
    def _show_setup_complete(self):
        """Show setup completion message"""
        self.console.print()
        
        complete_text = Text()
        complete_text.append("🎉 Setup Complete! 🎉", style="bold bright_green")
        complete_text.append("\n\n")
        complete_text.append("Syllabo is now ready to use!", style="bright_white")
        complete_text.append("\n\n")
        complete_text.append("Quick Start:", style="bold bright_cyan")
        complete_text.append("\n")
        complete_text.append("• Try the interactive quiz generator", style="bright_white")
        complete_text.append("\n")
        complete_text.append("• Analyze your syllabus files", style="bright_white")
        complete_text.append("\n")
        complete_text.append("• Set up study goals and tracking", style="bright_white")
        
        complete_panel = Panel(
            Align.center(complete_text),
            border_style="bright_green",
            padding=(1, 2),
            title="[bold bright_white]Ready to Learn![/bold bright_white]",
            title_align="center"
        )
        
        self.console.print(complete_panel)
        self.console.print()
        
        # Show next steps
        self.console.print("[dim]💡 Tip: You can reconfigure settings anytime by editing the .env file[/dim]")
        self.console.print()