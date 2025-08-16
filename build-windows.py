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
    
    # Build executable using directory mode (not onefile) to avoid AV detection
    print("\nBuilding Windows executable (directory mode)...")
    cmd = 'pyinstaller --console --name=syllabo "--add-data=src;src" --clean --noconfirm main.py'
    success, output = run_command(cmd, timeout=600)
    
    if not success:
        print("[FAIL] Build failed!")
        sys.exit(1)
    
    # Test executable
    print("\nTesting executable...")
    exe_path = Path("dist/syllabo/syllabo.exe")
    if not exe_path.exists():
        print("[FAIL] Executable not found")
        sys.exit(1)
    
    success, output = run_command("dist\\syllabo\\syllabo.exe --help", timeout=30)
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
    
    # Copy the entire syllabo directory from dist
    syllabo_dist_dir = Path("dist/syllabo")
    syllabo_release_dir = release_dir / "syllabo"
    shutil.copytree(syllabo_dist_dir, syllabo_release_dir)
    
    # Copy additional files to the main directory
    files_to_copy = [
        "README.md", "LICENSE", ".env.example", "INSTALLATION.md",
        "WINDOWS_DEFENDER_GUIDE.md", "ANTIVIRUS_TROUBLESHOOTING.md",
        "WINDOWS_README.md"
    ]
    for file_name in files_to_copy:
        if Path(file_name).exists():
            shutil.copy2(file_name, syllabo_release_dir / file_name)
    
    # Create runner script in the syllabo directory
    runner_script = """@echo off
echo Starting Syllabo...
echo.
syllabo.exe interactive
pause
"""
    with open(syllabo_release_dir / "run_syllabo.bat", "w") as f:
        f.write(runner_script)
    
    # Copy safe runner if it exists
    if Path("run_syllabo_safe.bat").exists():
        shutil.copy2("run_syllabo_safe.bat", syllabo_release_dir / "run_syllabo_safe.bat")
    
    # Create Windows install guide
    install_guide = """# Syllabo Windows Package

## Quick Start
1. Extract the zip file to your desired location
2. Double-click `run_syllabo.bat` to start
3. Or run `syllabo.exe` from command line

## Directory Structure
- `syllabo.exe` - Main executable
- `_internal/` - Required runtime files (do not delete)
- `src/` - Application source files
- Documentation and example files

## Usage
- Run `syllabo.exe --help` for all commands
- Run `syllabo.exe interactive` for interactive mode

## Important Notes
- Keep all files in the same directory
- Do not separate syllabo.exe from the _internal folder
- This directory-based format avoids antivirus false positives

## Support
- GitHub: https://github.com/PixelCode01/syllabo
- Issues: https://github.com/PixelCode01/syllabo/issues
"""
    
    with open(syllabo_release_dir / "WINDOWS_INSTALL.md", "w") as f:
        f.write(install_guide)
    
    # Create ZIP file
    print("\nCreating ZIP archive...")
    import zipfile
    
    zip_filename = f"syllabo-Windows-{platform.machine()}.zip"
    zip_path = release_dir / zip_filename
    
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(syllabo_release_dir):
            for file in files:
                file_path = Path(root) / file
                # Create archive path relative to syllabo directory
                arcname = file_path.relative_to(release_dir)
                zipf.write(file_path, arcname)
    
    # Show results
    exe_size = exe_path.stat().st_size / (1024 * 1024)
    zip_size = zip_path.stat().st_size / (1024 * 1024)
    print("Release package created")
    print(f"Executable size: {exe_size:.1f} MB")
    print(f"ZIP archive size: {zip_size:.1f} MB")
    print(f"ZIP file: {zip_filename}")
    print("Files included in directory:")
    for file in syllabo_release_dir.rglob("*"):
        if file.is_file():
            print(f"  - {file.relative_to(syllabo_release_dir)}")
    
    print("\n[SUCCESS] Windows build completed successfully!")
    print("\nNext steps:")
    print(f"1. Test: release\\syllabo\\syllabo.exe --help")
    print(f"2. Run: release\\syllabo\\syllabo.exe interactive")
    print(f"3. Upload {zip_filename} to GitHub releases")

if __name__ == "__main__":
    main()