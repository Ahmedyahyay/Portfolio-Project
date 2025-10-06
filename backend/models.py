from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Enum as SAEnum, JSON
import enum
from datetime import datetime


db = SQLAlchemy()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(120), nullable=True)
    last_name = db.Column(db.String(120), nullable=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    height_cm = db.Column(db.Float, nullable=False)
    weight_kg = db.Column(db.Float, nullable=False)
    BMI = db.Column(db.Float, nullable=True)
    allergies = db.Column(db.String(256), nullable=True)
    preferences = db.Column(db.String(256), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    meal_history = db.relationship('MealHistory', backref='user', lazy=True)
    user_allergies = db.relationship('UserAllergy', backref='user', lazy=True)
    user_preferences = db.relationship(
        'UserPreference', backref='user', lazy=True)
    user_progress = db.relationship('UserProgress', backref='user', lazy=True)

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
    ingredients = db.Column(JSON, nullable=True)
    allergens = db.Column(JSON, nullable=True)
    meal_history = db.relationship('MealHistory', backref='meal', lazy=True)

    def __repr__(self):
        return f"<Meal {self.name}>"


class MealHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(
        'user.id'), nullable=False, index=True)
    meal_id = db.Column(db.Integer, db.ForeignKey(
        'meal.id'), nullable=False, index=True)
    date_consumed = db.Column(db.DateTime, default=datetime.utcnow, index=True)

    def __repr__(self):
        return f"<MealHistory User:{self.user_id} Meal:{self.meal_id} Date:{self.date_consumed}>"


class Allergy(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)

    def __repr__(self):
        return f"<Allergy {self.name}>"


class UserAllergy(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(
        'user.id'), nullable=False, index=True)
    allergy_id = db.Column(db.Integer, db.ForeignKey(
        'allergy.id'), nullable=False, index=True)

    def __repr__(self):
        return f"<UserAllergy User:{self.user_id} Allergy:{self.allergy_id}>"


class UserPreference(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(
        'user.id'), nullable=False, index=True)
    key = db.Column(db.String(100), nullable=False)
    value = db.Column(db.String(500), nullable=True)

    def __repr__(self):
        return f"<UserPreference User:{self.user_id} Key:{self.key}>"


class UserProgress(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(
        'user.id'), nullable=False, index=True)
    weight_kg = db.Column(db.Float, nullable=False)
    measured_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)

    def __repr__(self):
        return f"<UserProgress User:{self.user_id} Weight:{self.weight_kg} Date:{self.measured_at}>"
