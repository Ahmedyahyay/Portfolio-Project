#!/usr/bin/env python3
"""
Integrated Server - Personal Nutrition Assistant
يخدم كل من الواجهة الأمامية والخادم الخلفي على منفذ واحد
"""

import os
import sys
import subprocess
import threading
import time
import signal
from pathlib import Path

# إضافة مجلد backend إلى المسار
sys.path.append('backend')

from backend.app import app as flask_app
from flask import send_from_directory, send_file

# إعداد المسارات
BASE_DIR = Path(__file__).parent
FRONTEND_DIR = BASE_DIR / 'src' / 'frontend'
FRONTEND_DIST = FRONTEND_DIR / 'dist'
FRONTEND_BUILD = FRONTEND_DIR / 'build'

# متغيرات البيئة
os.environ['DATABASE_URL'] = 'sqlite:///nutrition.db'
os.environ['SECRET_KEY'] = 'dev-secret-key'
os.environ['NUTRITION_API'] = 'usda'
os.environ['NUTRITION_API_KEY'] = 'dev-key'

class IntegratedServer:
    def __init__(self, port=3000):
        self.port = port
        self.vite_process = None
        self.flask_app = flask_app
        
        # إعداد Flask routes للواجهة الأمامية
        self.setup_frontend_routes()
        
    def setup_frontend_routes(self):
        """إعداد routes للواجهة الأمامية"""
        
        @self.flask_app.route('/')
        def serve_frontend():
            """خدمة الصفحة الرئيسية"""
            return send_file(FRONTEND_DIR / 'index.html')
        
        @self.flask_app.route('/<path:path>')
        def serve_static(path):
            """خدمة الملفات الثابتة"""
            # إذا كان مسار API، تجاهل
            if path.startswith('api/'):
                return self.flask_app.handle_404()
            
            # البحث عن الملف في مجلد frontend
            file_path = FRONTEND_DIR / path
            if file_path.exists() and file_path.is_file():
                return send_file(file_path)
            
            # إذا لم يوجد، إرسال index.html (لـ SPA routing)
            return send_file(FRONTEND_DIR / 'index.html')
    
    def build_frontend(self):
        """بناء الواجهة الأمامية"""
        print("🔨 Building frontend...")
        
        # التحقق من وجود package.json
        if not (FRONTEND_DIR / 'package.json').exists():
            print("❌ package.json not found in frontend directory")
            return False
        
        try:
            # تثبيت التبعيات
            subprocess.run(['npm', 'install'], cwd=FRONTEND_DIR, check=True)
            
            # بناء المشروع
            subprocess.run(['npm', 'run', 'build'], cwd=FRONTEND_DIR, check=True)
            
            print("✅ Frontend built successfully")
            return True
            
        except subprocess.CalledProcessError as e:
            print(f"❌ Frontend build failed: {e}")
            return False
        except FileNotFoundError:
            print("❌ npm not found. Please install Node.js")
            return False
    
    def start_vite_dev(self):
        """تشغيل Vite في وضع التطوير"""
        print("🚀 Starting Vite development server...")
        
        try:
            self.vite_process = subprocess.Popen(
                ['npm', 'run', 'dev'],
                cwd=FRONTEND_DIR,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            
            # انتظار قليل للتأكد من بدء الخادم
            time.sleep(3)
            
            if self.vite_process.poll() is None:
                print("✅ Vite development server started")
                return True
            else:
                print("❌ Failed to start Vite development server")
                return False
                
        except FileNotFoundError:
            print("❌ npm not found. Please install Node.js")
            return False
    
    def start_flask(self):
        """تشغيل خادم Flask"""
        print(f"🐍 Starting Flask server on port {self.port}...")
        
        try:
            self.flask_app.run(
                host='0.0.0.0',
                port=self.port,
                debug=False,  # تعطيل debug لتجنب التداخل
                use_reloader=False
            )
        except Exception as e:
            print(f"❌ Flask server error: {e}")
    
    def start_integrated(self):
        """تشغيل الخادم المتكامل"""
        print("🎯 Starting Integrated Server...")
        print(f"📡 Server will be available at: http://localhost:{self.port}")
        print("🔄 Frontend: React + Vite")
        print("🐍 Backend: Flask + SQLite")
        print("=" * 50)
        
        # محاولة تشغيل Vite في وضع التطوير أولاً
        if self.start_vite_dev():
            print("✅ Development mode: Vite + Flask")
        else:
            print("⚠️  Fallback mode: Flask only")
        
        # تشغيل Flask
        try:
            self.start_flask()
        except KeyboardInterrupt:
            print("\n🛑 Shutting down server...")
            self.cleanup()
    
    def cleanup(self):
        """تنظيف العمليات"""
        if self.vite_process:
            self.vite_process.terminate()
            self.vite_process.wait()
        print("✅ Server stopped")

def main():
    """الدالة الرئيسية"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Integrated Nutrition Assistant Server')
    parser.add_argument('--port', type=int, default=3000, help='Port to run server on')
    parser.add_argument('--build', action='store_true', help='Build frontend before starting')
    
    args = parser.parse_args()
    
    server = IntegratedServer(port=args.port)
    
    # بناء الواجهة الأمامية إذا طُلب
    if args.build:
        if not server.build_frontend():
            print("❌ Failed to build frontend. Exiting...")
            return
    
    # إعداد معالج الإشارات للتنظيف
    def signal_handler(sig, frame):
        print("\n🛑 Received interrupt signal...")
        server.cleanup()
        sys.exit(0)
    
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    # تشغيل الخادم
    server.start_integrated()

if __name__ == '__main__':
    main()
