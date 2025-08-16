#!/usr/bin/env python3
"""
Quick Demo Launcher for Syllabo
Standalone script to quickly run the features demo
"""

import sys
import os
import asyncio

# Add the current directory to the path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def main():
    """Quick launcher for the demo"""
    try:
        from demo_all_features import ComprehensiveFeaturesDemo
        
        print("🚀 Starting Syllabo Complete Features Demo...")
        print("=" * 50)
        print("📚 This will showcase ALL features with sample data")
        print("⏱️  Estimated time: 10-15 minutes")
        print("🎯 Perfect for testing and evaluation")
        print("=" * 50)
        
        demo = ComprehensiveFeaturesDemo()
        return asyncio.run(demo.run_demo())
        
    except ImportError as e:
        print(f"❌ Error: Could not import demo module: {e}")
        print("Please ensure demo_all_features.py is in the same directory.")
        return 1
    except KeyboardInterrupt:
        print("\n🛑 Demo interrupted by user")
        return 0
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
