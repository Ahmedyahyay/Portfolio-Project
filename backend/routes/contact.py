from flask import Blueprint, render_template, request, flash, redirect, url_for
import re

contact_bp = Blueprint('contact', __name__)

@contact_bp.route('/', methods=['GET', 'POST'])
def index():
    """Contact page with form handling following copilot API response conventions"""
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()
        subject = request.form.get('subject', '').strip()
        message = request.form.get('message', '').strip()
        
        # Validation following copilot input sanitization patterns
        if not all([name, email, subject, message]):
            flash('All fields are required', 'error')
        elif not re.match(r'^[^\s@]+@[^\s@]+\.[^\s@]+$', email):
            flash('Please enter a valid email address', 'error')
        else:
            # In production, this would send email or save to database
            flash(f'Thank you {name}! Your message has been received.', 'success')
            return redirect(url_for('contact.index'))
    
    contact_info = {
        'email': 'support@nutriassist.com',
        'phone': '+1 (555) 123-4567',
        'address': '123 Health Street, Nutrition City, NC 12345',
        'hours': 'Monday - Friday: 8:00 AM - 6:00 PM EST'
    }
    
    return render_template('contact.html', contact=contact_info)
