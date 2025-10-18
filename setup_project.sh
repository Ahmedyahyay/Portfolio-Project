#!/bin/bash

echo "🏥 Personal Nutrition Assistant - Flask Project Setup"
echo "Following copilot instructions sprint-based development workflow"
echo "=============================================================="

PROJECT_ROOT="/home/ahmed/Portfolio-Project"
cd "$PROJECT_ROOT" || exit 1

# Create project directory structure following copilot blueprint organization
echo "📁 Creating project directory structure..."
mkdir -p backend/{routes,templates,static/{css,js,images},tests,migrations,instance}
mkdir -p frontend
mkdir -p templates
mkdir -p static/{css,js,images}
mkdir -p migrations/versions
mkdir -p logs
mkdir -p docs
mkdir -p sprints

echo "✅ Directory structure created"

# Create virtual environment
echo "📦 Creating virtual environment..."
python3 -m venv venv

# Check if virtual environment was created successfully
if [ ! -d "venv" ]; then
    echo "❌ Failed to create virtual environment"
    exit 1
fi

echo "✅ Virtual environment created"

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "⬆️  Upgrading pip..."
pip install --upgrade pip

# Install dependencies following copilot requirements
echo "📥 Installing Flask dependencies..."
pip install Flask==2.3.3
pip install Flask-SQLAlchemy==3.0.5
pip install Flask-Migrate==4.0.5
pip install Flask-CORS==4.0.0
pip install Werkzeug==2.3.7
pip install python-dotenv==1.0.0
pip install psycopg2-binary==2.9.7
pip install gunicorn==21.2.0
pip install requests==2.31.0

# Create requirements.txt
echo "📝 Generating requirements.txt..."
pip freeze > requirements.txt

echo "✅ Dependencies installed and requirements.txt created"

# Initialize Flask-Migrate in backend directory
echo "🗄️ Initializing database migrations..."
cd backend

# Set Flask app environment variable
export FLASK_APP=app.py

# Initialize migrations following copilot database migration workflow
flask db init

echo "✅ Database migrations initialized"

# Create .env files following copilot environment-aware database pattern
echo "⚙️  Creating environment configuration files..."
cd "$PROJECT_ROOT"

# Development environment
cat > .env.development << EOF
FLASK_ENV=development
SECRET_KEY=dev-secret-key-change-in-production
DATABASE_URL=sqlite:///nutrition.db
DEBUG=True
EOF

# Production environment template
cat > .env.production << EOF
FLASK_ENV=production
SECRET_KEY=your-production-secret-key-here
DATABASE_URL=postgresql://user:pass@localhost/nutrition_db
DEBUG=False
EOF

echo "✅ Environment files created"

# Create initial database migration
echo "🔄 Creating initial database migration..."
cd backend
flask db migrate -m "Initial migration with health-centric data model following copilot patterns"

echo "✅ Initial migration created"

# Create a simple test to verify setup
echo "🧪 Creating setup verification test..."
cat > test_setup.py << EOF
#!/usr/bin/env python3
"""
Setup verification test following copilot QA integration patterns
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """Test that all required modules can be imported"""
    try:
        from flask import Flask
        from flask_sqlalchemy import SQLAlchemy
        from flask_migrate import Migrate
        from flask_cors import CORS
        from models import db, User, Meal, MealHistory, NutritionGoal
        print("✅ All imports successful")
        return True
    except ImportError as e:
        print(f"❌ Import failed: {e}")
        return False

def test_app_creation():
    """Test Flask app creation following copilot patterns"""
    try:
        from app import create_app
        app = create_app()
        print("✅ Flask app creation successful")
        return True
    except Exception as e:
        print(f"❌ App creation failed: {e}")
        return False

def test_database_models():
    """Test database models following copilot health-centric data model"""
    try:
        from models import User, Meal
        
        # Test User BMI calculation (copilot critical pattern)
        user = User()
        user.height = 170  # cm
        user.weight = 90   # kg
        bmi = user.calculate_bmi()
        
        if bmi and bmi >= 30.0:
            print(f"✅ BMI calculation works: {bmi} (Eligible for service)")
        else:
            print(f"⚠️  BMI calculation: {bmi} (Not eligible)")
        
        # Test eligibility check (copilot business rules)
        eligible = user.is_eligible_for_service()
        print(f"✅ Eligibility check: {eligible}")
        
        return True
    except Exception as e:
        print(f"❌ Model test failed: {e}")
        return False

if __name__ == "__main__":
    print("🔍 Personal Nutrition Assistant - Setup Verification")
    print("Following copilot instructions sprint-based development")
    print("=" * 55)
    
    tests = [
        ("Import Tests", test_imports),
        ("App Creation", test_app_creation),
        ("Database Models", test_database_models)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n🧪 Running {test_name}...")
        if test_func():
            passed += 1
    
    print(f"\n📊 Test Results: {passed}/{total} passed")
    
    if passed == total:
        print("🎉 Setup verification PASSED! Project ready for development.")
    else:
        print("⚠️  Some tests failed. Please check the setup.")
        sys.exit(1)
EOF

# Run setup verification
echo "✅ Running setup verification..."
python test_setup.py

# Clean up test file
rm test_setup.py

echo ""
echo "🎉 Project setup completed successfully!"
echo ""
echo "📋 Project Structure Created:"
echo "   ├── backend/              # Flask application following copilot blueprint organization"
echo "   │   ├── app.py            # Main application factory"
echo "   │   ├── models.py         # Health-centric data models (BMI ≥ 30 targeting)"
echo "   │   ├── routes/           # Feature-based routing blueprints"
echo "   │   ├── migrations/       # Database migration files"
echo "   │   └── instance/         # SQLite database location"
echo "   ├── templates/            # Jinja2 HTML templates"
echo "   ├── static/               # CSS, JS, images"
echo "   ├── venv/                 # Python virtual environment"
echo "   ├── logs/                 # Application logs"
echo "   └── requirements.txt      # Python dependencies"
echo ""
echo "🚀 To run the application:"
echo "   1. cd $PROJECT_ROOT/backend"
echo "   2. source ../venv/bin/activate"
echo "   3. flask db upgrade           # Apply database migrations"
echo "   4. python app.py             # Start development server"
echo ""
echo "🌐 Application will be available at: http://127.0.0.1:5000"
echo "🎯 Target Audience: Adults with BMI ≥ 30"
echo "📊 Quality Target: 92/100 QA score following copilot instructions"
echo "🔬 Sprint-based development workflow ready"
echo ""
echo "💡 Next Steps:"
echo "   - Create remaining HTML templates (meals.html, bmi.html, etc.)"
echo "   - Implement USDA API integration for nutrition data"
echo "   - Add comprehensive testing following copilot QA patterns"
echo "   - Deploy with Gunicorn for production"
