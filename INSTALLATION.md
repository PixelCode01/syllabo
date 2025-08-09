# Syllabo Installation Guide

This guide covers all the ways to install and run Syllabo on your system.

## Quick Start Options

### 🐳 Docker (Recommended)

The easiest way to run Syllabo with consistent behavior across all systems.

```bash
# Clone the repository
git clone https://github.com/PixelCode01/syllabo.git
cd syllabo

# Run setup script
./docker-setup.sh  # Linux/macOS
# or
docker-setup.bat   # Windows

# Start using Syllabo
make run
# or
docker-compose run --rm syllabo
```

### 📦 Standalone Executable

Download pre-built executables for your operating system:

1. Go to [Releases](https://github.com/PixelCode01/syllabo/releases/latest)
2. Download the appropriate file for your system:
   - `syllabo-Windows.exe` for Windows
   - `syllabo-Linux` for Linux
   - `syllabo-macOS` for macOS
3. Run the installer script included in the package
4. Start using: `syllabo interactive`

### Docker Container Registry

Pull the official Docker image (available after GitHub release):

```bash
# Pull the latest image
docker pull ghcr.io/pixelcode01/syllabo:latest

# Run interactively
docker run -it --rm ghcr.io/pixelcode01/syllabo:latest

# Run with persistent data
docker run -it --rm -v $(pwd)/data:/app/data ghcr.io/pixelcode01/syllabo:latest
```

### 🐍 Python Installation

Install from source for development or customization:

```bash
# Clone the repository
git clone https://github.com/PixelCode01/syllabo.git
cd syllabo

# Install dependencies
pip install -r requirements.txt

# Run the application
python main.py interactive
```

## Detailed Installation Instructions

### Docker Installation

#### Prerequisites
- Docker and Docker Compose installed on your system
- Internet connection for downloading images and finding resources

#### Step-by-step
1. **Clone the repository:**
   ```bash
   git clone https://github.com/PixelCode01/syllabo.git
   cd syllabo
   ```

2. **Run the setup script:**
   ```bash
   # Linux/macOS
   chmod +x docker-setup.sh
   ./docker-setup.sh
   
   # Windows
   docker-setup.bat
   ```

3. **Start using Syllabo:**
   ```bash
   # Interactive mode
   make run
   
   # Or directly with docker-compose
   docker-compose run --rm syllabo
   
   # Analyze a syllabus
   docker-compose run --rm syllabo python main.py analyze --file syllabus.pdf
   ```

#### Docker Commands Reference
```bash
make build      # Build the Docker image
make run        # Run interactively
make stop       # Stop containers
make logs       # View logs
make shell      # Open shell in container
make clean      # Remove everything
```

### Standalone Executable Installation

#### Windows
1. Download `syllabo-Windows.exe` from releases
2. Extract the package
3. Run `install.bat` as administrator (adds to PATH)
4. Open Command Prompt and run: `syllabo interactive`

#### Linux/macOS
1. Download the appropriate executable from releases
2. Extract the package
3. Run the installer:
   ```bash
   chmod +x install.sh
   ./install.sh
   ```
4. Restart your terminal or run: `source ~/.bashrc`
5. Run: `syllabo interactive`

#### Manual Installation
If you prefer manual installation:

1. Copy the executable to a directory in your PATH
2. Copy `.env.example` to your preferred config location
3. Make the executable file executable (Linux/macOS): `chmod +x syllabo`
4. Run: `syllabo interactive`

### Python Source Installation

#### Prerequisites
- Python 3.7 or higher
- pip package manager
- Internet connection

#### Step-by-step
1. **Clone the repository:**
   ```bash
   git clone https://github.com/PixelCode01/syllabo.git
   cd syllabo
   ```

2. **Create a virtual environment (recommended):**
   ```bash
   python -m venv syllabo-env
   
   # Activate it
   # Linux/macOS:
   source syllabo-env/bin/activate
   # Windows:
   syllabo-env\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

4. **Configure API keys (optional):**
   ```bash
   cp .env.example .env
   # Edit .env and add your API keys
   ```

5. **Run the application:**
   ```bash
   python main.py interactive
   ```

## Configuration

### API Keys (Optional)
Syllabo works without API keys, but some features are enhanced with them:

1. Copy `.env.example` to `.env`
2. Add your API keys:
   ```
   GOOGLE_API_KEY=your_youtube_api_key_here
   GEMINI_API_KEY=your_gemini_api_key_here
   ```

### Data Storage
- Docker: Data is stored in the `data/` directory (mounted as volume)
- Standalone: Data is stored in the same directory as the executable
- Python: Data is stored in the project directory

## Usage Examples

### Interactive Mode
```bash
# Docker
make run

# Standalone
syllabo interactive

# Python
python main.py interactive
```

### Command Line Usage
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

## Troubleshooting

### Common Issues

#### Docker Issues
- **Permission denied**: Make sure Docker is running and you have permissions
- **Port conflicts**: Check if ports 8000 or 5432 are already in use
- **Build failures**: Ensure you have enough disk space and internet connection

#### Executable Issues
- **Command not found**: Make sure the executable is in your PATH
- **Permission denied**: Make the file executable with `chmod +x syllabo`
- **Missing dependencies**: Use the Docker version for guaranteed compatibility

#### Python Issues
- **Import errors**: Make sure all dependencies are installed with `pip install -r requirements.txt`
- **Python version**: Ensure you're using Python 3.7 or higher
- **Virtual environment**: Use a virtual environment to avoid conflicts

### Getting Help
- Check the [GitHub Issues](https://github.com/PixelCode01/syllabo/issues)
- Read the [documentation](https://github.com/PixelCode01/syllabo/blob/main/README.md)
- Create a new issue if you can't find a solution

## Building from Source

### Building Executables
```bash
# Install build dependencies
pip install pyinstaller

# Run the build script
python build.py

# Or manually with PyInstaller
pyinstaller syllabo.spec
```

### Building Docker Images
```bash
# Build locally
docker build -t syllabo:latest .

# Publish to registry (requires authentication)
./docker-publish.sh  # Linux/macOS
docker-publish.bat   # Windows
```

## Next Steps

After installation, check out:
- [Usage Guide](docs/USAGE.md) - Learn how to use all features
- [API Setup](docs/API_SETUP.md) - Configure API keys for enhanced features
- [Spaced Repetition Guide](docs/SPACED_REPETITION_GUIDE.md) - Master the learning system

Happy learning with Syllabo! 🎓