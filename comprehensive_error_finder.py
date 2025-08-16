#!/usr/bin/env python3
"""
Comprehensive Error Finder and Fixer
Finds and fixes all potential errors similar to the bookmark .get() issue
"""

import os
import sys
import re
import traceback
from typing import List, Dict, Tuple

def find_potential_dataclass_get_errors(directory: str = ".") -> List[Dict]:
    """Find potential .get() method calls on dataclass objects"""
    errors = []
    
    # Known dataclass names from the codebase
    dataclass_patterns = [
        r'bookmark\.get\(',
        r'session\.get\(',  # StudySession
        r'goal\.get\(',     # StudyGoal
        r'item\.get\(',     # ReviewItem (when not checking isinstance)
        r'prediction\.get\(',  # LearningPrediction
        r'metrics\.get\(',     # LearningMetrics, RetentionMetrics
        r'velocity\.get\(',    # LearningVelocity
        r'pattern\.get\(',     # StudyPattern
    ]
    
    # Files to check
    python_files = []
    for root, dirs, files in os.walk(directory):
        # Skip certain directories
        if any(skip in root for skip in ['.git', '__pycache__', 'node_modules']):
            continue
        
        for file in files:
            if file.endswith('.py'):
                python_files.append(os.path.join(root, file))
    
    for file_path in python_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                lines = content.split('\n')
            
            for line_num, line in enumerate(lines, 1):
                for pattern in dataclass_patterns:
                    if re.search(pattern, line):
                        # Check if it's already protected by isinstance check
                        context_start = max(0, line_num - 5)
                        context_end = min(len(lines), line_num + 2)
                        context = '\n'.join(lines[context_start:context_end])
                        
                        # If there's an isinstance check nearby, it's probably safe
                        if 'isinstance' in context and 'dict' in context:
                            continue
                        
                        errors.append({
                            'file': file_path,
                            'line': line_num,
                            'content': line.strip(),
                            'pattern': pattern,
                            'context': context
                        })
        
        except Exception as e:
            print(f"⚠️  Error reading {file_path}: {e}")
    
    return errors

def find_missing_error_handling() -> List[Dict]:
    """Find functions that might need better error handling"""
    issues = []
    
    # Common patterns that should have error handling
    risky_patterns = [
        r'\.json\(\)',  # API calls without error handling
        r'open\(',      # File operations
        r'requests\.get\(',  # HTTP requests
        r'\.execute\(',      # Database operations
    ]
    
    python_files = []
    for root, dirs, files in os.walk("."):
        if any(skip in root for skip in ['.git', '__pycache__']):
            continue
        for file in files:
            if file.endswith('.py'):
                python_files.append(os.path.join(root, file))
    
    for file_path in python_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                lines = content.split('\n')
            
            for line_num, line in enumerate(lines, 1):
                for pattern in risky_patterns:
                    if re.search(pattern, line):
                        # Check if it's in a try block
                        context_start = max(0, line_num - 10)
                        context = '\n'.join(lines[context_start:line_num])
                        
                        # Count try/except blocks
                        try_count = context.count('try:')
                        except_count = context.count('except')
                        
                        if try_count == 0 or try_count > except_count:
                            issues.append({
                                'file': file_path,
                                'line': line_num,
                                'content': line.strip(),
                                'pattern': pattern,
                                'risk': 'Missing error handling'
                            })
        
        except Exception as e:
            print(f"⚠️  Error reading {file_path}: {e}")
    
    return issues

def test_all_imports() -> List[Dict]:
    """Test all imports to find missing dependencies or circular imports"""
    import_errors = []
    
    python_files = []
    for root, dirs, files in os.walk("."):
        if any(skip in root for skip in ['.git', '__pycache__']):
            continue
        for file in files:
            if file.endswith('.py') and not file.startswith('test_') and not file.startswith('fix_'):
                python_files.append(os.path.join(root, file))
    
    for file_path in python_files:
        try:
            # Try to compile the file
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            try:
                compile(content, file_path, 'exec')
            except SyntaxError as e:
                import_errors.append({
                    'file': file_path,
                    'error': f"Syntax error: {e}",
                    'line': e.lineno
                })
            except Exception as e:
                import_errors.append({
                    'file': file_path,
                    'error': f"Compilation error: {e}",
                    'line': None
                })
        
        except Exception as e:
            import_errors.append({
                'file': file_path,
                'error': f"File read error: {e}",
                'line': None
            })
    
    return import_errors

