import unittest
import json
from app import app, db
from models import User, Meal, MealHistory

class NutritionTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        with app.app_context():
            db.create_all()
            # Create test user
            self.user = User(
                first_name='John',
                last_name='Doe',
                email='john@example.com',
                password_hash='hashed_password',
                height_cm=175,
                weight_kg=70,
                BMI=22.86
            )
            db.session.add(self.user)
            
            # Create test meals
            self.meal1 = Meal(
                name='Grilled Chicken Salad',
                type=Meal.MealType.lunch,
                calories=450,
                ingredients=['chicken', 'lettuce', 'tomato'],
                allergens=['none']
            )
            self.meal2 = Meal(
                name='Oatmeal with Berries',
                type=Meal.MealType.breakfast,
                calories=320,
                ingredients=['oats', 'milk', 'blueberries'],
                allergens=['milk']
            )
            self.meal3 = Meal(
                name='High Calorie Meal',
                type=Meal.MealType.dinner,
                calories=800,
                ingredients=['beef', 'potatoes', 'cheese'],
                allergens=['dairy']
            )
            
            db.session.add_all([self.meal1, self.meal2, self.meal3])
            db.session.commit()

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_get_meal_recommendations_success(self):
        """Test successful meal recommendations"""
        response = self.app.get(f'/api/meals?user_id={self.user.id}')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('meals', data)
        self.assertIn('user_bmi', data)
        self.assertIn('max_calories_applied', data)

    def test_get_meal_recommendations_missing_user(self):
        """Test meal recommendations with missing user"""
        response = self.app.get('/api/meals?user_id=999')
        self.assertEqual(response.status_code, 404)

    def test_get_meal_recommendations_missing_user_id(self):
        """Test meal recommendations without user_id"""
        response = self.app.get('/api/meals')
        self.assertEqual(response.status_code, 400)

    def test_meal_recommendations_calorie_cap(self):
        """Test calorie cap for obese users"""
        # Create obese user
        obese_user = User(
            first_name='Obese',
            last_name='User',
            email='obese@example.com',
            password_hash='hashed_password',
            height_cm=170,
            weight_kg=100,
            BMI=34.6
        )
        db.session.add(obese_user)
        db.session.commit()
        
        response = self.app.get(f'/api/meals?user_id={obese_user.id}')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        
        # All meals should be <= 700 calories
        for meal in data['meals']:
            self.assertLessEqual(meal['calories'], 700)

    def test_add_meal_to_history_success(self):
        """Test adding meal to history"""
        response = self.app.post('/api/meals/history', json={
            'user_id': self.user.id,
            'meal_id': self.meal1.id
        })
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertIn('message', data)

    def test_add_meal_to_history_invalid_user(self):
        """Test adding meal to history with invalid user"""
        response = self.app.post('/api/meals/history', json={
            'user_id': 999,
            'meal_id': self.meal1.id
        })
        self.assertEqual(response.status_code, 404)

    def test_add_meal_to_history_invalid_meal(self):
        """Test adding meal to history with invalid meal"""
        response = self.app.post('/api/meals/history', json={
            'user_id': self.user.id,
            'meal_id': 999
        })
        self.assertEqual(response.status_code, 404)

    def test_get_meal_history_success(self):
        """Test getting meal history"""
        # Add meal to history first
        meal_history = MealHistory(
            user_id=self.user.id,
            meal_id=self.meal1.id
        )
        db.session.add(meal_history)
        db.session.commit()
        
        response = self.app.get(f'/api/meals/history/{self.user.id}')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('meal_history', data)
        self.assertEqual(len(data['meal_history']), 1)

    def test_get_meal_history_invalid_user(self):
        """Test getting meal history for invalid user"""
        response = self.app.get('/api/meals/history/999')
        self.assertEqual(response.status_code, 404)

if __name__ == '__main__':
    unittest.main()
