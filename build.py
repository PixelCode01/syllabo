#!/usr/bin/env python3
"""
Build script for creating distributable Syllabo packages
"""

import os
import sys
import subprocess
import platform
import shutil
from pathlib import Path

def run_command(cmd, cwd=None):
    """Run a command and return success status"""
    try:
        result = subprocess.run(cmd, shell=True, cwd=cwd, check=True, 
                              capture_output=True, text=True)
        print(f"✓ {cmd}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ {cmd}")
        print(f"Error: {e.stderr}")
        return False

def build_pyinstaller():
    """Build executable using PyInstaller"""
    print("Building executable with PyInstaller...")
    
    # Install PyInstaller if not present
    if not run_command("pip install pyinstaller"):
        return False
    
    # Clean previous builds
    if os.path.exists("dist"):
        shutil.rmtree("dist")
    if os.path.exists("build"):
        shutil.rmtree("build")
    
    # Determine platform-specific settings
    system = platform.system()
    if system == "Windows":
        exe_name = "syllabo.exe"
        data_separator = ";"
    else:
        exe_name = "syllabo"
        data_separator = ":"
    
    # Build command
    cmd = f"""pyinstaller --onefile --name {exe_name} \
        --add-data "src{data_separator}src" \
        --add-data ".env.example{data_separator}." \
        --hidden-import=src.database \
        --hidden-import=src.logger \
        --hidden-import=src.ai_client \
        --hidden-import=src.syllabus_parser \
        --hidden-import=src.quiz_generator \
        --hidden-import=src.progress_dashboard \
        --hidden-import=src.goals_manager \
        --hidden-import=src.platform_integrator \
        --hidden-import=src.bookmark_manager \
        --hidden-import=src.study_session_manager \
        --hidden-import=src.spaced_repetition \
        --hidden-import=src.notes_generator \
        --hidden-import=src.video_analyzer \
        --hidden-import=src.resource_finder \
        --hidden-import=src.youtube_client \
        --console \
        main.py"""
    
    if run_command(cmd):
        print(f"✓ Executable built: dist/{exe_name}")
        return True
    return False

def build_docker():
    """Build Docker image"""
    print("Building Docker image...")
    
    if not run_command("docker build -t syllabo:latest ."):
        return False
    
    print("✓ Docker image built: syllabo:latest")
    return True

def create_installer_script():
    """Create installation scripts"""
    print("Creating installer scripts...")
    
    # Windows installer script
    windows_installer = """@echo off
echo Installing Syllabo...

REM Create installation directory
if not exist "%USERPROFILE%\\Syllabo" mkdir "%USERPROFILE%\\Syllabo"

REM Copy executable
copy syllabo.exe "%USERPROFILE%\\Syllabo\\"
copy .env.example "%USERPROFILE%\\Syllabo\\"

REM Add to PATH (requires admin)
echo Adding Syllabo to PATH...
setx PATH "%PATH%;%USERPROFILE%\\Syllabo"

echo.
echo Syllabo installed successfully!
echo You can now run 'syllabo' from any command prompt.
echo.
echo To get started:
echo   1. Copy .env.example to .env and add your API keys (optional)
echo   2. Run 'syllabo interactive' to start the interactive mode
echo.
pause
"""
    
    # Linux/macOS installer script
    unix_installer = """#!/bin/bash
echo "Installing Syllabo..."

# Create installation directory
mkdir -p "$HOME/.local/bin"
mkdir -p "$HOME/.local/share/syllabo"

# Copy files
cp syllabo "$HOME/.local/bin/"
cp .env.example "$HOME/.local/share/syllabo/"
chmod +x "$HOME/.local/bin/syllabo"

# Add to PATH if not already there
if [[ ":$PATH:" != *":$HOME/.local/bin:"* ]]; then
    echo 'export PATH="$HOME/.local/bin:$PATH"' >> "$HOME/.bashrc"
    echo 'export PATH="$HOME/.local/bin:$PATH"' >> "$HOME/.zshrc" 2>/dev/null || true
fi

echo ""
echo "Syllabo installed successfully!"
echo "You may need to restart your terminal or run:"
echo "  source ~/.bashrc"
echo ""
echo "To get started:"
echo "  1. Copy ~/.local/share/syllabo/.env.example to .env and add your API keys (optional)"
echo "  2. Run 'syllabo interactive' to start the interactive mode"
echo ""
"""
    
    with open("install.bat", "w") as f:
        f.write(windows_installer)
    
    with open("install.sh", "w") as f:
        f.write(unix_installer)
    
    # Make Unix installer executable
    if platform.system() != "Windows":
        os.chmod("install.sh", 0o755)
    
    print("✓ Installer scripts created")
    return True

def create_release_package():
    """Create release package"""
    print("Creating release package...")
    
    system = platform.system()
    arch = platform.machine()
    package_name = f"syllabo-{system}-{arch}"
    
    # Create package directory
    package_dir = Path("release") / package_name
    package_dir.mkdir(parents=True, exist_ok=True)
    
    # Copy files
    if system == "Windows":
        shutil.copy("dist/syllabo.exe", package_dir)
        shutil.copy("install.bat", package_dir)
    else:
        shutil.copy("dist/syllabo", package_dir)
        shutil.copy("install.sh", package_dir)
    
    shutil.copy(".env.example", package_dir)
    shutil.copy("README.md", package_dir)
    
    # Create README for the package
    package_readme = f"""# Syllabo - Portable Installation

This package contains a portable version of Syllabo for {system}.

## Quick Start

### Option 1: Run the installer
- Windows: Double-click `install.bat`
- Linux/macOS: Run `./install.sh`

### Option 2: Manual installation
1. Copy the executable to a directory in your PATH
2. Copy `.env.example` to `.env` and configure if needed
3. Run `syllabo interactive` to start

## Usage

```bash
# Interactive mode
syllabo interactive

# Analyze a syllabus
syllabo analyze --file syllabus.pdf

# Generate quiz
syllabo quiz --topic "Machine Learning"

# View progress
syllabo progress

# Get help
syllabo --help
```

For full documentation, visit: https://github.com/PixelCode01/syllabo
"""
    
    with open(package_dir / "README.txt", "w") as f:
        f.write(package_readme)
    
    print(f"✓ Release package created: release/{package_name}")
    return True

def main():
    """Main build process"""
    print("Syllabo Build Script")
    print("===================")
    
    # Check if we're in the right directory
    if not os.path.exists("main.py"):
        print("Error: Please run this script from the Syllabo root directory")
        sys.exit(1)
    
    # Install dependencies
    print("Installing dependencies...")
    if not run_command("pip install -r requirements.txt"):
        print("Failed to install dependencies")
        sys.exit(1)
    
    success = True
    
    # Build executable
    if not build_pyinstaller():
        success = False
    
    # Create installer scripts
    if not create_installer_script():
        success = False
    
    # Create release package
    if not create_release_package():
        success = False
    
    # Build Docker image (optional)
    print("\nBuilding Docker image (optional)...")
    build_docker()  # Don't fail if Docker isn't available
    
    if success:
        print("\n✓ Build completed successfully!")
        print("\nNext steps:")
        print("1. Test the executable in dist/")
        print("2. Test the installer scripts")
        print("3. Upload release/ contents to GitHub releases")
        print("4. Push Docker image to registry")
    else:
        print("\n✗ Build failed!")
        sys.exit(1)

if __name__ == "__main__":
    main()