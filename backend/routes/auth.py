from flask import Blueprint, render_template, request, redirect, url_for, flash, session, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User
import re
import logging

# Setup logger following copilot QA integration patterns
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Create console handler if not already exists
if not logger.handlers:
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    
    # Create formatter
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(formatter)
    
    # Add handler to logger
    logger.addHandler(console_handler)

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """Login page following copilot authentication patterns with enhanced error handling"""
    if request.method == 'POST':
        email = None  # Initialize email for error handling
        try:
            email = request.form.get('email', '').strip().lower()
            password = request.form.get('password', '')
            
            # Debug logging for troubleshooting
            logger.info(f"Login attempt initiated for email: {email}")
            
            # Validation following copilot API response conventions
            if not all([email, password]):
                logger.warning(f"Login attempt with missing fields - email: {bool(email)}, password: {bool(password)}")
                flash('Please enter both email and password', 'error')
                return render_template('login.html')
            
            if not re.match(r'^[^\s@]+@[^\s@]+\.[^\s@]+$', email):
                logger.warning(f"Login attempt with invalid email format: {email}")
                flash('Please enter a valid email address', 'error')
                return render_template('login.html')
            
            # Database query with detailed logging
            logger.debug(f"Querying database for user with email: {email}")
            try:
                user = User.query.filter_by(email=email).first()
                logger.debug(f"Database query result - User found: {user is not None}")
                
                if user:
                    logger.debug(f"User details - ID: {user.id}, Username: {user.username}, BMI: {user.BMI}")
                    
                    # Verify all required User model columns exist
                    required_attrs = ['username', 'email', 'password_hash', 'height', 'weight', 'BMI']
                    missing_attrs = [attr for attr in required_attrs if not hasattr(user, attr)]
                    
                    if missing_attrs:
                        logger.error(f"User model missing required attributes: {missing_attrs}")
                        flash('Account data incomplete. Please contact support.', 'error')
                        return render_template('login.html')
                    
                else:
                    logger.info(f"No user found with email: {email}")
                    
            except Exception as db_error:
                logger.error(f"Database query error for email {email}: {db_error}")
                flash('Unable to access user database. Please try again.', 'error')
                return render_template('login.html')
            
            # Password verification
            if not user:
                logger.warning(f"Login attempt with non-existent email: {email}")
                flash('Invalid email or password', 'error')
                return render_template('login.html')
            
            try:
                password_valid = check_password_hash(user.password_hash, password)
                logger.debug(f"Password verification for {email}: {password_valid}")
                
                if not password_valid:
                    logger.warning(f"Failed login attempt - incorrect password for email: {email}")
                    flash('Invalid email or password', 'error')
                    return render_template('login.html')
                    
            except Exception as pwd_error:
                logger.error(f"Password verification error for {email}: {pwd_error}")
                flash('Authentication system error. Please try again.', 'error')
                return render_template('login.html')
            
            # BMI eligibility check following copilot business rules
            try:
                logger.debug(f"Checking BMI eligibility for user {email} - BMI: {user.BMI}")
                
                # Ensure BMI is calculated if missing
                if user.BMI is None:
                    logger.info(f"BMI missing for user {email}, calculating now")
                    user.calculate_bmi()
                    db.session.commit()
                    logger.debug(f"Calculated BMI for {email}: {user.BMI}")
                
                is_eligible = user.is_eligible_for_service()
                logger.debug(f"BMI eligibility check for {email}: {is_eligible} (BMI: {user.BMI})")
                
                if not is_eligible:
                    logger.info(f"User {email} attempted login with BMI {user.BMI} (not eligible for BMI ≥ 30 service)")
                    flash(f'Our service is designed for adults with BMI ≥ 30. Your BMI: {user.BMI}. Please consult with a healthcare professional for personalized advice.', 'warning')
                    return render_template('login.html')
                    
            except Exception as bmi_error:
                logger.error(f"BMI eligibility check error for {email}: {bmi_error}")
                flash('Unable to verify service eligibility. Please try again.', 'error')
                return render_template('login.html')
            
            # Session management with safe error handling
            try:
                logger.debug(f"Setting up session for user: {user.username}")
                
                # Clear any existing session data safely
                session.clear()
                
                # Store user session following copilot patterns
                session['user_id'] = user.id
                session['user_email'] = user.email
                session['user_username'] = user.username
                session['user_bmi'] = user.BMI
                
                logger.info(f"Successful login for user: {user.username} (BMI: {user.BMI})")
                flash(f'Welcome back, {user.username}! BMI: {user.BMI} - Access granted', 'success')
                
                return redirect(url_for('home.index'))
                
            except Exception as session_error:
                logger.error(f"Session setup error for {email}: {session_error}")
                flash('Login successful but session setup failed. Please try logging in again.', 'warning')
                return render_template('login.html')
            
        except Exception as general_error:
            # Catch-all error handler with specific logging
            logger.error(f"Unexpected login error for email '{email}': {type(general_error).__name__}: {general_error}")
            logger.exception("Full login error traceback:")  # This logs the full stack trace
            
            # Provide user-friendly error message
            flash('An unexpected error occurred during login. Please try again or contact support if the problem persists.', 'error')
            return render_template('login.html')
    
    # GET request - just render the login form
    return render_template('login.html')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """Registration with BMI eligibility enforcement and enhanced error handling following copilot patterns"""
    if request.method == 'POST':
        email = None  # Initialize for error handling
        try:
            email = request.form.get('email', '').strip().lower()
            password = request.form.get('password', '')
            height = request.form.get('height', '')
            weight = request.form.get('weight', '')
            allergies = request.form.get('allergies', '').strip()
            preferences = request.form.get('preferences', '').strip()
            
            logger.info(f"Registration attempt initiated for email: {email}")
            
            # Generate username from email (before @ symbol) following copilot patterns
            username = email.split('@')[0] if email else ''
            logger.debug(f"Generated initial username: {username} from email: {email}")
            
            # Enhanced validation following copilot input sanitization patterns
            if not all([email, password, height, weight]):
                logger.warning(f"Registration attempt with missing required fields - email: {bool(email)}, password: {bool(password)}, height: {bool(height)}, weight: {bool(weight)}")
                flash('Email, password, height, and weight are required', 'error')
                return render_template('register.html')
            
            if not re.match(r'^[^\s@]+@[^\s@]+\.[^\s@]+$', email):
                logger.warning(f"Registration attempt with invalid email format: {email}")
                flash('Please enter a valid email address', 'error')
                return render_template('register.html')
            
            if len(password) < 6:
                logger.warning(f"Registration attempt with short password for email: {email}")
                flash('Password must be at least 6 characters long', 'error')
                return render_template('register.html')
            
            # Validate and convert height/weight with detailed logging
            try:
                height_float = float(height)
                weight_float = float(weight)
                logger.debug(f"Height/weight conversion successful - Height: {height_float}cm, Weight: {weight_float}kg")
                
                if not (100 <= height_float <= 250) or not (30 <= weight_float <= 300):
                    logger.warning(f"Registration with invalid height/weight ranges - Height: {height_float}, Weight: {weight_float}")
                    raise ValueError("Invalid range")
                    
            except ValueError as ve:
                logger.error(f"Height/weight validation error for {email}: {ve}")
                flash('Please enter valid height (100-250 cm) and weight (30-300 kg)', 'error')
                return render_template('register.html')
            
            # Database existence checks with detailed logging
            try:
                logger.debug(f"Checking if email already exists: {email}")
                existing_user = User.query.filter_by(email=email).first()
                if existing_user:
                    logger.warning(f"Registration attempt with existing email: {email} (User ID: {existing_user.id})")
                    flash('An account with this email already exists', 'error')
                    return render_template('register.html')
                
                # Check and generate unique username with detailed logging
                logger.debug(f"Checking username availability: {username}")
                existing_username = User.query.filter_by(username=username).first()
                if existing_username:
                    logger.info(f"Username {username} already exists, generating unique variant")
                    base_username = username
                    counter = 1
                    while User.query.filter_by(username=username).first():
                        username = f"{base_username}{counter}"
                        counter += 1
                        if counter > 100:  # Prevent infinite loop
                            logger.error(f"Could not generate unique username after 100 attempts for email: {email}")
                            flash('Unable to generate unique username. Please try a different email.', 'error')
                            return render_template('register.html')
                    
                    logger.info(f"Generated unique username: {username} for email: {email}")
                    
            except Exception as db_check_error:
                logger.error(f"Database check error during registration for {email}: {db_check_error}")
                flash('Unable to verify account availability. Please try again.', 'error')
                return render_template('register.html')
            
            # Calculate BMI following copilot health-centric data model with enhanced logging
            try:
                bmi = round(weight_float / ((height_float / 100) ** 2), 2)
                logger.debug(f"BMI calculated for {email}: {bmi} (Height: {height_float}cm, Weight: {weight_float}kg)")
                
                # BMI eligibility check following copilot business rules
                if bmi < 30.0:
                    logger.info(f"Registration rejected - BMI {bmi} below threshold for email: {email}")
                    flash(f'Your BMI is {bmi}. Our service is designed for adults with BMI ≥ 30. Please consult with a healthcare professional for personalized advice.', 'warning')
                    return render_template('register.html')
                
                logger.info(f"BMI eligibility confirmed for {email}: {bmi} ≥ 30.0")
                
            except Exception as bmi_error:
                logger.error(f"BMI calculation error for {email}: {bmi_error}")
                flash('Error calculating BMI. Please verify your height and weight.', 'error')
                return render_template('register.html')
            
            # Create user with all required fields following copilot patterns
            try:
                logger.debug(f"Creating new user object for {email}")
                
                # Ensure all User model columns are properly set
                user_data = {
                    'username': username,
                    'email': email,
                    'password_hash': generate_password_hash(password),
                    'height': height_float,
                    'weight': weight_float,
                    'BMI': bmi,
                    'allergies': allergies if allergies else None,
                    'preferences': preferences if preferences else None
                }
                
                logger.debug(f"User data prepared: username={username}, email={email}, height={height_float}, weight={weight_float}, BMI={bmi}")
                
                user = User(**user_data)
                
                # Verify all required attributes are set
                required_attrs = ['username', 'email', 'password_hash', 'height', 'weight', 'BMI']
                missing_attrs = [attr for attr in required_attrs if not hasattr(user, attr) or getattr(user, attr) is None]
                
                if missing_attrs:
                    logger.error(f"User object missing required attributes: {missing_attrs}")
                    flash('Account creation failed due to missing data. Please try again.', 'error')
                    return render_template('register.html')
                
                logger.debug(f"User object validation passed for {email}")
                
            except Exception as user_creation_error:
                logger.error(f"User object creation error for {email}: {user_creation_error}")
                flash('Error creating account data. Please try again.', 'error')
                return render_template('register.html')
            
            # Database commit with comprehensive error handling
            try:
                logger.debug(f"Adding user to database session: {username}")
                db.session.add(user)
                
                logger.debug(f"Committing user registration to database: {username}")
                db.session.commit()
                
                logger.info(f"New user successfully registered: {username} (email: {email}, BMI: {bmi})")
                flash(f'Account created successfully! Username: {username}, BMI: {bmi} - You are eligible for our nutrition assistance program.', 'success')
                return redirect(url_for('auth.login'))
                
            except Exception as db_commit_error:
                logger.error(f"Database commit error for {email}: {type(db_commit_error).__name__}: {db_commit_error}")
                logger.exception("Full database commit error traceback:")
                
                try:
                    db.session.rollback()
                    logger.info(f"Database session rolled back for failed registration: {email}")
                except Exception as rollback_error:
                    logger.error(f"Database rollback error: {rollback_error}")
                
                # Provide specific error messages based on error type
                if 'UNIQUE constraint failed' in str(db_commit_error) or 'duplicate key' in str(db_commit_error).lower():
                    flash('An account with this information already exists. Please try different details.', 'error')
                elif 'NOT NULL constraint failed' in str(db_commit_error):
                    flash('Required account information is missing. Please fill all fields.', 'error')
                else:
                    flash('Database error during registration. Please try again or contact support.', 'error')
                
                return render_template('register.html')
            
        except Exception as general_error:
            logger.error(f"Unexpected registration error for email '{email}': {type(general_error).__name__}: {general_error}")
            logger.exception("Full registration error traceback:")
            
            # Ensure database cleanup
            try:
                db.session.rollback()
            except:
                pass
            
            flash('An unexpected error occurred during registration. Please try again or contact support if the problem persists.', 'error')
            return render_template('register.html')
    
    # GET request - render registration form
    return render_template('register.html')

