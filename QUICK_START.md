# Syllabo Quick Start Guide

Welcome to Syllabo - your AI-powered learning assistant! This guide will get you up and running in minutes.

## 🚀 Installation

```bash
# Clone the repository
git clone <your-repo-url>
cd syllabo

# Install dependencies
pip install -r requirements.txt

# Optional: Set up environment variables
cp .env.example .env
# Edit .env and add your API keys (optional for basic features)
```

## 🎯 Quick Demo

### Interactive Mode (Recommended for beginners)
```bash
python main.py
```
This launches an interactive menu with:
- Beautiful ASCII banner
- Quick stats overview
- Menu-driven interface
- Contextual help

### Analyze Your First Syllabus
```bash
# From file
python main.py analyze --file your_syllabus.pdf --search-videos --print-results

# From text
python main.py analyze --text "Machine Learning: supervised learning, neural networks, deep learning" --search-videos --include-podcasts --add-to-review
```

### Generate and Take a Quiz
```bash
python main.py quiz generate --topic "Machine Learning" --num-questions 5
```

### Track Your Progress
```bash
python main.py progress
```

### Start a Study Session
```bash
python main.py session start --topic "Neural Networks" --duration 25
```

## 🎨 UI/UX Features

### Enhanced Visual Experience
- **Beautiful ASCII Banner**: Eye-catching startup screen
- **Progress Bars**: Visual feedback for long operations
- **Color-coded Messages**: Green checkmarks for success, red X for errors
- **Professional Tables**: Clean data presentation
- **Interactive Menus**: Easy navigation without memorizing commands

### Smart Feedback
- **Contextual Help**: Get help exactly when you need it
- **Next Steps Suggestions**: Always know what to do next
- **Performance Indicators**: Visual progress tracking
- **Error Recovery**: Clear error messages with solutions

### Productivity Features
- **Quick Stats**: See your learning status at a glance
- **Interactive Options**: Choose actions without command-line complexity
- **Session Management**: Visual Pomodoro timer with focus scoring
- **Goal Tracking**: Beautiful progress visualization

## 📚 Core Features

### 1. Syllabus Analysis
- Extract topics from PDF or text
- Find YouTube videos, podcasts, and reading materials
- AI-powered content difficulty rating
- Multi-platform course discovery

### 2. Interactive Learning
- AI-generated quizzes with multiple question types
- Spaced repetition system for long-term retention
- Progress tracking with visual analytics
- Study goals and milestone management

### 3. Study Optimization
- Pomodoro technique integration
- Smart bookmarking with timestamps
- Focus session tracking
- Performance analytics

### 4. Content Discovery
- YouTube video and playlist search
- Coursera, Khan Academy, edX integration
- Educational podcast discovery
- Academic paper and article finding

## 🔧 Command Examples

### Comprehensive Analysis
```bash
python main.py analyze --file syllabus.pdf --search-videos --include-podcasts --include-reading --add-to-review --difficulty-filter intermediate --print-results
```

### Quiz Workflow
```bash
# Generate quiz
python main.py quiz generate --topic "Python Programming" --num-questions 10

# Take quiz (interactive)
python main.py quiz take

# View quiz history
python main.py quiz history
```

### Goal Management
```bash
# Create goals
python main.py goals create --title "Daily Study" --type daily --target 30 --unit minutes
python main.py goals create --title "Weekly Topics" --type weekly --target 3 --unit topics

# View progress
python main.py goals list

# Get suggestions
python main.py goals suggest
```

### Study Sessions
```bash
# Start session
python main.py session start --topic "Data Science" --duration 25

# Take break
python main.py session break --break-type short

# End session
python main.py session end --notes "Completed pandas tutorial"

# Check status
python main.py session stats
```

### Multi-Platform Search
```bash
python main.py platforms --topic "Machine Learning" --free-only
```

### Smart Bookmarking
```bash
# Add bookmark
python main.py bookmarks add --video-id "abc123" --video-title "ML Tutorial" --timestamp "15:30" --note "Important concept" --topic "ML" --importance 4

# Search bookmarks
python main.py bookmarks search --query "neural networks"

# Export bookmarks
python main.py bookmarks export --format markdown
```

## 💡 Tips for Best Experience

1. **Start with Interactive Mode**: Run `python main.py` without arguments
2. **Use Progress Dashboard**: Check `python main.py progress` regularly
3. **Set Daily Goals**: Create achievable daily study targets
4. **Combine Features**: Use analysis → quiz → session → progress workflow
5. **Bookmark Important Moments**: Save key video timestamps for review
6. **Enable Spaced Repetition**: Add topics to review schedule for retention

## 🆘 Getting Help

- **Interactive Help**: Available in the main menu
- **Command Help**: Add `--help` to any command
- **Feature Help**: Contextual help shown when needed
- **Documentation**: Check README.md and USAGE.md for detailed information

## 🎉 What's Next?

After your first session:
1. Check your progress dashboard
2. Set up daily study goals
3. Add topics to spaced repetition
4. Explore multi-platform content discovery
5. Try the quiz system for knowledge testing

Happy learning with Syllabo! 🚀