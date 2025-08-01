#!/usr/bin/env python3
"""
Demo script to showcase the enhanced UI/UX of main.py
"""

import subprocess
import sys
import os

def run_demo():
    """Run a demo of the enhanced UI features"""
    print("🚀 Syllabo Enhanced UI Demo")
    print("=" * 50)
    
    print("\n1. Interactive Mode (no arguments)")
    print("   Run: python main.py")
    print("   This will show the interactive menu with beautiful banner and stats")
    
    print("\n2. Enhanced Analysis with Progress")
    print("   Run: python main.py analyze --text 'Machine Learning basics' --search-videos --print-results")
    print("   Shows progress bars, checkmarks, and comprehensive summaries")
    
    print("\n3. Interactive Quiz Generation")
    print("   Run: python main.py quiz generate --topic 'Python Programming' --num-questions 5")
    print("   Features AI quiz generation with interactive options")
    
    print("\n4. Visual Progress Dashboard")
    print("   Run: python main.py progress")
    print("   Displays learning analytics with tables and progress indicators")
    
    print("\n5. Enhanced Study Sessions")
    print("   Run: python main.py session start --topic 'Data Science' --duration 25")
    print("   Pomodoro timer with visual progress and focus scoring")
    
    print("\n6. Smart Goals Management")
    print("   Run: python main.py goals list")
    print("   Beautiful tables showing goal progress and achievements")
    
    print("\n✨ Key UI/UX Improvements:")
    print("   • Beautiful ASCII banner with quick stats")
    print("   • Interactive menu system")
    print("   • Progress bars for long operations")
    print("   • Color-coded success/error messages with checkmarks")
    print("   • Contextual help and suggestions")
    print("   • Professional table formatting")
    print("   • Next steps recommendations")
    print("   • Visual progress indicators")
    
    print("\n🎯 Try it now:")
    choice = input("Run interactive demo? (y/n): ").lower().strip()
    
    if choice.startswith('y'):
        print("\nLaunching interactive mode...")
        try:
            subprocess.run([sys.executable, "main.py"], check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error running demo: {e}")
        except KeyboardInterrupt:
            print("\nDemo cancelled by user")
    else:
        print("Demo skipped. Run 'python main.py' anytime to see the enhanced UI!")

if __name__ == "__main__":
    run_demo()