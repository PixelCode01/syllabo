# Syllabo Makefile
# Cross-platform build and release automation

.PHONY: help install build build-local test clean release docker-build docker-run docker-clean portable

# Default target
help:
	@echo "Syllabo Build System"
	@echo "==================="
	@echo ""
	@echo "Available targets:"
	@echo "  install      - Install dependencies"
	@echo "  build        - Build executable for current platform"
	@echo "  build-local  - Quick local build for testing"
	@echo "  portable     - Create portable package (no installation required)"
	@echo "  test         - Run tests"
	@echo "  clean        - Clean build artifacts"
	@echo "  release      - Prepare a new release"
	@echo "  docker-build - Build Docker image"
	@echo "  docker-run   - Run in Docker container"
	@echo "  docker-clean - Clean Docker artifacts"
	@echo ""
	@echo "Release targets:"
	@echo "  release-patch - Bump patch version and release"
	@echo "  release-minor - Bump minor version and release"
	@echo "  release-major - Bump major version and release"
	@echo "  first-release - Create your first GitHub release"
	@echo ""
	@echo "Examples:"
	@echo "  make build           # Build for current platform"
	@echo "  make portable        # Create portable package"
	@echo "  make first-release   # Create first GitHub release"
	@echo "  make release-patch   # Create patch release"
	@echo "  make docker-run      # Run in Docker"

# Install dependencies
install:
	@echo "Installing dependencies..."
	pip install --upgrade pip
	pip install -r requirements.txt
	pip install pyinstaller setuptools wheel

# Build executable for current platform
build: install
	@echo "Building executable..."
	python build-all-platforms.py

# Quick local build for testing
build-local:
	@echo "Quick local build..."
	python build-local.py

# Run tests (if test files exist)
test:
	@echo "Running tests..."
	@if [ -f "test_main.py" ]; then python -m pytest test_main.py -v; else echo "No tests found"; fi
	@if [ -d "tests" ]; then python -m pytest tests/ -v; else echo "No test directory found"; fi

# Create portable package
portable: build-local
	@echo "Creating portable package..."
	python create-portable.py

# Clean build artifacts
clean:
	@echo "Cleaning build artifacts..."
	rm -rf build/ dist/ release/ portable/ *.spec
	rm -f install-*.sh install-*.bat uninstall-*.sh uninstall-*.bat
	find . -name "*.pyc" -delete
	find . -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null || true

# Release management
release:
	@echo "Preparing release..."
	python release.py

release-patch:
	@echo "Preparing patch release..."
	python release.py --bump patch

release-minor:
	@echo "Preparing minor release..."
	python release.py --bump minor

release-major:
	@echo "Preparing major release..."
	python release.py --bump major

release-dry-run:
	@echo "Dry run release..."
	python release.py --dry-run

first-release:
	@echo "Creating first GitHub release..."
	python create-first-release.py

# Docker targets
docker-build:
	@echo "Building Docker image..."
	docker build -t syllabo:latest .

docker-run: docker-build
	@echo "Running in Docker..."
	docker run -it --rm \
		-v $(PWD)/data:/app/data \
		-v $(PWD)/logs:/app/logs \
		syllabo:latest

docker-run-dev: docker-build
	@echo "Running in Docker (development mode)..."
	docker run -it --rm \
		-v $(PWD):/app \
		-v $(PWD)/data:/app/data \
		-v $(PWD)/logs:/app/logs \
		syllabo:latest /bin/bash

docker-clean:
	@echo "Cleaning Docker artifacts..."
	docker rmi syllabo:latest 2>/dev/null || true
	docker system prune -f

# Development targets
dev-setup: install
	@echo "Setting up development environment..."
	@if command -v pre-commit >/dev/null 2>&1; then \
		pip install pre-commit; \
		pre-commit install; \
		echo "Pre-commit hooks installed"; \
	fi

lint:
	@echo "Running linters..."
	@if command -v flake8 >/dev/null 2>&1; then flake8 src/ main.py; else echo "flake8 not installed"; fi
	@if command -v black >/dev/null 2>&1; then black --check src/ main.py; else echo "black not installed"; fi

format:
	@echo "Formatting code..."
	@if command -v black >/dev/null 2>&1; then black src/ main.py; else echo "black not installed"; fi

# Platform-specific targets
build-windows:
	@echo "Note: Cross-platform building requires GitHub Actions"
	@echo "Use 'make build' to build for current platform"

build-linux:
	@echo "Note: Cross-platform building requires GitHub Actions"
	@echo "Use 'make build' to build for current platform"

build-macos:
	@echo "Note: Cross-platform building requires GitHub Actions"
	@echo "Use 'make build' to build for current platform"

# Utility targets
version:
	@python -c "from src.version import VERSION; print(VERSION)" 2>/dev/null || \
	python -c "import sys; sys.path.append('src'); from version import VERSION; print(VERSION)" 2>/dev/null || \
	echo "1.0.0"

check-deps:
	@echo "Checking dependencies..."
	@python -c "import pkg_resources; pkg_resources.require(open('requirements.txt').read().splitlines())" && echo "✓ All dependencies satisfied" || echo "✗ Missing dependencies"

info:
	@echo "Syllabo Build Information"
	@echo "========================"
	@echo "Version: $(shell make version)"
	@echo "Python: $(shell python --version)"
	@echo "Platform: $(shell python -c 'import platform; print(platform.system())')"
	@echo "Architecture: $(shell python -c 'import platform; print(platform.machine())')"
	@echo "Working Directory: $(PWD)"

# Windows-specific commands (if running on Windows)
ifeq ($(OS),Windows_NT)
clean:
	@echo "Cleaning build artifacts (Windows)..."
	if exist build rmdir /s /q build
	if exist dist rmdir /s /q dist
	if exist release rmdir /s /q release
	del /q *.spec 2>nul || true
	del /q install-*.bat 2>nul || true
	del /q uninstall-*.bat 2>nul || true
	for /r %%i in (*.pyc) do del "%%i" 2>nul || true
	for /d /r %%i in (__pycache__) do rmdir /s /q "%%i" 2>nul || true
endif