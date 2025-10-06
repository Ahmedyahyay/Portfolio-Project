
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Enum as SAEnum
import enum
from datetime import datetime


db = SQLAlchemy()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(120), nullable=True)
    last_name = db.Column(db.String(120), nullable=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    height = db.Column(db.Float, nullable=False)
    weight = db.Column(db.Float, nullable=False)
    BMI = db.Column(db.Float, nullable=True)
    allergies = db.Column(db.String(256), nullable=True)
    preferences = db.Column(db.String(256), nullable=True)
    meal_history = db.relationship('MealHistory', backref='user', lazy=True)

    def __repr__(self):
        return f"<User {self.email}>"


class Meal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)

    class MealType(enum.Enum):
        breakfast = "breakfast"
        lunch = "lunch"
        dinner = "dinner"

    type = db.Column(SAEnum(MealType), nullable=False)
    calories = db.Column(db.Integer, nullable=False)
    ingredients = db.Column(db.String(256), nullable=True)
    allergens = db.Column(db.String(256), nullable=True)
    meal_history = db.relationship('MealHistory', backref='meal', lazy=True)

    def __repr__(self):
        return f"<Meal {self.name}>"


class MealHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(
        'user.id'), nullable=False, index=True)
    meal_id = db.Column(db.Integer, db.ForeignKey(
        'meal.id'), nullable=False, index=True)
    date = db.Column(db.DateTime, default=datetime.utcnow, index=True)

    def __repr__(self):
        return f"<MealHistory User:{self.user_id} Meal:{self.meal_id} Date:{self.date}>"
