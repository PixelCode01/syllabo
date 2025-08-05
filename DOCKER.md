# Docker Usage Guide

This guide explains how to use Syllabo with Docker for easy setup and deployment.

## Quick Start

1. Clone the repository:
```bash
git clone https://github.com/PixelCode01/syllabo.git
cd syllabo
```

2. Run the setup script:
```bash
# Linux/Mac
./docker-setup.sh

# Windows
docker-setup.bat
```

3. Start using the application:
```bash
docker-compose run --rm syllabo
```

## Available Commands

### Using Make (Recommended)

```bash
make build      # Build the Docker image
make run        # Run the application interactively
make interactive # Run in interactive mode with menu
make stop       # Stop all running containers
make clean      # Remove containers and images
make logs       # View application logs
make shell      # Open a shell in the container
```

### Using Docker Compose Directly

```bash
# Build the image
docker-compose build

# Run interactively
docker-compose run --rm syllabo

# Run specific commands
docker-compose run --rm syllabo python main.py analyze --file syllabus.pdf
docker-compose run --rm syllabo python main.py search --topic "Machine Learning"

# View logs
docker-compose logs -f syllabo

# Stop containers
docker-compose down
```

## Environment Setup

1. Copy the environment template:
```bash
cp .env.example .env
```

2. Edit `.env` and add your API keys:
```
YOUTUBE_API_KEY=your_youtube_api_key_here
GEMINI_API_KEY=your_gemini_api_key_here
```

The application works without API keys, but some features may be limited.

## Data Persistence

Your data is automatically saved in these directories:
- `./data/` - Database files and user data
- `./logs/` - Application logs

These directories are mounted as volumes, so your data persists between container runs.

## Troubleshooting

### Container won't start
```bash
# Check Docker is running
docker --version

# Rebuild the image
make clean
make build
```

### Permission issues
```bash
# Fix file permissions
chmod +x docker-setup.sh
chmod +x scripts/healthcheck.py
```

### View detailed logs
```bash
make logs
# or
docker-compose logs -f syllabo
```

### Access container shell for debugging
```bash
make shell
# or
docker-compose run --rm syllabo /bin/bash
```

## Development Mode

For development with live code reloading:

```bash
# Start development container
docker-compose --profile dev run --rm syllabo-dev

# This mounts your local code directory for live editing
```

## Health Check

Test if the application is working correctly:

```bash
docker-compose run --rm syllabo python scripts/healthcheck.py
```

## Updating

To update to the latest version:

```bash
git pull
make clean
make build
```

## Uninstalling

To completely remove Syllabo:

```bash
make clean
rm -rf data logs
```

This removes all containers, images, and data. Your source code remains untouched.