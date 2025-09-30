
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    height = db.Column(db.Float, nullable=False)
    weight = db.Column(db.Float, nullable=False)
    BMI = db.Column(db.Float, nullable=True)
    allergies = db.Column(db.String(256), nullable=True)
    preferences = db.Column(db.String(256), nullable=True)
    meal_history = db.relationship('MealHistory', backref='user', lazy=True)

class Meal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    type = db.Column(db.String(50), nullable=False)  # breakfast/lunch/dinner
    calories = db.Column(db.Integer, nullable=False)
    ingredients = db.Column(db.String(256), nullable=True)
    allergens = db.Column(db.String(256), nullable=True)
    meal_history = db.relationship('MealHistory', backref='meal', lazy=True)

class MealHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    meal_id = db.Column(db.Integer, db.ForeignKey('meal.id'), nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)
