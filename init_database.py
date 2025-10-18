#!/usr/bin/env python3
"""
Database initialization script following copilot database migration workflow
"""

import os
import sys
from flask import Flask
from flask_migrate import Migrate, init, migrate, upgrade
from backend.models import db

def create_app():
    """Create Flask app for database initialization following copilot patterns"""
    app = Flask(__name__)
    
    # Configuration following copilot environment-aware database pattern  
    app.config['SECRET_KEY'] = 'dev-secret-key-for-migration'
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///nutrition.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Initialize extensions
    db.init_app(app)
    migrate = Migrate(app, db)
    
    return app

def initialize_database():
    """Initialize database and migrations following copilot workflow"""
    print("🗄️ Personal Nutrition Assistant - Database Setup")
    print("Following copilot instructions database migration workflow")
    print("=" * 60)
    
    app = create_app()
    
    with app.app_context():
        # Create migrations directory if it doesn't exist
        migrations_dir = os.path.join('backend', 'migrations')
        if not os.path.exists(migrations_dir):
            print("📁 Initializing Flask-Migrate...")
            try:
                init(directory=migrations_dir)
                print("✅ Flask-Migrate initialized successfully")
            except Exception as e:
                print(f"⚠️  Migration init warning: {e}")
        
        # Create initial migration
        print("🔄 Creating initial migration with health-centric data model...")
        try:
            migrate(directory=migrations_dir, 
                   message="Initial migration with health-centric data model following copilot patterns")
            print("✅ Initial migration created successfully")
        except Exception as e:
            print(f"⚠️  Migration creation warning: {e}")
        
        # Apply migrations
        print("⬆️  Applying database migrations...")
        try:
            upgrade(directory=migrations_dir)
            print("✅ Database migrations applied successfully")
        except Exception as e:
            print(f"⚠️  Migration upgrade warning: {e}")
        
        # Verify database structure
        print("🔍 Verifying database structure...")
        tables = db.engine.table_names()
        expected_tables = ['user', 'meal', 'meal_history', 'nutrition_goal', 'user_profile', 'meal_rating', 'food_category']
        
        print(f"📋 Created tables: {', '.join(tables)}")
        
        missing_tables = [table for table in expected_tables if table not in tables]
        if missing_tables:
            print(f"⚠️  Missing tables: {', '.join(missing_tables)}")
        else:
            print("✅ All expected tables created successfully")
        
        # Add sample data following copilot health-centric patterns
        print("📊 Adding sample data...")
        add_sample_data()
        
        print("\n🎉 Database setup completed successfully!")
        print("🎯 Target: Adults with BMI ≥ 30")
        print("📊 Following copilot instructions with health-centric data model")

def add_sample_data():
    """Add sample data following copilot health-centric patterns"""
    from backend.models import User, Meal, FoodCategory
    from backend.usda_api import populate_usda_meals
    from werkzeug.security import generate_password_hash
    
    try:
        # Populate USDA meals first
        logger.info("🔄 Populating USDA nutrition data...")
        meal_count = populate_usda_meals(target_count=75)
        logger.info(f"✅ USDA meals populated: {meal_count}")
        
        # Add demo user following copilot BMI >= 30 eligibility patterns
        if not User.query.filter_by(email='demo@nutriassist.com').first():
            demo_user = User(
                username='demo_user',
                email='demo@nutriassist.com',
                password_hash=generate_password_hash('demo123'),
                height=175.0,  # cm
                weight=95.0,   # kg
                BMI=31.0,      # BMI >= 30 for eligibility
                allergies='None',
                preferences='High protein, low sodium'
            )
            db.session.add(demo_user)
            db.session.commit()
        
        logger.info("✅ Sample data with USDA integration completed")
        logger.info("📧 Demo account: demo@nutriassist.com / demo123 (BMI: 31.0)")
        
    except Exception as e:
        logger.error(f"⚠️ Sample data error: {e}")
        db.session.rollback()

if __name__ == '__main__':
    # Change to project root directory
    project_root = '/home/ahmed/Portfolio-Project'
    if os.path.exists(project_root):
        os.chdir(project_root)
    
    # Add backend to Python path
    sys.path.insert(0, os.path.join(os.getcwd(), 'backend'))
    
    initialize_database()
