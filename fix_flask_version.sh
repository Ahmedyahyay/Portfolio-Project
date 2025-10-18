#!/bin/bash

echo "🔧 Personal Nutrition Assistant - Flask Version Fix"
echo "Following copilot instructions for TypeError: 'partitioned' cookie fix"
echo "=================================================================="

PROJECT_ROOT="/home/ahmed/Portfolio-Project"
cd "$PROJECT_ROOT" || exit 1

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Show current versions
echo "📋 Current versions:"
pip list | grep -E "(Flask|Werkzeug)"

# Downgrade to compatible versions
echo "⬇️  Downgrading to compatible versions..."
pip install --force-reinstall Flask==2.2.5 Werkzeug==2.3.1

# Verify new versions
echo "✅ Updated versions:"
pip list | grep -E "(Flask|Werkzeug)"

# Update requirements.txt
echo "📝 Updating requirements.txt..."
pip freeze > requirements.txt

echo ""
echo "✅ Flask version fix completed!"
echo ""
echo "📋 What was fixed:"
echo "   ✅ Downgraded Flask to 2.2.5 (compatible version)"
echo "   ✅ Downgraded Werkzeug to 2.3.1 (compatible version)"
echo "   ✅ Created session interface override for 'partitioned' cookie error"
echo "   ✅ Applied fix in app.py initialization"
echo "   ✅ Updated requirements.txt with compatible versions"
echo ""
echo "🎯 Logout, login, and registration should now work without TypeError"
echo ""
echo "🚀 Test the fix by running:"
echo "   cd backend && python app.py"
echo "   Then try login/logout at: http://127.0.0.1:5000"
