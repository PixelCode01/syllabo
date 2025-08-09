@echo off
REM Docker publishing script for Syllabo (Windows)
REM This script builds and publishes Docker images to GitHub Container Registry

echo Syllabo Docker Publishing Script
echo ==================================

REM Configuration
set REGISTRY=ghcr.io
set NAMESPACE=pixelcode01
set IMAGE_NAME=syllabo
set FULL_IMAGE_NAME=%REGISTRY%/%NAMESPACE%/%IMAGE_NAME%

REM Check if Docker is installed
docker --version >nul 2>&1
if errorlevel 1 (
    echo Error: Docker is not installed
    pause
    exit /b 1
)

REM Get version from git tag or use 'latest'
for /f "tokens=*" %%i in ('git describe --tags --exact-match 2^>nul') do set VERSION=%%i
if "%VERSION%"=="" set VERSION=latest

echo Building version: %VERSION%

REM Build the image
echo Building Docker image...
docker build -t "%FULL_IMAGE_NAME%:%VERSION%" .
if errorlevel 1 (
    echo Failed to build Docker image
    pause
    exit /b 1
)

REM Tag as latest if this is a version tag
if not "%VERSION%"=="latest" (
    docker tag "%FULL_IMAGE_NAME%:%VERSION%" "%FULL_IMAGE_NAME%:latest"
)

REM Push the images
echo Pushing Docker images...
docker push "%FULL_IMAGE_NAME%:%VERSION%"
if errorlevel 1 (
    echo Failed to push Docker image
    echo Make sure you're logged in: docker login ghcr.io -u YOUR_GITHUB_USERNAME
    pause
    exit /b 1
)

if not "%VERSION%"=="latest" (
    docker push "%FULL_IMAGE_NAME%:latest"
)

echo.
echo Successfully published Docker images:
echo   %FULL_IMAGE_NAME%:%VERSION%
if not "%VERSION%"=="latest" (
    echo   %FULL_IMAGE_NAME%:latest
)

echo.
echo To use the published image:
echo   docker pull %FULL_IMAGE_NAME%:%VERSION%
echo   docker run -it --rm %FULL_IMAGE_NAME%:%VERSION%

echo.
echo Publishing complete!
pause