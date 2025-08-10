#!/usr/bin/env python3
"""
Helper script to create the first release of Syllabo
This script guides users through creating their first GitHub release
"""

import os
import sys
import subprocess
from pathlib import Path

def run_command(cmd, check=True):
    """Run command and return result"""
    try:
        result = subprocess.run(cmd, shell=True, check=check,
                              capture_output=True, text=True)
        return True, result.stdout.strip(), result.stderr.strip()
    except subprocess.CalledProcessError as e:
        return False, e.stdout, e.stderr

def check_git_setup():
    """Check if git is set up properly"""
    print("🔍 Checking Git setup...")
    
    # Check if we're in a git repo
    success, _, _ = run_command("git status", check=False)
    if not success:
        print("❌ Not a Git repository. Please run 'git init' first.")
        return False
    
    # Check if we have a remote
    success, output, _ = run_command("git remote -v", check=False)
    if not success or not output:
        print("❌ No Git remote found. Please add a GitHub remote:")
        print("   git remote add origin https://github.com/yourusername/syllabo.git")
        return False
    
    print("✅ Git setup looks good!")
    return True

def check_github_setup():
    """Check if GitHub is set up properly"""
    print("🔍 Checking GitHub setup...")
    
    # Check if we can access GitHub
    success, output, _ = run_command("git remote get-url origin", check=False)
    if not success:
        print("❌ Cannot get GitHub remote URL")
        return False
    
    if "github.com" not in output:
        print("❌ Remote is not a GitHub repository")
        return False
    
    print(f"✅ GitHub repository: {output}")
    return True

def check_files():
    """Check if required files exist"""
    print("🔍 Checking required files...")
    
    required_files = [
        "main.py",
        "requirements.txt", 
        "src/version.py",
        ".github/workflows/build-and-release.yml",
        ".github/workflows/pages.yml"
    ]
    
    missing_files = []
    for file_path in required_files:
        if not Path(file_path).exists():
            missing_files.append(file_path)
    
    if missing_files:
        print("❌ Missing required files:")
        for file_path in missing_files:
            print(f"   - {file_path}")
        return False
    
    print("✅ All required files present!")
    return True

def create_version_tag():
    """Create and push version tag"""
    print("🏷️ Creating version tag...")
    
    # Get current version
    try:
        with open("src/version.py", "r") as f:
            content = f.read()
            version = content.split('"')[1]  # Extract version from VERSION = "1.0.0"
    except:
        version = "1.0.0"
    
    tag_name = f"v{version}"
    print(f"Creating tag: {tag_name}")
    
    # Check if tag already exists
    success, _, _ = run_command(f"git tag -l {tag_name}", check=False)
    if success:
        print(f"⚠️ Tag {tag_name} already exists. Deleting and recreating...")
        run_command(f"git tag -d {tag_name}", check=False)
        run_command(f"git push origin --delete {tag_name}", check=False)
    
    # Create tag
    success, _, stderr = run_command(f'git tag -a {tag_name} -m "Release {tag_name}"')
    if not success:
        print(f"❌ Failed to create tag: {stderr}")
        return False
    
    # Push tag
    success, _, stderr = run_command(f"git push origin {tag_name}")
    if not success:
        print(f"❌ Failed to push tag: {stderr}")
        return False
    
    print(f"✅ Tag {tag_name} created and pushed!")
    return tag_name

def enable_github_pages():
    """Instructions for enabling GitHub Pages"""
    print("\n📄 GitHub Pages Setup")
    print("=" * 50)
    print("To enable GitHub Pages for your repository:")
    print("1. Go to your GitHub repository")
    print("2. Click 'Settings' tab")
    print("3. Scroll down to 'Pages' section")
    print("4. Under 'Source', select 'GitHub Actions'")
    print("5. Save the settings")
    print("\nYour site will be available at:")
    
    # Try to get repository URL
    success, output, _ = run_command("git remote get-url origin", check=False)
    if success and "github.com" in output:
        # Extract username and repo name
        parts = output.replace("https://github.com/", "").replace(".git", "").split("/")
        if len(parts) >= 2:
            username, repo = parts[0], parts[1]
            print(f"https://{username}.github.io/{repo}")

def main():
    """Main function"""
    print("🎓 Syllabo First Release Creator")
    print("=" * 40)
    print("This script will help you create your first GitHub release!")
    print()
    
    # Check prerequisites
    if not check_git_setup():
        return False
    
    if not check_github_setup():
        return False
    
    if not check_files():
        return False
    
    # Confirm with user
    print("\n🚀 Ready to create release!")
    response = input("Continue? (y/N): ")
    if response.lower() != 'y':
        print("Release cancelled.")
        return False
    
    # Commit any changes
    print("\n📝 Committing any pending changes...")
    run_command("git add .", check=False)
    success, _, _ = run_command('git commit -m "Prepare for first release"', check=False)
    if success:
        print("✅ Changes committed")
        run_command("git push origin main", check=False)
    else:
        print("ℹ️ No changes to commit")
    
    # Create and push tag
    tag_name = create_version_tag()
    if not tag_name:
        return False
    
    print(f"\n🎉 Release {tag_name} initiated!")
    print("=" * 40)
    print("GitHub Actions is now building your release...")
    print("This will take about 5-10 minutes.")
    print()
    print("You can monitor progress at:")
    
    # Get repository URL for actions
    success, output, _ = run_command("git remote get-url origin", check=False)
    if success:
        repo_url = output.replace(".git", "")
        print(f"{repo_url}/actions")
    
    print("\nOnce complete, you'll have:")
    print("✅ Standalone executables for Windows, Linux, and macOS")
    print("✅ GitHub release with download links")
    print("✅ GitHub Pages website (if enabled)")
    
    # GitHub Pages setup
    enable_github_pages()
    
    print(f"\n🎊 Congratulations! Your first release is on the way!")
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)