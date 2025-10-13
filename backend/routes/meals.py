from flask import Blueprint, request, jsonify
from models import db, Meal, User, MealHistory
from sqlalchemy import or_, and_

meals_bp = Blueprint('meals', __name__)

# USDA-based meal data - Sample realistic meals for MVP
USDA_MEALS_DATA = [
    {
        "name": "Grilled Chicken Breast with Vegetables",
        "type": "lunch",
        "calories": 285,
        "protein": 35.2,
        "carbs": 8.1,
        "fat": 12.3,
        "fiber": 3.2,
        "sugar": 4.1,
        "sodium": 89.2,
        "ingredients": "Chicken breast, broccoli, carrots, olive oil, garlic, herbs",
        "allergens": "None",
        "usda_id": "05064",
        "serving_size": "150g chicken + 200g vegetables"
    },
    {
        "name": "Quinoa Bowl with Black Beans",
        "type": "dinner",
        "calories": 378,
        "protein": 15.8,
        "carbs": 58.2,
        "fat": 9.4,
        "fiber": 12.1,
        "sugar": 3.8,
        "sodium": 245.6,
        "ingredients": "Quinoa, black beans, bell peppers, onions, lime, cilantro",
        "allergens": "None",
        "usda_id": "20035",
        "serving_size": "1 cup (250g)"
    },
    {
        "name": "Greek Yogurt with Berries and Nuts",
        "type": "breakfast",
        "calories": 195,
        "protein": 18.2,
        "carbs": 22.1,
        "fat": 6.8,
        "fiber": 4.2,
        "sugar": 16.3,
        "sodium": 67.4,
        "ingredients": "Plain Greek yogurt, mixed berries, almonds, walnuts",
        "allergens": "Tree nuts, Dairy",
        "usda_id": "01256",
        "serving_size": "150g yogurt + 50g berries + 15g nuts"
    },
    {
        "name": "Salmon with Sweet Potato",
        "type": "dinner",
        "calories": 425,
        "protein": 32.6,
        "carbs": 35.4,
        "fat": 18.7,
        "fiber": 5.8,
        "sugar": 7.2,
        "sodium": 198.3,
        "ingredients": "Atlantic salmon, sweet potato, asparagus, lemon, dill",
        "allergens": "Fish",
        "usda_id": "15236",
        "serving_size": "120g salmon + 200g sweet potato"
    },
    {
        "name": "Vegetable Stir-Fry with Brown Rice",
        "type": "lunch",
        "calories": 312,
        "protein": 9.8,
        "carbs": 54.6,
        "fat": 8.1,
        "fiber": 6.4,
        "sugar": 12.3,
        "sodium": 156.7,
        "ingredients": "Brown rice, broccoli, snap peas, carrots, soy sauce, ginger",
        "allergens": "Soy",
        "usda_id": "20040",
        "serving_size": "300g total"
    },
    {
        "name": "Turkey and Avocado Wrap",
        "type": "lunch",
        "calories": 298,
        "protein": 28.4,
        "carbs": 25.7,
        "fat": 11.9,
        "fiber": 8.2,
        "sugar": 3.1,
        "sodium": 487.2,
        "ingredients": "Whole wheat tortilla, turkey breast, avocado, lettuce, tomato",
        "allergens": "Gluten",
        "usda_id": "05165",
        "serving_size": "1 wrap (250g)"
    },
    {
        "name": "Oatmeal with Banana and Cinnamon",
        "type": "breakfast",
        "calories": 268,
        "protein": 8.1,
        "carbs": 48.3,
        "fat": 6.2,
        "fiber": 7.8,
        "sugar": 14.6,
        "sodium": 12.4,
        "ingredients": "Rolled oats, banana, cinnamon, milk, honey",
        "allergens": "Dairy",
        "usda_id": "20028",
        "serving_size": "1 cup (240g)"
    },
    {
        "name": "Mixed Green Salad with Chicken",
        "type": "dinner",
        "calories": 245,
        "protein": 26.8,
        "carbs": 12.4,
        "fat": 10.6,
        "fiber": 4.8,
        "sugar": 8.2,
        "sodium": 234.1,
        "ingredients": "Mixed greens, grilled chicken, cherry tomatoes, cucumber, olive oil vinaigrette",
        "allergens": "None",
        "usda_id": "05062",
        "serving_size": "Large bowl (300g)"
    }
]

@meals_bp.route('/search', methods=['POST'])
def search_meals():
    """Search meals based on query, type, and nutritional criteria"""
    data = request.get_json()
    query = data.get('query', '').lower()
    meal_type = data.get('meal_type', '')
    max_calories = data.get('max_calories')
    
    # Initialize meals database if empty
    if Meal.query.count() == 0:
        populate_meals_database()
    
    # Build query
    search_query = Meal.query
    
    # Filter by meal type
    if meal_type:
        search_query = search_query.filter(Meal.type == meal_type)
    
    # Filter by calories
    if max_calories:
        try:
            max_cal = int(max_calories)
            search_query = search_query.filter(Meal.calories <= max_cal)
        except ValueError:
            pass
    
    # Search in name and ingredients
    if query:
        search_query = search_query.filter(
            or_(
                Meal.name.contains(query),
                Meal.ingredients.contains(query)
            )
        )
    
    meals = search_query.limit(20).all()
    
    meals_data = []
    for meal in meals:
        meals_data.append({
            'id': meal.id,
            'name': meal.name,
            'type': meal.type,
            'calories': meal.calories,
            'protein': meal.protein,
            'carbs': meal.carbs,
            'fat': meal.fat,
            'fiber': meal.fiber,
            'ingredients': meal.ingredients,
            'allergens': meal.allergens,
            'serving_size': meal.serving_size,
            'usda_id': meal.usda_id
        })
    
    return jsonify({
        'meals': meals_data,
        'count': len(meals_data),
        'query': query
    }), 200

