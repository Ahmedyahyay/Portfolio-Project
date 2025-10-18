#!/bin/bash

echo "🏥 Personal Nutrition Assistant - Starting Application"
echo "Following copilot instructions sprint-based development workflow"
echo "=============================================================="

PROJECT_ROOT="/home/ahmed/Portfolio-Project"
cd "$PROJECT_ROOT" || exit 1

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Navigate to backend
cd backend

# Set Flask environment variables
export FLASK_APP=app.py
export FLASK_ENV=development

# Apply database migrations
echo "🗄️ Applying database migrations..."
flask db upgrade

# Add sample data following copilot health-centric patterns
echo "📊 Adding sample nutrition data..."
python3 -c "
import sys
sys.path.insert(0, '.')
from app import create_app
from models import db, Meal, User
from werkzeug.security import generate_password_hash

app = create_app()
with app.app_context():
    # Add sample meals following copilot patterns
    if not Meal.query.first():
        meals = [
            Meal(name='Grilled Chicken Breast', type='lunch', calories=285, protein=35.2, carbs=0.0, fat=12.8, fiber=0.0, ingredients='Chicken breast, olive oil, herbs', allergens='None', serving_size='150g'),
            Meal(name='Greek Yogurt with Berries', type='breakfast', calories=195, protein=18.2, carbs=22.5, fat=4.8, fiber=3.2, ingredients='Greek yogurt, mixed berries', allergens='Dairy', serving_size='200g'),
            Meal(name='Quinoa Power Bowl', type='dinner', calories=378, protein=15.8, carbs=58.2, fat=8.9, fiber=6.1, ingredients='Quinoa, vegetables, olive oil', allergens='None', serving_size='250g'),
            Meal(name='Salmon with Sweet Potato', type='dinner', calories=425, protein=32.6, carbs=28.4, fat=18.2, fiber=4.8, ingredients='Salmon, sweet potato, herbs', allergens='Fish', serving_size='200g')
        ]
        for meal in meals:
            db.session.add(meal)
    
    # Add demo user following copilot BMI >= 30 eligibility
    if not User.query.filter_by(email='demo@nutriassist.com').first():
        demo_user = User(
            email='demo@nutriassist.com',
            password_hash=generate_password_hash('demo123'),
            height=175.0,
            weight=95.0,
            BMI=31.0
        )
        db.session.add(demo_user)
    
    db.session.commit()
    print('✅ Sample data added')
"

echo ""
echo "🚀 Starting Flask development server..."
echo "🌐 Application will be available at: http://127.0.0.1:5000"
echo "🎯 Target: Adults with BMI ≥ 30"
echo "📊 Following copilot instructions with 92/100 QA score target"
echo ""
echo "📧 Demo Account: demo@nutriassist.com / demo123"
echo "Press Ctrl+C to stop the server"
echo ""

# Start the Flask application
python app.py
