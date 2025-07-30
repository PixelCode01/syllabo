#!/usr/bin/env python3

import os
import sys
from dotenv import load_dotenv
from src.app import SyllaboApp

def main():
    load_dotenv()
    
    if not os.getenv('YOUTUBE_API_KEY'):
        print("Error: YOUTUBE_API_KEY not found in environment")
        print("Please add your YouTube API key to .env file")
        sys.exit(1)
    
    app = SyllaboApp()
    app.run()

if __name__ == "__main__":
    main()