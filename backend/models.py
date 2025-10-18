from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    height = db.Column(db.Float, nullable=False)
    weight = db.Column(db.Float, nullable=False)
    BMI = db.Column(db.Float, nullable=True)
    allergies = db.Column(db.String(256), nullable=True)
    preferences = db.Column(db.String(256), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    meal_history = db.relationship('MealHistory', backref='user', lazy=True)

    def calculate_bmi(self):
        """Calculate BMI following copilot health-centric data model"""
        if self.height and self.weight:
            # Critical: height in cm, convert to meters for BMI calculation
            height_m = self.height / 100
            self.BMI = round(self.weight / (height_m ** 2), 2)
        return self.BMI

    def is_eligible_for_service(self):
        """Check BMI eligibility following copilot business rules"""
        return self.BMI and self.BMI >= 30.0

    def get_bmi_category(self):
        """Get BMI category following health-centric patterns"""
        if not self.BMI:
            return 'Unknown'
        if self.BMI < 18.5:
            return 'Underweight'
        elif self.BMI < 25:
            return 'Normal weight'
        elif self.BMI < 30:
            return 'Overweight'
        elif self.BMI < 35:
            return 'Class I Obesity'
        elif self.BMI < 40:
            return 'Class II Obesity'
        else:
            return 'Class III Obesity'

    def __repr__(self):
        return f'<User {self.username}>'

class Meal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    type = db.Column(db.String(50), nullable=False)  # breakfast/lunch/dinner/snack
    calories = db.Column(db.Integer, nullable=False)
    protein = db.Column(db.Float, nullable=True)  # grams
    carbs = db.Column(db.Float, nullable=True)    # grams
    fat = db.Column(db.Float, nullable=True)      # grams
    fiber = db.Column(db.Float, nullable=True)    # grams
    sugar = db.Column(db.Float, nullable=True)    # grams
    sodium = db.Column(db.Float, nullable=True)   # mg
    ingredients = db.Column(db.Text, nullable=True)
    allergens = db.Column(db.String(256), nullable=True)
    usda_id = db.Column(db.String(50), nullable=True)  # USDA FoodData Central ID
    serving_size = db.Column(db.String(100), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    meal_history = db.relationship('MealHistory', backref='meal', lazy=True)

    def calculate_nutrition_score(self):
        """Calculate nutrition score for meal recommendations following health-centric model"""
        score = 0
        
        # Protein scoring (higher is better for weight management)
        if self.protein:
            score += min(self.protein / 30 * 20, 20)  # Max 20 points for 30g+ protein
        
        # Fiber scoring (higher is better)
        if self.fiber:
            score += min(self.fiber / 10 * 15, 15)  # Max 15 points for 10g+ fiber
        
        # Calorie density scoring (lower density is better)
        if self.calories <= 200:
            score += 15
        elif self.calories <= 400:
            score += 10
        else:
            score += 5
        
        return min(score, 50)  # Max score of 50

    def meets_eligibility_criteria(self, user_bmi):
        """Check if meal meets criteria for BMI >= 30 demographic following copilot business rules"""
        if user_bmi < 30:
            return False
        
        criteria_met = 0
        total_criteria = 4
        
        # 1. Reasonable calorie count (not too high for weight management)
        if self.calories <= 400:
            criteria_met += 1
        
        # 2. Adequate protein (muscle preservation during weight loss)
        if (self.protein or 0) >= 15:
            criteria_met += 1
        
        # 3. Good fiber content (satiety and digestive health)
        if (self.fiber or 0) >= 3:
            criteria_met += 1
        
        # 4. Not too high in sugar (blood sugar management for obese adults)
        if (self.sugar or 0) <= 15:
            criteria_met += 1
        
        # Must meet at least 75% of criteria following copilot health-centric patterns
        return criteria_met >= (total_criteria * 0.75)

    def to_dict(self):
        """Convert meal to dictionary for API responses following copilot patterns"""
        return {
            'id': self.id,
            'name': self.name,
            'type': self.type,
            'calories': self.calories,
            'protein': self.protein,
            'carbs': self.carbs,
            'fat': self.fat,
            'fiber': self.fiber,
            'sugar': self.sugar,
            'sodium': self.sodium,
            'ingredients': self.ingredients,
            'allergens': self.allergens,
            'usda_id': self.usda_id,
            'serving_size': self.serving_size,
            'nutrition_score': self.calculate_nutrition_score(),
            'eligible_for_bmi_30': self.meets_eligibility_criteria(30.0)
        }

    def __repr__(self):
        return f'<Meal {self.name}>'

class MealHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    meal_id = db.Column(db.Integer, db.ForeignKey('meal.id'), nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    portion_size = db.Column(db.Float, default=1.0)  # multiplier for serving

    def calculate_adjusted_nutrition(self):
        """Calculate nutrition based on portion size following copilot health-centric model"""
        if not self.meal:
            return {}
        
        multiplier = self.portion_size or 1.0
        
        return {
            'calories': round((self.meal.calories or 0) * multiplier),
            'protein': round((self.meal.protein or 0) * multiplier, 1),
            'carbs': round((self.meal.carbs or 0) * multiplier, 1),
            'fat': round((self.meal.fat or 0) * multiplier, 1),
            'fiber': round((self.meal.fiber or 0) * multiplier, 1)
        }

    def __repr__(self):
        return f'<MealHistory User:{self.user_id} Meal:{self.meal_id}>'

class NutritionGoal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    daily_calories = db.Column(db.Integer, nullable=False)
    daily_protein = db.Column(db.Float, nullable=True)
    daily_carbs = db.Column(db.Float, nullable=True)
    daily_fat = db.Column(db.Float, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user = db.relationship('User', backref=db.backref('nutrition_goals', lazy=True))

    def __repr__(self):
        return f'<NutritionGoal User:{self.user_id} Calories:{self.daily_calories}>'

# Additional model for user preferences and settings
class UserProfile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False, unique=True)
    activity_level = db.Column(db.String(50), default='sedentary')  # sedentary/light/moderate/active
    weight_goal = db.Column(db.String(50), default='maintain')      # lose/maintain/gain
    target_weight = db.Column(db.Float, nullable=True)
    weekly_goal = db.Column(db.Float, default=0.5)  # kg per week
    notification_preferences = db.Column(db.JSON, nullable=True)
    privacy_settings = db.Column(db.JSON, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    user = db.relationship('User', backref=db.backref('profile', uselist=False))

    def __repr__(self):
        return f'<UserProfile User:{self.user_id}>'

# Model for meal ratings and reviews
class MealRating(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    meal_id = db.Column(db.Integer, db.ForeignKey('meal.id'), nullable=False)
    rating = db.Column(db.Integer, nullable=False)  # 1-5 stars
    review = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    user = db.relationship('User', backref='meal_ratings')
    meal = db.relationship('Meal', backref='ratings')
    
    # Unique constraint to prevent duplicate ratings from same user
    __table_args__ = (db.UniqueConstraint('user_id', 'meal_id', name='unique_user_meal_rating'),)

    def __repr__(self):
        return f'<MealRating User:{self.user_id} Meal:{self.meal_id} Rating:{self.rating}>'

# Model for food categories/tags
class FoodCategory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.Text, nullable=True)
    color_code = db.Column(db.String(7), default='#4CAF50')  # Hex color for UI
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<FoodCategory {self.name}>'

# Junction table for meal-category relationships
meal_categories = db.Table('meal_categories',
    db.Column('meal_id', db.Integer, db.ForeignKey('meal.id'), primary_key=True),
    db.Column('category_id', db.Integer, db.ForeignKey('food_category.id'), primary_key=True)
)

# Add relationship to Meal model for categories
Meal.categories = db.relationship('FoodCategory', secondary=meal_categories, lazy='subquery',
                                 backref=db.backref('meals', lazy=True))
