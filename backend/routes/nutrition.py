from flask import Blueprint, request, jsonify
import os
import requests
from sqlalchemy import and_

from models import db, User, Meal, MealHistory, Allergy, UserAllergy

nutrition_bp = Blueprint('nutrition', __name__)


def fetch_nutrition_data(api_key, query="chicken", max_results=10):
    """Fetch nutrition data from external API"""
    try:
        # Example with USDA FoodData Central
        url = f"https://api.nal.usda.gov/fdc/v1/foods/search"
        params = {
            'api_key': api_key,
            'query': query,
            'pageSize': max_results,
            'dataType': ['Foundation', 'SR Legacy']
        }
        response = requests.get(url, params=params, timeout=10)

        if response.status_code == 200:
            data = response.json()
            return data.get('foods', [])
        else:
            return None
    except Exception as e:
        print(f"Error fetching nutrition data: {e}")
        return None


def normalize_allergens(allergen_list):
    """Normalize allergen names to lowercase for consistent matching"""
    if not allergen_list:
        return []
    return [allergen.strip().lower() for allergen in allergen_list if allergen.strip()]


def has_allergy_conflict(meal_allergens, user_allergens):
    """Check if meal has any allergens that conflict with user allergies"""
    if not meal_allergens or not user_allergens:
        return False

    meal_allergens_normalized = normalize_allergens(meal_allergens)
    user_allergens_normalized = normalize_allergens(user_allergens)

    return bool(set(meal_allergens_normalized) & set(user_allergens_normalized))


def get_user_allergies(user_id):
    """Get user's allergies from database"""
    user = User.query.get(user_id)
    if not user:
        return []

    # Get from user_allergies relationship
    user_allergy_objects = UserAllergy.query.filter_by(user_id=user_id).all()
    allergy_names = [
        ua.allergy.name for ua in user_allergy_objects if ua.allergy]

    # Also check legacy allergies field
    if user.allergies:
        legacy_allergies = [a.strip()
                            for a in user.allergies.split(',') if a.strip()]
        allergy_names.extend(legacy_allergies)

    return list(set(allergy_names))  # Remove duplicates


@nutrition_bp.route('/api/meals', methods=['GET'])
def get_meal_recommendations():
    """Get personalized meal recommendations for a user"""
    user_id = request.args.get('user_id', type=int)
    meal_type = request.args.get('type', '').strip()
    max_calories = request.args.get('max_calories', type=int)

    if not user_id:
        return jsonify({'error': 'user_id is required'}), 400

    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404

    # Get user's BMI and allergies
    user_bmi = user.BMI or (user.weight_kg / ((user.height_cm/100) ** 2))
    user_allergies = get_user_allergies(user_id)

    # Apply calorie cap for obese users (BMI >= 30)
    if user_bmi >= 30:
        max_calories = min(max_calories or 700, 700)
    else:
        max_calories = max_calories or 800

    # Query meals from database
    query = Meal.query

    if meal_type:
        try:
            from models import Meal
            mt = Meal.MealType(meal_type)
            query = query.filter(Meal.type == mt)
        except ValueError:
            return jsonify({"error": "Invalid meal type"}), 400

    if max_calories:
        query = query.filter(Meal.calories <= max_calories)

    all_meals = query.all()

    # Group by meal type and filter by allergy safety
    grouped = {'breakfast': [], 'lunch': [], 'dinner': []}
    uncertain_flags = {}
    for meal in all_meals:
        meal_type_value = meal.type.value if hasattr(
            meal.type, 'value') else str(meal.type)
        if meal_type_value not in grouped:
            continue
        meal_allergens = meal.allergens if isinstance(
            meal.allergens, list) else []
        if has_allergy_conflict(meal_allergens, user_allergies):
            continue
        is_uncertain = not meal_allergens or len(meal_allergens) == 0
        grouped[meal_type_value].append(meal)
        uncertain_flags[meal.id] = is_uncertain

    # For each type, select up to 3, prioritizing safe over uncertain
    def select_top_three(meals_list):
        safe = [m for m in meals_list if not uncertain_flags.get(m.id, False)]
        uncertain = [m for m in meals_list if uncertain_flags.get(m.id, False)]
        selected = (safe[:3])
        if len(selected) < 3:
            selected.extend(uncertain[:3-len(selected)])
        return selected

    selected_breakfast = select_top_three(grouped['breakfast'])
    selected_lunch = select_top_three(grouped['lunch'])
    selected_dinner = select_top_three(grouped['dinner'])

    recommended_meals = selected_breakfast + selected_lunch + selected_dinner

    meals_data = []
    for meal in recommended_meals:
        meals_data.append({
            'id': meal.id,
            'name': meal.name,
            'type': meal.type.value if hasattr(meal.type, 'value') else str(meal.type),
            'calories': meal.calories,
            'ingredients': meal.ingredients,
            'allergens': meal.allergens,
            'uncertain_allergens': uncertain_flags.get(meal.id, False)
        })

    insufficient_data = any(len(grouped[t]) < 3 for t in grouped)

    response = {
        'meals': meals_data,
        'user_bmi': round(user_bmi, 2),
        'max_calories_applied': max_calories,
        'insufficient_data': insufficient_data,
        'allergy_note': "We filtered meals based on your allergies — please confirm any uncertainty." if any(uncertain_flags.values()) else None
    }

    if insufficient_data:
        response['fallback_message'] = "Insufficient meal options found. Please consult a nutritionist for personalized recommendations."

    return jsonify(response), 200


