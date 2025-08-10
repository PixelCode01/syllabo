# Syllabo Installation Guide

This comprehensive guide covers all the ways to install and run Syllabo on Windows, Linux, and macOS.

## 🚀 Quick Start Options

### 📦 Standalone Executable (Recommended)

**✅ No Python Required • ✅ No Dependencies • ✅ Just Download & Run**

The easiest way to get started - completely standalone executables that work out of the box:

1. **Visit the [Releases Page](https://github.com/PixelCode01/syllabo/releases/latest)**
2. **Download for your system:**
   - `syllabo-vX.X.X-Windows.zip` for Windows (10/11, 64-bit)
   - `syllabo-vX.X.X-Linux.tar.gz` for Linux (Ubuntu, Debian, CentOS, etc.)
   - `syllabo-vX.X.X-macOS.tar.gz` for macOS (10.15+, Intel & Apple Silicon)
3. **Extract and run** - No installation needed!
4. **Start learning:** `syllabo interactive`

> **🎯 Truly Standalone**: These executables include everything needed to run Syllabo. No Python, no dependencies, no setup required!

### 🐳 Docker (Cross-platform)

Consistent behavior across all systems with Docker:

```bash
# Clone the repository
git clone https://github.com/PixelCode01/syllabo.git
cd syllabo

# Build and run
make docker-run
# or
docker-compose run --rm syllabo
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

## 📋 Platform-Specific Installation

### 🪟 Windows Installation

#### Method 1: Automatic Installer (Recommended)
1. Download `syllabo-vX.X.X-Windows.zip`
2. Extract the ZIP file
3. **Right-click** on `install-windows.bat`
4. Select **"Run as administrator"**
5. Follow the installation prompts
6. Open Command Prompt and run: `syllabo interactive`

#### Method 2: Manual Installation
1. Extract the ZIP file to a folder (e.g., `C:\Syllabo`)
2. Add the folder to your system PATH:
   - Open System Properties → Advanced → Environment Variables
   - Edit the PATH variable and add your folder
3. Copy `.env.example` to `.env` if you want to configure API keys
4. Run: `syllabo interactive`

#### Uninstallation
- Run `uninstall-windows.bat` as administrator, or
- Remove the installation folder and PATH entry manually

### 🐧 Linux Installation

#### Method 1: Automatic Installer (Recommended)
```bash
# Extract the package
tar -xzf syllabo-vX.X.X-Linux.tar.gz
cd syllabo-vX.X.X-Linux

# Run installer
chmod +x install-linux.sh
./install-linux.sh

# Restart terminal or reload PATH
source ~/.bashrc

# Start using
syllabo interactive
```

#### Method 2: Manual Installation
```bash
# Extract and copy
tar -xzf syllabo-vX.X.X-Linux.tar.gz
sudo cp syllabo-vX.X.X-Linux/syllabo /usr/local/bin/
chmod +x /usr/local/bin/syllabo

# Or for user-only installation
mkdir -p ~/.local/bin
cp syllabo-vX.X.X-Linux/syllabo ~/.local/bin/
chmod +x ~/.local/bin/syllabo
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
```

#### Uninstallation
```bash
# If you used the installer
./uninstall-unix.sh

# Or manually
sudo rm /usr/local/bin/syllabo
# or
rm ~/.local/bin/syllabo
```

### 🍎 macOS Installation

#### Method 1: Automatic Installer (Recommended)
```bash
# Extract the package
tar -xzf syllabo-vX.X.X-macOS.tar.gz
cd syllabo-vX.X.X-macOS

# Run installer
chmod +x install-macos.sh
./install-macos.sh

# Restart terminal or reload PATH
source ~/.zshrc

# Start using
syllabo interactive
```

#### Method 2: Manual Installation
```bash
# Extract and copy
tar -xzf syllabo-vX.X.X-macOS.tar.gz

# System-wide installation (requires admin)
sudo cp syllabo-vX.X.X-macOS/syllabo /usr/local/bin/
chmod +x /usr/local/bin/syllabo

# Or user-only installation
mkdir -p ~/.local/bin
cp syllabo-vX.X.X-macOS/syllabo ~/.local/bin/
chmod +x ~/.local/bin/syllabo
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.zshrc
```

#### Uninstallation
```bash
# If you used the installer
./uninstall-unix.sh

# Or manually
sudo rm /usr/local/bin/syllabo
# or
rm ~/.local/bin/syllabo
```

## 🐳 Detailed Docker Instructions

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