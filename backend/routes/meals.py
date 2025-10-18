from flask import Blueprint, render_template, request, jsonify
from models import db, Meal

meals_bp = Blueprint('meals', __name__)

@meals_bp.route('/')
def index():
    """Meals page displaying ALL USDA nutrition database records following health-centric data model"""
    try:
        # Get search and filter parameters
        search_query = request.args.get('search', '').strip()
        meal_type_filter = request.args.get('meal_type', '').strip()
        max_calories = request.args.get('max_calories', type=int)
        min_protein = request.args.get('min_protein', type=float)
        
        # Build query following copilot patterns - NO LIMITS, return ALL meals
        meals_query = Meal.query
        
        # Apply filters only if specified, otherwise show ALL meals
        if search_query:
            meals_query = meals_query.filter(
                db.or_(
                    Meal.name.ilike(f'%{search_query}%'),
                    Meal.ingredients.ilike(f'%{search_query}%')
                )
            )
        
        if meal_type_filter:
            meals_query = meals_query.filter(Meal.type == meal_type_filter)
        
        if max_calories and max_calories > 0:
            meals_query = meals_query.filter(Meal.calories <= max_calories)
            
        if min_protein and min_protein > 0:
            meals_query = meals_query.filter(Meal.protein >= min_protein)
        
        # Get ALL meals - no pagination, no limits
        meals = meals_query.all()
        
        # Calculate nutrition scores and eligibility for ALL meals following copilot health patterns
        for meal in meals:
            meal.nutrition_score = meal.calculate_nutrition_score()
            meal.eligible_for_target = meal.meets_eligibility_criteria(30.0)
        
        # Sort by nutrition score (higher is better for BMI >= 30 demographic)
        meals.sort(key=lambda m: m.nutrition_score, reverse=True)
        
        # Calculate comprehensive statistics for ALL meals
        stats = {
            'total_meals': len(meals),
            'breakfast_meals': len([m for m in meals if m.type == 'breakfast']),
            'lunch_meals': len([m for m in meals if m.type == 'lunch']),
            'dinner_meals': len([m for m in meals if m.type == 'dinner']),
            'snack_meals': len([m for m in meals if m.type == 'snack']),
            'high_protein_meals': len([m for m in meals if (m.protein or 0) >= 15]),
            'high_fiber_meals': len([m for m in meals if (m.fiber or 0) >= 3]),
            'low_calorie_meals': len([m for m in meals if m.calories <= 200]),
            'medium_calorie_meals': len([m for m in meals if 200 < m.calories <= 400]),
            'high_calorie_meals': len([m for m in meals if m.calories > 400]),
            'eligible_meals': len([m for m in meals if m.eligible_for_target]),
            'avg_nutrition_score': round(sum(m.nutrition_score for m in meals) / len(meals), 1) if meals else 0,
            'avg_calories': round(sum(m.calories for m in meals) / len(meals), 0) if meals else 0,
            'avg_protein': round(sum(m.protein or 0 for m in meals) / len(meals), 1) if meals else 0,
            'avg_fiber': round(sum(m.fiber or 0 for m in meals) / len(meals), 1) if meals else 0,
            'usda_verified': len([m for m in meals if m.usda_id]),
            'allergen_free': len([m for m in meals if not m.allergens or m.allergens == 'None'])
        }
        
        return render_template('meals.html', meals=meals, stats=stats, show_all=True)
        
    except Exception as e:
        # Return empty results with error message but maintain full display capability
        empty_stats = {
            'total_meals': 0, 'breakfast_meals': 0, 'lunch_meals': 0, 'dinner_meals': 0, 'snack_meals': 0,
            'high_protein_meals': 0, 'high_fiber_meals': 0, 'low_calorie_meals': 0, 'medium_calorie_meals': 0,
            'high_calorie_meals': 0, 'eligible_meals': 0, 'avg_nutrition_score': 0, 'avg_calories': 0,
            'avg_protein': 0, 'avg_fiber': 0, 'usda_verified': 0, 'allergen_free': 0
        }
        return render_template('meals.html', meals=[], error="Unable to load meals database", stats=empty_stats, show_all=True)

