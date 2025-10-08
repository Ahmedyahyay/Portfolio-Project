@echo off
echo 🎯 Personal Nutrition Assistant - Quick Start
echo ================================================

REM التحقق من Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python not found. Please install Python 3.8+
    pause
    exit /b 1
)

REM التحقق من Node.js
node --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Node.js not found. Please install Node.js
    pause
    exit /b 1
)

echo ✅ Requirements found
echo.

REM تثبيت تبعيات Python
echo 📦 Installing Python dependencies...
pip install -r backend/requirements.txt
if errorlevel 1 (
    echo ❌ Failed to install Python dependencies
    pause
    exit /b 1
)

REM تثبيت تبعيات Node.js
echo 📦 Installing Node.js dependencies...
cd src/frontend
npm install
if errorlevel 1 (
    echo ❌ Failed to install Node.js dependencies
    pause
    exit /b 1
)
cd ../..

echo.
echo 🚀 Starting integrated server...
echo 🌐 Server will be available at: http://localhost:3000
echo.
echo Press Ctrl+C to stop the server
echo ================================================

REM تشغيل الخادم
python start.py 3000

pause
