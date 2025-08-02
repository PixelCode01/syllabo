# Syllabo

AI-powered learning assistant that analyzes course syllabi and finds educational resources. Includes quiz generation, progress tracking, study sessions, and spaced repetition learning.

## Features

- **Syllabus Analysis**: Extract topics from PDF or text files using AI
- **Resource Discovery**: Find YouTube videos, courses, and educational content
- **Interactive Quizzes**: Generate and take AI-powered quizzes from content
- **Progress Dashboard**: Track learning progress, streaks, and performance
- **Study Sessions**: Pomodoro timer with focus tracking
- **Goals Management**: Set and track daily, weekly, and monthly learning goals
- **Smart Bookmarks**: Save video timestamps with notes and tags
- **Spaced Repetition**: Scientific review scheduling for better retention

## Installation

```bash
git clone https://github.com/PixelCode01/syllabo
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

### Interactive Mode
```bash
python main.py
```

### Command Line
```bash
# Analyze syllabus
python main.py analyze --file syllabus.pdf --search-videos --print-results

# Generate quiz
python main.py quiz generate --topic "Machine Learning" --num-questions 5

# View progress
python main.py progress

# Start study session
python main.py session start --topic "Python" --duration 25

# Manage goals
python main.py goals create --title "Daily Study" --type daily --target 30 --unit minutes
```

## Available Commands

- `analyze` - Process syllabus and find learning resources
- `quiz` - Generate and take interactive quizzes  
- `progress` - View learning progress and analytics
- `goals` - Manage study goals and milestones
- `platforms` - Search across learning platforms
- `bookmarks` - Manage video bookmarks and notes
- `session` - Start Pomodoro study sessions

## Requirements

- Python 3.7+
- Dependencies listed in `requirements.txt`
- Optional: API keys for enhanced features

## Project Structure

```
syllabo/
├── main.py                 # Main application entry point
├── src/                    # Core modules
│   ├── ai_client.py        # AI service integration
│   ├── database.py         # Data storage
│   ├── syllabus_parser.py  # Syllabus processing
│   ├── quiz_generator.py   # Quiz creation
│   ├── progress_dashboard.py # Progress tracking
│   └── study_session_manager.py # Session management
├── docs/                   # Documentation
├── data/                   # User data and database files
├── scripts/                # Additional scripts and tools
├── tests/                  # Test files
└── requirements.txt        # Dependencies
```

## License

MIT License - see LICENSE file for details.