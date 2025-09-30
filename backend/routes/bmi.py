from flask import Blueprint, request, jsonify

from models import User

bmi_bp = Blueprint('bmi', __name__)

@bmi_bp.route('/api/bmi', methods=['POST'])
def calculate_bmi():
    data = request.get_json()
    height = data.get('height')
    weight = data.get('weight')
    if not height or not weight:
        return jsonify({'error': 'Missing height or weight'}), 400
    try:
        height = float(height)
        weight = float(weight)
        bmi = weight / ((height/100) ** 2)
    except Exception:
        return jsonify({'error': 'Invalid input'}), 400
    return jsonify({'BMI': round(bmi, 2)}), 200
