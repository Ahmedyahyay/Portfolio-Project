from .auth import auth_bp
from .bmi import bmi_bp

def register_blueprints(app):
    app.register_blueprint(auth_bp)
    app.register_blueprint(bmi_bp)
