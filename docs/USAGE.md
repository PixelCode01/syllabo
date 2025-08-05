# Syllabo Usage Guide

This guide explains which files to use for different purposes.

## Main Applications

### 1. `main.py` - Enhanced Full-Featured CLI (RECOMMENDED)
The main application with all features including quizzes, progress tracking, multi-platform search, and spaced repetition.

```bash
# Comprehensive syllabus analysis with multi-platform resources
python main.py analyze --file syllabus.pdf --search-videos --include-podcasts --include-reading --add-to-review --difficulty-filter intermediate

# Interactive quiz system
python main.py quiz --topic "Machine Learning" --num-questions 10
python main.py quiz --content-file syllabus.pdf --num-questions 5
python main.py quiz --source topics
python main.py quiz  # Interactive mode - prompts for topic/syllabus/text

# Progress tracking and analytics
python main.py progress --export

# Study goals management
python main.py goals create --title "Study 30 min daily" --type daily --target 30 --unit minutes
python main.py goals list
python main.py goals suggest

# Multi-platform content search
python main.py platforms --topic "Data Science" --free-only

# Smart bookmarking system
python main.py bookmarks add --video-id "abc123" --video-title "ML Tutorial" --timestamp "15:30" --note "Key concept explanation" --topic "Machine Learning" --tags ml tutorial --importance 4
python main.py bookmarks search --query "neural networks"
python main.py bookmarks export --format markdown

# Study session management (Pomodoro technique)
python main.py session start --topic "Neural Networks" --duration 25
python main.py session break --break-type short
python main.py session end --notes "Completed backpropagation review"
python main.py session stats
```

### 2. `syllabo.py` - Original Full-Featured CLI
The original application with core features and spaced repetition.

```bash
# Analyze syllabus and add topics to spaced repetition
python syllabo.py analyze --file syllabus.pdf --search-videos --add-to-review --print-results

# Search for specific topic
python syllabo.py search --topic "Machine Learning" --max-videos 10

# Spaced repetition commands
python syllabo.py review list
python syllabo.py review due --notify
python syllabo.py review mark --topic "Neural Networks" --success

# View history and export
python syllabo.py history
python syllabo.py export --syllabus-id 1 --format html
```

## New Features Guide

### Interactive Quiz System
Generate and take quizzes from topics, syllabus files, or text content:

```bash
# Generate quiz from specific topic
python main.py quiz --topic "Machine Learning" --num-questions 10

# Generate quiz from content file
python main.py quiz --content-file notes.txt --num-questions 5

# Interactive mode - choose from topics/syllabus/text
python main.py quiz

# Use specific source
python main.py quiz --source topics     # From database topics
python main.py quiz --source syllabus   # From syllabus file
python main.py quiz --source text       # From direct text input
```

### Progress Tracking Dashboard
Monitor your learning progress with visual analytics:

```bash
# View comprehensive progress dashboard
python main.py progress

# Export progress report
python main.py progress --export
```

### Study Goals & Milestones
Set and track learning objectives:

```bash
# Create different types of goals
python main.py goals create --title "Daily Study" --type daily --target 30 --unit minutes
python main.py goals create --title "Weekly Topics" --type weekly --target 3 --unit topics
python main.py goals create --title "Quiz Mastery" --type milestone --target 90 --unit percent

# List active goals
python main.py goals list

# Get goal suggestions based on your level
python main.py goals suggest
```

### Multi-Platform Content Search
Search across multiple learning platforms:

```bash
# Search all platforms
python main.py platforms --topic "Python Programming"

# Filter for free content only
python main.py platforms --topic "Data Science" --free-only
```

### Smart Bookmarking
Save important video moments with context:

```bash
# Add bookmark with full details
python main.py bookmarks add --video-id "dQw4w9WgXcQ" --video-title "Python Tutorial" --timestamp "15:30" --note "Important function explanation" --topic "Python" --tags tutorial function --importance 4

# List bookmarks by topic
python main.py bookmarks list --topic "Python"

# Search bookmarks
python main.py bookmarks search --query "function"

# Export bookmarks in different formats
python main.py bookmarks export --format markdown
python main.py bookmarks export --format csv
```

### Study Session Management (Pomodoro)
Manage focused study sessions:

```bash
# Start a study session
python main.py session start --topic "Neural Networks" --duration 25

# Take breaks during study
python main.py session break --break-type short
python main.py session break --break-type long

# End session with notes
python main.py session end --notes "Completed backpropagation chapter"

# Check current session status
python main.py session stats
```

## Core Modules (src/)

These are the building blocks used by the main applications:

- `ai_client.py` - AI integration for content analysis
- `database.py` - SQLite database management
- `export_system.py` - Export results to various formats
- `feedback_system.py` - User feedback and ratings
- `logger.py` - Logging system
- `notes_generator.py` - Generate study materials
- `notification_system.py` - Desktop notifications
- `optimal_learning_engine.py` - Learning optimization
- `spaced_repetition.py` - Spaced repetition engine
- `syllabus_parser.py` - Parse PDF and text files
- `utils.py` - Utility functions
- `video_analyzer.py` - Analyze and score videos
- `youtube_client.py` - YouTube data scraping

## Quick Start

1. **For comprehensive analysis with all new features:**
   ```bash
   python main.py analyze --file your_syllabus.pdf --search-videos --include-podcasts --include-reading --add-to-review --print-results
   ```

2. **For interactive quiz and study sessions:**
   ```bash
   python main.py quiz --topic "Your Topic" --num-questions 5
   python main.py session start --topic "Your Topic" --duration 25
   ```

3. **For progress tracking and goals:**
   ```bash
   python main.py progress
   python main.py goals create --title "Daily Study" --type daily --target 30 --unit minutes
   ```

## File Structure

```
syllabo/
├── main.py                 # Enhanced main CLI application (RECOMMENDED)
├── syllabo.py              # Original CLI application
├── src/                    # Core modules with all new features
│   ├── quiz_generator.py   # Interactive quiz system
│   ├── progress_dashboard.py # Progress tracking
│   ├── goals_manager.py    # Study goals management
│   ├── platform_integrator.py # Multi-platform search
│   ├── podcast_integrator.py # Podcast and reading resources
│   ├── bookmark_manager.py # Smart bookmarking
│   ├── difficulty_analyzer.py # Content difficulty rating
│   ├── study_session_manager.py # Pomodoro sessions
│   └── ... (other core modules)
├── README.md              # Project overview
├── SPACED_REPETITION_GUIDE.md  # Detailed spaced repetition docs
└── USAGE.md               # This file
```

## Environment Setup

1. Install dependencies: `pip install -r requirements.txt`
2. Copy `.env.example` to `.env` and add your API keys (optional)
3. Start using the applications above

## Need Help?

- Run any command with `--help` for detailed options
- Check `README.md` for project overview
- Check `SPACED_REPETITION_GUIDE.md` for spaced repetition details
- All applications have built-in help commands