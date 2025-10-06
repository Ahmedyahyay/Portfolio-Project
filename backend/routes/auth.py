from flask import Blueprint, request, jsonify
from werkzeug.security import check_password_hash as werkzeug_check_password_hash
import bcrypt
import re

from models import db, User

auth_bp = Blueprint('auth', __name__)


def validate_password(password):
    """Validate password strength"""
    if len(password) < 8:
        return False, "Password must be at least 8 characters long"
    if not re.search(r'[A-Z]', password):
        return False, "Password must contain at least one uppercase letter"
    if not re.search(r'[a-z]', password):
        return False, "Password must contain at least one lowercase letter"
    if not re.search(r'\d', password):
        return False, "Password must contain at least one number"
    return True, "Valid password"


@auth_bp.route('/api/register', methods=['POST'])
def register():
    data = request.get_json(silent=True) or {}
    email = (data.get('email') or '').strip()
    password = data.get('password') or ''
    first_name = (data.get('first_name') or '').strip()
    last_name = (data.get('last_name') or '').strip()
    height_cm = data.get('height_cm')
    weight_kg = data.get('weight_kg')

    # Enhanced validation
    errors = {}
    if not email or not re.match(r'^[^@]+@[^@]+\.[^@]+$', email):
        errors['email'] = 'Valid email is required'
    if not password:
        errors['password'] = 'Password is required'
    else:
        is_valid, msg = validate_password(password)
        if not is_valid:
            errors['password'] = msg
    if not first_name:
        errors['first_name'] = 'First name is required'
    if not last_name:
        errors['last_name'] = 'Last name is required'
    try:
        height_cm = float(height_cm)
        weight_kg = float(weight_kg)
        if height_cm <= 0 or height_cm > 300:
            errors['height_cm'] = 'Height must be between 1-300 cm'
        if weight_kg <= 0 or weight_kg > 500:
            errors['weight_kg'] = 'Weight must be between 1-500 kg'
    except (ValueError, TypeError):
        errors['measurements'] = 'Valid height and weight are required'

    if errors:
        return jsonify({'error': 'Validation error', 'details': errors}), 400

    if User.query.filter_by(email=email).first():
        return jsonify({'error': 'Email already registered'}), 409

    # Calculate BMI
    bmi = weight_kg / ((height_cm/100) ** 2)

    # Hash password using bcrypt
    password_bytes = password.encode('utf-8')
    bcrypt_hash = bcrypt.hashpw(password_bytes, bcrypt.gensalt()).decode('utf-8')

    user = User(
        first_name=first_name,
        last_name=last_name,
        email=email,
        password_hash=bcrypt_hash,
        height_cm=height_cm,
        weight_kg=weight_kg,
        BMI=bmi
    )
    db.session.add(user)
    db.session.commit()
    return jsonify({
        'message': 'User registered successfully',
        'user_id': user.id,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'full_name': f"{user.first_name} {user.last_name}".strip(),
        'bmi': bmi
    }), 201


@auth_bp.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({'error': 'Email and password are required'}), 400

    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify({'error': 'Invalid credentials'}), 401

    # Support legacy werkzeug hashes and new bcrypt hashes
    stored_hash = user.password_hash or ''
    is_valid = False
    try:
        if stored_hash.startswith('pbkdf2:'):
            is_valid = werkzeug_check_password_hash(stored_hash, password)
        else:
            is_valid = bcrypt.checkpw(password.encode('utf-8'), stored_hash.encode('utf-8'))
    except Exception:
        is_valid = False

    if not is_valid:
        return jsonify({'error': 'Invalid credentials'}), 401

    return jsonify({
        'message': 'Login successful',
        'user_id': user.id,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'full_name': f"{user.first_name} {user.last_name}".strip(),
        'email': user.email,
        'bmi': user.BMI
    }), 200


@auth_bp.route('/api/forgot-password', methods=['POST'])
def forgot_password():
    data = request.get_json()
    email = data.get('email')
    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify({'error': 'Email not found'}), 404
    # Placeholder: send reset email logic here
    return jsonify({'message': 'Password reset instructions sent'}), 200
