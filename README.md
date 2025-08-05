# Syllabo

A learning assistant that helps you analyze course syllabi and find educational resources. Built with Python and designed for students who want to organize their study materials effectively.

## What it does

Syllabo takes your course syllabus and breaks it down into manageable topics, then helps you find relevant learning materials. It includes tools for tracking progress, generating quizzes, and managing study sessions.

## Key Features

- Analyze PDF or text syllabi to extract topics
- Find YouTube videos and educational content for each topic
- Generate practice quizzes based on course material
- Track study progress with visual dashboards
- Pomodoro timer for focused study sessions
- Bookmark system for saving useful resources
- Spaced repetition system for better retention
- Search across multiple learning platforms

## Additional Tools

- Video analysis to assess topic coverage
- Automatic note generation from video content
- Resource database with books and courses
- Learning analytics and progress tracking
- Goal setting and milestone tracking
- Export functionality for study materials

## Getting Started

### Option 1: Docker (Recommended)

The easiest way to run Syllabo is using Docker. This ensures consistent behavior across different systems.

1. Clone the repository:
```bash
git clone https://github.com/PixelCode01/syllabo.git
cd syllabo
```

2. Run the setup script:
```bash
# On Linux/Mac
./docker-setup.sh

# On Windows
docker-setup.bat
```

3. Start using Syllabo:
```bash
# Interactive mode
docker-compose run --rm syllabo

# Or use the Makefile
make run
```

### Option 2: Local Installation

1. Clone the repository:
```bash
git clone https://github.com/PixelCode01/syllabo.git
cd syllabo
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up API keys (optional):
Copy `.env.example` to `.env` and add your API keys if you have them. The app works without keys but some features may be limited.

## How to Use

### Docker Usage

Run the main program:
```bash
# Interactive mode with full menu
docker-compose run --rm syllabo

# Or using make
make interactive
```

This opens an interactive menu where you can:
- Upload and analyze your syllabus
- Search for educational videos
- Take practice quizzes
- Track your study progress
- Start timed study sessions
- Manage bookmarks and notes

### Docker Commands

```bash
# Interactive mode with full menu
docker-compose run --rm syllabo
# or
make run

# Analyze a syllabus file
docker-compose run --rm syllabo python main.py analyze --file syllabus.pdf

# Search for educational videos
docker-compose run --rm syllabo python main.py search --topic "Machine Learning" --max-videos 10

# Manage spaced repetition reviews
docker-compose run --rm syllabo python main.py review list
docker-compose run --rm syllabo python main.py review add --topic "Neural Networks" --description "Deep learning concepts"

# Manage study goals
docker-compose run --rm syllabo python main.py goals list
docker-compose run --rm syllabo python main.py goals create --title "Daily Study" --type daily --target 30 --unit minutes

# View logs
make logs

# Open shell for debugging
make shell
```

### Local Installation Commands

```bash
# Interactive mode with full menu
python main.py interactive

# Analyze a syllabus file
python main.py analyze --file syllabus.pdf

# Search for educational videos
python main.py search --topic "Machine Learning" --max-videos 10

# Manage spaced repetition reviews
python main.py review list
python main.py review add --topic "Neural Networks" --description "Deep learning concepts"
python main.py review due
python main.py review mark --topic "Linear Algebra" --success

# Manage study goals
python main.py goals list
python main.py goals create --title "Daily Study" --type daily --target 30 --unit minutes
python main.py goals suggest
```

## Main Features

**Syllabus Analysis**: Upload a PDF or paste text to extract course topics automatically.

**Resource Discovery**: Find relevant YouTube videos, online courses, and study materials for each topic.

**Quiz Generation**: Create practice questions based on your course content.

**Progress Tracking**: See visual charts of your study progress and time spent on different topics.

**Study Sessions**: Built-in Pomodoro timer to help you stay focused during study time.

**Bookmarks**: Save useful video timestamps and add your own notes.

**Spaced Repetition**: Review topics at optimal intervals to improve long-term retention. Fully functional with CLI and interactive modes.

**Goal Management**: Set and track daily, weekly, and milestone-based study goals with progress monitoring.

## Example Workflow

1. Upload your course syllabus
2. Let the program extract topics automatically
3. Browse recommended videos and resources
4. Take practice quizzes to test your knowledge
5. Track your progress over time
6. Use spaced repetition to review difficult topics

## Docker Quick Start

If you have Docker installed, you can get started in just a few commands:

```bash
git clone https://github.com/PixelCode01/syllabo.git
cd syllabo
./docker-setup.sh  # or docker-setup.bat on Windows
make run
```

## Docker Commands Reference

```bash
make build      # Build the Docker image
make run        # Run interactively
make stop       # Stop containers
make logs       # View logs
make shell      # Open shell in container
make clean      # Remove everything
```

## Requirements

### For Docker (Recommended)
- Docker and Docker Compose
- Internet connection for finding resources

### For Local Installation
- Python 3.7 or higher
- Internet connection for finding resources
- Optional: API keys for enhanced features (see .env.example)

## License

MIT License