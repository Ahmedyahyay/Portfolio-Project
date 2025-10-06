# Personal Nutrition Assistant

## Overview
The Personal Nutrition Assistant is a mobile/web application designed to empower individuals to make healthier food choices. By providing personalized meal recommendations based on user dietary preferences, restrictions, and local grocery availability, the app helps users achieve their nutrition goals conveniently and effectively.


## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/Ahmedyahyay/Portfolio-Project.git

## Running the App

```bash
source venv/bin/activate
pip install -r backend/requirements.txt
python backend/app.py
```

Open `http://127.0.0.1:5000/` in your browser.

### Frontend (React) Dev Setup

The repository includes a minimal React app under `src/frontend` (Vite-style structure):

1. Ensure Node 18+ is installed.
2. From repo root, create a vite config or run with your preferred dev server. Example with Vite:
   ```bash
   npm create vite@latest frontend -- --template react
   # Move/merge src/frontend files into the created project or point your vite root to src/frontend
   ```
3. Mount point is `src/frontend/index.html` with entry `src/frontend/main.jsx`.
4. The React app calls the Flask backend on the same origin (proxy if different port).

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
