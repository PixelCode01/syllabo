# Syllabo Usage Guide

This guide explains which files to use for different purposes.

## Main Applications

### 1. `enhanced_cli.py` - Enhanced Full-Featured CLI (RECOMMENDED)
The enhanced application with all new features including quizzes, progress tracking, and multi-platform search.

```bash
# Comprehensive syllabus analysis with multi-platform resources
python enhanced_cli.py analyze --file syllabus.pdf --search-videos --include-podcasts --include-reading --add-to-review --difficulty-filter intermediate

# Interactive quiz system
python enhanced_cli.py quiz generate --topic "Machine Learning" --num-questions 10
python enhanced_cli.py quiz take

# Progress tracking and analytics
python enhanced_cli.py progress --export

# Study goals management
python enhanced_cli.py goals create --title "Study 30 min daily" --type daily --target 30 --unit minutes
python enhanced_cli.py goals list
python enhanced_cli.py goals suggest

# Multi-platform content search
python enhanced_cli.py platforms --topic "Data Science" --free-only --include-coursera --include-edx --include-khan

# Smart bookmarking system
python enhanced_cli.py bookmarks add --video-id "abc123" --video-title "ML Tutorial" --timestamp "15:30" --note "Key concept explanation" --topic "Machine Learning" --tags ml tutorial --importance 4
python enhanced_cli.py bookmarks search --query "neural networks"
python enhanced_cli.py bookmarks export --format markdown

# Study session management (Pomodoro technique)
python enhanced_cli.py session start --topic "Neural Networks" --duration 25
python enhanced_cli.py session break --break-type short
python enhanced_cli.py session end --notes "Completed backpropagation review"
python enhanced_cli.py session stats
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
Generate and take quizzes from your study content:

```bash
# Generate quiz from content file
python enhanced_cli.py quiz generate --topic "Machine Learning" --content-file notes.txt --num-questions 10

# Take a quiz interactively
python enhanced_cli.py quiz take

# View quiz history
python enhanced_cli.py quiz history
```

### Progress Tracking Dashboard
Monitor your learning progress with visual analytics:

```bash
# View comprehensive progress dashboard
python enhanced_cli.py progress

# Export progress report
python enhanced_cli.py progress --export
```

### Study Goals & Milestones
Set and track learning objectives:

```bash
# Create different types of goals
python enhanced_cli.py goals create --title "Daily Study" --type daily --target 30 --unit minutes
python enhanced_cli.py goals create --title "Weekly Topics" --type weekly --target 3 --unit topics
python enhanced_cli.py goals create --title "Quiz Mastery" --type milestone --target 90 --unit percent

# List active goals
python enhanced_cli.py goals list

# Get goal suggestions based on your level
python enhanced_cli.py goals suggest
```

### Multi-Platform Content Search
Search across multiple learning platforms:

```bash
# Search all platforms
python enhanced_cli.py platforms --topic "Python Programming"

# Filter for free content only
python enhanced_cli.py platforms --topic "Data Science" --free-only

# Search specific platforms
python enhanced_cli.py platforms --topic "Machine Learning" --include-coursera --include-edx
```

### Smart Bookmarking
Save important video moments with context:

```bash
# Add bookmark with full details
python enhanced_cli.py bookmarks add --video-id "dQw4w9WgXcQ" --video-title "Python Tutorial" --timestamp "15:30" --note "Important function explanation" --topic "Python" --tags tutorial function --importance 4

# List bookmarks by topic
python enhanced_cli.py bookmarks list --topic "Python"

# Search bookmarks
python enhanced_cli.py bookmarks search --query "function"

# Export bookmarks in different formats
python enhanced_cli.py bookmarks export --format markdown
python enhanced_cli.py bookmarks export --format csv
```

### Study Session Management (Pomodoro)
Manage focused study sessions:

```bash
# Start a study session
python enhanced_cli.py session start --topic "Neural Networks" --duration 25

# Take breaks during study
python enhanced_cli.py session break --break-type short
python enhanced_cli.py session break --break-type long

# End session with notes
python enhanced_cli.py session end --notes "Completed backpropagation chapter"

# Check current session status
python enhanced_cli.py session stats
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

1. **For comprehensive syllabus analysis with spaced repetition:**
   ```bash
   python syllabo.py analyze --file your_syllabus.pdf --search-videos --add-to-review --print-results
   ```

2. **For daily review routine:**
   ```bash
   forgetmenot list --urgent
   forgetmenot review "Topic Name" --success
   ```

3. **For interactive exploration:**
   ```bash
   python interactive_scraper.py
   ```

## File Structure

```
syllabo/
├── syllabo.py              # Main CLI application
├── src/                    # Core modules (don't run directly)
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