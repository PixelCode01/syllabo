# Syllabo Standalone Builds

This document explains how to create and distribute standalone executables for Syllabo that don't require Python installation.

## Overview

Syllabo provides standalone executables for:
- **Windows** (.exe) - Single executable file
- **Linux** (binary) - Single executable file  
- **macOS** (binary) - Single executable file

These executables include all dependencies and can run on systems without Python installed.

## Building Standalone Executables

### Windows Build

```cmd
# Run the Windows build script
python build-windows.py

# Test the executable
dist\syllabo.exe --help

# Release package will be in release/ directory
```

### Linux Build

```bash
# Run the Linux build script
python build-linux.py

# Test the executable
./dist/syllabo --help

# Release package will be in release/ directory
```

### macOS Build

```bash
# Use the Linux build script (same process)
python build-linux.py

# Test the executable
./dist/syllabo --help
```

## Build Requirements

### System Requirements
- Python 3.8+ (for building only)
- PyInstaller 5.13.0+
- Platform-specific build tools

### Dependencies
All runtime dependencies are automatically bundled:
- textual==0.47.1
- rich==13.7.0
- youtube-transcript-api==0.6.1
- requests==2.31.0
- PyPDF2==3.0.1
- python-dotenv==1.0.0
- beautifulsoup4==4.12.2
- feedparser==6.0.10
- google-api-python-client==2.108.0
- google-generativeai==0.3.2

## Release Packages

Each platform build creates a complete release package:

### Windows Package (`syllabo-vX.X.X-Windows.zip`)
```
syllabo-vX.X.X-Windows/
├── syllabo.exe              # Main executable
├── install-windows.bat      # Automatic installer
├── uninstall-windows.bat    # Uninstaller
├── run_syllabo.bat         # Portable runner
├── .env.example            # Configuration template
└── README.txt              # Installation guide
```

### Linux Package (`syllabo-vX.X.X-Linux.tar.gz`)
```
syllabo-vX.X.X-Linux/
├── syllabo                 # Main executable
├── install-linux.sh        # Automatic installer
├── uninstall-linux.sh      # Uninstaller
├── run_syllabo.sh          # Portable runner
├── .env.example            # Configuration template
└── README.txt              # Installation guide
```

### macOS Package (`syllabo-vX.X.X-macOS.tar.gz`)
```
syllabo-vX.X.X-macOS/
├── syllabo                 # Main executable
├── install-macos.sh        # Automatic installer
├── uninstall-unix.sh       # Uninstaller
├── run_syllabo.sh          # Portable runner
├── .env.example            # Configuration template
└── README.txt              # Installation guide
```

## Installation Options

### Option 1: Automatic Installation (Recommended)

**Windows:**
```cmd
# Right-click and "Run as administrator"
install-windows.bat
```

**Linux/macOS:**
```bash
chmod +x install-*.sh
./install-*.sh
```

### Option 2: Portable Mode (No Installation)

**Windows:**
```cmd
# Double-click or run from command line
run_syllabo.bat
```

**Linux/macOS:**
```bash
chmod +x run_syllabo.sh
./run_syllabo.sh
```

### Option 3: Manual Installation

Copy the executable to a directory in your PATH and run directly.

## GitHub Actions Automation

The build process is automated using GitHub Actions:

### Workflow Triggers
- Push to tags matching `v*` (e.g., `v1.0.0`)
- Manual workflow dispatch

### Build Matrix
- **Windows**: `windows-latest` runner
- **Linux**: `ubuntu-latest` runner  
- **macOS**: `macos-latest` runner

### Artifacts
- Each platform creates a release package
- Packages are uploaded as GitHub release assets
- SHA256 checksums are generated for verification

## GitHub Pages Integration

The GitHub Pages site automatically links to the latest releases:

- **Download Page**: `https://username.github.io/syllabo`
- **Direct Links**: Point to latest release assets
- **Auto-Update**: Updates when new releases are published

### Download URLs
```
Windows: /releases/latest/download/syllabo-vX.X.X-Windows.zip
Linux:   /releases/latest/download/syllabo-vX.X.X-Linux.tar.gz
macOS:   /releases/latest/download/syllabo-vX.X.X-macOS.tar.gz
```

## Testing Builds

Use the test script to verify builds work correctly:

```bash
# Test current platform build
python test-standalone-builds.py
```

## Troubleshooting

### Build Issues

**PyInstaller fails:**
```bash
# Update PyInstaller
pip install --upgrade pyinstaller

# Clear cache
pyinstaller --clean
```

**Missing dependencies:**
```bash
# Install all requirements
pip install -r requirements.txt

# Install platform-specific packages
pip install pywin32 pywin32-ctypes  # Windows
```

**Large executable size:**
- This is normal for standalone builds (~30-40MB)
- All dependencies are bundled for portability
- Use `--strip` and `--noupx` for optimization

### Runtime Issues

**Executable won't start:**
- Check antivirus software (may quarantine)
- Verify platform compatibility
- Run from command line to see error messages

**Missing features:**
- Configure API keys in `.env` file
- Ensure internet connection for online features

**Permission denied (Linux/macOS):**
```bash
chmod +x syllabo
```

## Distribution

### Release Process
1. Tag a new version: `git tag v1.0.0`
2. Push tag: `git push origin v1.0.0`
3. GitHub Actions builds all platforms
4. Release is created with download links
5. GitHub Pages updates automatically

### File Verification
Each release includes SHA256 checksums:
```bash
# Verify download integrity
sha256sum -c syllabo-vX.X.X-Platform.sha256
```

## Security Considerations

### Code Signing
- Windows executables should be code signed for distribution
- macOS executables may need notarization
- Consider using certificates for production releases

### Antivirus Detection
- Standalone executables may trigger false positives
- Submit to antivirus vendors for whitelisting
- Provide checksums for verification

## Performance

### Startup Time
- First run may be slower (extracting bundled files)
- Subsequent runs are faster
- Use `--runtime-tmpdir` for better performance

### Memory Usage
- Standalone builds use more memory than Python scripts
- This is normal due to bundled interpreter
- Monitor with system tools if needed

## Support

For build-related issues:
- Check GitHub Actions logs
- Review PyInstaller documentation
- Open issues on the repository
- Test locally before releasing

---

**Note**: Standalone builds are created for distribution convenience. Users can still run from source if they prefer.