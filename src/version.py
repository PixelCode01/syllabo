"""
Version information for Syllabo
"""

VERSION = "1.2.0"
__version__ = VERSION

# Version history
VERSION_HISTORY = {
    "1.2.0": {
        "date": "2025-08-11",
        "features": [
            "Enhanced video search with 70% faster performance",
            "Improved quiz generation from content",
            "Comprehensive syllabus analysis with detailed summaries",
            "First-run setup with Gemini API configuration",
            "Multi-line text input for better user experience",
            "Fast video filtering and ranking algorithms",
            "Educational content scoring system",
            "Caching for video details and search results",
            "Timeout protection for API calls",
            "Better educational video detection"
        ]
    },
    "1.1.0": {
        "date": "2025-08-10", 
        "features": [
            "Major fixes and improvements",
            "Fixed encoding issues in file operations",
            "Enhanced error handling throughout application",
            "Added comprehensive input validation",
            "Implemented performance monitoring",
            "Created configuration validation system"
        ]
    },
    "1.0.0": {
        "date": "2025-08-09",
        "features": [
            "Initial release",
            "Syllabus analysis and topic extraction",
            "Quiz generation from topics and content",
            "Video search and analysis",
            "Study goals management",
            "Spaced repetition system",
            "Progress tracking dashboard",
            "Multi-platform learning resource search"
        ]
    }
}

def get_version():
    """Get current version string"""
    return VERSION

def get_version_info():
    """Get detailed version information"""
    return {
        "version": VERSION,
        "history": VERSION_HISTORY.get(VERSION, {}),
        "latest_features": VERSION_HISTORY.get(VERSION, {}).get("features", [])
    }