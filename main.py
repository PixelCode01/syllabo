#!/usr/bin/env python3

import os
import sys
import argparse
from dotenv import load_dotenv
from src.app import SyllaboApp

def main():
    load_dotenv()
    
    parser = argparse.ArgumentParser(description='Syllabo - YouTube Video Finder for Course Topics')
    parser.add_argument('--file', '-f', help='Load syllabus from file')
    parser.add_argument('--text', '-t', help='Syllabus text directly')
    args = parser.parse_args()
    
    if not os.getenv('YOUTUBE_API_KEY'):
        print("Error: YOUTUBE_API_KEY not found in environment")
        print("Please add your YouTube API key to .env file")
        sys.exit(1)
    
    app = SyllaboApp()
    
    if args.file or args.text:
        app.cli_mode = True
        app.cli_input = args.file or args.text
        app.is_file = bool(args.file)
    
    app.run()

if __name__ == "__main__":
    main()