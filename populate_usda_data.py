#!/usr/bin/env python3
"""
USDA data population script following copilot health-centric patterns
"""

import os
import sys
import logging
from flask import Flask
from backend.models import db
from backend.usda_api import populate_usda_meals

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def create_app():
    """Create Flask app for USDA data population"""
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'dev-secret-for-data-population'
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///nutrition.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    db.init_app(app)
    return app

def main():
    """Main function to populate USDA nutrition data"""
    print("🍽️ Personal Nutrition Assistant - USDA Data Population")
    print("Following copilot instructions health-centric data model")
    print("Target: 75 meals suitable for BMI >= 30 demographic")
    print("=" * 65)
    
    # Change to project directory
    project_root = '/home/ahmed/Portfolio-Project'
    if os.path.exists(project_root):
        os.chdir(project_root)
    
    # Add backend to Python path
    sys.path.insert(0, os.path.join(os.getcwd(), 'backend'))
    
    # Create Flask app and populate data
    app = create_app()
    
    with app.app_context():
        try:
            # Ensure database tables exist
            db.create_all()
            
            # Populate USDA meals
            meal_count = populate_usda_meals(target_count=75)
            
            print(f"\n✅ Database population completed!")
            print(f"📊 Total meals in database: {meal_count}")
            print(f"🎯 Optimized for BMI >= 30 demographic")
            print(f"🔗 USDA FoodData Central integration active")
            
        except Exception as e:
            logger.error(f"❌ Population failed: {e}")
            sys.exit(1)

if __name__ == '__main__':
    main()
