# Syllabo for Windows

## Important Notice About Antivirus Software

**Windows Defender and other antivirus programs may flag this software as suspicious. This is a false positive.**

Syllabo is packaged using PyInstaller, which creates standalone executables. This packaging method often triggers false positives because the executable contains compressed Python code that unpacks at runtime.

### The software is completely safe because:
- It's open source - you can review all code on GitHub
- It doesn't modify system files or registry
- It only accesses the internet for educational content APIs
- No personal data is collected or transmitted

## Quick Solutions

### If Windows Defender blocks the file:

**Option 1: Add Exclusion (Recommended)**
1. Open Windows Security
2. Go to "Virus & threat protection"
3. Click "Manage settings" under protection settings
4. Scroll to "Exclusions" and click "Add or remove exclusions"
5. Click "Add an exclusion" → "File"
6. Select the syllabo.exe file

**Option 2: Use the Safe Runner**
1. Double-click `run_syllabo_safe.bat`
2. Follow the on-screen instructions

## Installation Options

### Option 1: Portable (No Installation)
1. Extract all files to a folder
2. Double-click `run_syllabo.bat`
3. Or run `syllabo.exe interactive` from command prompt

### Option 2: Add to PATH
1. Copy syllabo.exe to a folder in your PATH
2. Run `syllabo interactive` from any command prompt

## Getting Started

### First Run
```cmd
syllabo.exe interactive
```

### Basic Commands
```cmd
syllabo.exe --help                    # Show all commands
syllabo.exe config show               # Check configuration
syllabo.exe analyze --text "content"  # Analyze text
syllabo.exe quiz --topic "Python"     # Generate quiz
```

### Configuration (Optional)
For enhanced features, configure API keys:
```cmd
syllabo.exe config gemini    # Configure Gemini AI
syllabo.exe config youtube   # Configure YouTube API
```

## System Requirements
- Windows 10 or later (64-bit)
- No Python installation required
- Internet connection for AI features
- 50MB free disk space

## Troubleshooting

### Executable won't run
1. Check Windows Defender exclusions
2. Try running as administrator
3. Ensure you have Windows 10 or later
4. Check that the file wasn't corrupted during download

### Features not working
1. Check internet connection
2. Configure API keys for full functionality
3. Run `syllabo.exe config show` to check status

### Still having issues?
- See `ANTIVIRUS_TROUBLESHOOTING.md` for detailed solutions
- Visit our GitHub page for support
- Check the issues page for known problems

## Files Included

- `syllabo.exe` - Main application (23+ MB)
- `run_syllabo.bat` - Simple runner script
- `run_syllabo_safe.bat` - Antivirus-aware runner
- `.env.example` - Configuration template
- `WINDOWS_INSTALL.md` - Installation guide
- Documentation files

## Support

- GitHub: https://github.com/PixelCode01/syllabo
- Issues: https://github.com/PixelCode01/syllabo/issues
- Documentation: https://github.com/PixelCode01/syllabo/blob/main/README.md

## Privacy and Security

Syllabo:
- Does not collect personal information
- Only connects to educational APIs (YouTube, Gemini)
- Stores data locally on your computer
- Does not modify system settings
- Is completely open source

The antivirus detection is a false positive caused by the packaging method, not malicious behavior.