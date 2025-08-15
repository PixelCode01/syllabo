#!/usr/bin/env python3
"""
Check if all required methods exist in SyllaboMain
"""

import sys
import os

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from main import SyllaboMain

def check_methods():
    app = SyllaboMain()
    
    # List of methods that should exist based on the code
    required_methods = [
        '_find_youtube_resources_for_topics',
        '_combine_all_resources',
        '_display_resource_summary',
        '_comprehensive_analysis_workflow',
        '_create_resource_based_quiz',
        '_interactive_enhanced_resources',
        '_interactive_saved_resources',
        '_interactive_saved_quizzes',
        '_show_sample_direct_links',
        '_select_and_take_quiz',
        '_take_persistent_quiz',
        '_show_quiz_statistics',
        '_delete_quiz'
    ]
    
    print("Checking if all required methods exist...")
    print("=" * 50)
    
    missing_methods = []
    existing_methods = []
    
    for method_name in required_methods:
        if hasattr(app, method_name):
            existing_methods.append(method_name)
            print(f"✅ {method_name}")
        else:
            missing_methods.append(method_name)
            print(f"❌ {method_name}")
    
    print("=" * 50)
    print(f"Total methods checked: {len(required_methods)}")
    print(f"Existing methods: {len(existing_methods)}")
    print(f"Missing methods: {len(missing_methods)}")
    
    if missing_methods:
        print(f"\n❌ Missing methods:")
        for method in missing_methods:
            print(f"   - {method}")
        return False
    else:
        print(f"\n✅ All methods exist!")
        return True

if __name__ == "__main__":
    success = check_methods()
    sys.exit(0 if success else 1)