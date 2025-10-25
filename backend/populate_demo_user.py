#!/usr/bin/env python3
"""
Demo user population script health-centric patterns
Ensures demo user has proper username field
"""

import sys
import os
from flask import Flask
from models import db, User
from werkzeug.security import generate_password_hash

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///nutrition.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    return app

def create_demo_user():
    """Create demo user with proper username patterns"""
    app = create_app()
    
    with app.app_context():
        # Check if demo user already exists
        demo_user = User.query.filter_by(email='demo@nutriassist.com').first()
        
        if demo_user:
            # Update existing demo user with username if missing
            if not demo_user.username:
                demo_user.username = 'demo_user'
                db.session.commit()
                print("✅ Updated existing demo user with username")
            else:
                print("✅ Demo user already exists with username")
        else:
            # Create new demo user BMI >= 30 eligibility patterns
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
            print("✅ Created new demo user with username")
        
        print("📧 Demo Login: demo@nutriassist.com / demo123")
        print(f"👤 Username: {demo_user.username}")
        print(f"📊 BMI: {demo_user.BMI} (Eligible for service)")

if __name__ == '__main__':
    # Add backend to path
    sys.path.insert(0, '/home/ahmed/Portfolio-Project/backend')
    create_demo_user()
