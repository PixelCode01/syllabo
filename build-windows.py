#!/usr/bin/env python3
"""
Windows build script for Syllabo - Creates standalone executable
"""

import os
import sys
import subprocess
import shutil
import platform
from pathlib import Path

def run_command(cmd, timeout=300):
    """Run command and return success status"""
    try:
        print(f"Running: {cmd}")
        result = subprocess.run(cmd, shell=True, check=True,
                              capture_output=True, text=True, timeout=timeout)
        print("Success")
        return True, result.stdout
    except subprocess.TimeoutExpired:
        print(f"Timeout after {timeout} seconds")
        return False, "Command timed out"
    except subprocess.CalledProcessError as e:
        print(f"Failed with exit code {e.returncode}")
        if e.stderr:
            print(f"Error: {e.stderr}")
        return False, e.stderr

def main():
    """Main build process"""
    print("Syllabo Windows Build Script")
    print("============================")
    
    # Check if we're in the right directory
    if not Path("main.py").exists():
        print("Error: main.py not found. Run from Syllabo root directory")
        sys.exit(1)
    
    print(f"Python {sys.version}")
    print("main.py found")
    
    # Warning about antivirus software
    print("\nIMPORTANT: Windows Defender may flag the executable as suspicious.")
    print("This is a false positive common with PyInstaller executables.")
    print("See WINDOWS_DEFENDER_GUIDE.md for solutions.")
    
    # Install dependencies
    print("\nInstalling build dependencies...")
    success, output = run_command("pip install pyinstaller>=5.0")
    if not success:
        print("Failed to install PyInstaller")
        sys.exit(1)
    
    success, output = run_command("pip install -r requirements.txt")
    if not success:
        print("Warning: Some requirements failed to install")
    
    # Clean previous builds
    print("\nCleaning previous builds...")
    for dir_name in ["build", "dist"]:
        if Path(dir_name).exists():
            shutil.rmtree(dir_name)
            print(f"Removed {dir_name}")
    
    # Build executable using the simple command that worked before
    print("\nBuilding Windows executable...")
    cmd = 'pyinstaller --onefile --console --name=syllabo "--add-data=src;src" --clean --noconfirm main.py'
    success, output = run_command(cmd, timeout=600)
    
    if not success:
        print("[FAIL] Build failed!")
        sys.exit(1)
    
    # Test executable
    print("\nTesting executable...")
    exe_path = Path("dist/syllabo.exe")
    if not exe_path.exists():
        print("[FAIL] Executable not found")
        sys.exit(1)
    
    success, output = run_command("dist\\syllabo.exe --help", timeout=30)
    if not success:
        print("[FAIL] Executable test failed")
        sys.exit(1)
    
    print("Executable test passed")
    
    # Create release package
    print("\nCreating release package...")
    release_dir = Path("release")
    if release_dir.exists():
        shutil.rmtree(release_dir)
    release_dir.mkdir()
    
    # Copy executable
    shutil.copy2(exe_path, release_dir / "syllabo.exe")
    
    # Copy additional files
    files_to_copy = [
        "README.md", "LICENSE", ".env.example", "INSTALLATION.md",
        "WINDOWS_DEFENDER_GUIDE.md", "ANTIVIRUS_TROUBLESHOOTING.md",
        "WINDOWS_README.md"
    ]
    for file_name in files_to_copy:
        if Path(file_name).exists():
            shutil.copy2(file_name, release_dir / file_name)
    
    # Create runner script
    runner_script = """@echo off
echo Starting Syllabo...
echo.
syllabo.exe interactive
pause
"""
    with open(release_dir / "run_syllabo.bat", "w") as f:
        f.write(runner_script)
    
    # Copy safe runner if it exists
    if Path("run_syllabo_safe.bat").exists():
        shutil.copy2("run_syllabo_safe.bat", release_dir / "run_syllabo_safe.bat")
    
    # Create Windows install guide
    install_guide = """# Syllabo Windows Package

## Important: Antivirus Software Notice

Windows Defender may flag this executable as suspicious. This is a false positive common with PyInstaller executables. The software is safe to use.

### If Windows Defender blocks the file:
1. Open Windows Security
2. Go to "Virus & threat protection"
3. Click "Manage settings" under protection settings
4. Add an exclusion for the syllabo.exe file

## Quick Start
1. Double-click `run_syllabo.bat` to start
2. Or run `syllabo.exe` from command line

## Usage
- Run `syllabo.exe --help` for all commands
- Run `syllabo.exe interactive` for interactive mode

## Support
- GitHub: https://github.com/PixelCode01/syllabo
- Issues: https://github.com/PixelCode01/syllabo/issues
"""
    
    with open(release_dir / "WINDOWS_INSTALL.md", "w") as f:
        f.write(install_guide)
    
    # Show results
    exe_size = exe_path.stat().st_size / (1024 * 1024)
    print("Release package created")
    print(f"Executable size: {exe_size:.1f} MB")
    print("Files included:")
    for file in release_dir.iterdir():
        print(f"  - {file.name}")
    
    print("\n[SUCCESS] Windows build completed successfully!")
    print("\nNext steps:")
    print("1. Test: release\\syllabo.exe --help")
    print("2. Run: release\\syllabo.exe interactive")
    print("3. Share the 'release' folder with users")

if __name__ == "__main__":
    main()