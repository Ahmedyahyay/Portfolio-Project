# Central blueprint registry following copilot blueprint organization
from .auth import auth_bp
from .meals import meals_bp
from .bmi import bmi_bp
from .features import features_bp
from .contact import contact_bp
from .home import home_bp

def register_blueprints(app):
    """Register all application blueprints following Flask blueprint organization"""
    app.register_blueprint(home_bp)
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(meals_bp, url_prefix='/meals')
    app.register_blueprint(bmi_bp, url_prefix='/bmi')
    app.register_blueprint(features_bp, url_prefix='/features')
    app.register_blueprint(contact_bp, url_prefix='/contact')
    
    # Add API info route following copilot API response conventions
    @app.route('/api')
    def api_info():
        return {
            'message': 'Personal Nutrition Assistant API',
            'version': '1.0.0',
            'target_audience': 'Adults with BMI ≥ 30',
            'endpoints': {
                'home': 'GET /',
                'features': 'GET /features',
                'meals': 'GET /meals',
                'contact': 'GET /contact',
                'bmi': 'GET /bmi',
                'auth': 'GET /auth/login, POST /auth/register'
            }
        }
