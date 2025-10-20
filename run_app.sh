#!/bin/bash

echo "🏥 Personal Nutrition Assistant - Complete Local Setup"
echo "Sprint-based development workflow"
echo "Target: Adults with BMI ≥ 30 | QA Score: 92/100"
echo "=============================================================="

PROJECT_ROOT="/home/ahmed/Portfolio-Project"
cd "$PROJECT_ROOT" || exit 1

# Step 1: Activate virtual environment
echo "📦 Step 1: Activating virtual environment..."
if [ ! -d "venv" ]; then
    echo "Creating new virtual environment..."
    python3 -m venv venv
    if [ $? -ne 0 ]; then
        echo "❌ Failed to create virtual environment"
        exit 1
    fi
    echo "✅ Virtual environment created"
fi

source venv/bin/activate
if [ $? -ne 0 ]; then
    echo "❌ Failed to activate virtual environment"
    exit 1
fi
echo "✅ Virtual environment activated"

# Install/update dependencies
echo "📥 Installing dependencies..."
pip install --upgrade pip
pip install Flask==2.2.5 Werkzeug==2.3.1 Flask-SQLAlchemy==3.0.5 Flask-Migrate==4.0.5 Flask-CORS==4.0.0 python-dotenv==1.0.0 gunicorn==21.2.0 requests==2.31.0

if [ $? -eq 0 ]; then
    echo "✅ Dependencies installed successfully"
    pip freeze > requirements.txt
else
    echo "❌ Failed to install dependencies"
    exit 1
fi

# Step 2: Navigate to backend folder
echo ""
echo "📁 Step 2: Navigating to backend folder..."
cd backend
if [ $? -ne 0 ]; then
    echo "❌ Backend folder not found"
    exit 1
fi
echo "✅ In backend directory: $(pwd)"

# Step 3: Set Flask environment variables
echo ""
echo "⚙️ Step 3: Setting Flask environment variables..."
export FLASK_APP=app.py
export FLASK_DEBUG=1
unset FLASK_ENV  # Remove deprecated variable
echo "✅ Flask environment variables set"

# Step 4: Force complete database recreation
echo ""
echo "🔄 Step 4: Complete database recreation with correct schema..."

# Remove ALL database files
for db_file in nutrition.db nutrition.db-journal nutrition.db-wal nutrition.db-shm; do
    if [ -f "$db_file" ]; then
        rm -f "$db_file"
        echo "✅ Removed $db_file"
    fi
done

# Clear Python cache to ensure fresh imports
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null
find . -type f -name "*.pyc" -delete 2>/dev/null
echo "✅ Cleared Python cache"

# Create database with COMPLETE schema including username
python3 -c "
import sys
import sqlite3
import os
sys.path.insert(0, '.')

