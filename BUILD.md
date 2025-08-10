# Syllabo Build System

This document explains how to build Syllabo executables and create releases for Windows, Linux, and macOS.

## 🏗️ Build System Overview

The Syllabo build system provides multiple ways to create distributable packages:

- **Local builds** for testing on your current platform
- **GitHub Actions** for automated cross-platform builds
- **Docker builds** for consistent environments
- **Release management** with automatic versioning and tagging

## 🚀 Quick Start

### Local Build (Current Platform Only)

```bash
# Quick build for testing
make build-local
# or
python build-local.py

# Test the build
python test-build.py

# Run the executable
./dist/syllabo interactive  # Linux/macOS
dist\syllabo.exe interactive  # Windows
```

### Full Build with Installers

```bash
# Build with installer scripts
make build
# or
python build-all-platforms.py

# This creates:
# - Executable in dist/
# - Installer scripts (install-*.sh, install-*.bat)
# - Uninstaller scripts
# - Release packages in release/
```

## 📦 Release Process

### Automated Release (Recommended)

1. **Prepare the release:**
   ```bash
   # Patch release (1.0.0 → 1.0.1)
   make release-patch
   
   # Minor release (1.0.0 → 1.1.0)
   make release-minor
   
   # Major release (1.0.0 → 2.0.0)
   make release-major
   ```

2. **Push to GitHub:**
   ```bash
   git push origin main
   git push origin v1.0.1  # or your version
   ```

3. **GitHub Actions automatically:**
   - Builds for Windows, Linux, and macOS
   - Creates release packages
   - Uploads to GitHub Releases
   - Deploys documentation to GitHub Pages

### Manual Release

```bash
# Dry run to see what would happen
python release.py --dry-run

# Create a patch release
python release.py --bump patch

# Create a minor release  
python release.py --bump minor

# Create a major release
python release.py --bump major
```

## 🔧 Build Scripts

### `build-local.py`
Quick build for testing on current platform only.
- Installs PyInstaller
- Creates executable in `dist/`
- Minimal dependencies for fast iteration

### `build-all-platforms.py`
Comprehensive build script that creates:
- Platform-specific executables
- Installer and uninstaller scripts
- Release packages with documentation
- Cross-platform compatibility

### `release.py`
Release management script that:
- Bumps version numbers
- Updates changelog
- Creates git tags
- Pushes to remote repository

## 🐳 Docker Builds

### Build Docker Image

```bash
# Build the image
make docker-build

# Run interactively
make docker-run

# Development mode with mounted source
make docker-run-dev
```

### Docker Commands

```bash
# Build image
docker build -t syllabo:latest .

# Run with data persistence
docker run -it --rm \
  -v $(pwd)/data:/app/data \
  -v $(pwd)/logs:/app/logs \
  syllabo:latest

# Run specific command
docker run --rm syllabo:latest python main.py --help
```

## ⚙️ GitHub Actions

### Build and Release Workflow

Located in `.github/workflows/build-and-release.yml`, this workflow:

1. **Triggers on:**
   - Git tags starting with `v` (e.g., `v1.0.0`)
   - Manual workflow dispatch

2. **Builds for:**
   - Windows (latest)
   - Ubuntu Linux (latest)
   - macOS (latest)

3. **Creates:**
   - Executable packages for each platform
   - GitHub release with download links
   - Release notes with changelog

4. **Deploys:**
   - GitHub Pages with download site
   - Documentation and installation guides

### GitHub Pages Workflow

Located in `.github/workflows/pages.yml`, this workflow:

1. **Triggers on:**
   - Pushes to main branch
   - Manual workflow dispatch

2. **Creates:**
   - Beautiful download page
   - Platform-specific download links
   - Feature showcase
   - Documentation links

## 📁 Build Artifacts

### Directory Structure

