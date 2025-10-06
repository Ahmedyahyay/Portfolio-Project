# Personal Nutrition Assistant

## Overview
The Personal Nutrition Assistant is a mobile/web application designed to empower individuals to make healthier food choices. By providing personalized meal recommendations based on user dietary preferences, restrictions, and local grocery availability, the app helps users achieve their nutrition goals conveniently and effectively.


## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/Ahmedyahyay/Portfolio-Project.git

## Prerequisites

- Python 3.9+
- Node.js 18+
- PostgreSQL 13+
- Git

## Environment Setup

1. Copy environment variables:
   ```bash
   cp env.example .env
   ```

2. Edit `.env` with your configuration:
   - Set `DATABASE_URL` to your PostgreSQL connection string
   - Set `SECRET_KEY` to a secure random string
   - Set `NUTRITION_API_KEY` for USDA FoodData Central (optional)

## Database Setup

1. Create PostgreSQL database:
   ```sql
   CREATE DATABASE nutrition_assistant;
   ```

2. Run migrations:
   ```bash
   source venv/bin/activate
   cd backend
   export DATABASE_URL=postgresql+psycopg2://postgres:postgres@localhost:5432/nutrition_assistant
   flask db upgrade
   ```

## Backend Setup

1. Install Python dependencies:
   ```bash
   source venv/bin/activate
   pip install -r backend/requirements.txt
   ```

2. Run the Flask application:
   ```bash
   cd backend
   export DATABASE_URL=postgresql+psycopg2://postgres:postgres@localhost:5432/nutrition_assistant
   python app.py
   ```

   The API will be available at `http://127.0.0.1:5000/`

## Frontend Setup

1. Install Node.js dependencies:
   ```bash
   cd src/frontend
   npm install
   ```

2. Start the development server:
   ```bash
   npm run dev
   ```

   The React app will be available at `http://localhost:5173/`

## Running Tests

### Backend Tests
```bash
cd backend
python -m pytest tests/ -v
```

### Frontend Tests
```bash
cd src/frontend
npm test
```

### All Tests
```bash
# Run both backend and frontend tests
cd backend && python -m pytest tests/ -v && cd ../src/frontend && npm test
```

## API Endpoints

### Authentication
- `POST /api/register` - User registration
- `POST /api/login` - User login
- `POST /api/forgot-password` - Password reset (future)

### BMI Calculation
- `POST /api/bmi` - Calculate BMI with messaging
- `GET /api/bmi/user/<id>` - Get user's BMI

### Meal Recommendations
- `GET /api/meals?user_id=<id>` - Get personalized meal recommendations
- `GET /api/meals/external` - Fetch from external nutrition API
- `POST /api/meals/history` - Add meal to user history
- `GET /api/meals/history/<user_id>` - Get user's meal history

### Profile Management
- `GET /api/profile?user_id=<id>` - Get user profile
- `PUT /api/profile` - Update user profile

## Development

### Code Style
- Backend: Follow PEP 8, use flake8 for linting
- Frontend: Use Prettier and ESLint
- Run `python -m flake8 .` in backend directory
- Run `npm run lint` in frontend directory

### Database Migrations
```bash
# Create new migration
flask db migrate -m "Description of changes"

# Apply migrations
flask db upgrade

# Rollback migration
flask db downgrade
```

### Environment Variables
See `env.example` for all required environment variables.

## Deployment

### Production Checklist
- [ ] Set `FLASK_ENV=production`
- [ ] Use strong `SECRET_KEY`
- [ ] Configure production database
- [ ] Set up HTTPS
- [ ] Configure CORS for production domains
- [ ] Set up monitoring and logging
- [ ] Run security audit

### Docker (Optional)
```bash
# Build and run with Docker Compose
docker-compose up --build

### Pull Request Template (Paste in PR body)

#### Summary
- Implements BMI messaging, allergy-aware meals (<=700 kcal for BMI>=30), secure bcrypt hashing, and CI.

#### Changes
- Backend: `routes/auth.py`, `routes/nutrition.py` updates; migrations.
- CI: `.github/workflows/ci.yml` to run migrations and pytest on PR.
- Docs: `Technical_Documentation.md`, `project-charter.md` updated.

#### Migrations
```bash
cd backend
export DATABASE_URL=postgresql+psycopg2://<user>:<pass>@<host>:<port>/<db>
flask db upgrade
```

#### Local Run
```bash
# Backend
python3 -m venv venv && source venv/bin/activate
pip install -r backend/requirements.txt
export DATABASE_URL=postgresql+psycopg2://postgres:postgres@localhost:5432/nutrition_assistant
export SECRET_KEY=dev-secret
export NUTRITION_API=usda
export NUTRITION_API_KEY=dev-key
python backend/app.py

# Frontend
cd src/frontend && npm install && npm run dev
```

#### Tests
```bash
cd backend
python -m pytest -v
```

#### Reviewers
- SCM, QA
```

## Frontend Behavior

- The homepage shows two buttons: `Register` and `Login`.
- Clicking `Register` reveals the registration form without a page reload.
- Clicking `Login` reveals the login form without a page reload.
- A BMI calculator section is also available.

## Meal APIs and AI Suggestions

- List meals: `GET /get_meals?type=breakfast|lunch|dinner&max_calories=600`
- AI suggestions: `GET /ai_suggest_meals/<user_id>`
- Add to history: `POST /add_meal_history` with `{ user_id, meal_id }`

The server seeds a few sample meals automatically. You can set an environment variable `USDA_API_KEY` and extend `routes/meals.py` to fetch from USDA FoodData Central.

## Registration and Login

- Registration endpoint: `POST /api/register`
  - Validates email, password length (>= 6), height and weight are positive numbers.
  - Returns `409` if the email is already registered.
  - Returns detailed validation errors with `400` status.

- Login endpoint: `POST /api/login`
  - Returns `401` on invalid credentials.

### Common Issues

- Ensure the client sends `Content-Type: application/json` and a JSON body.
- For SQLite default, no `DATABASE_URL` is required. For other DBs, set `DATABASE_URL`.
