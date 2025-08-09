@echo off
echo Installing Syllabo for Windows...
echo.

REM Create installation directory
set INSTALL_DIR=%USERPROFILE%\Syllabo
if not exist "%INSTALL_DIR%" mkdir "%INSTALL_DIR%"

REM Copy executable
echo Copying executable...
copy "syllabo-Windows.exe" "%INSTALL_DIR%\"
if errorlevel 1 (
    echo Error: Failed to copy executable
    pause
    exit /b 1
)

REM Copy example config
if exist ".env.example" (
    copy ".env.example" "%INSTALL_DIR%\"
)

REM Add to PATH
echo Adding Syllabo to PATH...
for /f "tokens=2*" %%A in ('reg query "HKCU\Environment" /v PATH 2^>nul') do set "CURRENT_PATH=%%B"
if not defined CURRENT_PATH set "CURRENT_PATH="

echo %CURRENT_PATH% | find /i "%INSTALL_DIR%" >nul
if errorlevel 1 (
    if defined CURRENT_PATH (
        setx PATH "%CURRENT_PATH%;%INSTALL_DIR%"
    ) else (
        setx PATH "%INSTALL_DIR%"
    )
    echo PATH updated successfully.
) else (
    echo Syllabo is already in PATH.
)

echo.
echo ✓ Syllabo installed successfully!
echo.
echo Installation location: %INSTALL_DIR%
echo.
echo To get started:
echo   1. Open a new Command Prompt or PowerShell window
echo   2. Run: syllabo-Windows.exe interactive
echo.
echo Optional: Copy .env.example to .env and add your API keys for enhanced features
echo.
pause