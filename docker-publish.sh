#!/bin/bash

# Docker publishing script for Syllabo
# This script builds and publishes Docker images to GitHub Container Registry

set -e

# Configuration
REGISTRY="ghcr.io"
NAMESPACE="pixelcode01"  # Change this to your GitHub username
IMAGE_NAME="syllabo"
FULL_IMAGE_NAME="${REGISTRY}/${NAMESPACE}/${IMAGE_NAME}"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}Syllabo Docker Publishing Script${NC}"
echo "=================================="

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo -e "${RED}Error: Docker is not installed${NC}"
    exit 1
fi

# Check if we're logged in to the registry
echo -e "${YELLOW}Checking Docker registry login...${NC}"
if ! docker info | grep -q "Username"; then
    echo -e "${YELLOW}Please log in to GitHub Container Registry:${NC}"
    echo "docker login ghcr.io -u YOUR_GITHUB_USERNAME"
    echo "Use a Personal Access Token as the password"
    exit 1
fi

# Get version from git tag or use 'latest'
VERSION=$(git describe --tags --exact-match 2>/dev/null || echo "latest")
echo -e "${BLUE}Building version: ${VERSION}${NC}"

# Build the image
echo -e "${YELLOW}Building Docker image...${NC}"
docker build -t "${FULL_IMAGE_NAME}:${VERSION}" .

# Tag as latest if this is a version tag
if [[ "${VERSION}" != "latest" ]]; then
    docker tag "${FULL_IMAGE_NAME}:${VERSION}" "${FULL_IMAGE_NAME}:latest"
fi

# Push the images
echo -e "${YELLOW}Pushing Docker images...${NC}"
docker push "${FULL_IMAGE_NAME}:${VERSION}"

if [[ "${VERSION}" != "latest" ]]; then
    docker push "${FULL_IMAGE_NAME}:latest"
fi

echo -e "${GREEN}Successfully published Docker images:${NC}"
echo "  ${FULL_IMAGE_NAME}:${VERSION}"
if [[ "${VERSION}" != "latest" ]]; then
    echo "  ${FULL_IMAGE_NAME}:latest"
fi

echo ""
echo -e "${BLUE}To use the published image:${NC}"
echo "  docker pull ${FULL_IMAGE_NAME}:${VERSION}"
echo "  docker run -it --rm ${FULL_IMAGE_NAME}:${VERSION}"

echo ""
echo -e "${GREEN}Publishing complete!${NC}"