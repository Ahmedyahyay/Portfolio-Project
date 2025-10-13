from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    height = data.get('height')
    weight = data.get('weight')
    
    if not all([email, password, height, weight]):
        return jsonify({'error': 'Missing fields'}), 400
    
    if User.query.filter_by(email=email).first():
        return jsonify({'error': 'Email already registered'}), 409
    
    try:
        height = float(height)
        weight = float(weight)
        bmi = weight / ((height/100) ** 2)
        
        user = User(
            email=email,
            password_hash=generate_password_hash(password),
            height=height,
            weight=weight,
            BMI=round(bmi, 2)
        )
        
        db.session.add(user)
        db.session.commit()
        
        return jsonify({'message': 'User registered successfully'}), 201
    except Exception:
        return jsonify({'error': 'Invalid input'}), 400

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    
    if not all([email, password]):
        return jsonify({'error': 'Missing fields'}), 400
    
    user = User.query.filter_by(email=email).first()
    
    if not user or not check_password_hash(user.password_hash, password):
        return jsonify({'error': 'Invalid credentials'}), 401
    
    return jsonify({'message': 'Login successful', 'user_id': user.id}), 200

@auth_bp.route('/forgot-password', methods=['POST'])
def forgot_password():
    data = request.get_json()
    email = data.get('email')
    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify({'error': 'Email not found'}), 404
    # Placeholder: send reset email logic here
    return jsonify({'message': 'Password reset instructions sent'}), 200
