from flask import Blueprint, request, jsonify
import os
import requests
from sqlalchemy import and_

from models import db, User, Meal, MealHistory

meals_bp = Blueprint('meals', __name__)


def upsert_sample_meals():
    # Minimal seed data if DB is empty
    if Meal.query.first():
        return
    samples = [
        {"name": "Oatmeal with Berries", "type": Meal.MealType.breakfast, "calories": 320, "ingredients": "oats, milk, blueberries", "allergens": "milk"},
        {"name": "Grilled Chicken Salad", "type": Meal.MealType.lunch, "calories": 450, "ingredients": "chicken, lettuce, tomato, olive oil", "allergens": ""},
        {"name": "Salmon with Quinoa", "type": Meal.MealType.dinner, "calories": 520, "ingredients": "salmon, quinoa, lemon", "allergens": "fish"},
    ]
    for s in samples:
        m = Meal(name=s["name"], type=s["type"], calories=s["calories"], ingredients=s["ingredients"], allergens=s["allergens"])
        db.session.add(m)
    db.session.commit()


@meals_bp.route('/get_meals', methods=['GET'])
def get_meals():
    upsert_sample_meals()
    meal_type = request.args.get('type')  # breakfast/lunch/dinner
    max_cal = request.args.get('max_calories', type=int)

    query = Meal.query
    if meal_type:
        try:
            mt = Meal.MealType(meal_type)
            query = query.filter(Meal.type == mt)
        except ValueError:
            return jsonify({"error": "Invalid meal type"}), 400
    if max_cal is not None:
        query = query.filter(Meal.calories <= max_cal)

    meals = query.limit(50).all()
    return jsonify([
        {"id": m.id, "name": m.name, "type": m.type.value, "calories": m.calories, "ingredients": m.ingredients, "allergens": m.allergens}
        for m in meals
    ])


@meals_bp.route('/api/meals', methods=['POST'])
def meals_filter_advanced():
    """Advanced filter that excludes common and specific allergens.
    Body: { type?: 'breakfast'|'lunch'|'dinner', max_calories?: int, specific_allergies?: 'a,b,c' }
    """
    upsert_sample_meals()
    data = request.get_json(silent=True) or {}
    meal_type = (data.get('type') or '').strip()
    max_cal = data.get('max_calories')
    specific = (data.get('specific_allergies') or '').lower()
    specific_set = {x.strip() for x in specific.split(',') if x.strip()}

    query = Meal.query
    if meal_type:
        try:
            mt = Meal.MealType(meal_type)
            query = query.filter(Meal.type == mt)
        except ValueError:
            return jsonify({"error": "Invalid meal type"}), 400
    if max_cal is not None:
        try:
            max_cal = int(max_cal)
            query = query.filter(Meal.calories <= max_cal)
        except Exception:
            return jsonify({"error": "Invalid max_calories"}), 400

    meals = query.limit(100).all()
    filtered = []
    for m in meals:
        ing = (m.ingredients or '').lower()
        alg = (m.allergens or '').lower()
        # Exclude if any specific allergens appear in ingredients or allergens
        if any(s in ing or s in alg for s in specific_set):
            continue
        filtered.append(m)
    return jsonify([
        {"id": m.id, "name": m.name, "type": m.type.value, "calories": m.calories, "ingredients": m.ingredients, "allergens": m.allergens}
        for m in filtered
    ])


def fetch_usda_samples(api_key: str, query: str = "chicken"):
    # Example: fetch from USDA FoodData Central if key provided
    try:
        url = f"https://api.nal.usda.gov/fdc/v1/foods/search?api_key={api_key}&query={query}&pageSize=5"
        r = requests.get(url, timeout=10)
        if r.ok:
            return r.json()
    except Exception:
        return None
    return None


def ai_score(meal: Meal, user: User) -> float:
    score = 0.0
    # Prefer meals closer to 500 kcal if BMI is high, lighter if BMI high, heavier if low BMI
    bmi = user.BMI or (user.weight / ((user.height/100) ** 2))
    target = 500 if bmi >= 25 else 650 if bmi < 18.5 else 600
    score -= abs(meal.calories - target) / 100.0

    # Penalize allergens
    if user.allergies and meal.allergens:
        user_allergens = {a.strip().lower() for a in user.allergies.split(',') if a.strip()}
        meal_allergens = {a.strip().lower() for a in meal.allergens.split(',') if a.strip()}
        if user_allergens & meal_allergens:
            score -= 100

    # Simple preference boost
    if user.preferences and meal.ingredients:
        prefs = {p.strip().lower() for p in user.preferences.split(',') if p.strip()}
        ings = meal.ingredients.lower()
        for p in prefs:
            if p in ings:
                score += 1.5

    return score


@meals_bp.route('/ai_suggest_meals/<int:user_id>', methods=['GET'])
def ai_suggest_meals(user_id: int):
    upsert_sample_meals()
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    # Basic strategy: score meals and exclude recently eaten ones
    recent_meal_ids = {mh.meal_id for mh in MealHistory.query.filter_by(user_id=user.id).order_by(MealHistory.date.desc()).limit(10)}
    candidates = [m for m in Meal.query.all() if m.id not in recent_meal_ids]

    # Exclude meals that violate user's allergies or 700 kcal cap for obese users
    user_allergens = {a.strip().lower() for a in (user.allergies or '').split(',') if a.strip()}
    obese = (user.BMI or (user.weight / ((user.height/100) ** 2))) >= 30
    filtered = []
    for m in candidates:
        if obese and m.calories > 700:
            continue
        ing = (m.ingredients or '').lower()
        alg = (m.allergens or '').lower()
        if any(a in ing or a in alg for a in user_allergens):
            continue
        filtered.append(m)
    ranked = sorted(filtered, key=lambda m: ai_score(m, user), reverse=True)[:10]

    return jsonify([
        {"id": m.id, "name": m.name, "type": m.type.value, "calories": m.calories, "ingredients": m.ingredients, "allergens": m.allergens}
        for m in ranked
    ])


@meals_bp.route('/add_meal_history', methods=['POST'])
def add_meal_history():
    data = request.get_json(silent=True) or {}
    user_id = data.get('user_id')
    meal_id = data.get('meal_id')
    if not user_id or not meal_id:
        return jsonify({"error": "user_id and meal_id required"}), 400
    user = User.query.get(user_id)
    meal = Meal.query.get(meal_id)
    if not user or not meal:
        return jsonify({"error": "Invalid user or meal"}), 404
    mh = MealHistory(user_id=user.id, meal_id=meal.id)
    db.session.add(mh)
    db.session.commit()
    return jsonify({"message": "Added to history"}), 201


@meals_bp.route('/api/profile', methods=['GET', 'PUT'])
def profile():
    # For demo: user_id from query/body; in real app, derive from auth
    if request.method == 'GET':
        user_id = request.args.get('user_id', type=int)
        user = User.query.get(user_id)
        if not user:
            return jsonify({"error": "User not found"}), 404
        return jsonify({
            'id': user.id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
            'weight': user.weight,
            'allergies': user.allergies,
        })
    else:
        data = request.get_json(silent=True) or {}
        user_id = data.get('user_id')
        user = User.query.get(user_id)
        if not user:
            return jsonify({"error": "User not found"}), 404
        # update fields if provided
        for key in ['first_name', 'last_name', 'weight', 'allergies']:
            if key in data and data[key] is not None:
                setattr(user, key, data[key])
        db.session.commit()
        return jsonify({"message": "Profile updated"})


