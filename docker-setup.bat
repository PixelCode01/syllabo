@echo off
REM Syllabo Docker Setup Script for Windows
REM This script helps set up the Syllabo application using Docker

echo Setting up Syllabo with Docker...

REM Check if Docker is installed
docker --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Error: Docker is not installed. Please install Docker Desktop first.
    echo Visit: https://docs.docker.com/desktop/install/windows-install/
    pause
    exit /b 1
)

REM Check if Docker Compose is installed
docker-compose --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Error: Docker Compose is not installed. Please install Docker Desktop first.
    echo Visit: https://docs.docker.com/desktop/install/windows-install/
    pause
    exit /b 1
)

REM Create .env file if it doesn't exist
if not exist .env (
    echo Creating .env file from template...
    copy .env.example .env
    echo.
    echo Please edit .env file and add your API keys:
    echo   - YOUTUBE_API_KEY: Get from Google Cloud Console
    echo   - GEMINI_API_KEY: Get from Google AI Studio (optional)
    echo.
    echo Opening .env file for editing...
    notepad .env
    echo.
    pause
)

REM Create necessary directories
echo Creating necessary directories...
if not exist data mkdir data
if not exist logs mkdir logs

REM Build and start the application
echo Building Docker image...
docker-compose build

echo.
echo Syllabo Docker setup complete!
echo.
echo To start the application:
echo   docker-compose --profile app up
echo.
echo To run interactively:
echo   docker-compose run --rm syllabo
echo.
echo To run specific commands:
echo   docker-compose run --rm syllabo python main.py analyze --file syllabus.pdf
echo.
echo To view logs:
echo   docker-compose logs -f syllabo
echo.
echo To stop the application:
echo   docker-compose down
echo.
echo Data is saved in the ./data directory
echo Logs are available in the ./logs directory
echo.
pause