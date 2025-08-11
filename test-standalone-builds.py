#!/usr/bin/env python3
"""
Test script to verify standalone builds work correctly
"""

import os
import sys
import subprocess
import platform
from pathlib import Path

def run_command(cmd, timeout=60):
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
        print(f"Error: {e.stderr}")
        return False, e.stderr

def test_windows_build():
    """Test Windows build"""
    print("\n" + "="*50)
    print("TESTING WINDOWS BUILD")
    print("="*50)
    
    if platform.system() != "Windows":
        print("Skipping Windows build test (not on Windows)")
        return True
    
    # Run Windows build
    success, output = run_command("python build-windows.py", timeout=600)
    if not success:
        print("Windows build failed")
        return False
    
    # Check if executable exists
    exe_path = Path("dist/syllabo.exe")
    if not exe_path.exists():
        print("Windows executable not found")
        return False
    
    # Test executable
    success, output = run_command("dist\\syllabo.exe --help", timeout=30)
    if not success:
        print("Windows executable test failed")
        return False
    
    print("Windows build test passed")
    return True

def test_linux_build():
    """Test Linux build"""
    print("\n" + "="*50)
    print("TESTING LINUX BUILD")
    print("="*50)
    
    if platform.system() != "Linux":
        print("Skipping Linux build test (not on Linux)")
        return True
    
    # Run Linux build
    success, output = run_command("python build-linux.py", timeout=600)
    if not success:
        print("Linux build failed")
        return False
    
    # Check if executable exists
    exe_path = Path("dist/syllabo")
    if not exe_path.exists():
        print("Linux executable not found")
        return False
    
    # Make executable
    os.chmod(exe_path, 0o755)
    
    # Test executable
    success, output = run_command("./dist/syllabo --help", timeout=30)
    if not success:
        print("Linux executable test failed")
        return False
    
    print("Linux build test passed")
    return True

def test_current_platform():
    """Test build for current platform"""
    current_os = platform.system()
    
    if current_os == "Windows":
        return test_windows_build()
    elif current_os == "Linux":
        return test_linux_build()
    else:
        print(f"Unsupported platform: {current_os}")
        return False

def main():
    """Main test function"""
    print("Syllabo Standalone Build Test")
    print("============================")
    print(f"Platform: {platform.system()}")
    print(f"Python: {sys.version}")
    
    # Check if we're in the right directory
    if not Path("main.py").exists():
        print("Error: main.py not found. Run from Syllabo root directory")
        sys.exit(1)
    
    # Test current platform
    success = test_current_platform()
    
    if success:
        print("\n" + "="*50)
        print("ALL TESTS PASSED!")
        print("="*50)
        print("Standalone build is working correctly")
        
        # Show release files
        release_dir = Path("release")
        if release_dir.exists():
            print(f"\nRelease files in {release_dir}:")
            for file in release_dir.iterdir():
                if file.is_file():
                    size_mb = file.stat().st_size / (1024 * 1024)
                    print(f"  - {file.name} ({size_mb:.1f} MB)")
    else:
        print("\n" + "="*50)
        print("TESTS FAILED!")
        print("="*50)
        print("Check the error messages above")
        sys.exit(1)

if __name__ == "__main__":
    main()