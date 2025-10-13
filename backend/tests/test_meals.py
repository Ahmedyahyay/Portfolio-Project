import unittest
import json
from app import create_app
from models import db, User, Meal
from werkzeug.security import generate_password_hash

class MealsTestCase(unittest.TestCase):
    
    def setUp(self):
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.client = self.app.test_client()
        
        with self.app.app_context():
            db.create_all()
            
            # Create test user with BMI >= 30
            test_user = User(
                email='test@example.com',
                password_hash=generate_password_hash('password123'),
                height=170.0,
                weight=90.0,
                BMI=31.1,
                allergies='nuts',
                preferences='low-sodium'
            )
            db.session.add(test_user)
            db.session.commit()
            self.test_user_id = test_user.id

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_meal_search_by_query(self):
        """Test searching meals by name/ingredients"""
        response = self.client.post('/search',
            data=json.dumps({'query': 'chicken'}),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('meals', data)
        self.assertIn('count', data)
        
        # Should find chicken-related meals
        if data['count'] > 0:
            self.assertTrue(any('chicken' in meal['name'].lower() or 
                               'chicken' in meal['ingredients'].lower() 
                               for meal in data['meals']))

    def test_meal_search_by_type(self):
        """Test filtering meals by type"""
        response = self.client.post('/search',
            data=json.dumps({'meal_type': 'breakfast'}),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        
        # All returned meals should be breakfast type
        for meal in data['meals']:
            self.assertEqual(meal['type'], 'breakfast')

    def test_meal_search_by_calories(self):
        """Test filtering meals by maximum calories"""
        response = self.client.post('/search',
            data=json.dumps({'max_calories': 300}),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        
        # All returned meals should be under 300 calories
        for meal in data['meals']:
            self.assertLessEqual(meal['calories'], 300)

    def test_personalized_recommendations(self):
        """Test getting personalized meal recommendations"""
        response = self.client.post('/recommendations',
            data=json.dumps({'user_id': self.test_user_id}),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        
        # Should include daily calorie goal and meal plan
        self.assertIn('daily_calorie_goal', data)
        self.assertIn('meal_plan', data)
        self.assertIn('user_bmi', data)
        self.assertIn('nutrition_tips', data)
        
        # BMI should match test user
        self.assertEqual(data['user_bmi'], 31.1)
        
        # Should have calorie goal appropriate for weight loss
        self.assertGreater(data['daily_calorie_goal'], 1200)
        self.assertLess(data['daily_calorie_goal'], 2500)

    def test_recommendations_invalid_user(self):
        """Test recommendations with invalid user ID"""
        response = self.client.post('/recommendations',
            data=json.dumps({'user_id': 99999}),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 404)
        data = json.loads(response.data)
        self.assertEqual(data['error'], 'User not found')

    def test_add_meal_to_history(self):
        """Test adding consumed meal to user history"""
        # First, get a meal
        search_response = self.client.post('/search',
            data=json.dumps({'query': 'chicken'}),
            content_type='application/json'
        )
        meals_data = json.loads(search_response.data)
        
        if meals_data['count'] > 0:
            meal_id = meals_data['meals'][0]['id']
            
            response = self.client.post('/add_to_history',
                data=json.dumps({
                    'user_id': self.test_user_id,
                    'meal_id': meal_id,
                    'portion_size': 1.0
                }),
                content_type='application/json'
            )
            
            self.assertEqual(response.status_code, 201)
            data = json.loads(response.data)
            self.assertEqual(data['message'], 'Meal added to history successfully')

    def test_meal_database_population(self):
        """Test that USDA meal data is properly populated"""
        response = self.client.post('/search',
            data=json.dumps({}),
            content_type='application/json'
        )
        
        data = json.loads(response.data)
        
        # Should have populated sample meals
        self.assertGreater(data['count'], 0)
        
        # Check meal data structure
        if data['count'] > 0:
            meal = data['meals'][0]
            required_fields = ['id', 'name', 'type', 'calories', 'protein', 
                              'carbs', 'fat', 'ingredients', 'usda_id']
            for field in required_fields:
                self.assertIn(field, meal)
                
            # Validate USDA ID exists
            self.assertIsNotNone(meal['usda_id'])

if __name__ == '__main__':
    unittest.main()
