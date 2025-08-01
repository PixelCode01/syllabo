# Syllabo Usage Guide

This guide explains which files to use for different purposes.

## Main Applications

### 1. `syllabo.py` - Full-Featured CLI
The main application with all features including spaced repetition.

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

### 2. `forgetmenot.py` - Standalone Spaced Repetition
Quick access to spaced repetition features only.

```bash
# Add topic for review
forgetmenot add "Neural Networks" -d "Forward and backward propagation"

# Mark review
forgetmenot review "Neural Networks" --success

# List urgent reviews
forgetmenot list --urgent

# Show statistics
forgetmenot stats

# Send notifications
forgetmenot remind
```

### 3. `interactive_scraper.py` - Interactive Interface
User-friendly interactive interface for syllabus processing.

```bash
python interactive_scraper.py
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