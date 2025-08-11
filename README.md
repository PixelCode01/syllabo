# Syllabo

An AI-powered learning assistant that transforms your study materials into interactive learning experiences. Syllabo analyzes course syllabi, generates personalized quizzes, and helps you organize your learning journey with advanced progress tracking and spaced repetition.

## Installation

### Standalone Executables

Download ready-to-run executables that require no Python installation:

1. Visit the [Releases Page](https://github.com/PixelCode01/syllabo/releases/latest)
2. Download for your system:
   - Windows: `syllabo-vX.X.X-Windows.zip`
   - Linux: `syllabo-vX.X.X-Linux.tar.gz`
   - macOS: `syllabo-vX.X.X-macOS.tar.gz`
3. Extract and run the installer
4. Start with: `syllabo interactive`

### Development Installation

**Docker (Cross-platform):**
```bash
git clone https://github.com/PixelCode01/syllabo.git
cd syllabo
make docker-run
```

**Python Source (Development):**
```bash
git clone https://github.com/PixelCode01/syllabo.git
cd syllabo
pip install -r requirements.txt
python main.py interactive
```

## Core Features

**Learning Management:**
- Syllabus analysis and topic extraction
- AI-powered quiz generation
- Progress tracking with detailed analytics
- Study goals and milestone management

**Study Tools:**
- Spaced repetition system for better retention
- Pomodoro timer and focus sessions
- Smart bookmarks and note-taking
- Video analysis and content extraction

**Resource Discovery:**
- Multi-platform search (YouTube, Coursera, Udemy)
- Automatic resource recommendations
- Educational content analysis
- Learning material organization

## Usage

### Interactive Mode

The easiest way to use Syllabo:

```bash
# Standalone executable
syllabo interactive

# Docker
make docker-run

# Python source
python main.py interactive
```

### Command Line Interface

```bash
# Analyze a syllabus
syllabo analyze --file syllabus.pdf

# Generate quiz
syllabo quiz --topic "Machine Learning" --num-questions 5

# Search for videos
syllabo search --topic "Python Programming" --max-videos 10

# View progress
syllabo progress

# Manage goals
syllabo goals list
syllabo goals create --title "Daily Study" --type daily --target 30 --unit minutes

# Spaced repetition
syllabo review list
syllabo review due
```

## Typical Workflow

1. **Import Syllabus**: Upload your course syllabus or paste text content
2. **Topic Extraction**: AI automatically identifies key learning topics
3. **Resource Discovery**: Browse curated educational videos and materials
4. **Knowledge Testing**: Generate and take practice quizzes
5. **Progress Monitoring**: Track learning progress and identify focus areas
6. **Spaced Review**: Use spaced repetition to reinforce learning

## Configuration

For enhanced features, configure API keys:

1. Copy `.env.example` to `.env`
2. Add your API keys:
   ```
   GOOGLE_API_KEY=your_youtube_api_key_here
   GEMINI_API_KEY=your_gemini_api_key_here
   ```

## Development

### Setup Development Environment

```bash
git clone https://github.com/PixelCode01/syllabo.git
cd syllabo
make install
```

### Build Commands

```bash
# Quick local build
make build-local

# Create portable package
make portable

# Test build
python test-build.py

# Create release
make release-patch
```

### Docker Development

```bash
# Build and run
make docker-build
make docker-run

# Development mode
make docker-run-dev
```

## Documentation

- [Installation Guide](INSTALLATION.md) - Detailed installation instructions
- [Build Guide](BUILD.md) - Building from source
- [Release Guide](RELEASE.md) - Creating releases

## Support

- [GitHub Issues](https://github.com/PixelCode01/syllabo/issues) - Bug reports and feature requests
- [GitHub Discussions](https://github.com/PixelCode01/syllabo/discussions) - Community support
- [Project Website](https://pixelcode01.github.io/syllabo) - Documentation and downloads

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please read the contributing guidelines and submit pull requests for any improvements.