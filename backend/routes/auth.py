from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash

from models import db, User

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/api/register', methods=['POST'])
def register():
    data = request.get_json(silent=True) or {}
    email = (data.get('email') or '').strip()
    password = data.get('password') or ''
    first_name = (data.get('first_name') or '').strip()
    last_name = (data.get('last_name') or '').strip()
    height = data.get('height')
    weight = data.get('weight')

    # Basic validation
    errors = {}
    if not email:
        errors['email'] = 'Email is required'
    if not password:
        errors['password'] = 'Password is required'
    elif len(password) < 6:
        errors['password'] = 'Password too short'
    if not first_name:
        errors['first_name'] = 'First name is required'
    if not last_name:
        errors['last_name'] = 'Last name is required'
    try:
        height = float(height)
        weight = float(weight)
        if height <= 0 or weight <= 0:
            raise ValueError
    except Exception:
        errors['body'] = 'Invalid height/weight'

    if errors:
        return jsonify({'error': 'Validation error', 'details': errors}), 400

    if User.query.filter_by(email=email).first():
        return jsonify({'error': 'Email already registered'}), 409

    user = User(
        first_name=first_name,
        last_name=last_name,
        email=email,
        password_hash=generate_password_hash(password),
        height=height,
        weight=weight,
        BMI=weight / ((height/100) ** 2)
    )
    db.session.add(user)
    db.session.commit()
    return jsonify({'message': 'User registered successfully'}), 201


@auth_bp.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    user = User.query.filter_by(email=email).first()
    if not user or not check_password_hash(user.password_hash, password):
        return jsonify({'error': 'Invalid credentials'}), 401
    return jsonify({'message': 'Login successful', 'user_id': user.id, 'first_name': user.first_name, 'last_name': user.last_name}), 200


@auth_bp.route('/api/forgot-password', methods=['POST'])
def forgot_password():
    data = request.get_json()
    email = data.get('email')
    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify({'error': 'Email not found'}), 404
    # Placeholder: send reset email logic here
    return jsonify({'message': 'Password reset instructions sent'}), 200
