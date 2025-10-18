from flask import Blueprint, render_template, request, flash, jsonify

from models import User

bmi_bp = Blueprint('bmi', __name__)

@bmi_bp.route('/', methods=['GET', 'POST'])
def calculator():
    """BMI calculator page following copilot health-centric patterns"""
    bmi_result = None
    
    if request.method == 'POST':
        try:
            height = float(request.form.get('height', 0))
            weight = float(request.form.get('weight', 0))
            
            if not (100 <= height <= 250) or not (30 <= weight <= 300):
                flash('Please enter valid height (100-250 cm) and weight (30-300 kg)', 'error')
                return render_template('bmi.html', result=None)
            
            # BMI calculation following copilot pattern (height in cm)
            bmi = round(weight / ((height / 100) ** 2), 2)
            
            # Determine category following copilot health-centric patterns
            if bmi < 18.5:
                category = 'Underweight'
            elif bmi < 25:
                category = 'Normal weight'
            elif bmi < 30:
                category = 'Overweight'
            elif bmi < 35:
                category = 'Class I Obesity'
            elif bmi < 40:
                category = 'Class II Obesity'
            else:
                category = 'Class III Obesity'
            
            # Eligibility check following copilot business rules
            eligible = bmi >= 30.0
            
            bmi_result = {
                'bmi': bmi,
                'category': category,
                'eligible': eligible,
                'height': height,
                'weight': weight
            }
            
            if eligible:
                flash(f'BMI: {bmi} - Eligible for nutrition assistance!', 'success')
            else:
                flash(f'BMI: {bmi} - Service designed for BMI ≥ 30', 'info')
                
        except Exception as e:
            flash('Please enter valid numeric values', 'error')
    
    return render_template('bmi.html', result=bmi_result)

@bmi_bp.route('/api/calculate', methods=['POST'])
def api_calculate():
    """API endpoint for BMI calculation following copilot API response conventions"""
    try:
        data = request.get_json()
        height = float(data.get('height', 0))
        weight = float(data.get('weight', 0))
        
        # Input validation following copilot input sanitization patterns
        if not (100 <= height <= 250) or not (30 <= weight <= 300):
            return jsonify({'error': 'Invalid input'}), 400
        
        bmi = round(weight / ((height/100) ** 2), 2)
        
        return jsonify({
            'BMI': bmi,
            'category': 'Class I Obesity' if 30 <= bmi < 35 else 'Class II Obesity' if 35 <= bmi < 40 else 'Class III Obesity' if bmi >= 40 else 'Overweight' if 25 <= bmi < 30 else 'Normal weight' if 18.5 <= bmi < 25 else 'Underweight',
            'eligible': bmi >= 30.0
        }), 200
        
    except Exception:
        return jsonify({'error': 'Invalid input'}), 400
