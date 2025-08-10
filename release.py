#!/usr/bin/env python3
"""
Release script for Syllabo
Handles version bumping, tagging, and release preparation
"""

import os
import sys
import subprocess
import json
import re
from pathlib import Path
from datetime import datetime

class ReleaseManager:
    def __init__(self):
        self.repo_root = Path.cwd()
        self.version_file = self.repo_root / "src" / "version.py"
        self.main_file = self.repo_root / "main.py"
        
    def get_current_version(self):
        """Get current version from version file or main.py"""
        # Try version.py first
        if self.version_file.exists():
            with open(self.version_file, 'r') as f:
                content = f.read()
                match = re.search(r'VERSION\s*=\s*["\']([^"\']+)["\']', content)
                if match:
                    return match.group(1)
        
        # Fallback to main.py
        if self.main_file.exists():
            with open(self.main_file, 'r') as f:
                content = f.read()
                # Look for version patterns
                patterns = [
                    r'version\s*=\s*["\']([^"\']+)["\']',
                    r'__version__\s*=\s*["\']([^"\']+)["\']',
                    r'VERSION\s*=\s*["\']([^"\']+)["\']'
                ]
                for pattern in patterns:
                    match = re.search(pattern, content, re.IGNORECASE)
                    if match:
                        return match.group(1)
        
        return "1.0.0"  # Default version
    
    def bump_version(self, current_version, bump_type="patch"):
        """Bump version number"""
        parts = current_version.lstrip('v').split('.')
        major, minor, patch = int(parts[0]), int(parts[1]), int(parts[2]) if len(parts) > 2 else 0
        
        if bump_type == "major":
            major += 1
            minor = 0
            patch = 0
        elif bump_type == "minor":
            minor += 1
            patch = 0
        else:  # patch
            patch += 1
        
        return f"{major}.{minor}.{patch}"
    
    def update_version_files(self, new_version):
        """Update version in all relevant files"""
        # Create/update version.py
        self.version_file.parent.mkdir(exist_ok=True)
        with open(self.version_file, 'w') as f:
            f.write(f'VERSION = "{new_version}"\n')
        
        # Update main.py if it has version info
        if self.main_file.exists():
            with open(self.main_file, 'r') as f:
                content = f.read()
            
            # Replace version patterns
            patterns = [
                (r'version\s*=\s*["\'][^"\']+["\']', f'version = "{new_version}"'),
                (r'__version__\s*=\s*["\'][^"\']+["\']', f'__version__ = "{new_version}"'),
                (r'VERSION\s*=\s*["\'][^"\']+["\']', f'VERSION = "{new_version}"')
            ]
            
            for pattern, replacement in patterns:
                content = re.sub(pattern, replacement, content, flags=re.IGNORECASE)
            
            with open(self.main_file, 'w') as f:
                f.write(content)
        
        print(f"✓ Updated version to {new_version}")
    
    def run_command(self, cmd, check=True):
        """Run command and return result"""
        try:
            result = subprocess.run(cmd, shell=True, check=check,
                                  capture_output=True, text=True)
            return True, result.stdout.strip(), result.stderr.strip()
        except subprocess.CalledProcessError as e:
            return False, e.stdout, e.stderr
    
    def git_operations(self, version):
        """Perform git operations for release"""
        print("Performing git operations...")
        
        # Check if git repo
        success, _, _ = self.run_command("git status", check=False)
        if not success:
            print("Warning: Not a git repository")
            return False
        
        # Check for uncommitted changes
        success, output, _ = self.run_command("git status --porcelain")
        if output:
            print("Committing changes...")
            self.run_command("git add .")
            self.run_command(f'git commit -m "Bump version to {version}"')
        
        # Create tag
        tag_name = f"v{version}"
        print(f"Creating tag: {tag_name}")
        success, _, stderr = self.run_command(f'git tag -a {tag_name} -m "Release {tag_name}"', check=False)
        
        if not success and "already exists" in stderr:
            print(f"Tag {tag_name} already exists")
            return False
        
        # Push changes and tags
        print("Pushing to remote...")
        self.run_command("git push origin main", check=False)
        self.run_command(f"git push origin {tag_name}", check=False)
        
        return True
    
    def create_changelog_entry(self, version):
        """Create changelog entry"""
        changelog_file = self.repo_root / "CHANGELOG.md"
        
        # Create changelog if it doesn't exist
        if not changelog_file.exists():
            with open(changelog_file, 'w') as f:
                f.write("# Changelog\n\n")
                f.write("All notable changes to this project will be documented in this file.\n\n")
        
        # Read existing changelog
        with open(changelog_file, 'r') as f:
            content = f.read()
        
        # Create new entry
        date = datetime.now().strftime("%Y-%m-%d")
        new_entry = f"""## [{version}] - {date}

### Added
- New features and improvements

### Changed
- Updates and modifications

### Fixed
- Bug fixes and patches

"""
        
        # Insert new entry after the header
        lines = content.split('\n')
        header_end = 0
        for i, line in enumerate(lines):
            if line.startswith('## [') or line.startswith('# '):
                if 'Changelog' not in line:
                    header_end = i
                    break
            elif line.strip() == '' and i > 3:
                header_end = i
                break
        
        if header_end == 0:
            # No existing entries, add after header
            for i, line in enumerate(lines):
                if line.strip() == '' and i > 2:
                    header_end = i + 1
                    break
        
        lines.insert(header_end, new_entry)
        
        with open(changelog_file, 'w') as f:
            f.write('\n'.join(lines))
        
        print(f"✓ Updated CHANGELOG.md")
    
    def prepare_release(self, bump_type="patch", dry_run=False):
        """Prepare a new release"""
        print("Syllabo Release Manager")
        print("======================")
        
        current_version = self.get_current_version()
        new_version = self.bump_version(current_version, bump_type)
        
        print(f"Current version: {current_version}")
        print(f"New version: {new_version}")
        
        if dry_run:
            print("DRY RUN - No changes will be made")
            return
        
        # Confirm release
        response = input(f"Create release {new_version}? (y/N): ")
        if response.lower() != 'y':
            print("Release cancelled")
            return
        
        # Update version files
        self.update_version_files(new_version)
        
        # Create changelog entry
        self.create_changelog_entry(new_version)
        
        # Git operations
        if self.git_operations(new_version):
            print(f"\n✓ Release {new_version} prepared successfully!")
            print("\nNext steps:")
            print("1. GitHub Actions will automatically build and create the release")
            print("2. Edit the release notes on GitHub if needed")
            print("3. Announce the release to users")
        else:
            print(f"\n⚠ Release {new_version} prepared locally")
            print("Git operations failed - you may need to push manually")
    
    def build_local(self):
        """Build locally for testing"""
        print("Building locally for testing...")
        
        success, _, stderr = self.run_command("python build-local.py", check=False)
        if success:
            print("✓ Local build completed")
        else:
            print(f"✗ Local build failed: {stderr}")

def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Syllabo Release Manager")
    parser.add_argument("--bump", choices=["major", "minor", "patch"], 
                       default="patch", help="Version bump type")
    parser.add_argument("--dry-run", action="store_true", 
                       help="Show what would be done without making changes")
    parser.add_argument("--build", action="store_true", 
                       help="Build locally for testing")
    
    args = parser.parse_args()
    
    manager = ReleaseManager()
    
    if args.build:
        manager.build_local()
    else:
        manager.prepare_release(args.bump, args.dry_run)

if __name__ == "__main__":
    main()