try:
    print('Creating fresh database with complete schema...')
    
    # Create database file
    conn = sqlite3.connect('nutrition.db')
    cursor = conn.cursor()
    
    # Create user table with ALL required columns including username
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user (
            id INTEGER NOT NULL PRIMARY KEY,
            username VARCHAR(80) NOT NULL UNIQUE,
            email VARCHAR(120) NOT NULL UNIQUE,
            password_hash VARCHAR(128) NOT NULL,
            height FLOAT NOT NULL,
            weight FLOAT NOT NULL,
            BMI FLOAT,
            allergies VARCHAR(256),
            preferences VARCHAR(256),
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Create meal table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS meal (
            id INTEGER NOT NULL PRIMARY KEY,
            name VARCHAR(200) NOT NULL,
            type VARCHAR(50) NOT NULL,
            calories INTEGER NOT NULL,
            protein FLOAT,
            carbs FLOAT,
            fat FLOAT,
            fiber FLOAT,
            sugar FLOAT,
            sodium FLOAT,
            ingredients TEXT,
            allergens VARCHAR(256),
            usda_id VARCHAR(50),
            serving_size VARCHAR(100),
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Create meal_history table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS meal_history (
            id INTEGER NOT NULL PRIMARY KEY,
            user_id INTEGER NOT NULL,
            meal_id INTEGER NOT NULL,
            date DATETIME DEFAULT CURRENT_TIMESTAMP,
            portion_size FLOAT DEFAULT 1.0,
            FOREIGN KEY (user_id) REFERENCES user(id),
            FOREIGN KEY (meal_id) REFERENCES meal(id)
        )
    ''')
    
    # Create nutrition_goal table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS nutrition_goal (
            id INTEGER NOT NULL PRIMARY KEY,
            user_id INTEGER NOT NULL,
            daily_calories INTEGER NOT NULL,
            daily_protein FLOAT,
            daily_carbs FLOAT,
            daily_fat FLOAT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES user(id)
        )
    ''')
    
    # Create user_profile table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_profile (
            id INTEGER NOT NULL PRIMARY KEY,
            user_id INTEGER NOT NULL UNIQUE,
            activity_level VARCHAR(50) DEFAULT 'sedentary',
            weight_goal VARCHAR(50) DEFAULT 'maintain',
            target_weight FLOAT,
            weekly_goal FLOAT DEFAULT 0.5,
            notification_preferences TEXT,
            privacy_settings TEXT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES user(id)
        )
    ''')
    
    # Create meal_rating table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS meal_rating (
            id INTEGER NOT NULL PRIMARY KEY,
            user_id INTEGER NOT NULL,
            meal_id INTEGER NOT NULL,
            rating INTEGER NOT NULL,
            review TEXT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES user(id),
            FOREIGN KEY (meal_id) REFERENCES meal(id),
            UNIQUE(user_id, meal_id)
        )
    ''')
    
    # Create food_category table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS food_category (
            id INTEGER NOT NULL PRIMARY KEY,
            name VARCHAR(100) NOT NULL UNIQUE,
            description TEXT,
            color_code VARCHAR(7) DEFAULT '#4CAF50',
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Create meal_categories junction table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS meal_categories (
            meal_id INTEGER NOT NULL,
            category_id INTEGER NOT NULL,
            PRIMARY KEY (meal_id, category_id),
            FOREIGN KEY (meal_id) REFERENCES meal(id),
            FOREIGN KEY (category_id) REFERENCES food_category(id)
        )
    ''')
    
    # Create essential indexes
    cursor.execute('CREATE INDEX IF NOT EXISTS ix_user_email ON user(email)')
    cursor.execute('CREATE INDEX IF NOT EXISTS ix_user_username ON user(username)')
    cursor.execute('CREATE INDEX IF NOT EXISTS ix_user_bmi ON user(BMI)')
    cursor.execute('CREATE INDEX IF NOT EXISTS ix_meal_type ON meal(type)')
    cursor.execute('CREATE INDEX IF NOT EXISTS ix_meal_calories ON meal(calories)')
    cursor.execute('CREATE INDEX IF NOT EXISTS ix_meal_protein ON meal(protein)')
    
    conn.commit()
    
    # Verify the schema
    cursor.execute('PRAGMA table_info(user)')
    columns = cursor.fetchall()
    column_names = [col[1] for col in columns]
    print(f'✅ User table created with columns: {column_names}')
    
    if 'username' not in column_names:
        print('❌ Username column STILL missing - this should not happen!')
        sys.exit(1)
    
    cursor.execute('SELECT name FROM sqlite_master WHERE type=\"table\"')
    tables = [row[0] for row in cursor.fetchall()]
    print(f'✅ All tables created: {tables}')
    
    conn.close()
    print('✅ Database created successfully with username column')
    
except Exception as e:
    print(f'❌ Database creation failed: {e}')
    import traceback
    traceback.print_exc()
    sys.exit(1)
"

if [ $? -ne 0 ]; then
    echo "❌ Failed to create database"
    exit 1
fi

# Step 5: Add sample data using the new database
echo ""
echo "📊 Step 5: Adding sample data to fresh database..."
python3 -c "
import sys
sys.path.insert(0, '.')

# Clear any cached modules first
for module_name in list(sys.modules.keys()):
    if any(x in module_name.lower() for x in ['models', 'app']):
        if module_name in sys.modules:
            del sys.modules[module_name]

try:
    from app import create_app
    from models import db, Meal, User, FoodCategory
    from werkzeug.security import generate_password_hash
    
    app = create_app()
    with app.app_context():
        # Test the database connection first
        from sqlalchemy import text
        result = db.session.execute(text('SELECT COUNT(*) FROM user')).scalar()
        print(f'✅ Database connection test successful - user count: {result}')
        
        # Check if demo user exists
        demo_user = User.query.filter_by(email='demo@nutriassist.com').first()
        if not demo_user:
            print('Creating demo user with BMI >= 30...')
            demo_user = User(
                username='demo_user',
                email='demo@nutriassist.com',
                password_hash=generate_password_hash('demo123'),
                height=175.0,
                weight=95.0,
                allergies='None',
                preferences='High protein, low sodium, weight management focused'
            )
            demo_user.calculate_bmi()
            db.session.add(demo_user)
            print(f'✅ Demo user created: BMI {demo_user.BMI} (Eligible: {demo_user.is_eligible_for_service()})')
        else:
            print('✅ Demo user already exists')
        
        # Add sample meals
        if Meal.query.count() == 0:
            print('Adding sample meals optimized for BMI ≥ 30...')
            meals = [
                Meal(
                    name='Greek Yogurt with Mixed Berries',
                    type='breakfast',
                    calories=195,
                    protein=18.2,
                    carbs=22.5,
                    fat=4.8,
                    fiber=3.2,
                    sugar=18.0,
                    sodium=85.0,
                    ingredients='Plain Greek yogurt, strawberries, blueberries, raspberries',
                    allergens='Dairy',
                    usda_id='170900',
                    serving_size='200g'
                ),
                Meal(
                    name='Grilled Chicken Breast',
                    type='lunch',
                    calories=285,
                    protein=35.2,
                    carbs=0.0,
                    fat=12.8,
                    fiber=0.0,
                    sugar=0.0,
                    sodium=140.0,
                    ingredients='Boneless skinless chicken breast, olive oil, herbs, black pepper',
                    allergens='None',
                    usda_id='171077',
                    serving_size='150g'
                ),
                Meal(
                    name='Quinoa Power Bowl with Vegetables',
                    type='dinner',
                    calories=378,
                    protein=15.8,
                    carbs=58.2,
                    fat=8.9,
                    fiber=6.1,
                    sugar=4.2,
                    sodium=245.0,
                    ingredients='Quinoa, broccoli, bell peppers, carrots, olive oil, lemon juice',
                    allergens='None',
                    usda_id='168917',
                    serving_size='250g'
                )
            ]
            
            for meal in meals:
                db.session.add(meal)
            print(f'✅ Added {len(meals)} sample meals')
        else:
            print('✅ Sample meals already exist')
        
        # Commit all changes
        db.session.commit()
        
        # Final verification
        user_count = User.query.count()
        meal_count = Meal.query.count()
        print(f'✅ Sample data added - Users: {user_count}, Meals: {meal_count}')
        
except Exception as e:
    print(f'❌ Error adding sample data: {e}')
    import traceback
    traceback.print_exc()
    sys.exit(1)
"

if [ $? -ne 0 ]; then
    echo "❌ Failed to add sample data"
    exit 1
fi

# Step 6: Start Flask development server
echo ""
echo "🎉 Setup completed successfully!"
echo "================================================================"
echo "📋 Personal Nutrition Assistant - Ready to Launch"
echo "🎯 Target Audience: Adults with BMI ≥ 30"
echo ""
echo "📧 Demo Account Credentials:"
echo "   Email: demo@nutriassist.com"
echo "   Password: demo123"
echo "   BMI: ~31.0 (Eligible for service)"
echo ""
echo "🌐 Starting Flask development server..."
echo "   URL: http://127.0.0.1:5000"
echo ""
echo "Press Ctrl+C to stop the server"
echo "================================================================"

# Start the Flask application
python app.py
