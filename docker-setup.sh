#!/bin/bash

# Syllabo Docker Setup Script
# This script helps set up the Syllabo application using Docker

set -e

echo "Setting up Syllabo with Docker..."

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "Error: Docker is not installed. Please install Docker first."
    echo "Visit: https://docs.docker.com/get-docker/"
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo "Error: Docker Compose is not installed. Please install Docker Compose first."
    echo "Visit: https://docs.docker.com/compose/install/"
    exit 1
fi

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "Creating .env file from template..."
    cp .env.example .env
    echo "Please edit .env file and add your API keys:"
    echo "  - YOUTUBE_API_KEY: Get from Google Cloud Console"
    echo "  - GEMINI_API_KEY: Get from Google AI Studio (optional)"
    echo ""
    echo "Opening .env file for editing..."
    ${EDITOR:-nano} .env
    echo ""
    read -p "Press Enter after you've updated the .env file..."
fi

# Create necessary directories
echo "Creating necessary directories..."
mkdir -p data logs

# Build the application
echo "Building Docker image..."
docker-compose build

echo ""
echo "Syllabo Docker setup complete!"
echo ""
echo "To start the application:"
echo "  docker-compose --profile app up"
echo ""
echo "To run interactively:"
echo "  docker-compose run --rm syllabo"
echo ""
echo "To run specific commands:"
echo "  docker-compose run --rm syllabo python main.py analyze --file syllabus.pdf"
echo ""
echo "To view logs:"
echo "  docker-compose logs -f syllabo"
echo ""
echo "To stop the application:"
echo "  docker-compose down"
echo ""
echo "Data is saved in the ./data directory"
echo "Logs are available in the ./logs directory"