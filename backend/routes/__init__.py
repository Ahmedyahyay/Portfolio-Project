from .auth import auth_bp
from .bmi import bmi_bp

def register_blueprints(app):
    """Register all application blueprints following Flask blueprint organization"""
    app.register_blueprint(auth_bp)
    app.register_blueprint(bmi_bp)
    
    # Add root route
    @app.route('/')
    def index():
        return {
            'message': 'Personal Nutrition Assistant API',
            'endpoints': {
                'auth': '/register, /login',
                'bmi': '/calculate'
            }
        }

# Import all blueprints for easy access
__all__ = ['auth_bp', 'bmi_bp', 'register_blueprints']
