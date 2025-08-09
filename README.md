# Syllabo

An AI-powered learning assistant that analyzes course syllabi and helps students organize their study materials effectively. Built with Python, Syllabo transforms your syllabus into a comprehensive learning management system.

## Overview

Syllabo automatically breaks down your course syllabus into manageable topics and helps you find relevant learning materials. The application includes comprehensive tools for progress tracking, quiz generation, study session management, and spaced repetition learning.

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

## Installation

### Windows Executable (Ready Now)

Download the pre-built Windows executable - no installation required:

1. Go to [Releases](https://github.com/PixelCode01/syllabo/releases/latest)
2. Download `syllabo-windows-v1.0.1.zip`
3. Extract and run `install-windows.bat` as Administrator
4. Open new Command Prompt and run: `syllabo-Windows.exe interactive`

### Docker Installation (Available After Release)

Docker images will be built automatically when the GitHub release is created:

```bash
# Will be available after GitHub release
docker pull ghcr.io/pixelcode01/syllabo:latest
docker run -it --rm ghcr.io/pixelcode01/syllabo:latest
```

### Docker Hub

Docker images will be available after the first GitHub release is created:

```bash
# Will be available after release
docker pull ghcr.io/pixelcode01/syllabo:latest
docker run -it --rm ghcr.io/pixelcode01/syllabo:latest
```

### Standalone Executables (Coming Soon)

Pre-built executables for Windows, Linux, and macOS will be available in future releases. Currently, please use Docker or Python source installation.

### Python Source Installation

For development or customization:

```bash
git clone https://github.com/PixelCode01/syllabo.git
cd syllabo
pip install -r requirements.txt
python main.py interactive
```

### Documentation

Visit the [project website](https://pixelcode01.github.io/syllabo) for comprehensive documentation and additional resources.

## Usage

### Interactive Mode

Launch the interactive interface:

```bash
# Docker
docker-compose run --rm syllabo
# or
make interactive

# Standalone executable
./syllabo interactive

# Python source
python main.py interactive
```

The interactive menu provides access to all features:
- Syllabus analysis and topic extraction
- Educational video search and discovery
- Interactive quiz generation and testing
- Progress tracking and analytics
- Timed study sessions with Pomodoro timer
- Bookmark and note management

### Command Line Interface

#### Docker Commands

```bash
# Interactive mode
docker-compose run --rm syllabo
make run

# Analyze syllabus
docker-compose run --rm syllabo python main.py analyze --file syllabus.pdf

# Search for educational content
docker-compose run --rm syllabo python main.py search --topic "Machine Learning" --max-videos 10

# Spaced repetition management
docker-compose run --rm syllabo python main.py review list
docker-compose run --rm syllabo python main.py review add --topic "Neural Networks" --description "Deep learning concepts"

# Quiz generation and testing
docker-compose run --rm syllabo python main.py quiz --topic "Machine Learning" --num-questions 5
docker-compose run --rm syllabo python main.py quiz --content-file syllabus.pdf
docker-compose run --rm syllabo python main.py quiz --source topics

# Study goal management
docker-compose run --rm syllabo python main.py goals list
docker-compose run --rm syllabo python main.py goals create --title "Daily Study" --type daily --target 30 --unit minutes

# System management
make logs    # View application logs
make shell   # Open debugging shell
```

#### Direct Commands

```bash
# Interactive mode
python main.py interactive

# Syllabus analysis
python main.py analyze --file syllabus.pdf

# Content search
python main.py search --topic "Machine Learning" --max-videos 10

# Spaced repetition
python main.py review list
python main.py review add --topic "Neural Networks" --description "Deep learning concepts"
python main.py review due
python main.py review mark --topic "Linear Algebra" --success

# Quiz system
python main.py quiz --topic "Machine Learning" --num-questions 5
python main.py quiz --content-file syllabus.pdf
python main.py quiz --source topics
python main.py quiz  # Interactive quiz mode

# Goal management
python main.py goals list
python main.py goals create --title "Daily Study" --type daily --target 30 --unit minutes
python main.py goals suggest
```

## Core Features

### Syllabus Analysis
Upload PDF files or paste text content to automatically extract course topics and create structured learning plans.

### Resource Discovery
Automatically find relevant educational content including YouTube videos, online courses, and study materials for each extracted topic.

### Quiz Generation
Create practice questions from various sources including topics, syllabus files, or any text content. Supports multiple question types with interactive testing capabilities.

### Progress Tracking
Monitor your learning progress with visual charts and analytics showing time spent on different topics and overall study patterns.

### Study Sessions
Built-in Pomodoro timer system to maintain focus during study sessions with customizable work and break intervals.

### Bookmark Management
Save important video timestamps and add personal notes to create a comprehensive resource library.

### Spaced Repetition System
Review topics at scientifically optimized intervals to improve long-term retention. Fully integrated with both CLI and interactive interfaces.

### Goal Management
Set and track study objectives with support for daily, weekly, and milestone-based goals including progress monitoring and achievement tracking.

## Typical Workflow

1. **Import Syllabus**: Upload your course syllabus in PDF format or paste the text content
2. **Topic Extraction**: Allow the AI system to automatically identify and extract key learning topics
3. **Resource Discovery**: Browse automatically curated educational videos and learning materials
4. **Knowledge Testing**: Generate and take practice quizzes to assess your understanding
5. **Progress Monitoring**: Track your learning progress and identify areas needing attention
6. **Spaced Review**: Use the spaced repetition system to reinforce learning and improve retention

## Distribution

Syllabo is available in multiple distribution formats:

- **Docker Images**: Container images available at `ghcr.io/pixelcode01/syllabo:latest`
- **Python Source**: Install directly from source code for development and customization
- **Standalone Executables**: Pre-built binaries (coming in future releases)
- **Documentation**: Comprehensive guides available at [GitHub Pages](https://pixelcode01.github.io/syllabo)

## Development

For developers interested in contributing or customizing Syllabo:

### Setup Development Environment

```bash
git clone https://github.com/PixelCode01/syllabo.git
cd syllabo
make install-deps
```

### Development Commands

```bash
# Run in development mode
python main.py interactive

# Build standalone executables
make build-exe

# Clean development environment
make clean-dev          # Linux/macOS
make clean-dev-windows  # Windows

# Create complete release package
make release
```

## Quick Start Guide

### Standalone Executable
```bash
./syllabo interactive
```

### Docker Container
```bash
docker run -it --rm ghcr.io/pixelcode01/syllabo:latest
```

### Python Source
```bash
git clone https://github.com/PixelCode01/syllabo.git
cd syllabo
python main.py interactive
```

## Docker Management

### Container Operations
```bash
make build      # Build the Docker image
make run        # Run application interactively
make stop       # Stop all running containers
make logs       # View application logs
make shell      # Open debugging shell in container
make clean      # Remove containers and images
```

## System Requirements

### Docker Installation
- Docker Engine and Docker Compose
- Internet connection for resource discovery and content search

### Local Python Installation
- Python 3.7 or higher
- pip package manager
- Internet connection for educational content discovery
- Optional: API keys for enhanced functionality (configuration details in .env.example)

### Standalone Executable
- No additional dependencies required
- Internet connection for full functionality

## License

MIT License