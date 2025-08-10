#!/usr/bin/env python3
"""
Configuration validator for Syllabo
"""

import os
import json
from typing import Dict, List, Tuple

class ConfigValidator:
    """Validate Syllabo configuration"""
    
    def __init__(self):
        self.errors = []
        self.warnings = []
    
    def validate_env_file(self) -> bool:
        """Validate .env file configuration"""
        if not os.path.exists('.env'):
            self.errors.append("Missing .env file")
            return False
        
        with open('.env', 'r') as f:
            content = f.read()
        
        # Check for placeholder values
        if 'your_youtube_api_key_here' in content:
            self.warnings.append("YouTube API key not configured")
        
        if 'your_gemini_api_key_here' in content:
            self.warnings.append("Gemini API key not configured")
        
        return len(self.errors) == 0
    
    def validate_directories(self) -> bool:
        """Validate required directories exist"""
        required_dirs = ['data', 'exports', 'logs']
        
        for directory in required_dirs:
            if not os.path.exists(directory):
                self.errors.append(f"Missing directory: {directory}")
        
        return len(self.errors) == 0
    
    def validate_database(self) -> bool:
        """Validate database configuration"""
        db_path = 'data/syllabo.db'
        
        if not os.path.exists(db_path):
            self.warnings.append("Database file doesn't exist (will be created)")
        
        return True
    
    def get_validation_report(self) -> Dict:
        """Get validation report"""
        return {
            'errors': self.errors,
            'warnings': self.warnings,
            'is_valid': len(self.errors) == 0
        }
    
    def validate_all(self) -> bool:
        """Run all validations"""
        self.validate_env_file()
        self.validate_directories()
        self.validate_database()
        
        return len(self.errors) == 0

if __name__ == '__main__':
    validator = ConfigValidator()
    is_valid = validator.validate_all()
    report = validator.get_validation_report()
    
    print("Configuration Validation Report:")
    print(f"Valid: {is_valid}")
    
    if report['errors']:
        print("\nErrors:")
        for error in report['errors']:
            print(f"  ❌ {error}")
    
    if report['warnings']:
        print("\nWarnings:")
        for warning in report['warnings']:
            print(f"  ⚠️  {warning}")
