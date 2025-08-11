#!/usr/bin/env python3
"""
Build standalone executable for current platform
"""

import platform
import subprocess
import sys
from pathlib import Path

def main():
    current_os = platform.system()
    
    print(f"Building Syllabo for {current_os}...")
    print(f"Python version: {sys.version}")
    print()
    
    if not Path("main.py").exists():
        print("Error: main.py not found. Run from Syllabo root directory")
        sys.exit(1)
    
    if current_os == "Windows":
        script = "build-windows.py"
    elif current_os in ["Linux", "Darwin"]:  # Darwin is macOS
        script = "build-linux.py"
    else:
        print(f"Unsupported platform: {current_os}")
        sys.exit(1)
    
    try:
        subprocess.run([sys.executable, script], check=True)
        print(f"\n✓ Build completed successfully for {current_os}")
        
        # Show release files
        release_dir = Path("release")
        if release_dir.exists():
            print(f"\nRelease files:")
            for file in release_dir.iterdir():
                if file.is_file():
                    size_mb = file.stat().st_size / (1024 * 1024)
                    print(f"  - {file.name} ({size_mb:.1f} MB)")
        
    except subprocess.CalledProcessError as e:
        print(f"\n✗ Build failed with exit code {e.returncode}")
        sys.exit(1)

if __name__ == "__main__":
    main()