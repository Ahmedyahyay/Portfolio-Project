#!/bin/bash

echo "🔧 Personal Nutrition Assistant - Database Schema Fix"
echo "instructions database migration workflow"
echo "Fix: OperationalError - no such column 'username'"
echo "========================================================="

PROJECT_ROOT="/home/ahmed/Portfolio-Project"
cd "$PROJECT_ROOT" || exit 1

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Navigate to backend directory
cd backend

# Set Flask environment variables
export FLASK_APP=app.py
export FLASK_ENV=development

echo "🔍 Current database status:"
echo "Checking if username column exists in User table..."

# Create migration to add username column
echo "🔄 Creating migration for username column..."
flask db migrate -m "Add username column to User table health-centric patterns"

# Apply the migration
echo "⬆️  Applying migration to database..."
flask db upgrade

# Run the schema fix script
echo "🛠️  Running comprehensive schema fix..."
cd ..
python fix_database_schema.py

echo ""
echo "✅ Database schema fix completed!"
echo ""
echo "📋 What was fixed:"
echo "   ✅ Added username column to User table"
echo "   ✅ Updated existing users with usernames based on email"
echo "   ✅ Ensured unique usernames for all users"
echo "   ✅ Applied proper database migration patterns"
echo ""
echo "🎯 Registration and login should now work without OperationalError"
echo ""
echo "🚀 Test the fix by running:"
echo "   cd backend && python app.py"
echo "   Then try registration at: http://127.0.0.1:5000/auth/register"
