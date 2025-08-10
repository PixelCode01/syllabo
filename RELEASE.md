# Syllabo Release Guide

This guide explains how to create releases for Syllabo with automated GitHub releases and GitHub Pages.

## 🚀 Quick Start - First Release

If this is your first time creating a release:

```bash
# Make sure everything is committed and pushed
git add .
git commit -m "Ready for first release"
git push origin main

# Create your first release
make first-release
```

This will:
1. ✅ Check your setup (Git, GitHub, required files)
2. 🏷️ Create and push a version tag
3. 🔄 Trigger automated builds for all platforms
4. 📦 Create GitHub release with standalone executables
5. 🌐 Deploy GitHub Pages website

## 📋 What Gets Created

### GitHub Releases
Each release automatically creates:

- **Windows Package** (`syllabo-vX.X.X-Windows.zip`)
  - Standalone executable (`syllabo.exe`)
  - Automatic installer (`install-windows.bat`)
  - Uninstaller (`uninstall-windows.bat`)
  - Configuration template (`.env.example`)
  - Documentation (`README.txt`)

- **Linux Package** (`syllabo-vX.X.X-Linux.tar.gz`)
  - Standalone executable (`syllabo`)
  - Automatic installer (`install-linux.sh`)
  - Uninstaller (`uninstall-unix.sh`)
  - Configuration template (`.env.example`)
  - Documentation (`README.txt`)

- **macOS Package** (`syllabo-vX.X.X-macOS.tar.gz`)
  - Standalone executable (`syllabo`)
  - Automatic installer (`install-macos.sh`)
  - Uninstaller (`uninstall-unix.sh`)
  - Configuration template (`.env.example`)
  - Documentation (`README.txt`)

### GitHub Pages Website
Automatically deployed to `https://yourusername.github.io/syllabo`:

- 🎨 Beautiful download page
- 📱 Mobile-responsive design
- 🔗 Direct download links
- 📚 Feature showcase
- 📖 Documentation links
- 🆕 Latest release information

## 🔄 Regular Releases

After your first release, use these commands for updates:

```bash
# Patch release (1.0.0 → 1.0.1)
make release-patch

# Minor release (1.0.0 → 1.1.0)  
make release-minor

# Major release (1.0.0 → 2.0.0)
make release-major

# Dry run (see what would happen)
make release-dry-run
```

## 🛠️ Manual Release Process

If you prefer manual control:

### 1. Update Version
```bash
# Edit src/version.py
echo 'VERSION = "1.0.1"' > src/version.py

# Commit changes
git add src/version.py
git commit -m "Bump version to 1.0.1"
git push origin main
```

### 2. Create Tag
```bash
# Create and push tag
git tag -a v1.0.1 -m "Release v1.0.1"
git push origin v1.0.1
```

### 3. GitHub Actions Takes Over
The workflows automatically:
- Build executables for all platforms
- Create release packages
- Upload to GitHub Releases
- Deploy GitHub Pages

## 📊 Release Workflow Details

### Build Process
1. **Multi-platform builds** on GitHub Actions runners
2. **PyInstaller** creates standalone executables
3. **Comprehensive testing** ensures executables work
4. **Package creation** with installers and documentation
5. **Checksum generation** for security verification

### Supported Platforms
- **Windows**: 10/11 (64-bit)
- **Linux**: Ubuntu, Debian, CentOS, Fedora, etc.
- **macOS**: 10.15+ (Intel & Apple Silicon)

### File Sizes
- Windows: ~30MB
- Linux: ~35MB  
- macOS: ~35MB

## 🔧 Customizing Releases

### Release Notes
Edit `.github/workflows/build-and-release.yml` to customize:
- Release description
- Feature highlights
- Download instructions
- Documentation links

### GitHub Pages
Edit `.github/workflows/pages.yml` to customize:
- Website design
- Download page layout
- Feature descriptions
- Branding elements

### Build Configuration
Edit `syllabo.spec` to customize:
- Included dependencies
- Executable optimization
- Platform-specific settings
- File exclusions

## 🐛 Troubleshooting

### Build Failures

**Problem**: PyInstaller fails to build
```bash
# Solution: Check dependencies
pip install -r requirements.txt
python test-build.py
```

**Problem**: Missing modules in executable
```bash
# Solution: Add to syllabo.spec hidden imports
hiddenimports=['missing_module']
```

### Release Issues

**Problem**: Tag already exists
```bash
# Solution: Delete and recreate
git tag -d v1.0.1
git push origin --delete v1.0.1
git tag -a v1.0.1 -m "Release v1.0.1"
git push origin v1.0.1
```

**Problem**: GitHub Actions not triggering
- Check if workflows are enabled in repository settings
- Verify tag format matches `v*` pattern
- Check GitHub Actions permissions

### GitHub Pages Issues

**Problem**: Pages not deploying
1. Go to repository Settings → Pages
2. Set Source to "GitHub Actions"
3. Check workflow permissions

**Problem**: Download links broken
- Verify release assets were uploaded
- Check asset naming matches page expectations
- Ensure release is not marked as draft

## 📈 Release Best Practices

### Before Release
- [ ] Test build locally: `make build-local`
- [ ] Run tests: `python test-build.py`
- [ ] Update documentation
- [ ] Update changelog
- [ ] Commit all changes

### Version Numbering
Follow [Semantic Versioning](https://semver.org/):
- **Patch** (1.0.1): Bug fixes
- **Minor** (1.1.0): New features, backward compatible
- **Major** (2.0.0): Breaking changes

### Release Frequency
- **Patch releases**: As needed for bug fixes
- **Minor releases**: Monthly or when significant features are ready
- **Major releases**: Quarterly or for major overhauls

## 🔒 Security Considerations

### Code Signing
For production releases, consider code signing:
- Windows: Use SignTool with certificate
- macOS: Use Apple Developer certificate
- Linux: Use GPG signatures

### Checksums
All releases include SHA256 checksums:
```bash
# Verify download integrity
sha256sum syllabo-v1.0.1-Linux.tar.gz
# Compare with checksums.txt from release
```

### Supply Chain Security
- All builds happen on GitHub Actions
- Source code is publicly auditable
- No external build dependencies
- Reproducible builds

## 📞 Support

### For Users
- 🌐 **Website**: https://yourusername.github.io/syllabo
- 📖 **Documentation**: [INSTALLATION.md](INSTALLATION.md)
- 🐛 **Issues**: [GitHub Issues](https://github.com/yourusername/syllabo/issues)
- 💬 **Discussions**: [GitHub Discussions](https://github.com/yourusername/syllabo/discussions)

### For Developers
- 🏗️ **Build Guide**: [BUILD.md](BUILD.md)
- 🤝 **Contributing**: [CONTRIBUTING.md](CONTRIBUTING.md)
- 📜 **License**: [LICENSE](LICENSE)

---

**Happy Releasing!** 🎉 Your users will love the easy installation experience.