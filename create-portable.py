#!/usr/bin/env python3
"""
Create portable packages for Syllabo
These packages are completely self-contained and don't require any installation
"""

import os
import sys
import shutil
import zipfile
import tarfile
import platform
from pathlib import Path

def create_portable_package():
    """Create a portable package that can run anywhere"""
    
    system = platform.system()
    arch = platform.machine()
    
    if system == "Windows":
        exe_name = "syllabo.exe"
        package_ext = "zip"
    else:
        exe_name = "syllabo"
        package_ext = "tar.gz"
    
    exe_path = Path("dist") / exe_name
    
    if not exe_path.exists():
        print(f"Error: Executable not found at {exe_path}")
        print("Please run 'make build' or 'python build-local.py' first")
        return False
    
    # Create portable directory
    portable_name = f"syllabo-portable-{system}-{arch}"
    portable_dir = Path("portable") / portable_name
    
    # Clean and create directory
    if portable_dir.exists():
        shutil.rmtree(portable_dir)
    portable_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"Creating portable package: {portable_name}")
    
    # Copy executable
    shutil.copy2(exe_path, portable_dir / exe_name)
    
    # Make executable on Unix systems
    if system != "Windows":
        os.chmod(portable_dir / exe_name, 0o755)
    
    # Copy configuration files
    config_files = [".env.example", "LICENSE", "README.md"]
    for config_file in config_files:
        if Path(config_file).exists():
            shutil.copy2(config_file, portable_dir)
    
    # Create portable README
    portable_readme = f"""# Syllabo Portable - {system}

This is a portable version of Syllabo that runs without installation.

## Quick Start

### Windows:
1. Double-click `{exe_name}` or
2. Open Command Prompt in this folder and run: `{exe_name} interactive`

### Linux/macOS:
1. Open terminal in this folder
2. Run: `./{exe_name} interactive`

## Features

- ✅ No installation required
- ✅ No Python required  
- ✅ No dependencies required
- ✅ Runs from any location
- ✅ Completely self-contained

## Usage

```bash
# Interactive mode (recommended)
{'./' if system != 'Windows' else ''}{exe_name} interactive

# Analyze a syllabus
{'./' if system != 'Windows' else ''}{exe_name} analyze --file syllabus.pdf

# Generate quiz
{'./' if system != 'Windows' else ''}{exe_name} quiz --topic "Machine Learning"

# View progress
{'./' if system != 'Windows' else ''}{exe_name} progress

# Get help
{'./' if system != 'Windows' else ''}{exe_name} --help
```

## Configuration (Optional)

For enhanced features with API access:

1. Copy `.env.example` to `.env`
2. Edit `.env` and add your API keys:
   ```
   GOOGLE_API_KEY=your_youtube_api_key_here
   GEMINI_API_KEY=your_gemini_api_key_here
   ```

## Data Storage

Syllabo will create a `data` folder in the same directory as the executable
to store your progress, goals, and other information.

## Troubleshooting

### Windows
- If Windows Defender blocks the executable, click "More info" → "Run anyway"
- If you get a "Windows protected your PC" message, this is normal for unsigned executables

### Linux
- If you get "Permission denied", run: `chmod +x {exe_name}`
- If you get library errors, try running on a different Linux distribution

### macOS  
- If you get "cannot be opened because it is from an unidentified developer":
  1. Right-click the executable → "Open"
  2. Click "Open" in the dialog
- Or run: `xattr -d com.apple.quarantine {exe_name}`

## Support

- Documentation: https://github.com/PixelCode01/syllabo
- Issues: https://github.com/PixelCode01/syllabo/issues

---

**Syllabo Portable** - AI-Powered Learning Assistant
No installation, no dependencies, just learning! 🎓
"""
    
    with open(portable_dir / "README.txt", "w") as f:
        f.write(portable_readme)
    
    # Create run script for easier execution
    if system == "Windows":
        run_script = f"""@echo off
echo Starting Syllabo...
echo.
{exe_name} interactive
pause
"""
        with open(portable_dir / "run.bat", "w") as f:
            f.write(run_script)
    else:
        run_script = f"""#!/bin/bash
echo "Starting Syllabo..."
echo
./{exe_name} interactive
"""
        run_script_path = portable_dir / "run.sh"
        with open(run_script_path, "w") as f:
            f.write(run_script)
        os.chmod(run_script_path, 0o755)
    
    # Create archive
    archive_name = f"{portable_name}.{package_ext}"
    archive_path = Path("portable") / archive_name
    
    print(f"Creating archive: {archive_name}")
    
    if package_ext == "zip":
        with zipfile.ZipFile(archive_path, 'w', zipfile.ZIP_DEFLATED) as zf:
            for file_path in portable_dir.rglob('*'):
                if file_path.is_file():
                    arcname = file_path.relative_to(portable_dir.parent)
                    zf.write(file_path, arcname)
    else:
        with tarfile.open(archive_path, 'w:gz') as tf:
            tf.add(portable_dir, arcname=portable_name)
    
    # Get file size
    size_mb = archive_path.stat().st_size / (1024 * 1024)
    
    print(f"\n✅ Portable package created successfully!")
    print(f"📦 Package: {archive_path}")
    print(f"📏 Size: {size_mb:.1f} MB")
    print(f"🎯 Target: {system} {arch}")
    
    print(f"\n📋 Package contents:")
    print(f"   • {exe_name} - Main executable")
    print(f"   • README.txt - Usage instructions")
    print(f"   • {'run.bat' if system == 'Windows' else 'run.sh'} - Quick start script")
    if Path(".env.example").exists():
        print(f"   • .env.example - Configuration template")
    
    print(f"\n🚀 To test:")
    print(f"   1. Extract {archive_name}")
    print(f"   2. {'Double-click run.bat' if system == 'Windows' else 'Run ./run.sh'}")
    
    return True

def main():
    """Main entry point"""
    print("Syllabo Portable Package Creator")
    print("================================")
    
    if not create_portable_package():
        print("❌ Failed to create portable package")
        sys.exit(1)
    
    print("\n🎉 Portable package ready for distribution!")

if __name__ == "__main__":
    main()