from .auth import auth_bp
from .bmi import bmi_bp
from .meals import meals_bp

def register_blueprints(app):
    """Register all application blueprints following Flask blueprint organization"""
    app.register_blueprint(auth_bp)
    app.register_blueprint(bmi_bp)
    app.register_blueprint(meals_bp)
    
    # Add root route with enhanced API information
    @app.route('/')
    def index():
        return {
            'message': 'Personal Nutrition Assistant API',
            'version': '2.0.0',
            'data_source': 'USDA FoodData Central',
            'target_audience': 'Adults with BMI ≥ 30',
            'endpoints': {
                'authentication': {
                    'register': 'POST /register',
                    'login': 'POST /login'
                },
                'health_metrics': {
                    'calculate_bmi': 'POST /calculate'
                },
                'nutrition': {
                    'search_meals': 'POST /search',
                    'get_recommendations': 'POST /recommendations', 
                    'add_to_history': 'POST /add_to_history'
                }
            },
            'features': [
                'BMI eligibility verification',
                'USDA-verified nutrition data',
                'Personalized meal recommendations',
                'Allergen filtering',
                'Progress tracking'
            ]
        }

# Import all blueprints for easy access
__all__ = ['auth_bp', 'bmi_bp', 'meals_bp', 'register_blueprints']
