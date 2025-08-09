# Syllabo v1.0.1 - Initial Release

An AI-powered learning assistant that analyzes course syllabi and helps students organize their study materials effectively.

## 🚀 Features

### Core Functionality
- **Syllabus Analysis**: Upload PDF files or paste text to automatically extract course topics
- **AI-Generated Quizzes**: Create practice questions from topics, syllabus files, or any text content
- **Progress Tracking**: Visual dashboards showing study progress and time analytics
- **Spaced Repetition**: Review topics at optimal intervals for better retention
- **Study Sessions**: Built-in Pomodoro timer for focused study sessions
- **Resource Discovery**: Find relevant YouTube videos and educational materials
- **Bookmark Management**: Save video timestamps and add personal notes
- **Goal Management**: Set and track daily, weekly, and milestone-based study goals

### Technical Features
- **Interactive CLI**: Rich terminal interface with full menu system
- **Docker Support**: Containerized deployment with automated builds
- **Multi-platform**: Runs on Windows, Linux, and macOS
- **API Integration**: Support for YouTube API and Google Gemini AI
- **Export System**: Export study materials and progress reports
- **Database**: SQLite-based storage for all user data

## 📦 Installation

### Docker (Recommended)
```bash
# Pull and run the official image
docker pull ghcr.io/pixelcode01/syllabo:latest
docker run -it --rm ghcr.io/pixelcode01/syllabo:latest

# Or clone and build locally
git clone https://github.com/PixelCode01/syllabo.git
cd syllabo
make run
```

### Python Source
```bash
git clone https://github.com/PixelCode01/syllabo.git
cd syllabo
pip install -r requirements.txt
python main.py interactive
```

## 🎯 Quick Start

1. **Launch Interactive Mode**:
   ```bash
   # Docker
   docker run -it --rm ghcr.io/pixelcode01/syllabo:latest
   
   # Source
   python main.py interactive
   ```

2. **Analyze Your Syllabus**:
   - Choose option 1 in the menu
   - Upload a PDF file or paste text content
   - Let AI extract topics automatically

3. **Generate Quizzes**:
   - Choose option 2 in the menu
   - Select from topics, syllabus, or custom text
   - Take interactive quizzes to test knowledge

4. **Track Progress**:
   - View dashboards and analytics
   - Set study goals and milestones
   - Use spaced repetition for review

## 🛠️ What's New in v1.0.1

- **Complete Distribution System**: Docker images, GitHub Actions, and build scripts
- **Professional Documentation**: Comprehensive guides and API documentation
- **GitHub Pages Website**: Professional landing page with installation guides
- **Automated Builds**: CI/CD pipeline for consistent releases
- **Enhanced CLI**: Improved interactive interface with better error handling
- **Docker Optimization**: Smaller images and better performance

## 🔧 System Requirements

### Docker Installation
- Docker Engine and Docker Compose
- Internet connection for resource discovery

### Python Installation
- Python 3.7 or higher
- pip package manager
- Internet connection for full functionality
- Optional: API keys for enhanced features

## 📚 Documentation

- **Installation Guide**: [INSTALLATION.md](INSTALLATION.md)
- **Usage Guide**: [docs/USAGE.md](docs/USAGE.md)
- **API Setup**: [docs/API_SETUP.md](docs/API_SETUP.md)
- **Spaced Repetition Guide**: [docs/SPACED_REPETITION_GUIDE.md](docs/SPACED_REPETITION_GUIDE.md)
- **Project Website**: [https://pixelcode01.github.io/syllabo](https://pixelcode01.github.io/syllabo)

## 🚧 Coming Soon

- **Standalone Executables**: Pre-built binaries for Windows, Linux, and macOS
- **Web Interface**: Browser-based version of the application
- **Mobile App**: iOS and Android applications
- **Cloud Sync**: Synchronize data across devices
- **Team Features**: Collaborative study groups and sharing

## 🐛 Known Issues

- Standalone executables not yet available (use Docker or Python source)
- Some dependencies may require build tools on certain systems
- API keys required for full YouTube integration

## 🤝 Contributing

We welcome contributions! Please see our development setup:

```bash
git clone https://github.com/PixelCode01/syllabo.git
cd syllabo
make install-deps
python main.py interactive
```

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with Python, Rich, and Textual
- AI powered by Google Gemini
- Educational content from YouTube and various learning platforms
- Inspired by spaced repetition research and learning science

---

**Full Changelog**: https://github.com/PixelCode01/syllabo/commits/v1.0.1