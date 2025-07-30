#!/usr/bin/env python3

import os
import sys
import subprocess

def check_dependencies():
    """Check if required packages are installed"""
    required_packages = ['requests', 'beautifulsoup4', 'lxml']
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print("Missing required packages:")
        for package in missing_packages:
            print(f"  - {package}")
        print("\nInstalling missing packages...")
        
        for package in missing_packages:
            try:
                subprocess.check_call([sys.executable, "-m", "pip", "install", package])
                print(f"Installed {package}")
            except subprocess.CalledProcessError:
                print(f"Failed to install {package}")
                return False
    
    return True

def main():
    print("=" * 60)
    print("                SYLLABO LAUNCHER")
    print("         YouTube Video Finder + Study Materials")
    print("=" * 60)
    
    print("\nChecking dependencies...")
    if not check_dependencies():
        print("Failed to install required packages. Please install manually:")
        print("pip install requests beautifulsoup4 lxml")
        return
    
    print("All dependencies available")
    
    print("\nAvailable options:")
    print("1. Run main application (syllabo_final.py)")
    print("2. Test YouTube scraping")
    print("3. Demo study materials generation")
    print("4. Verify video links generation")
    print("5. Exit")
    
    while True:
        try:
            choice = input("\nChoose option (1-5): ").strip()
            
            if choice == '1':
                print("\nStarting main application...")
                subprocess.run([sys.executable, "syllabo_final.py"])
                break
            elif choice == '2':
                print("\nTesting YouTube scraping...")
                subprocess.run([sys.executable, "test_youtube_scraping.py"])
                break
            elif choice == '3':
                print("\nDemo study materials...")
                subprocess.run([sys.executable, "demo_study_materials.py"])
                break
            elif choice == '4':
                print("\nVerifying video links...")
                subprocess.run([sys.executable, "verify_video_links.py"])
                break
            elif choice == '5':
                print("Goodbye!")
                break
            else:
                print("Invalid choice. Please enter 1-5.")
                
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break

if __name__ == "__main__":
    main()