# Syllabo

AI-powered learning assistant that analyzes course syllabi and finds educational resources. Features an interactive terminal interface with rich colors, progress tracking, quiz generation, and comprehensive study management tools.

## Features

### Core Learning Features
- **Interactive Terminal UI**: Rich, colorful interface with intuitive navigation
- **Syllabus Analysis**: Extract topics from PDF or text files using AI
- **Resource Discovery**: Find YouTube videos, courses, and educational content
- **Interactive Quizzes**: Generate and take AI-powered quizzes with instant feedback
- **Progress Dashboard**: Visual progress tracking with charts and statistics
- **Study Sessions**: Pomodoro timer with focus tracking and break management
- **Goals Management**: Set and track daily, weekly, and monthly learning goals
- **Smart Bookmarks**: Save video timestamps with notes and tags
- **Spaced Repetition**: Scientific review scheduling for better retention
- **Multi-Platform Search**: Search across educational platforms simultaneously

### New Enhanced Features
- **Smart Video Analysis**: AI-powered analysis of educational videos with topic coverage assessment
- **Intelligent Notes Generation**: Automatically generate study notes and questions from video content
- **Resource Finder**: Comprehensive database of books, courses, and learning materials with free/paid filtering
- **Advanced Spaced Repetition**: Full Leitner system implementation with analytics and progress tracking
- **Topic Coverage Analysis**: Detailed analysis of what topics are covered and missing in educational content
- **Learning Path Optimization**: AI-recommended study sequences based on content analysis
- **User Preference System**: Customizable note generation and learning preferences

## Installation

```bash
git clone https://github.com/PixelCode01/syllabo.git
cd syllabo
pip install -r requirements.txt
```

## Configuration

Create a `.env` file for optional API keys:

```bash
# Optional - for enhanced AI features
GEMINI_API_KEY=your_key_here
YOUTUBE_API_KEY=your_key_here
```

The application works without API keys using free AI services and web scraping.

## Usage

### Interactive Mode (Recommended)
```bash
python main.py
```

The interactive mode provides a user-friendly menu system with:
- Colorful, intuitive interface
- Step-by-step guided workflows
- Real-time progress indicators
- Enhanced error handling and feedback
- Smart prompts with validation

### Command Line Interface
```bash
# Analyze syllabus with enhanced UI
python main.py analyze --file syllabus.pdf --search-videos --print-results

# Generate interactive quiz
python main.py quiz generate --topic "Machine Learning" --num-questions 5

# View visual progress dashboard
python main.py progress

# Start focused study session
python main.py session start --topic "Python" --duration 25

# Manage learning goals
python main.py goals create --title "Daily Study" --type daily --target 30 --unit minutes

# Review topics with spaced repetition
python main.py review due --notify
```

## Available Commands

### Core Commands
- `analyze` - Process syllabus and find learning resources with AI
- `quiz` - Generate and take interactive quizzes with instant feedback
- `progress` - View visual learning progress and analytics dashboard
- `goals` - Manage study goals and track milestones
- `platforms` - Search across multiple learning platforms
- `bookmarks` - Manage video bookmarks with smart organization
- `session` - Start Pomodoro study sessions with focus tracking
- `review` - Spaced repetition system for optimal learning retention

### New Enhanced Commands
- `videos` - Smart video search and analysis with topic coverage assessment
- `resources` - Find books, courses, and learning materials with preference filtering
- `notes` - Generate study notes and questions from educational content

### Integrated Analysis Workflow
The `analyze` command now includes a comprehensive learning workflow that integrates all new features:
- **Automatic Topic Processing**: After extracting topics from your syllabus, the system offers to create a complete learning plan
- **Video Analysis Integration**: Find and analyze educational videos for each topic with AI-powered coverage assessment
- **Resource Discovery Integration**: Automatically find books, courses, and learning materials for all topics
- **Notes Generation Integration**: Generate study notes and questions from recommended video content
- **Spaced Repetition Integration**: Automatically add topics to the spaced repetition system for optimal retention
- **Personalized Preferences**: Customize the analysis based on your learning style and resource preferences

## New Features Guide

### Smart Video Analysis
Find and analyze educational videos with AI-powered topic coverage assessment:
- Ask user preferences for learning style (single video vs multiple videos vs playlists)
- Analyze video content to determine what topics are covered and missing
- Provide recommendations for optimal learning paths
- Generate study notes and questions for recommended content

### Resource Finder
Comprehensive resource discovery for any topic:
- Extensive database of books, courses, and learning materials
- Filter by free/paid preferences
- Topic coverage analysis showing what's included and missing
- Alternative suggestions for topics with limited resources

### Enhanced Notes Generation
AI-powered study material creation:
- User preference system for note style and question types
- Generate detailed study notes from video content
- Create relevant questions for review and retention
- Extract key concepts and provide study tips

### Advanced Spaced Repetition
Full implementation of the Leitner system:
- Adaptive intervals based on performance (1, 3, 5, 11, 25, 44, 88 days)
- Comprehensive learning analytics and progress tracking
- Review history and retention rate analysis
- Export/import functionality for data backup

## Usage Examples

### Comprehensive Syllabus Analysis (Integrated Workflow)
```bash
python main.py
# Select option 1 (Analyze Syllabus)
# Choose file or text input
# The system will automatically offer to:
# - Find and analyze educational videos for each topic
# - Discover books, courses, and learning materials
# - Generate study notes and questions from video content
# - Add topics to spaced repetition system
# - Create a personalized learning plan
```

### Individual Feature Usage
```bash
# Smart video analysis only
python main.py
# Select option 9 (Smart Video Analysis)

# Resource discovery only  
python main.py
# Select option 10 (Resource Finder)

# Notes generation only
python main.py
# Select option 11 (Generate Study Notes)
```

## User Interface Highlights

- **Rich Terminal Experience**: Colorful, modern interface with progress bars and animations
- **Interactive Prompts**: Smart input validation and helpful suggestions
- **Visual Progress Tracking**: Charts, graphs, and progress indicators
- **Error Handling**: Clear, actionable error messages with recovery suggestions
- **Responsive Design**: Adapts to different terminal sizes and preferences

## Requirements

- Python 3.7+
- Dependencies listed in `requirements.txt`
- Optional: API keys for enhanced features

## Licenses
MIT License - see LICENSE file for details.