# Copilot Instructions - Personal Nutrition Assistant

## Project Overview
Flask-based MVP targeting obese adults (BMI ≥ 30) with secure authentication, BMI verification, and meal recommendations. Uses sprint-based development with comprehensive QA tracking across multiple team roles (Dev, QA, SCM).

## Architecture & Core Patterns

### Flask Blueprint Organization
```python
# routes/__init__.py - Central blueprint registry
from .auth import auth_bp
from .bmi import bmi_bp

def register_blueprints(app):
    app.register_blueprint(auth_bp)
    app.register_blueprint(bmi_bp)
```
- **Feature-based routing**: Each blueprint handles one domain (`auth.py`, `bmi.py`)
- **Centralized registration**: All blueprints imported and registered via `register_blueprints(app)`
- **Environment-aware database**: Uses `os.getenv('DATABASE_URL', 'sqlite:///nutrition.db')` for dev/prod switching

### Health-Centric Data Model
```python
# Always auto-calculate BMI during user creation
user = User(
    email=email,
    password_hash=generate_password_hash(password),
    height=height,
    weight=weight,
    BMI=weight / ((height/100) ** 2)  # Critical: height in cm, not meters
)
```
- **BMI enforcement**: Business rule requires BMI ≥ 30 for eligibility
- **Junction table pattern**: `User -> MealHistory <- Meal` for tracking meal consumption
- **Health data structure**: User model includes `allergies`, `preferences` as string fields

### API Response Conventions
```python
# Standard error responses
return jsonify({'error': 'Missing fields'}), 400
return jsonify({'error': 'Email already registered'}), 409
return jsonify({'error': 'Invalid credentials'}), 401

# Success patterns
return jsonify({'message': 'User registered successfully'}), 201
return jsonify({'BMI': round(bmi, 2)}), 200
```

## Sprint-Based Development Workflow

### Team Role Structure
- **Dev**: Feature implementation (Saad Alarifi, Abdullah Alameeri)
- **QA**: Testing and bug tracking (Ahmed Dawwari)  
- **SCM**: Git workflow and branching (Ahmed Dawwari)

### Quality Assurance Integration
- **Bug tracking**: Use `sprints/bug-tracker-sprint1.md` with status tracking
- **Test case documentation**: `sprints/qa-report-sprint1.md` with pass/fail status
- **Daily standups**: Document in `sprints/standup-sprint1.md`
- **Sprint retrospectives**: Track what went well/challenges in `sprint1-review.md`

### Database Migration Workflow
```bash
# After model changes in models.py
cd backend
flask db migrate -m "descriptive message"
flask db upgrade

# Database is created at backend/instance/nutrition.db (SQLite dev)
```

## Testing Architecture

### Isolated Test Pattern
```python
def setUp(self):
    self.app = app.test_client()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    with app.app_context():
        db.create_all()

def tearDown(self):
    with app.app_context():
        db.session.remove()
        db.drop_all()
```
- **Memory isolation**: Each test uses fresh `sqlite:///:memory:` database
- **Context management**: Always use `with app.app_context():` for database operations
- **Naming convention**: `backend/tests/test_{feature}.py`

## Critical Security & Validation Patterns

### Authentication Implementation
```python
# Registration validation (routes/auth.py)
if not all([email, password, height, weight]):
    return jsonify({'error': 'Missing fields'}), 400

# Login verification with proper hashing
if not user or not check_password_hash(user.password_hash, password):
    return jsonify({'error': 'Invalid credentials'}), 401
```

### Input Sanitization
```python
# BMI calculation with error handling (routes/bmi.py)
try:
    height = float(height)
    weight = float(weight)
    bmi = weight / ((height/100) ** 2)
except Exception:
    return jsonify({'error': 'Invalid input'}), 400
```

## Key Project Files
- `Technical_Documentation.md`: Complete API specs, user stories, and system architecture with Mermaid diagrams
- `sprints/sprint1-plan.md`: Task assignments with deadlines and team member roles
- `backend/migrations/versions/`: Alembic auto-generated migration files (e.g., `aed9515dfe1e_initial_migration.py`)
- `backend/requirements.txt`: Core dependencies (Flask, Flask-SQLAlchemy, psycopg2-binary, Flask-Migrate)

## Development Commands
```bash
# Backend setup
cd backend
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
pip install -r requirements.txt

# Run application
python app.py  # Starts Flask dev server on debug mode

# Testing
python -m unittest tests.test_auth
python -m pytest tests/  # If pytest is preferred
```