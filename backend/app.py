from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
import os
import logging
from datetime import datetime

# Import models and routes blueprint organization
from models import db
from routes import register_blueprints
from session_fix import apply_session_fix

def create_app(config_name=None):
    """Application factory pattern"""
    app = Flask(__name__, 
                template_folder='../templates',
                static_folder='../static')
    
    # Configuration environment-aware database pattern
    config_name = config_name or os.environ.get('FLASK_ENV', 'development')
    
    if config_name == 'production':
        app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'production-secret-key-change-me')
        app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'postgresql://user:pass@localhost/nutrition')
        app.config['DEBUG'] = False
    else:
        app.config['SECRET_KEY'] = 'dev-secret-key-change-in-production'
        app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///nutrition.db')
        app.config['DEBUG'] = True
    
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Initialize extensions blueprint organization
    db.init_app(app)
    migrate = Migrate(app, db)
    
    # CORS configuration for frontend integration
    CORS(app, origins=['http://localhost:3000', 'http://127.0.0.1:3000'])
    
    # Apply session fix to prevent 'partitioned' cookie TypeError
    apply_session_fix(app)
    
    # Setup logging QA integration patterns
    if not app.debug:
        if not os.path.exists('logs'):
            os.mkdir('logs')
        file_handler = logging.FileHandler('logs/nutrition_assistant.log')
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
        ))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)
        app.logger.setLevel(logging.INFO)
        app.logger.info('Personal Nutrition Assistant startup')
    
    # Register blueprints using centralized registration patterns
    register_blueprints(app)
    
    return app

# Create app instance
app = create_app()

if __name__ == '__main__':
    # Initialize database if needed
    with app.app_context():
        # Create all tables if they don't exist
        try:
            db.create_all()
            app.logger.info('Database tables created successfully')
        except Exception as e:
            app.logger.error(f'Database creation error: {e}')
        
        # Log startup info health-centric patterns
        app.logger.info('🏥 Personal Nutrition Assistant - Flask MVP')
        app.logger.info('🎯 Target: Adults with BMI ≥ 30')
        app.logger.info('🔬 sprint-based development')
        app.logger.info('🗄️ Database: SQLite (development) / PostgreSQL (production)')
        app.logger.info('🔧 Session interface fix applied for cookie compatibility')
    
    print("🏥 Personal Nutrition Assistant - Starting Server")
    print("🎯 Target: Adults with BMI ≥ 30")
    print("🌐 Server: http://127.0.0.1:5000")
    print("📧 Demo Login: demo@nutriassist.com / demo123")
    print("🔬 with health-centric data model")
    print("🔧 Session cookie fix applied for Flask compatibility")
    
    app.run(debug=True, host='127.0.0.1', port=5000)
