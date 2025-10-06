from .auth import auth_bp
from .bmi import bmi_bp
from .meals import meals_bp
from .nutrition import nutrition_bp
from flask import Blueprint


def register_blueprints(app):
    app.register_blueprint(auth_bp)
    app.register_blueprint(bmi_bp)
    app.register_blueprint(meals_bp)
    app.register_blueprint(nutrition_bp)
