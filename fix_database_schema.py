#!/usr/bin/env python3
"""
Database schema fix script following copilot database migration workflow
Adds missing username column to User table
"""

import os
import sys
import logging
from flask import Flask
from flask_migrate import Migrate, migrate, upgrade
from backend.models import db, User

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_app():
    """Create Flask app for database migration"""
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'dev-secret-for-migration'
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///nutrition.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    db.init_app(app)
    migrate = Migrate(app, db)
    
    return app

def fix_database_schema():
    """Fix database schema by adding missing username column"""
    print("🔧 Personal Nutrition Assistant - Database Schema Fix")
    print("Following copilot instructions database migration workflow")
    print("Adding missing username column to User table")
    print("=" * 60)
    
    # Change to project directory
    project_root = '/home/ahmed/Portfolio-Project'
    if os.path.exists(project_root):
        os.chdir(project_root)
    
    # Add backend to Python path
    sys.path.insert(0, os.path.join(os.getcwd(), 'backend'))
    
    # Create Flask app
    app = create_app()
    
    with app.app_context():
        try:
            # Check current User table structure
            print("🔍 Checking current User table structure...")
            inspector = db.inspect(db.engine)
            
            if 'user' in inspector.get_table_names():
                columns = [col['name'] for col in inspector.get_columns('user')]
                print(f"📋 Current User table columns: {columns}")
                
                if 'username' not in columns:
                    print("⚠️  Username column missing - creating migration...")
                    
                    # Change to backend directory for migration
                    os.chdir('backend')
                    
                    # Create migration to add username column
                    print("🔄 Creating migration to add username column...")
                    migrate(message="Add username column to User table following copilot patterns")
                    
                    # Apply migration
                    print("⬆️  Applying migration to add username column...")
                    upgrade()
                    
                    print("✅ Username column added successfully")
                    
                    # Update existing users with username based on email
                    print("🔄 Updating existing users with usernames...")
                    users_without_username = User.query.filter(User.username.is_(None)).all()
                    
                    for user in users_without_username:
                        if user.email:
                            base_username = user.email.split('@')[0]
                            username = base_username
                            counter = 1
                            
                            # Ensure unique username
                            while User.query.filter_by(username=username).first():
                                username = f"{base_username}{counter}"
                                counter += 1
                            
                            user.username = username
                            print(f"  📧 {user.email} -> username: {username}")
                    
                    db.session.commit()
                    print("✅ Existing users updated with usernames")
                    
                else:
                    print("✅ Username column already exists")
            else:
                print("⚠️  User table doesn't exist - creating all tables...")
                db.create_all()
                print("✅ All database tables created")
            
            # Verify the fix
            print("🔍 Verifying database schema...")
            columns = [col['name'] for col in inspector.get_columns('user')]
            print(f"📋 Updated User table columns: {columns}")
            
            if 'username' in columns:
                print("🎉 Schema fix completed successfully!")
                print("✅ Username column is now available")
                print("✅ Registration and login should work without OperationalError")
            else:
                print("❌ Schema fix failed - username column still missing")
                
        except Exception as e:
            print(f"❌ Schema fix failed: {e}")
            logger.error(f"Database schema fix error: {e}")
            sys.exit(1)

if __name__ == '__main__':
    fix_database_schema()
