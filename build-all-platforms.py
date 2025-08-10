#!/usr/bin/env python3
"""
Cross-platform build script for Syllabo
Creates executables and installers for Windows, Linux, and macOS
"""

import os
import sys
import subprocess
import platform
import shutil
import zipfile
import tarfile
from pathlib import Path
import json

class PlatformBuilder:
    def __init__(self):
        self.current_platform = platform.system()
        self.current_arch = platform.machine()
        self.version = self.get_version()
        self.build_dir = Path("build")
        self.dist_dir = Path("dist")
        self.release_dir = Path("release")
        
    def get_version(self):
        """Get version from main.py or default"""
        try:
            with open("main.py", "r") as f:
                content = f.read()
                # Look for version string
                for line in content.split('\n'):
                    if 'version' in line.lower() and '=' in line:
                        version = line.split('=')[1].strip().strip('"\'')
                        if version:
                            return version
        except:
            pass
        return "1.0.0"
    
    def run_command(self, cmd, cwd=None, check=True):
        """Run command with error handling"""
        try:
            result = subprocess.run(cmd, shell=True, cwd=cwd, check=check,
                                  capture_output=True, text=True)
            return True, result.stdout, result.stderr
        except subprocess.CalledProcessError as e:
            return False, e.stdout, e.stderr
    
    def clean_build_dirs(self):
        """Clean build directories"""
        for dir_path in [self.build_dir, self.dist_dir, self.release_dir]:
            if dir_path.exists():
                shutil.rmtree(dir_path)
            dir_path.mkdir(parents=True, exist_ok=True)
    
    def install_dependencies(self):
        """Install build dependencies for standalone executable creation"""
        print("Installing build dependencies for standalone executables...")
        
        # Essential build tools
        build_deps = [
            "pyinstaller>=5.13.0",  # Latest version for better standalone support
            "setuptools>=65.0",
            "wheel>=0.38.0",
            "pip>=22.0"
        ]
        
        for dep in build_deps:
            success, stdout, stderr = self.run_command(f"pip install --upgrade {dep}")
            if not success:
                print(f"Warning: Failed to install {dep}")
        
        # Install all app dependencies with specific versions for stability
        print("Installing application dependencies...")
        app_deps = [
            "textual==0.47.1",
            "rich==13.7.0",
            "youtube-transcript-api==0.6.1", 
            "requests==2.31.0",
            "PyPDF2==3.0.1",
            "python-dotenv==1.0.0",
            "beautifulsoup4==4.12.2",
            "feedparser==6.0.10",
            "google-api-python-client==2.108.0",
            "google-generativeai==0.3.2",
            
            # Additional dependencies for standalone builds
            "certifi",              # SSL certificates
            "charset-normalizer",   # Character encoding
            "idna",                # Internationalized domain names
            "urllib3",             # HTTP library
            "six",                 # Python 2/3 compatibility
            "packaging",           # Package version handling
            "pyparsing",           # Parsing library
        ]
        
        # Try to install lxml separately (often problematic)
        print("Installing lxml...")
        success, stdout, stderr = self.run_command("pip install --only-binary=lxml lxml==4.9.3", check=False)
        if not success:
            print("Warning: lxml installation failed. Some features may not work.")
            print("Continuing without lxml...")
        
        # Install other dependencies
        failed_deps = []
        for dep in app_deps:
            success, stdout, stderr = self.run_command(f"pip install {dep}", check=False)
            if not success:
                print(f"Warning: Failed to install {dep}")
                failed_deps.append(dep)
        
        if failed_deps:
            print(f"Failed to install {len(failed_deps)} dependencies:")
            for dep in failed_deps:
                print(f"  - {dep}")
            print("Build may still succeed with reduced functionality.")
        
        return True
    
    def build_executable(self, target_platform=None):
        """Build standalone executable for current or target platform"""
        platform_name = target_platform or self.current_platform
        
        print(f"Building standalone executable for {platform_name}...")
        
        # Platform-specific settings
        if platform_name == "Windows":
            exe_name = "syllabo.exe"
            data_sep = ";"
            icon_flag = "--icon=assets/icon.ico" if Path("assets/icon.ico").exists() else ""
        else:
            exe_name = "syllabo"
            data_sep = ":"
            icon_flag = "--icon=assets/icon.icns" if Path("assets/icon.icns").exists() else ""
        
        # Build command for completely standalone executable
        cmd_parts = [
            "pyinstaller",
            "--onefile",                    # Single executable file
            "--windowed" if platform_name == "Windows" else "--console",  # No console window on Windows GUI
            f"--name={exe_name}",
            f"--add-data=src{data_sep}src",
            
            # Include all Python modules we need
            "--hidden-import=src.database",
            "--hidden-import=src.logger",
            "--hidden-import=src.ai_client",
            "--hidden-import=src.syllabus_parser",
            "--hidden-import=src.quiz_generator",
            "--hidden-import=src.progress_dashboard",
            "--hidden-import=src.goals_manager",
            "--hidden-import=src.platform_integrator",
            "--hidden-import=src.bookmark_manager",
            "--hidden-import=src.study_session_manager",
            "--hidden-import=src.spaced_repetition",
            "--hidden-import=src.notes_generator",
            "--hidden-import=src.video_analyzer",
            "--hidden-import=src.resource_finder",
            "--hidden-import=src.youtube_client",
            
            # Include all required third-party modules
            "--hidden-import=textual",
            "--hidden-import=rich",
            "--hidden-import=requests",
            "--hidden-import=PyPDF2",
            "--hidden-import=beautifulsoup4",
            "--hidden-import=feedparser",
            "--hidden-import=google.generativeai",
            "--hidden-import=google.api_core",
            "--hidden-import=googleapiclient",
            "--hidden-import=youtube_transcript_api",
            "--hidden-import=dotenv",
            "--hidden-import=sqlite3",
            "--hidden-import=json",
            "--hidden-import=os",
            "--hidden-import=sys",
            "--hidden-import=asyncio",
            "--hidden-import=typing",
            "--hidden-import=pathlib",
            "--hidden-import=datetime",
            "--hidden-import=time",
            "--hidden-import=re",
            "--hidden-import=urllib",
            "--hidden-import=http",
            "--hidden-import=ssl",
            "--hidden-import=socket",
            "--hidden-import=threading",
            "--hidden-import=multiprocessing",
            
            # Collect all submodules
            "--collect-all=textual",
            "--collect-all=rich",
            "--collect-all=requests",
            "--collect-all=google",
            "--collect-all=googleapiclient",
            "--collect-all=youtube_transcript_api",
            
            # Ensure no external dependencies
            "--noconfirm",
            "--clean",
            "--strip",                      # Strip debug symbols (smaller size)
            "--noupx",                      # Don't use UPX compression (better compatibility)
            
            # Runtime options for standalone execution
            "--runtime-tmpdir",             # Use temp directory for runtime files
        ]
        
        if icon_flag:
            cmd_parts.append(icon_flag)
            
        cmd_parts.append("main.py")
        
        # Try building with spec file first (more reliable)
        spec_file = Path("syllabo.spec")
        if spec_file.exists():
            print("Using PyInstaller spec file for better standalone build...")
            cmd = f"pyinstaller --clean --noconfirm syllabo.spec"
            success, stdout, stderr = self.run_command(cmd)
        else:
            # Fallback to command line build
            cmd = " ".join(cmd_parts)
            success, stdout, stderr = self.run_command(cmd)
        
        if success:
            print(f"✓ Standalone executable built: dist/{exe_name}")
            
            # Verify the executable is truly standalone
            self._verify_standalone_executable(f"dist/{exe_name}")
            return True
        else:
            print(f"✗ Build failed: {stderr}")
            print("Trying fallback build method...")
            
            # Try simpler build as fallback
            simple_cmd = f"pyinstaller --onefile --name {exe_name} --add-data src{data_sep}src --console --clean main.py"
            success, stdout, stderr = self.run_command(simple_cmd)
            
            if success:
                print(f"✓ Fallback build successful: dist/{exe_name}")
                return True
            else:
                print(f"✗ All build methods failed: {stderr}")
                return False
    
    def _verify_standalone_executable(self, exe_path):
        """Verify that the executable is truly standalone"""
        print("Verifying standalone executable...")
        
        # Test basic execution
        success, stdout, stderr = self.run_command(f'"{exe_path}" --help', check=False)
        if success:
            print("✓ Executable runs without external dependencies")
        else:
            print(f"⚠ Executable test failed: {stderr}")
        
        # Check file size (should be substantial for standalone)
        try:
            size_mb = Path(exe_path).stat().st_size / (1024 * 1024)
            print(f"✓ Executable size: {size_mb:.1f} MB")
            if size_mb < 10:
                print("⚠ Executable seems small - may be missing dependencies")
        except:
            print("⚠ Could not check executable size")
    
    def create_installer_scripts(self):
        """Create platform-specific installer scripts"""
        print("Creating installer scripts...")
        
        # Windows installer
        windows_installer = f'''@echo off
echo Installing Syllabo v{self.version}...
echo.

REM Check for admin rights
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo This installer requires administrator privileges.
    echo Please run as administrator.
    pause
    exit /b 1
)

REM Create installation directory
set INSTALL_DIR=%ProgramFiles%\\Syllabo
if not exist "%INSTALL_DIR%" mkdir "%INSTALL_DIR%"

REM Copy files
echo Copying files...
copy "syllabo.exe" "%INSTALL_DIR%\\"
copy ".env.example" "%INSTALL_DIR%\\"
copy "README.txt" "%INSTALL_DIR%\\"

REM Create desktop shortcut
echo Creating desktop shortcut...
powershell "$WshShell = New-Object -comObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%USERPROFILE%\\Desktop\\Syllabo.lnk'); $Shortcut.TargetPath = '%INSTALL_DIR%\\syllabo.exe'; $Shortcut.Arguments = 'interactive'; $Shortcut.Save()"

REM Add to PATH
echo Adding to system PATH...
for /f "tokens=2*" %%A in ('reg query "HKLM\\SYSTEM\\CurrentControlSet\\Control\\Session Manager\\Environment" /v PATH 2^>nul') do set "CURRENT_PATH=%%B"
echo %CURRENT_PATH% | find /i "%INSTALL_DIR%" >nul
if errorlevel 1 (
    reg add "HKLM\\SYSTEM\\CurrentControlSet\\Control\\Session Manager\\Environment" /v PATH /t REG_EXPAND_SZ /d "%CURRENT_PATH%;%INSTALL_DIR%" /f
)

REM Create start menu entry
set START_MENU=%ProgramData%\\Microsoft\\Windows\\Start Menu\\Programs
if not exist "%START_MENU%\\Syllabo" mkdir "%START_MENU%\\Syllabo"
powershell "$WshShell = New-Object -comObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%START_MENU%\\Syllabo\\Syllabo.lnk'); $Shortcut.TargetPath = '%INSTALL_DIR%\\syllabo.exe'; $Shortcut.Arguments = 'interactive'; $Shortcut.Save()"

echo.
echo ✓ Syllabo v{self.version} installed successfully!
echo.
echo Installation location: %INSTALL_DIR%
echo Desktop shortcut created
echo Start menu entry created
echo.
echo To get started:
echo   1. Double-click the desktop shortcut, or
echo   2. Open Command Prompt and run: syllabo interactive
echo.
echo Optional: Configure API keys in %INSTALL_DIR%\\.env
echo.
pause
'''
        
        # Linux installer
        linux_installer = f'''#!/bin/bash
set -e

echo "Installing Syllabo v{self.version}..."
echo

# Check if running as root for system-wide install
if [[ $EUID -eq 0 ]]; then
    INSTALL_DIR="/usr/local/bin"
    CONFIG_DIR="/etc/syllabo"
    DESKTOP_DIR="/usr/share/applications"
    echo "Installing system-wide..."
else
    INSTALL_DIR="$HOME/.local/bin"
    CONFIG_DIR="$HOME/.config/syllabo"
    DESKTOP_DIR="$HOME/.local/share/applications"
    echo "Installing for current user..."
fi

# Create directories
mkdir -p "$INSTALL_DIR"
mkdir -p "$CONFIG_DIR"
mkdir -p "$DESKTOP_DIR"

# Copy files
echo "Copying files..."
cp syllabo "$INSTALL_DIR/"
cp .env.example "$CONFIG_DIR/"
cp README.txt "$CONFIG_DIR/"
chmod +x "$INSTALL_DIR/syllabo"

# Create desktop entry
echo "Creating desktop entry..."
cat > "$DESKTOP_DIR/syllabo.desktop" << EOF
[Desktop Entry]
Name=Syllabo
Comment=AI-Powered Learning Assistant
Exec=$INSTALL_DIR/syllabo interactive
Icon=applications-education
Terminal=true
Type=Application
Categories=Education;
EOF

# Update desktop database
if command -v update-desktop-database >/dev/null 2>&1; then
    update-desktop-database "$DESKTOP_DIR" 2>/dev/null || true
fi

# Add to PATH if needed
if [[ ":$PATH:" != *":$INSTALL_DIR:"* ]]; then
    echo "Adding to PATH..."
    if [[ $EUID -eq 0 ]]; then
        echo "export PATH=\\$PATH:$INSTALL_DIR" >> /etc/profile
    else
        echo "export PATH=\\$PATH:$INSTALL_DIR" >> "$HOME/.bashrc"
        echo "export PATH=\\$PATH:$INSTALL_DIR" >> "$HOME/.zshrc" 2>/dev/null || true
    fi
fi

echo
echo "✓ Syllabo v{self.version} installed successfully!"
echo
echo "Installation location: $INSTALL_DIR"
echo "Configuration: $CONFIG_DIR"
echo
echo "To get started:"
echo "  1. Restart your terminal or run: source ~/.bashrc"
echo "  2. Run: syllabo interactive"
echo
echo "Optional: Configure API keys in $CONFIG_DIR/.env"
echo
'''
        
        # macOS installer
        macos_installer = f'''#!/bin/bash
set -e

echo "Installing Syllabo v{self.version} for macOS..."
echo

# Installation directories
INSTALL_DIR="/usr/local/bin"
CONFIG_DIR="$HOME/.config/syllabo"
APP_DIR="/Applications"

# Check for Homebrew directory preference
if [[ -d "/opt/homebrew/bin" ]]; then
    INSTALL_DIR="/opt/homebrew/bin"
elif [[ -d "$HOME/.local/bin" ]]; then
    INSTALL_DIR="$HOME/.local/bin"
fi

echo "Installing to: $INSTALL_DIR"

# Create directories
mkdir -p "$INSTALL_DIR"
mkdir -p "$CONFIG_DIR"

# Copy files
echo "Copying files..."
cp syllabo "$INSTALL_DIR/"
cp .env.example "$CONFIG_DIR/"
cp README.txt "$CONFIG_DIR/"
chmod +x "$INSTALL_DIR/syllabo"

# Create app bundle (optional)
if [[ -w "$APP_DIR" ]]; then
    echo "Creating app bundle..."
    APP_BUNDLE="$APP_DIR/Syllabo.app"
    mkdir -p "$APP_BUNDLE/Contents/MacOS"
    mkdir -p "$APP_BUNDLE/Contents/Resources"
    
    # Create Info.plist
    cat > "$APP_BUNDLE/Contents/Info.plist" << EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>CFBundleExecutable</key>
    <string>Syllabo</string>
    <key>CFBundleIdentifier</key>
    <string>com.syllabo.app</string>
    <key>CFBundleName</key>
    <string>Syllabo</string>
    <key>CFBundleVersion</key>
    <string>{self.version}</string>
    <key>CFBundleShortVersionString</key>
    <string>{self.version}</string>
</dict>
</plist>
EOF
    
    # Create launcher script
    cat > "$APP_BUNDLE/Contents/MacOS/Syllabo" << EOF
#!/bin/bash
cd "\$HOME"
exec "$INSTALL_DIR/syllabo" interactive
EOF
    chmod +x "$APP_BUNDLE/Contents/MacOS/Syllabo"
fi

# Add to PATH
echo "Updating PATH..."
for profile in "$HOME/.bash_profile" "$HOME/.zshrc" "$HOME/.profile"; do
    if [[ -f "$profile" ]]; then
        if ! grep -q "$INSTALL_DIR" "$profile"; then
            echo "export PATH=\\$PATH:$INSTALL_DIR" >> "$profile"
        fi
    fi
done

echo
echo "✓ Syllabo v{self.version} installed successfully!"
echo
echo "Installation location: $INSTALL_DIR"
echo "Configuration: $CONFIG_DIR"
if [[ -d "$APP_BUNDLE" ]]; then
    echo "App bundle: $APP_BUNDLE"
fi
echo
echo "To get started:"
echo "  1. Restart your terminal or run: source ~/.zshrc"
echo "  2. Run: syllabo interactive"
echo "  3. Or launch from Applications folder (if app bundle created)"
echo
echo "Optional: Configure API keys in $CONFIG_DIR/.env"
echo
'''
        
        # Write installer scripts
        with open("install-windows.bat", "w") as f:
            f.write(windows_installer)
        
        with open("install-linux.sh", "w") as f:
            f.write(linux_installer)
        os.chmod("install-linux.sh", 0o755)
        
        with open("install-macos.sh", "w") as f:
            f.write(macos_installer)
        os.chmod("install-macos.sh", 0o755)
        
        print("✓ Installer scripts created")
        return True
    
    def create_uninstaller_scripts(self):
        """Create uninstaller scripts"""
        print("Creating uninstaller scripts...")
        
        # Windows uninstaller
        windows_uninstaller = f'''@echo off
echo Uninstalling Syllabo v{self.version}...
echo.

REM Check for admin rights
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo This uninstaller requires administrator privileges.
    echo Please run as administrator.
    pause
    exit /b 1
)

set INSTALL_DIR=%ProgramFiles%\\Syllabo

REM Remove from PATH
echo Removing from system PATH...
for /f "tokens=2*" %%A in ('reg query "HKLM\\SYSTEM\\CurrentControlSet\\Control\\Session Manager\\Environment" /v PATH 2^>nul') do set "CURRENT_PATH=%%B"
set "NEW_PATH=%CURRENT_PATH:;%INSTALL_DIR%=%"
reg add "HKLM\\SYSTEM\\CurrentControlSet\\Control\\Session Manager\\Environment" /v PATH /t REG_EXPAND_SZ /d "%NEW_PATH%" /f

REM Remove shortcuts
echo Removing shortcuts...
del "%USERPROFILE%\\Desktop\\Syllabo.lnk" 2>nul
rmdir /s /q "%ProgramData%\\Microsoft\\Windows\\Start Menu\\Programs\\Syllabo" 2>nul

REM Remove installation directory
echo Removing installation files...
rmdir /s /q "%INSTALL_DIR%" 2>nul

echo.
echo ✓ Syllabo uninstalled successfully!
echo.
pause
'''
        
        # Unix uninstaller
        unix_uninstaller = f'''#!/bin/bash
echo "Uninstalling Syllabo v{self.version}..."
echo

# Determine installation type
if [[ -f "/usr/local/bin/syllabo" ]]; then
    INSTALL_DIR="/usr/local/bin"
    CONFIG_DIR="/etc/syllabo"
    DESKTOP_DIR="/usr/share/applications"
    SYSTEM_WIDE=true
elif [[ -f "/opt/homebrew/bin/syllabo" ]]; then
    INSTALL_DIR="/opt/homebrew/bin"
    CONFIG_DIR="$HOME/.config/syllabo"
    DESKTOP_DIR="$HOME/.local/share/applications"
    SYSTEM_WIDE=false
else
    INSTALL_DIR="$HOME/.local/bin"
    CONFIG_DIR="$HOME/.config/syllabo"
    DESKTOP_DIR="$HOME/.local/share/applications"
    SYSTEM_WIDE=false
fi

# Remove files
echo "Removing files..."
rm -f "$INSTALL_DIR/syllabo"
rm -f "$DESKTOP_DIR/syllabo.desktop"
rm -rf "$CONFIG_DIR"

# Remove app bundle (macOS)
if [[ "$OSTYPE" == "darwin"* ]]; then
    rm -rf "/Applications/Syllabo.app"
fi

# Update desktop database
if command -v update-desktop-database >/dev/null 2>&1; then
    update-desktop-database "$DESKTOP_DIR" 2>/dev/null || true
fi

echo
echo "✓ Syllabo uninstalled successfully!"
echo "Note: You may need to restart your terminal for PATH changes to take effect."
echo
'''
        
        with open("uninstall-windows.bat", "w") as f:
            f.write(windows_uninstaller)
        
        with open("uninstall-unix.sh", "w") as f:
            f.write(unix_uninstaller)
        os.chmod("uninstall-unix.sh", 0o755)
        
        print("✓ Uninstaller scripts created")
        return True
    
    def create_readme(self, platform_name):
        """Create README for the package"""
        readme_content = f"""# Syllabo v{self.version} - {platform_name} Package

## Quick Start

### Automatic Installation (Recommended)
"""
        
        if platform_name == "Windows":
            readme_content += """
1. Right-click on `install-windows.bat`
2. Select "Run as administrator"
3. Follow the installation prompts
4. Open Command Prompt and run: `syllabo interactive`
"""
        else:
            installer_name = "install-linux.sh" if platform_name == "Linux" else "install-macos.sh"
            readme_content += f"""
1. Open terminal in this directory
2. Run: `chmod +x {installer_name}`
3. Run: `./{installer_name}`
4. Restart your terminal
5. Run: `syllabo interactive`
"""
        
        readme_content += f"""
### Manual Installation

1. Copy the executable to a directory in your PATH
2. Copy `.env.example` to your preferred config location
3. Make executable (Linux/macOS): `chmod +x syllabo`
4. Run: `syllabo interactive`

## Usage

```bash
# Interactive mode (recommended for beginners)
syllabo interactive

# Analyze a syllabus
syllabo analyze --file syllabus.pdf

# Generate quiz
syllabo quiz --topic "Machine Learning" --num-questions 5

# View progress
syllabo progress

# Get help
syllabo --help
```

## Configuration (Optional)

For enhanced features, configure API keys:

1. Copy `.env.example` to `.env`
2. Edit `.env` and add your API keys:
   ```
   GOOGLE_API_KEY=your_youtube_api_key_here
   GEMINI_API_KEY=your_gemini_api_key_here
   ```

## Features

- 📚 Syllabus analysis and topic extraction
- 🧠 AI-powered quiz generation
- 📊 Progress tracking and analytics
- 🎯 Study goals and milestones
- 🔄 Spaced repetition system
- 🎥 Video analysis and bookmarking
- 🔍 Multi-platform resource search
- ⏱️ Pomodoro study sessions

## Support

- Documentation: https://github.com/PixelCode01/syllabo
- Issues: https://github.com/PixelCode01/syllabo/issues
- Discussions: https://github.com/PixelCode01/syllabo/discussions

## Uninstallation

"""
        
        if platform_name == "Windows":
            readme_content += "Run `uninstall-windows.bat` as administrator"
        else:
            readme_content += "Run `./uninstall-unix.sh`"
        
        readme_content += f"""

---

**Syllabo v{self.version}** - AI-Powered Learning Assistant
Built with ❤️ for learners everywhere
"""
        
        return readme_content
    
    def create_package(self, platform_name):
        """Create release package for a platform"""
        print(f"Creating package for {platform_name}...")
        
        # Determine executable name
        if platform_name == "Windows":
            exe_name = "syllabo.exe"
            package_ext = "zip"
        else:
            exe_name = "syllabo"
            package_ext = "tar.gz"
        
        # Create package directory
        package_name = f"syllabo-v{self.version}-{platform_name}-{self.current_arch}"
        package_dir = self.release_dir / package_name
        package_dir.mkdir(parents=True, exist_ok=True)
        
        # Copy executable
        exe_path = self.dist_dir / exe_name
        if exe_path.exists():
            shutil.copy2(exe_path, package_dir / exe_name)
        else:
            print(f"Warning: Executable not found: {exe_path}")
            return False
        
        # Copy installer scripts
        if platform_name == "Windows":
            shutil.copy2("install-windows.bat", package_dir)
            shutil.copy2("uninstall-windows.bat", package_dir)
        elif platform_name == "Linux":
            shutil.copy2("install-linux.sh", package_dir)
            shutil.copy2("uninstall-unix.sh", package_dir)
        else:  # macOS
            shutil.copy2("install-macos.sh", package_dir)
            shutil.copy2("uninstall-unix.sh", package_dir)
        
        # Copy additional files
        files_to_copy = [".env.example", "LICENSE"]
        for file_name in files_to_copy:
            if Path(file_name).exists():
                shutil.copy2(file_name, package_dir)
        
        # Create README
        readme_content = self.create_readme(platform_name)
        with open(package_dir / "README.txt", "w") as f:
            f.write(readme_content)
        
        # Create archive
        archive_path = self.release_dir / f"{package_name}.{package_ext}"
        
        if package_ext == "zip":
            with zipfile.ZipFile(archive_path, 'w', zipfile.ZIP_DEFLATED) as zf:
                for file_path in package_dir.rglob('*'):
                    if file_path.is_file():
                        arcname = file_path.relative_to(self.release_dir)
                        zf.write(file_path, arcname)
        else:
            with tarfile.open(archive_path, 'w:gz') as tf:
                tf.add(package_dir, arcname=package_name)
        
        print(f"✓ Package created: {archive_path}")
        return True
    
    def build_for_platform(self, platform_name):
        """Build complete package for a platform"""
        print(f"\n{'='*50}")
        print(f"Building for {platform_name}")
        print(f"{'='*50}")
        
        if not self.build_executable(platform_name):
            return False
        
        if not self.create_package(platform_name):
            return False
        
        return True
    
    def build_all(self):
        """Build packages for all platforms"""
        print(f"Building Syllabo v{self.version} for all platforms")
        print(f"Current platform: {self.current_platform}")
        
        # Clean and prepare
        self.clean_build_dirs()
        
        if not self.install_dependencies():
            print("Failed to install dependencies")
            return False
        
        # Create installer scripts
        self.create_installer_scripts()
        self.create_uninstaller_scripts()
        
        # Build for current platform (we can only build for current platform with PyInstaller)
        success = self.build_for_platform(self.current_platform)
        
        if success:
            print(f"\n{'='*50}")
            print("BUILD COMPLETED SUCCESSFULLY!")
            print(f"{'='*50}")
            print(f"Version: {self.version}")
            print(f"Platform: {self.current_platform}")
            print(f"Architecture: {self.current_arch}")
            print(f"Release directory: {self.release_dir}")
            print("\nNext steps:")
            print("1. Test the package on your platform")
            print("2. Use GitHub Actions to build for other platforms")
            print("3. Upload to GitHub releases")
        else:
            print(f"\n{'='*50}")
            print("BUILD FAILED!")
            print(f"{'='*50}")
        
        return success

def main():
    """Main entry point"""
    if len(sys.argv) > 1 and sys.argv[1] == "--version":
        builder = PlatformBuilder()
        print(builder.version)
        return
    
    builder = PlatformBuilder()
    success = builder.build_all()
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()