@meals_bp.route('/api/search')
def api_search():
    """API endpoint for meal search following copilot API response conventions - returns ALL matching results"""
    try:
        query = request.args.get('q', '').strip()
        meal_type = request.args.get('type', '').strip()
        
        # Build search query - NO LIMITS for full API access
        search_query = Meal.query
        
        if query:
            search_query = search_query.filter(Meal.name.ilike(f'%{query}%'))
        
        if meal_type:
            search_query = search_query.filter(Meal.type == meal_type)
        
        # Return ALL matching meals
        meals = search_query.all()
        
        results = []
        for meal in meals:
            meal.nutrition_score = meal.calculate_nutrition_score()
            results.append({
                'id': meal.id,
                'name': meal.name,
                'type': meal.type,
                'calories': meal.calories,
                'protein': meal.protein,
                'carbs': meal.carbs,
                'fat': meal.fat,
                'fiber': meal.fiber,
                'sugar': meal.sugar,
                'sodium': meal.sodium,
                'ingredients': meal.ingredients,
                'allergens': meal.allergens,
                'usda_id': meal.usda_id,
                'serving_size': meal.serving_size,
                'nutrition_score': meal.nutrition_score,
                'eligible_for_bmi_30': meal.meets_eligibility_criteria(30.0)
            })
        
        return jsonify({
            'meals': results, 
            'count': len(results),
            'showing_all': True,
            'message': f'Displaying all {len(results)} meals from database'
        })
        
    except Exception as e:
        return jsonify({'error': str(e), 'meals': [], 'count': 0}), 500

@meals_bp.route('/api/all')
def api_all_meals():
    """API endpoint to get ALL meals with complete data following copilot patterns"""
    try:
        # Get absolutely ALL meals from database
        meals = Meal.query.all()
        
        results = []
        for meal in meals:
            results.append(meal.to_dict())
        
        return jsonify({
            'meals': results,
            'total_count': len(results),
            'message': f'Retrieved all {len(results)} meals from USDA database',
            'data_source': 'USDA FoodData Central',
            'target_demographic': 'Adults with BMI >= 30'
        })
        
    except Exception as e:
        return jsonify({'error': str(e), 'meals': [], 'total_count': 0}), 500

@meals_bp.route('/stats')
def meal_stats():
    """Comprehensive meal statistics for ALL database records"""
    try:
        meals = Meal.query.all()
        
        if not meals:
            return render_template('meal_stats.html', stats={}, meals=[])
        
        # Calculate comprehensive statistics for ALL meals
        stats = {
            'database_summary': {
                'total_meals': len(meals),
                'usda_verified': len([m for m in meals if m.usda_id]),
                'data_completeness': round(len([m for m in meals if all([m.protein, m.carbs, m.fat, m.fiber])]) / len(meals) * 100, 1)
            },
            'meal_types': {
                'breakfast': len([m for m in meals if m.type == 'breakfast']),
                'lunch': len([m for m in meals if m.type == 'lunch']),
                'dinner': len([m for m in meals if m.type == 'dinner']),
                'snack': len([m for m in meals if m.type == 'snack'])
            },
            'nutrition_categories': {
                'high_protein': len([m for m in meals if (m.protein or 0) >= 15]),
                'high_fiber': len([m for m in meals if (m.fiber or 0) >= 3]),
                'low_calorie': len([m for m in meals if m.calories <= 200]),
                'medium_calorie': len([m for m in meals if 200 < m.calories <= 400]),
                'high_calorie': len([m for m in meals if m.calories > 400])
            },
            'bmi_eligibility': {
                'suitable_for_bmi_30': len([m for m in meals if m.meets_eligibility_criteria(30.0)]),
                'percentage_suitable': round(len([m for m in meals if m.meets_eligibility_criteria(30.0)]) / len(meals) * 100, 1)
            },
            'averages': {
                'calories': round(sum(m.calories for m in meals) / len(meals), 1),
                'protein': round(sum(m.protein or 0 for m in meals) / len(meals), 1),
                'carbs': round(sum(m.carbs or 0 for m in meals) / len(meals), 1),
                'fat': round(sum(m.fat or 0 for m in meals) / len(meals), 1),
                'fiber': round(sum(m.fiber or 0 for m in meals) / len(meals), 1),
                'nutrition_score': round(sum(m.calculate_nutrition_score() for m in meals) / len(meals), 1)
            }
        }
        
        # Get top scoring meals for display
        for meal in meals:
            meal.nutrition_score = meal.calculate_nutrition_score()
        
        top_meals = sorted(meals, key=lambda m: m.nutrition_score, reverse=True)[:10]
        
        return render_template('meal_stats.html', stats=stats, top_meals=top_meals)
        
    except Exception as e:
        return render_template('meal_stats.html', stats={}, top_meals=[], error=str(e))
