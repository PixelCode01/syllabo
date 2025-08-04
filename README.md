# Syllabo

AI-powered learning assistant that analyzes course syllabi and finds educational resources. Features an interactive terminal interface with rich colors, progress tracking, quiz generation, and comprehensive study management tools.

## Features

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

- `analyze` - Process syllabus and find learning resources with AI
- `quiz` - Generate and take interactive quizzes with instant feedback
- `progress` - View visual learning progress and analytics dashboard
- `goals` - Manage study goals and track milestones
- `platforms` - Search across multiple learning platforms
- `bookmarks` - Manage video bookmarks with smart organization
- `session` - Start Pomodoro study sessions with focus tracking
- `review` - Spaced repetition system for optimal learning retention

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