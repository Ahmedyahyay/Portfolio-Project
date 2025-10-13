from flask import Blueprint, request, jsonify

bmi_bp = Blueprint('bmi', __name__)

@bmi_bp.route('/calculate', methods=['POST'])
def calculate_bmi():
    data = request.get_json()
    height = data.get('height')
    weight = data.get('weight')
    
    if not all([height, weight]):
        return jsonify({'error': 'Missing fields'}), 400
    
    try:
        height = float(height)
        weight = float(weight)
        bmi = weight / ((height/100) ** 2)
        return jsonify({'BMI': round(bmi, 2)}), 200
    except Exception:
        return jsonify({'error': 'Invalid input'}), 400
