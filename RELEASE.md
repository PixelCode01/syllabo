# Release Guide for Syllabo

This guide covers how to create and publish releases for Syllabo.

## Automated Release Process

The project uses GitHub Actions to automatically build and publish releases when you push a tag.

### Creating a Release

1. **Update version information:**
   ```bash
   # Update version in relevant files if needed
   # Commit any final changes
   git add .
   git commit -m "Prepare for release v1.0.0"
   ```

2. **Create and push a tag:**
   ```bash
   git tag -a v1.0.0 -m "Release version 1.0.0"
   git push origin v1.0.0
   ```

3. **GitHub Actions will automatically:**
   - Build Docker images for multiple platforms
   - Build standalone executables for Windows, Linux, and macOS
   - Publish Docker images to GitHub Container Registry
   - Create a GitHub release with all artifacts

## Manual Release Process

If you need to create releases manually:

### 1. Build Executables

```bash
# Install dependencies
make install-deps

# Build all executables
make build-exe

# Or use the build script directly
python build.py
```

This creates:
- `dist/syllabo.exe` (Windows)
- `dist/syllabo` (Linux/macOS)
- `release/` directory with packaged releases

### 2. Build and Publish Docker Image

```bash
# Build Docker image
make build

# Publish to GitHub Container Registry
make publish

# Or manually:
docker build -t ghcr.io/pixelcode01/syllabo:latest .
docker push ghcr.io/pixelcode01/syllabo:latest
```

### 3. Create GitHub Release

1. Go to GitHub repository
2. Click "Releases" → "Create a new release"
3. Choose your tag or create a new one
4. Upload the built executables from `release/` directory
5. Write release notes
6. Publish the release

## Docker Publishing

### GitHub Container Registry

The project is configured to publish to GitHub Container Registry (ghcr.io):

```bash
# Login to GitHub Container Registry
echo $GITHUB_TOKEN | docker login ghcr.io -u USERNAME --password-stdin

# Build and push
docker build -t ghcr.io/pixelcode01/syllabo:latest .
docker push ghcr.io/pixelcode01/syllabo:latest
```

### Docker Hub (Optional)

To also publish to Docker Hub:

1. **Login to Docker Hub:**
   ```bash
   docker login
   ```

2. **Tag and push:**
   ```bash
   docker tag ghcr.io/pixelcode01/syllabo:latest pixelcode01/syllabo:latest
   docker push pixelcode01/syllabo:latest
   ```

## GitHub Pages

The project website is automatically deployed to GitHub Pages when you push to the main branch.

### Manual Pages Deployment

If you need to update the website manually:

1. **Update `docs/index.html`** with any changes
2. **Commit and push:**
   ```bash
   git add docs/
   git commit -m "Update website"
   git push origin main
   ```

The GitHub Pages workflow will automatically deploy the changes.

## Release Checklist

Before creating a release:

- [ ] All tests pass
- [ ] Documentation is up to date
- [ ] Version numbers are updated
- [ ] CHANGELOG.md is updated (if you have one)
- [ ] Docker image builds successfully
- [ ] Executables build on all platforms
- [ ] API keys and sensitive data are not included
- [ ] Installation instructions are tested

### Testing the Release

1. **Test Docker image:**
   ```bash
   docker run -it --rm ghcr.io/pixelcode01/syllabo:latest
   ```

2. **Test executables:**
   - Download from the release
   - Test on different operating systems
   - Verify all features work

3. **Test installation methods:**
   - Docker installation
   - Executable installation
   - Python source installation

## Versioning

The project follows semantic versioning (SemVer):

- **MAJOR** version for incompatible API changes
- **MINOR** version for backwards-compatible functionality additions
- **PATCH** version for backwards-compatible bug fixes

Examples:
- `v1.0.0` - Initial release
- `v1.1.0` - New features added
- `v1.1.1` - Bug fixes
- `v2.0.0` - Breaking changes

## Troubleshooting

### Build Issues

- **PyInstaller fails:** Check that all dependencies are installed
- **Docker build fails:** Ensure Docker is running and you have internet access
- **Permission denied:** Make sure scripts are executable (Linux/macOS)

### Publishing Issues

- **Docker push fails:** Check that you're logged in to the registry
- **GitHub Actions fail:** Check the workflow logs for specific errors
- **Release upload fails:** Ensure you have the necessary permissions

### Common Solutions

1. **Clear build cache:**
   ```bash
   make clean
   docker system prune -f
   ```

2. **Rebuild everything:**
   ```bash
   make release
   ```

3. **Check logs:**
   ```bash
   make logs
   ```

## Post-Release

After creating a release:

1. **Announce the release:**
   - Update README.md with new version info
   - Post on social media or relevant forums
   - Update documentation sites

2. **Monitor for issues:**
   - Watch GitHub issues for bug reports
   - Monitor Docker Hub/GHCR for download stats
   - Check website analytics

3. **Plan next release:**
   - Create milestone for next version
   - Prioritize features and bug fixes
   - Update project roadmap

## Automation

The project includes several automation features:

- **GitHub Actions:** Automatic building and publishing
- **Docker Compose:** Easy local development
- **Makefile:** Simplified command interface
- **Build scripts:** Cross-platform executable creation

This ensures consistent and reliable releases across all platforms.