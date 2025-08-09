#!/usr/bin/env python3
"""
Local build script for Syllabo executables
This script attempts to build executables locally with better error handling
"""

import os
import sys
import subprocess
import platform
import shutil
from pathlib import Path

def run_command(cmd, cwd=None, check=True):
    """Run a command and return result"""
    try:
        result = subprocess.run(cmd, shell=True, cwd=cwd, check=check, 
                              capture_output=True, text=True)
        return result.returncode == 0, result.stdout, result.stderr
    except subprocess.CalledProcessError as e:
        return False, e.stdout, e.stderr

def install_dependencies():
    """Install dependencies with better error handling"""
    print("Installing dependencies...")
    
    # Try to install without lxml first
    basic_deps = [
        "textual==0.47.1",
        "rich==13.7.0", 
        "youtube-transcript-api==0.6.1",
        "requests==2.31.0",
        "PyPDF2==3.0.1",
        "python-dotenv==1.0.0",
        "beautifulsoup4==4.12.2",
        "feedparser==6.0.10",
        "google-api-python-client==2.108.0",
        "google-generativeai==0.3.2",
        "pyinstaller"
    ]
    
    for dep in basic_deps:
        success, stdout, stderr = run_command(f"pip install {dep}")
        if not success:
            print(f"Failed to install {dep}: {stderr}")
            return False
    
    # Try to install lxml separately with pre-built wheel
    print("Installing lxml...")
    success, stdout, stderr = run_command("pip install --only-binary=lxml lxml==4.9.3")
    if not success:
        print("Warning: lxml installation failed. Some features may not work.")
        print("You can continue without lxml or install it manually.")
        
    return True

def build_executable():
    """Build executable with PyInstaller"""
    print("Building executable...")
    
    # Clean previous builds
    for dir_name in ["build", "dist"]:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
    
    # Determine platform
    system = platform.system()
    if system == "Windows":
        exe_name = "syllabo.exe"
        data_sep = ";"
    else:
        exe_name = "syllabo"
        data_sep = ":"
    
    # Build command - simplified to avoid lxml issues
    cmd = f"""pyinstaller --onefile --name {exe_name} \
        --add-data "src{data_sep}src" \
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
    
    success, stdout, stderr = run_command(cmd)
    if success:
        print(f"✓ Executable built successfully: dist/{exe_name}")
        return True
    else:
        print(f"✗ Build failed: {stderr}")
        return False

def main():
    """Main build process"""
    print("Syllabo Local Build Script")
    print("==========================")
    
    if not os.path.exists("main.py"):
        print("Error: Please run this script from the Syllabo root directory")
        sys.exit(1)
    
    # Install dependencies
    if not install_dependencies():
        print("Failed to install all dependencies. You may need to install them manually.")
        print("Try: pip install -r requirements.txt")
        
        # Ask if user wants to continue anyway
        response = input("Continue with build anyway? (y/N): ")
        if response.lower() != 'y':
            sys.exit(1)
    
    # Build executable
    if build_executable():
        print("\n✓ Build completed successfully!")
        print(f"Executable location: dist/")
        print("\nTo test the executable:")
        if platform.system() == "Windows":
            print("  dist\\syllabo.exe interactive")
        else:
            print("  ./dist/syllabo interactive")
    else:
        print("\n✗ Build failed!")
        print("\nTroubleshooting:")
        print("1. Make sure you have Python 3.7+ installed")
        print("2. Try installing Visual C++ Build Tools (Windows)")
        print("3. Use Docker instead: make build && make run")
        sys.exit(1)

if __name__ == "__main__":
    main()