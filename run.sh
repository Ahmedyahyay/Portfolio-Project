#!/bin/bash

echo "🎯 Personal Nutrition Assistant - Quick Start"
echo "================================================"

# التحقق من Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 not found. Please install Python 3.8+"
    exit 1
fi

# التحقق من Node.js
if ! command -v node &> /dev/null; then
    echo "❌ Node.js not found. Please install Node.js"
    exit 1
fi

if ! command -v npm &> /dev/null; then
    echo "❌ npm not found. Please install npm"
    exit 1
fi

echo "✅ Requirements found"
echo

# تثبيت تبعيات Python
echo "📦 Installing Python dependencies..."
pip3 install -r backend/requirements.txt
if [ $? -ne 0 ]; then
    echo "❌ Failed to install Python dependencies"
    exit 1
fi

# تثبيت تبعيات Node.js
echo "📦 Installing Node.js dependencies..."
cd src/frontend
npm install
if [ $? -ne 0 ]; then
    echo "❌ Failed to install Node.js dependencies"
    exit 1
fi
cd ../..

echo
echo "🚀 Starting integrated server..."
echo "🌐 Server will be available at: http://localhost:3000"
echo
echo "Press Ctrl+C to stop the server"
echo "================================================"

# تشغيل الخادم
python3 start.py 3000
