@echo off
echo.
echo ========================================
echo  SYLLABO COMPLETE FEATURES DEMO
echo ========================================
echo.
echo Starting comprehensive features demo...
echo This will showcase ALL Syllabo features
echo with realistic sample data.
echo.
echo Estimated time: 10-15 minutes
echo Perfect for testing and evaluation!
echo.

python run_demo.py
if %ERRORLEVEL% EQU 0 (
    echo.
    echo Demo completed successfully!
    echo Ready to use Syllabo for your learning needs!
) else (
    echo.
    echo Demo encountered an error. Error code: %ERRORLEVEL%
)

echo.
echo Press any key to exit...
pause >nul