@nutrition_bp.route('/api/meals/external', methods=['GET'])
def fetch_external_meals():
    """Fetch meals from external nutrition API"""
    api_key = os.getenv('NUTRITION_API_KEY')
    if not api_key:
        return jsonify({'error': 'Nutrition API key not configured'}), 500

    query = request.args.get('query', 'chicken')
    max_results = request.args.get('max_results', 10, type=int)

    nutrition_data = fetch_nutrition_data(api_key, query, max_results)

    if not nutrition_data:
        return jsonify({'error': 'Failed to fetch nutrition data'}), 500

    # Process and return nutrition data
    processed_meals = []
    for food in nutrition_data:
        if 'foodNutrients' in food:
            calories = None
            for nutrient in food['foodNutrients']:
                if nutrient.get('nutrient', {}).get('name') == 'Energy':
                    calories = nutrient.get('amount', 0)
                    break

            meal_data = {
                'name': food.get('description', 'Unknown'),
                'calories': int(calories) if calories else 0,
                'ingredients': [food.get('description', '')],
                'allergens': [],  # Would need additional processing
                'source': 'USDA'
            }
            processed_meals.append(meal_data)

    return jsonify({'meals': processed_meals}), 200


@nutrition_bp.route('/api/meals/history', methods=['POST'])
def add_meal_to_history():
    """Add a meal to user's meal history"""
    data = request.get_json(silent=True) or {}
    user_id = data.get('user_id')
    meal_id = data.get('meal_id')

    if not user_id or not meal_id:
        return jsonify({'error': 'user_id and meal_id are required'}), 400

    user = User.query.get(user_id)
    meal = Meal.query.get(meal_id)

    if not user or not meal:
        return jsonify({'error': 'User or meal not found'}), 404

    # Add to meal history
    meal_history = MealHistory(user_id=user_id, meal_id=meal_id)
    db.session.add(meal_history)
    db.session.commit()

    return jsonify({'message': 'Meal added to history successfully'}), 201


@nutrition_bp.route('/api/meals/history/<int:user_id>', methods=['GET'])
def get_meal_history(user_id):
    """Get user's meal history"""
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404

    # Get recent meal history (last 30 days)
    from datetime import datetime, timedelta
    thirty_days_ago = datetime.utcnow() - timedelta(days=30)

    history = MealHistory.query.filter(
        MealHistory.user_id == user_id,
        MealHistory.date_consumed >= thirty_days_ago
    ).order_by(MealHistory.date_consumed.desc()).all()

    history_data = []
    for entry in history:
        history_data.append({
            'id': entry.id,
            'meal_name': entry.meal.name,
            'meal_type': entry.meal.type.value,
            'calories': entry.meal.calories,
            'date_consumed': entry.date_consumed.isoformat()
        })

    return jsonify({'meal_history': history_data}), 200
