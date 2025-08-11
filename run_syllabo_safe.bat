@echo off
REM Syllabo Safe Runner - Handles Windows Defender issues
REM This script helps users run Syllabo when Windows Defender blocks it

echo Syllabo Safe Runner
echo ==================
echo.

REM Check if syllabo.exe exists
if not exist "syllabo.exe" (
    echo Error: syllabo.exe not found in current directory
    echo Please make sure you're running this from the Syllabo folder
    echo.
    pause
    exit /b 1
)

echo Checking Windows Defender status...
echo.

REM Try to run syllabo.exe
echo Attempting to run Syllabo...
syllabo.exe --help >nul 2>&1

if %errorlevel% equ 0 (
    echo Syllabo is working correctly!
    echo.
    echo Starting interactive mode...
    syllabo.exe interactive
) else (
    echo.
    echo Windows Defender may be blocking Syllabo.
    echo This is a false positive - the software is safe.
    echo.
    echo Solutions:
    echo 1. Add syllabo.exe to Windows Defender exclusions
    echo 2. Temporarily disable real-time protection
    echo 3. Run as administrator
    echo.
    echo Would you like to:
    echo [1] Try running as administrator
    echo [2] Open Windows Defender settings
    echo [3] View troubleshooting guide
    echo [4] Exit
    echo.
    set /p choice="Enter your choice (1-4): "
    
    if "%choice%"=="1" (
        echo.
        echo Attempting to run as administrator...
        powershell -Command "Start-Process 'syllabo.exe' -ArgumentList 'interactive' -Verb RunAs"
    ) else if "%choice%"=="2" (
        echo.
        echo Opening Windows Defender settings...
        start ms-settings:windowsdefender
        echo.
        echo Add syllabo.exe to exclusions, then run this script again.
    ) else if "%choice%"=="3" (
        echo.
        echo Opening troubleshooting guide...
        if exist "ANTIVIRUS_TROUBLESHOOTING.md" (
            start notepad "ANTIVIRUS_TROUBLESHOOTING.md"
        ) else (
            echo Troubleshooting guide not found.
            echo Please visit: https://github.com/PixelCode01/syllabo
        )
    ) else (
        echo Exiting...
        exit /b 0
    )
)

echo.
pause