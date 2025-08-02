# Syllabo Project Summary

## What This Project Does
Syllabo is an AI-powered educational resource finder that helps students discover the best YouTube videos and learning materials for their course syllabus, enhanced with a spaced repetition system for long-term retention.

## Main Applications (3 Entry Points)

### 1. `syllabo_enhanced.py` - Full-Featured CLI ⭐ RECOMMENDED
The complete application with all features.

**Key Features:**
- Analyze syllabus files (PDF/text) and extract topics
- Search YouTube for relevant educational videos
- AI-powered video analysis and scoring
- Spaced repetition system integration
- Export results in multiple formats
- Progress tracking and history

**Usage:**
```bash
python syllabo_enhanced.py analyze --file syllabus.pdf --search-videos --add-to-review --print-results
python syllabo_enhanced.py review list
python syllabo_enhanced.py review due --notify
```

### 2. `forgetmenot.py` - Standalone Spaced Repetition
Quick access to spaced repetition features only.

**Key Features:**
- Add topics for spaced repetition review
- Mark reviews as successful/failed
- Track progress and mastery levels
- Desktop notifications for due reviews
- Uses scientifically-proven Leitner algorithm

**Usage:**
```bash
forgetmenot add "Neural Networks" -d "Forward and backward propagation"
forgetmenot list --urgent
forgetmenot review "Neural Networks" --success
```

### 3. `interactive_scraper.py` - Interactive Interface
User-friendly interactive interface for syllabus processing.

**Key Features:**
- Menu-driven interface
- Real-time course scraping from multiple platforms
- No command-line knowledge required
- Built-in examples and demos

**Usage:**
```bash
python interactive_scraper.py
```

## Core Technology Stack

### AI & Analysis
- **AI Client**: Hack Club AI for content analysis
- **Video Analyzer**: Multi-criteria scoring system
- **Syllabus Parser**: PDF and text processing

### Data & Storage
- **Database**: SQLite for persistent storage
- **Spaced Repetition Engine**: Leitner algorithm implementation
- **Export System**: JSON, CSV, Markdown, HTML formats

### User Experience
- **Notification System**: Cross-platform desktop alerts
- **Rich Terminal UI**: Clean, professional output
- **Progress Tracking**: Success rates and mastery levels

## Spaced Repetition System

Uses the scientifically-proven **Leitner algorithm** with these intervals:
- Day 1: New topics (1 day)
- Day 3: First review (3 days)
- Day 5: Second review (5 days)
- Day 11, 25, 44, 88: Progressive intervals

**Features:**
- Automatic scheduling based on success/failure
- Progress tracking with mastery levels
- Desktop notifications for due reviews
- Local data storage (no cloud dependency)

## Quick Start

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Analyze a syllabus with spaced repetition:**
   ```bash
   python syllabo_enhanced.py analyze --file your_syllabus.pdf --search-videos --add-to-review --print-results
   ```

3. **Daily review routine:**
   ```bash
   forgetmenot list --urgent
   forgetmenot review "Topic Name" --success
   ```

## File Structure (Cleaned Up)

```
syllabo/
├── syllabo_enhanced.py      # Main CLI application
├── forgetmenot.py          # Standalone spaced repetition
├── interactive_scraper.py  # Interactive interface
├── src/                    # Core modules
├── README.md              # Project overview
├── USAGE.md               # Usage instructions
├── SPACED_REPETITION_GUIDE.md # Detailed spaced repetition docs
└── PROJECT_SUMMARY.md     # This file
```

## Key Benefits

1. **No API Keys Required**: Works with web scraping
2. **Scientifically-Backed**: Uses proven spaced repetition algorithms
3. **Local Data**: All data stored locally, privacy-focused
4. **Multi-Platform**: Works on Windows, macOS, Linux
5. **Professional Output**: Clean, human-like documentation
6. **Comprehensive**: From syllabus analysis to long-term retention

## Documentation

- **README.md**: Project overview and features
- **USAGE.md**: Detailed usage instructions for all applications
- **SPACED_REPETITION_GUIDE.md**: Complete spaced repetition documentation
- **PROJECT_SUMMARY.md**: This overview document

The project is now clean, focused, and easy to understand with clear entry points for different use cases.