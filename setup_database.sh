#!/bin/bash

echo "🗄️ Personal Nutrition Assistant - Database Migration Setup"
echo "Following copilot instructions database migration workflow"
echo "=========================================================="

PROJECT_ROOT="/home/ahmed/Portfolio-Project"
cd "$PROJECT_ROOT" || exit 1

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install Flask-Migrate if not already installed
echo "📦 Ensuring Flask-Migrate is installed..."
pip install Flask-Migrate==4.0.5

# Set environment variables
export FLASK_APP=backend/app.py
export FLASK_ENV=development

# Navigate to backend directory for migrations
cd backend

# Initialize Flask-Migrate (creates migrations directory)
echo "📁 Initializing Flask-Migrate..."
if [ ! -d "migrations" ]; then
    flask db init
    echo "✅ Flask-Migrate initialized"
else
    echo "ℹ️  Migrations directory already exists"
fi

# Create initial migration with all models
echo "🔄 Creating initial migration..."
flask db migrate -m "Initial migration with health-centric data model following copilot patterns - User, Meal, MealHistory, NutritionGoal, UserProfile, MealRating, FoodCategory models"

# Apply the migration
echo "⬆️  Applying database migration..."
flask db upgrade

# Run the database initialization script
echo "📊 Running database initialization with sample data..."
cd ..
python init_database.py

echo ""
echo "✅ Database setup completed successfully!"
echo ""
echo "📋 Database Structure:"
echo "   ├── user              # User authentication and BMI data"
echo "   ├── meal              # Nutrition database with USDA integration"
echo "   ├── meal_history      # Junction table for user meal tracking"
echo "   ├── nutrition_goal    # Personalized nutrition targets"
echo "   ├── user_profile      # Extended user preferences and settings"
echo "   ├── meal_rating       # User feedback and meal reviews"
echo "   ├── food_category     # Meal categorization and tagging"
echo "   └── meal_categories   # Junction table for meal-category relationships"
echo ""
echo "🎯 Health-Centric Features:"
echo "   ✅ BMI ≥ 30 eligibility enforcement"
echo "   ✅ Nutrition scoring for weight management"
echo "   ✅ USDA FoodData Central integration ready"
echo "   ✅ Complete macro and micronutrient tracking"
echo "   ✅ User preference and allergy management"
echo ""
echo "📧 Demo Account Created:"
echo "   Email: demo@nutriassist.com"
echo "   Password: demo123"
echo "   BMI: 31.0 (Eligible for service)"
echo ""
echo "🚀 Ready to run the application with:"
echo "   cd backend && python app.py"
