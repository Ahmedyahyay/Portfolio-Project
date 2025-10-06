from flask import Blueprint, request, jsonify
import random

from models import User

bmi_bp = Blueprint('bmi', __name__)

# Motivational messages for BMI >= 30
MOTIVATIONAL_MESSAGES = [
    "Your BMI indicates that you're in the overweight range. Don't worry — small, consistent steps can lead to big changes! 💪 Keep going!",
    "You've taken the first step towards better health! Remember, every journey begins with a single step. We're here to support you every step of the way! 🌟",
    "Your BMI shows room for improvement, but that's okay! Focus on making small, sustainable changes. You've got this! 💪 Let's start this journey together!"
]

# Maintenance messages for healthy BMI
MAINTENANCE_MESSAGES = [
    "Great job maintaining a healthy weight! Keep up your balanced habits 🌿",
    "Excellent work! Your BMI is in a healthy range. Continue with your current lifestyle choices! 🌟",
    "Fantastic! You're maintaining a healthy weight. Keep up the great work with balanced nutrition! 🌿"
]

# Neutral guidance for other ranges
NEUTRAL_MESSAGES = [
    "Your BMI is outside the typical range. Consider consulting with a healthcare provider for personalized guidance.",
    "Your BMI suggests you may benefit from professional nutritional guidance. We recommend speaking with a healthcare provider.",
    "Your BMI is in an unusual range. For the best results, consider consulting with a nutritionist or healthcare provider."
]

@bmi_bp.route('/api/bmi', methods=['POST'])
def calculate_bmi():
    """Calculate BMI and return appropriate message based on range"""
    data = request.get_json(silent=True) or {}
    height_cm = data.get('height_cm')
    weight_kg = data.get('weight_kg')
    
    # Validation
    if not height_cm or not weight_kg:
        return jsonify({'error': 'Height and weight are required'}), 400
    
    try:
        height_cm = float(height_cm)
        weight_kg = float(weight_kg)
        
        if height_cm <= 0 or height_cm > 300:
            return jsonify({'error': 'Height must be between 1-300 cm'}), 400
        if weight_kg <= 0 or weight_kg > 500:
            return jsonify({'error': 'Weight must be between 1-500 kg'}), 400
            
    except (ValueError, TypeError):
        return jsonify({'error': 'Height and weight must be valid numbers'}), 400
    
    # Calculate BMI
    height_m = height_cm / 100
    bmi = weight_kg / (height_m ** 2)
    
    # Determine eligibility and message
    eligibility = bmi >= 30
    
    if bmi >= 30:
        message = random.choice(MOTIVATIONAL_MESSAGES)
    elif 18.5 <= bmi <= 24.9:
        message = random.choice(MAINTENANCE_MESSAGES)
    else:
        message = random.choice(NEUTRAL_MESSAGES)
    
    return jsonify({
        'bmi': round(bmi, 2),
        'eligibility': eligibility,
        'message': message,
        'height_cm': height_cm,
        'weight_kg': weight_kg
    }), 200

@bmi_bp.route('/api/bmi/user/<int:user_id>', methods=['GET'])
def get_user_bmi(user_id):
    """Get BMI for a specific user"""
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    if not user.height_cm or not user.weight_kg:
        return jsonify({'error': 'User height and weight not set'}), 400
    
    height_m = user.height_cm / 100
    bmi = user.weight_kg / (height_m ** 2)
    eligibility = bmi >= 30
    
    if bmi >= 30:
        message = random.choice(MOTIVATIONAL_MESSAGES)
    elif 18.5 <= bmi <= 24.9:
        message = random.choice(MAINTENANCE_MESSAGES)
    else:
        message = random.choice(NEUTRAL_MESSAGES)
    
    return jsonify({
        'bmi': round(bmi, 2),
        'eligibility': eligibility,
        'message': message,
        'height_cm': user.height_cm,
        'weight_kg': user.weight_kg,
        'first_name': user.first_name,
        'last_name': user.last_name
    }), 200