```
syllabo/
├── build/              # PyInstaller build files (temporary)
├── dist/               # Built executables
│   ├── syllabo         # Linux/macOS executable
│   └── syllabo.exe     # Windows executable
├── release/            # Release packages
│   ├── syllabo-v1.0.0-Windows.zip
│   ├── syllabo-v1.0.0-Linux.tar.gz
│   └── syllabo-v1.0.0-macOS.tar.gz
├── install-*.sh        # Unix installer scripts
├── install-*.bat       # Windows installer scripts
├── uninstall-*.sh      # Unix uninstaller scripts
└── uninstall-*.bat     # Windows uninstaller scripts
```

### Package Contents

Each release package contains:
- Platform-specific executable
- Installer script
- Uninstaller script
- `.env.example` configuration file
- `README.txt` with installation instructions
- `LICENSE` file (if present)

## 🛠️ Development Builds

### Prerequisites

- Python 3.7+
- pip package manager
- Git (for release management)

### Setup Development Environment

```bash
# Clone repository
git clone https://github.com/PixelCode01/syllabo.git
cd syllabo

# Install dependencies
make install
# or
pip install -r requirements.txt
pip install pyinstaller

# Set up development tools (optional)
make dev-setup
```

### Build Commands

```bash
# Quick local build
make build-local

# Full build with packages
make build

# Test the build
python test-build.py

# Clean build artifacts
make clean

# Check dependencies
make check-deps

# Show build information
make info
```

## 🔍 Troubleshooting

### Common Build Issues

#### PyInstaller Errors

**Problem:** `ModuleNotFoundError` during build
```bash
# Solution: Add missing modules to hidden imports
pyinstaller --hidden-import=missing_module main.py
```

**Problem:** `lxml` installation fails on Windows
```bash
# Solution: Install pre-built wheel
pip install --only-binary=lxml lxml
```

#### Windows Build Issues

**Problem:** "Microsoft Visual C++ 14.0 is required"
```bash
# Solution: Install Visual C++ Build Tools
# Download from: https://visualstudio.microsoft.com/visual-cpp-build-tools/
```

**Problem:** Permission denied during installation
```bash
# Solution: Run installer as administrator
# Right-click install-windows.bat → "Run as administrator"
```

#### Linux/macOS Issues

**Problem:** Permission denied for executable
```bash
# Solution: Make executable
chmod +x dist/syllabo
```

**Problem:** Command not found after installation
```bash
# Solution: Reload PATH
source ~/.bashrc  # Linux
source ~/.zshrc   # macOS
```

### Build Environment Issues

#### Missing Dependencies

```bash
# Check what's missing
make check-deps

# Install missing packages
pip install -r requirements.txt
```

#### Python Version Issues

```bash
# Check Python version
python --version

# Syllabo requires Python 3.7+
# Update Python if needed
```

### Testing Builds

```bash
# Run comprehensive tests
python test-build.py

# Test specific functionality
./dist/syllabo --help
./dist/syllabo interactive

# Test with sample data
./dist/syllabo analyze --file sample.pdf
```

## 📋 Build Checklist

Before creating a release:

- [ ] All tests pass (`python test-build.py`)
- [ ] Version number updated
- [ ] Changelog updated
- [ ] Documentation updated
- [ ] Build works on target platforms
- [ ] Installer scripts tested
- [ ] GitHub Actions workflow passes

## 🤝 Contributing to Builds

### Adding New Platforms

1. Update `build-all-platforms.py` with platform-specific settings
2. Create platform-specific installer script
3. Update GitHub Actions workflow
4. Test on target platform

### Improving Build Process

1. Fork the repository
2. Make changes to build scripts
3. Test thoroughly
4. Submit pull request with description

### Reporting Build Issues

1. Check existing issues on GitHub
2. Include platform and Python version
3. Provide full error messages
4. Include steps to reproduce

---

For more information, see:
- [Installation Guide](INSTALLATION.md)
- [Contributing Guidelines](CONTRIBUTING.md)
- [GitHub Issues](https://github.com/PixelCode01/syllabo/issues)