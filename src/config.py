import os
from typing import Dict, Any

class Config:
    """Simple configuration management"""
    
    def __init__(self):
        self.cli_theme = 'minimal'
        self.export_directory = 'exports'
        
    def get_api_keys(self) -> Dict[str, str]:
        """Get API keys from environment"""
        return {
            'youtube': os.getenv('YOUTUBE_API_KEY', ''),
            'gemini': os.getenv('GEMINI_API_KEY', '')
        }
    
    def validate_api_keys(self) -> Dict[str, bool]:
        """Validate API keys"""
        keys = self.get_api_keys()
        return {
            'youtube': bool(keys['youtube']),
            'gemini': bool(keys['gemini'])
        }