@auth_bp.route('/logout')
def logout():
    """Logout user and clear session with proper cookie handling"""
    try:
        user_email = session.get('user_email', 'Unknown')
        
        # Clear session data following copilot patterns
        session.clear()
        
        logger.info(f"User logged out: {user_email}")
        flash('You have been logged out successfully', 'info')
        return redirect(url_for('home.index'))
        
    except Exception as e:
        logger.error(f"Logout error (handled gracefully): {e}")
        # Force clear session even if error occurs
        try:
            session.clear()
        except:
            pass
        flash('Logged out successfully', 'info')
        return redirect(url_for('home.index'))

# API endpoints following copilot API response conventions
@auth_bp.route('/api/register', methods=['POST'])
def api_register():
    """API registration endpoint with proper logging"""
    try:
        data = request.get_json()
        
        if not data or not all([data.get('email'), data.get('password'), data.get('height'), data.get('weight')]):
            logger.warning("API registration attempt with missing fields")
            return jsonify({'error': 'Missing fields'}), 400
        
        email = data.get('email', '').strip().lower()
        
        # Check if user exists
        if User.query.filter_by(email=email).first():
            logger.warning(f"API registration attempt with existing email: {email}")
            return jsonify({'error': 'Email already registered'}), 409
        
        # BMI calculation and validation
        try:
            height = float(data['height'])
            weight = float(data['weight'])
            bmi = weight / ((height/100) ** 2)
            
            if bmi < 30.0:
                logger.info(f"API registration rejected - BMI {bmi} below threshold for email: {email}")
                return jsonify({'error': 'BMI must be ≥ 30 for service eligibility'}), 400
            
            # Generate username
            username = email.split('@')[0]
            counter = 1
            base_username = username
            while User.query.filter_by(username=username).first():
                username = f"{base_username}{counter}"
                counter += 1
            
            user = User(
                username=username,
                email=email,
                password_hash=generate_password_hash(data['password']),
                height=height,
                weight=weight,
                BMI=round(bmi, 2)
            )
            
            db.session.add(user)
            db.session.commit()
            
            logger.info(f"API user registered: {username} (email: {email}, BMI: {round(bmi, 2)})")
            return jsonify({
                'message': 'User registered successfully', 
                'username': username,
                'BMI': user.BMI
            }), 201
            
        except ValueError as e:
            logger.error(f"API registration validation error: {e}")
            return jsonify({'error': 'Invalid input data'}), 400
            
    except Exception as e:
        logger.error(f"API registration error: {e}")
        return jsonify({'error': 'Registration failed'}), 500

@auth_bp.route('/api/login', methods=['POST'])
def api_login():
    """API login endpoint with proper logging"""
    try:
        data = request.get_json()
        
        if not data or not all([data.get('email'), data.get('password')]):
            logger.warning("API login attempt with missing credentials")
            return jsonify({'error': 'Missing credentials'}), 400
        
        email = data.get('email', '').strip().lower()
        password = data.get('password', '')
        
        user = User.query.filter_by(email=email).first()
        
        if not user or not check_password_hash(user.password_hash, password):
            logger.warning(f"API failed login attempt for email: {email}")
            return jsonify({'error': 'Invalid credentials'}), 401
        
        if not user.is_eligible_for_service():
            logger.info(f"API login attempt with ineligible BMI for user: {email}")
            return jsonify({'error': f'Service requires BMI ≥ 30. Your BMI: {user.BMI}'}), 403
        
        logger.info(f"API successful login for user: {user.username}")
        return jsonify({
            'message': 'Login successful',
            'user_id': user.id,
            'username': user.username,
            'BMI': user.BMI,
            'eligible': True
        }), 200
        
    except Exception as e:
        logger.error(f"API login error: {e}")
        return jsonify({'error': 'Login failed'}), 500
