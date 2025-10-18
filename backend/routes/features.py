from flask import Blueprint, render_template

features_bp = Blueprint('features', __name__)

@features_bp.route('/')
def index():
    """Features page showcasing BMI >= 30 targeting following copilot business rules"""
    features_list = [
        {
            'icon': 'fas fa-calculator',
            'title': 'BMI Calculator',
            'description': 'Accurate BMI calculation with eligibility verification for BMI ≥ 30',
            'color': '#4CAF50'
        },
        {
            'icon': 'fas fa-database',
            'title': 'Nutrition Database',
            'description': 'Comprehensive meal database with detailed nutrition information',
            'color': '#2196F3'
        },
        {
            'icon': 'fas fa-shield-alt',
            'title': 'Secure Platform',
            'description': 'Enterprise-grade security with password hashing and input validation',
            'color': '#FF9800'
        },
        {
            'icon': 'fas fa-chart-line',
            'title': 'Progress Tracking',
            'description': 'Monitor your nutrition journey with detailed analytics and insights',
            'color': '#9C27B0'
        },
        {
            'icon': 'fas fa-utensils',
            'title': 'Meal Recommendations',
            'description': 'Personalized meal suggestions optimized for BMI >= 30 demographic',
            'color': '#795548'
        },
        {
            'icon': 'fas fa-mobile-alt',
            'title': 'Responsive Design',
            'description': 'Modern, mobile-first interface that works on all devices',
            'color': '#607D8B'
        }
    ]
    
    return render_template('features.html', features=features_list)
