# Creating a Release for Syllabo

## Prerequisites

1. Make sure you have pushed all changes to GitHub
2. Ensure the repository is public on GitHub
3. Have the necessary permissions to create releases

## Steps to Create a Release

### Method 1: Using GitHub Web Interface

1. **Go to your GitHub repository**
   - Navigate to `https://github.com/PixelCode01/syllabo`

2. **Create a new release**
   - Click on "Releases" (on the right side of the repository page)
   - Click "Create a new release"

3. **Tag the release**
   - Choose a tag: `v1.0.0` (or increment as needed)
   - Target: `main` branch

4. **Release details**
   - Release title: `Syllabo v1.0.0 - Initial Release`
   - Description:
   ```markdown
   # Syllabo v1.0.0 - Initial Release
   
   An AI-powered learning assistant that analyzes course syllabi and helps students organize their study materials.
   
   ## Features
   - Syllabus analysis and topic extraction
   - AI-generated quizzes
   - Progress tracking and analytics
   - Spaced repetition learning system
   - Study session management with Pomodoro timer
   - Educational resource discovery
   
   ## Installation
   
   ### Docker (Recommended)
   ```bash
   docker pull ghcr.io/pixelcode01/syllabo:latest
   docker run -it --rm ghcr.io/pixelcode01/syllabo:latest
   ```
   
   ### From Source
   ```bash
   git clone https://github.com/PixelCode01/syllabo.git
   cd syllabo
   pip install -r requirements.txt
   python main.py interactive
   ```
   
   ## What's New
   - Initial release with full feature set
   - Docker support with automated builds
   - Comprehensive documentation
   - Interactive CLI interface
   
   ## Coming Soon
   - Standalone executables for Windows, Linux, and macOS
   - Web interface
   - Mobile app
   ```

5. **Publish the release**
   - Click "Publish release"

### Method 2: Using Git Tags (Triggers GitHub Actions)

If you have GitHub Actions set up:

```bash
# Create and push a tag
git tag -a v1.0.0 -m "Release v1.0.0"
git push origin v1.0.0
```

This will trigger the GitHub Actions workflow to:
- Build Docker images
- Build executables (if the build environment supports it)
- Create a release automatically

### Method 3: Manual Release with Files

If you want to include pre-built files:

1. **Build locally** (if possible):
   ```bash
   python build-local.py
   ```

2. **Create release on GitHub** (Method 1 above)

3. **Upload files**:
   - Drag and drop any built executables
   - Add installation scripts
   - Include documentation files

## Current Status

Since the executables aren't built yet due to dependency issues, create the release with:

1. **Docker image** (will be built by GitHub Actions)
2. **Source code** (automatically included)
3. **Documentation** pointing users to Docker and source installation

## After Creating the Release

1. **Update the website** (`docs/index.html`) to point to the actual release
2. **Test the Docker image**: `docker pull ghcr.io/pixelcode01/syllabo:latest`
3. **Update README** if needed
4. **Announce the release** on relevant platforms

## Troubleshooting

- **No executables**: Focus on Docker and source installation for now
- **GitHub Actions failing**: Check the workflow logs and fix any issues
- **Docker image not building**: Verify the Dockerfile and dependencies

The key is to create a release that works with what we have (Docker + source) and add executables in future releases.