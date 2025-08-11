#!/usr/bin/env python3
"""
Local build script for Syllabo
Quick build for testing on current platform
"""

import os
import sys
import subprocess
import platform
import shutil
from pathlib import Path

def run_command(cmd, cwd=None):
    """Run command and return success status"""
    try:
        result = subprocess.run(cmd, shell=True, cwd=cwd, check=True,
                              capture_output=True, text=True)
        print(f"✓ {cmd}")
        return True, result.stdout
    except subprocess.CalledProcessError as e:
        print(f"✗ {cmd}")
        print(f"Error: {e.stderr}")
        return False, e.stderr

def main():
    """Quick local build"""
    print("Syllabo Local Build")
    print("==================")
    
    if not Path("main.py").exists():
        print("Error: Please run from Syllabo root directory")
        sys.exit(1)
    
    # Clean previous builds
    for dir_name in ["build", "dist"]:
        if Path(dir_name).exists():
            shutil.rmtree(dir_name)
    
    # Install dependencies
    print("\nInstalling dependencies...")
    success, output = run_command("pip install pyinstaller")
    if not success:
        print("Failed to install PyInstaller")
        sys.exit(1)
    
    # Try to install requirements (don't fail if some packages fail)
    print("Installing app requirements...")
    run_command("pip install -r requirements.txt")
    
    # Build executable
    print("\nBuilding executable...")
    
    system = platform.system()
    if system == "Windows":
        exe_name = "syllabo.exe"
        data_sep = ";"
    else:
        exe_name = "syllabo"
        data_sep = ":"
    
    # Standalone build command with all dependencies
    cmd_parts = [
        "pyinstaller",
        "--onefile",
        f"--name={exe_name}",
        f"--add-data=src{data_sep}src",
        
        # Include all required modules for standalone execution
        "--hidden-import=src.database",
        "--hidden-import=src.logger", 
        "--hidden-import=src.ai_client",
        "--hidden-import=src.syllabus_parser",
        "--hidden-import=src.quiz_generator",
        "--hidden-import=src.progress_dashboard",
        "--hidden-import=src.goals_manager",
        "--hidden-import=src.platform_integrator",
        "--hidden-import=src.bookmark_manager",
        "--hidden-import=src.study_session_manager",
        "--hidden-import=src.spaced_repetition",
        "--hidden-import=src.notes_generator",
        "--hidden-import=src.video_analyzer",
        "--hidden-import=src.video_analyzer_fast",
        "--hidden-import=src.resource_finder",
        "--hidden-import=src.youtube_client",
        "--hidden-import=src.setup_manager",
        "--hidden-import=src.config_manager",
        "--hidden-import=src.validation_utils",
        "--hidden-import=src.performance_monitor",
        "--hidden-import=src.config_validator",
        
        # Third-party dependencies
        "--hidden-import=textual",
        "--hidden-import=rich",
        "--hidden-import=requests",
        "--hidden-import=PyPDF2",
        "--hidden-import=beautifulsoup4",
        "--hidden-import=feedparser",
        "--hidden-import=google.generativeai",
        "--hidden-import=googleapiclient",
        "--hidden-import=youtube_transcript_api",
        "--hidden-import=dotenv",
        
        # Collect all submodules
        "--collect-all=textual",
        "--collect-all=rich",
        "--collect-all=requests",
        "--collect-all=google",
        
        # Standalone options
        "--console",
        "--clean",
        "--noconfirm",
        "--strip",
        "--noupx",
        "main.py"
    ]
    
    cmd = " ".join(cmd_parts)
    
    # Try spec file first if it exists
    spec_file = Path("syllabo.spec")
    if spec_file.exists():
        print("Using PyInstaller spec file...")
        success, output = run_command("pyinstaller --clean --noconfirm syllabo.spec")
    else:
        success, output = run_command(cmd)
    
    if success:
        print(f"\n✓ Build completed successfully!")
        print(f"Executable: dist/{exe_name}")
        
        # Test the executable
        print("\nTesting executable...")
        test_success, test_output = run_command(f"dist/{exe_name} --help", timeout=10)
        if test_success:
            print("✓ Executable test passed")
        else:
            print("⚠ Executable test failed - but build completed")
        
        print(f"\nTo run:")
        if system == "Windows":
            print(f"  dist\\{exe_name} interactive")
        else:
            print(f"  ./dist/{exe_name} interactive")
    else:
        print(f"\n✗ Build failed!")
        print("Trying simple fallback build...")
        
        # Try simple fallback
        simple_cmd = f"pyinstaller --onefile --name {exe_name} --console --clean main.py"
        success, output = run_command(simple_cmd)
        
        if success:
            print("✓ Fallback build successful!")
        else:
            print("✗ All build methods failed!")
            print("Try installing Visual C++ Build Tools (Windows) or build dependencies")
            sys.exit(1)

if __name__ == "__main__":
    main()