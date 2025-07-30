#!/usr/bin/env python3

import os
import subprocess
import sys

def print_banner():
    print("=" * 60)
    print("                SYLLABO SETUP")
    print("         AI-Powered Study Guide Generator")
    print("=" * 60)

def install_requirements():
    print("Installing Python dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("Dependencies installed successfully!")
        return True
    except subprocess.CalledProcessError:
        print("Error installing dependencies. Please install manually:")
        print("pip install -r requirements.txt")
        return False

def create_env_file():
    if not os.path.exists('.env'):
        print("Creating .env file...")
        with open('.env', 'w') as f:
            f.write("# Syllabo Configuration\n")
            f.write("# These are optional - app works without API keys\n\n")
            f.write("# Optional: Gemini API for enhanced AI features\n")
            f.write("GEMINI_API_KEY=your_gemini_api_key_here_optional\n\n")
            f.write("# Optional: YouTube API for additional metadata\n")
            f.write("YOUTUBE_API_KEY=your_youtube_api_key_here_optional\n")
        print(".env file created!")
    else:
        print(".env file already exists.")

def create_logs_directory():
    if not os.path.exists('logs'):
        os.makedirs('logs')
        print("Logs directory created!")

def run_demo():
    print("\nWould you like to run a demo? (y/n): ", end="")
    choice = input().strip().lower()
    
    if choice == 'y':
        print("Running demo without API keys...")
        try:
            subprocess.run([sys.executable, "demo_no_api.py"])
        except KeyboardInterrupt:
            print("\nDemo interrupted.")
        except Exception as e:
            print(f"Error running demo: {e}")

def main():
    print_banner()
    
    print("Setting up Syllabo...")
    print()
    
    # Install dependencies
    if not install_requirements():
        return
    
    # Create environment file
    create_env_file()
    
    # Create logs directory
    create_logs_directory()
    
    print("\nSetup completed successfully!")
    print()
    print("Quick Start:")
    print("1. Run demo: python demo_no_api.py")
    print("2. Simple CLI: python syllabo_cli.py")
    print("3. Test features: python test_new_cli.py")
    print("4. Enhanced CLI: python syllabo_enhanced.py --help")
    print()
    print("Note: The app works without any API keys using web scraping!")
    
    run_demo()

if __name__ == "__main__":
    main()