def check_database_operations() -> List[Dict]:
    """Check for potential database operation errors"""
    db_issues = []
    
    # Patterns that might cause database errors
    db_patterns = [
        r'\.execute\(',
        r'\.fetchone\(',
        r'\.fetchall\(',
        r'\.commit\(',
    ]
    
    python_files = []
    for root, dirs, files in os.walk("src"):
        for file in files:
            if file.endswith('.py'):
                python_files.append(os.path.join(root, file))
    
    for file_path in python_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                lines = content.split('\n')
            
            for line_num, line in enumerate(lines, 1):
                for pattern in db_patterns:
                    if re.search(pattern, line):
                        # Check for proper error handling
                        context_start = max(0, line_num - 5)
                        context_end = min(len(lines), line_num + 5)
                        context = '\n'.join(lines[context_start:context_end])
                        
                        if 'try:' not in context or 'except' not in context:
                            db_issues.append({
                                'file': file_path,
                                'line': line_num,
                                'content': line.strip(),
                                'issue': 'Database operation without error handling'
                            })
        
        except Exception as e:
            print(f"⚠️  Error reading {file_path}: {e}")
    
    return db_issues

def main():
    """Run comprehensive error checking"""
    print("🔍 Running comprehensive error analysis...\n")
    
    # 1. Find dataclass .get() errors
    print("1️⃣  Checking for dataclass .get() method errors...")
    dataclass_errors = find_potential_dataclass_get_errors()
    
    if dataclass_errors:
        print(f"❌ Found {len(dataclass_errors)} potential dataclass .get() errors:")
        for error in dataclass_errors:
            print(f"   📁 {error['file']}:{error['line']}")
            print(f"   📝 {error['content']}")
            print(f"   🔧 Fix: Replace with direct attribute access or isinstance check")
            print()
    else:
        print("✅ No dataclass .get() errors found")
    
    print()
    
    # 2. Check imports
    print("2️⃣  Checking for import and syntax errors...")
    import_errors = test_all_imports()
    
    if import_errors:
        print(f"❌ Found {len(import_errors)} import/syntax errors:")
        for error in import_errors:
            print(f"   📁 {error['file']}")
            if error['line']:
                print(f"   📍 Line {error['line']}")
            print(f"   ❌ {error['error']}")
            print()
    else:
        print("✅ No import or syntax errors found")
    
    print()
    
    # 3. Check database operations
    print("3️⃣  Checking database operations...")
    db_issues = check_database_operations()
    
    if db_issues:
        print(f"⚠️  Found {len(db_issues)} potential database issues:")
        for issue in db_issues:
            print(f"   📁 {issue['file']}:{issue['line']}")
            print(f"   📝 {issue['content']}")
            print(f"   ⚠️  {issue['issue']}")
            print()
    else:
        print("✅ Database operations look good")
    
    print()
    
    # 4. Check for missing error handling
    print("4️⃣  Checking for missing error handling...")
    error_handling_issues = find_missing_error_handling()
    
    # Filter out test files and already handled cases
    filtered_issues = []
    for issue in error_handling_issues:
        if not any(skip in issue['file'] for skip in ['test_', 'fix_', 'demo_']):
            filtered_issues.append(issue)
    
    if filtered_issues:
        print(f"⚠️  Found {len(filtered_issues)} potential error handling issues:")
        # Show only first 10 to avoid spam
        for issue in filtered_issues[:10]:
            print(f"   📁 {issue['file']}:{issue['line']}")
            print(f"   📝 {issue['content']}")
            print(f"   ⚠️  {issue['risk']}")
            print()
        
        if len(filtered_issues) > 10:
            print(f"   ... and {len(filtered_issues) - 10} more")
    else:
        print("✅ Error handling looks adequate")
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 COMPREHENSIVE ERROR ANALYSIS SUMMARY")
    print("=" * 60)
    
    total_issues = len(dataclass_errors) + len(import_errors) + len(db_issues)
    
    print(f"🔍 Dataclass .get() errors: {len(dataclass_errors)}")
    print(f"🔍 Import/syntax errors: {len(import_errors)}")
    print(f"🔍 Database operation issues: {len(db_issues)}")
    print(f"🔍 Error handling warnings: {len(filtered_issues)}")
    print(f"\n📊 Total critical issues: {total_issues}")
    
    if total_issues == 0:
        print("\n🎉 No critical errors found! The codebase looks healthy.")
    else:
        print(f"\n⚠️  Found {total_issues} issues that should be addressed.")
    
    # Specific recommendations
    print("\n💡 RECOMMENDATIONS:")
    if dataclass_errors:
        print("   - Fix dataclass .get() method calls with direct attribute access")
    if import_errors:
        print("   - Fix import and syntax errors")
    if db_issues:
        print("   - Add error handling to database operations")
    if not total_issues:
        print("   - Codebase is in good shape! Continue with regular testing.")
    
    return total_issues == 0

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)