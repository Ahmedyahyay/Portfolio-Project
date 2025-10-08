#!/usr/bin/env python3
"""
ملف تشغيل مبسط للموقع المتكامل
"""

import os
import sys
import subprocess
from pathlib import Path

def check_requirements():
    """التحقق من المتطلبات"""
    print("🔍 Checking requirements...")
    
    # التحقق من Python
    if sys.version_info < (3, 8):
        print("❌ Python 3.8+ required")
        return False
    
    # التحقق من Node.js
    try:
        subprocess.run(['node', '--version'], check=True, capture_output=True)
        subprocess.run(['npm', '--version'], check=True, capture_output=True)
        print("✅ Node.js and npm found")
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ Node.js and npm required")
        return False
    
    # التحقق من Python packages
    try:
        import flask
        import flask_cors
        import flask_sqlalchemy
        print("✅ Python packages found")
    except ImportError as e:
        print(f"❌ Missing Python package: {e}")
        print("Run: pip install -r backend/requirements.txt")
        return False
    
    return True

def setup_environment():
    """إعداد البيئة"""
    print("⚙️  Setting up environment...")
    
    # متغيرات البيئة
    os.environ['DATABASE_URL'] = 'sqlite:///nutrition.db'
    os.environ['SECRET_KEY'] = 'dev-secret-key'
    os.environ['NUTRITION_API'] = 'usda'
    os.environ['NUTRITION_API_KEY'] = 'dev-key'
    os.environ['FLASK_ENV'] = 'development'
    
    print("✅ Environment configured")

def install_frontend_deps():
    """تثبيت تبعيات الواجهة الأمامية"""
    print("📦 Installing frontend dependencies...")
    
    frontend_dir = Path('src/frontend')
    if not frontend_dir.exists():
        print("❌ Frontend directory not found")
        return False
    
    try:
        subprocess.run(['npm', 'install'], cwd=frontend_dir, check=True)
        print("✅ Frontend dependencies installed")
        return True
    except subprocess.CalledProcessError:
        print("❌ Failed to install frontend dependencies")
        return False

def start_server(port=3000):
    """تشغيل الخادم"""
    print(f"🚀 Starting server on port {port}...")
    
    try:
        # تشغيل الخادم المتكامل
        subprocess.run([sys.executable, 'server.py', '--port', str(port)], check=True)
    except subprocess.CalledProcessError:
        print("❌ Failed to start server")
        return False
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
        return True

def main():
    """الدالة الرئيسية"""
    print("🎯 Personal Nutrition Assistant - Integrated Server")
    print("=" * 50)
    
    # التحقق من المتطلبات
    if not check_requirements():
        print("\n❌ Requirements check failed")
        return
    
    # إعداد البيئة
    setup_environment()
    
    # تثبيت تبعيات الواجهة الأمامية
    if not install_frontend_deps():
        print("\n❌ Frontend setup failed")
        return
    
    # الحصول على المنفذ
    port = 3000
    if len(sys.argv) > 1:
        try:
            port = int(sys.argv[1])
        except ValueError:
            print("❌ Invalid port number")
            return
    
    print(f"\n🎉 Ready to start server on port {port}")
    print("📱 Frontend: React + Vite")
    print("🐍 Backend: Flask + SQLite")
    print("🌐 URL: http://localhost:" + str(port))
    print("\nPress Ctrl+C to stop the server")
    print("=" * 50)
    
    # تشغيل الخادم
    start_server(port)

if __name__ == '__main__':
    main()
