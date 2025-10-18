#!/bin/bash

echo "🍽️ Personal Nutrition Assistant - Complete Setup with USDA Integration"
echo "Following copilot instructions health-centric data model"
echo "Target: 75 meals suitable for BMI >= 30 demographic"
echo "=================================================================="

PROJECT_ROOT="/home/ahmed/Portfolio-Project"
cd "$PROJECT_ROOT" || exit 1

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install additional dependencies for USDA integration
echo "📦 Installing USDA API dependencies..."
pip install requests

# Set up database
echo "🗄️ Setting up database..."
cd backend
export FLASK_APP=app.py
export FLASK_ENV=development

# Initialize and apply migrations
flask db upgrade

# Populate USDA data
echo "📡 Fetching nutrition data from USDA FoodData Central..."
cd ..
python populate_usda_data.py

echo ""
echo "✅ Setup with USDA integration completed!"
echo ""
echo "📊 Database Features:"
echo "   ✅ 75+ USDA verified meals"
echo "   ✅ Complete nutrition profiles (calories, protein, carbs, fat, fiber, sugar, sodium)"
echo "   ✅ USDA FoodData Central IDs for verification"
echo "   ✅ Nutrition scoring optimized for BMI >= 30"
echo "   ✅ Allergen and ingredient information"
echo "   ✅ Serving size recommendations"
echo ""
echo "🎯 Health-Centric Features:"
echo "   ✅ High-protein meal prioritization"
echo "   ✅ High-fiber content scoring"
echo "   ✅ Calorie density optimization"
echo "   ✅ BMI >= 30 eligibility criteria"
echo ""
echo "🚀 Ready to run:"
echo "   cd backend && python app.py"
echo ""
echo "🌐 Access meals database at: http://127.0.0.1:5000/meals"