@meals_bp.route('/recommendations', methods=['POST'])
def get_recommendations():
    """Get personalized meal recommendations based on user profile"""
    data = request.get_json()
    user_id = data.get('user_id')
    
    if not user_id:
        return jsonify({'error': 'User ID required'}), 400
    
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    # Calculate daily calorie needs based on BMI and weight loss goals
    bmr = calculate_bmr(user.weight, user.height, 35)  # Assuming average age 35
    daily_calories = int(bmr * 1.4)  # Sedentary activity level with deficit
    
    # Get meals that fit calorie goals
    breakfast_cals = int(daily_calories * 0.25)
    lunch_cals = int(daily_calories * 0.35)
    dinner_cals = int(daily_calories * 0.30)
    snack_cals = int(daily_calories * 0.10)
    
    recommendations = {
        'daily_calorie_goal': daily_calories,
        'meal_plan': {
            'breakfast': get_meal_by_criteria('breakfast', breakfast_cals, user.allergies),
            'lunch': get_meal_by_criteria('lunch', lunch_cals, user.allergies),
            'dinner': get_meal_by_criteria('dinner', dinner_cals, user.allergies),
            'snack': get_meal_by_criteria('snack', snack_cals, user.allergies)
        },
        'user_bmi': user.BMI,
        'nutrition_tips': get_nutrition_tips(user.BMI)
    }
    
    return jsonify(recommendations), 200

def calculate_bmr(weight, height, age):
    """Calculate Basal Metabolic Rate using Mifflin-St Jeor equation"""
    # For males (simplified for MVP)
    return (10 * weight) + (6.25 * height) - (5 * age) + 5

def get_meal_by_criteria(meal_type, target_calories, allergies):
    """Get meal recommendation based on criteria"""
    if Meal.query.count() == 0:
        populate_meals_database()
    
    query = Meal.query.filter(Meal.type == meal_type)
    query = query.filter(Meal.calories <= target_calories + 50)
    query = query.filter(Meal.calories >= target_calories - 100)
    
    # Filter out allergens if specified
    if allergies:
        allergy_list = [allergy.strip().lower() for allergy in allergies.split(',')]
        for allergy in allergy_list:
            if allergy:
                query = query.filter(~Meal.allergens.contains(allergy))
    
    meal = query.first()
    if meal:
        return {
            'id': meal.id,
            'name': meal.name,
            'calories': meal.calories,
            'protein': meal.protein,
            'carbs': meal.carbs,
            'fat': meal.fat,
            'ingredients': meal.ingredients,
            'serving_size': meal.serving_size
        }
    return None

def get_nutrition_tips(bmi):
    """Get personalized nutrition tips based on BMI"""
    tips = []
    
    if bmi >= 35:
        tips.extend([
            "Focus on portion control - use smaller plates",
            "Increase vegetable intake to 50% of each meal",
            "Limit processed foods and added sugars"
        ])
    elif bmi >= 30:
        tips.extend([
            "Aim for 150 minutes of moderate activity per week",
            "Include lean protein in every meal",
            "Stay hydrated with 8-10 glasses of water daily"
        ])
    
    tips.extend([
        "Eat slowly and mindfully",
        "Plan meals ahead to avoid impulsive choices",
        "Consider consulting with a registered dietitian"
    ])
    
    return tips

def populate_meals_database():
    """Populate database with USDA-based meal data"""
    for meal_data in USDA_MEALS_DATA:
        existing_meal = Meal.query.filter_by(name=meal_data['name']).first()
        if not existing_meal:
            meal = Meal(
                name=meal_data['name'],
                type=meal_data['type'],
                calories=meal_data['calories'],
                protein=meal_data['protein'],
                carbs=meal_data['carbs'],
                fat=meal_data['fat'],
                fiber=meal_data['fiber'],
                sugar=meal_data['sugar'],
                sodium=meal_data['sodium'],
                ingredients=meal_data['ingredients'],
                allergens=meal_data['allergens'],
                usda_id=meal_data['usda_id'],
                serving_size=meal_data['serving_size']
            )
            db.session.add(meal)
    
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print(f"Error populating meals database: {e}")

@meals_bp.route('/add_to_history', methods=['POST'])
def add_meal_to_history():
    """Add consumed meal to user's history"""
    data = request.get_json()
    user_id = data.get('user_id')
    meal_id = data.get('meal_id')
    portion_size = data.get('portion_size', 1.0)
    
    if not all([user_id, meal_id]):
        return jsonify({'error': 'Missing required fields'}), 400
    
    # Verify user and meal exist
    user = User.query.get(user_id)
    meal = Meal.query.get(meal_id)
    
    if not user or not meal:
        return jsonify({'error': 'User or meal not found'}), 404
    
    # Add to history
    history_entry = MealHistory(
        user_id=user_id,
        meal_id=meal_id,
        portion_size=portion_size
    )
    
    try:
        db.session.add(history_entry)
        db.session.commit()
        return jsonify({'message': 'Meal added to history successfully'}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to add meal to history'}), 500
