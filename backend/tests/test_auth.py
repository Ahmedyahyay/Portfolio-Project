import unittest
import pytest
from app import app, db
from models import User
import json

class AuthTestCase(unittest.TestCase):
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

    def test_register_success(self):
        """Test successful user registration"""
        response = self.app.post('/api/register', json={
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'john@example.com',
            'password': 'Password123',
            'height_cm': 175,
            'weight_kg': 70
        })
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertIn('user_id', data)
        self.assertEqual(data['first_name'], 'John')
        self.assertEqual(data['last_name'], 'Doe')
        self.assertAlmostEqual(data['bmi'], 22.86, places=1)

    def test_register_validation_errors(self):
        """Test registration validation errors"""
        # Test missing fields
        response = self.app.post('/api/register', json={
            'first_name': 'John',
            'email': 'john@example.com'
        })
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn('details', data)

    def test_register_weak_password(self):
        """Test weak password rejection"""
        response = self.app.post('/api/register', json={
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'john@example.com',
            'password': 'weak',
            'height_cm': 175,
            'weight_kg': 70
        })
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn('password', data['details'])

    def test_register_duplicate_email(self):
        """Test duplicate email rejection"""
        # First registration
        self.app.post('/api/register', json={
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'john@example.com',
            'password': 'Password123',
            'height_cm': 175,
            'weight_kg': 70
        })
        
        # Second registration with same email
        response = self.app.post('/api/register', json={
            'first_name': 'Jane',
            'last_name': 'Doe',
            'email': 'john@example.com',
            'password': 'Password123',
            'height_cm': 165,
            'weight_kg': 60
        })
        self.assertEqual(response.status_code, 409)

    def test_login_success(self):
        """Test successful login"""
        # Register user first
        self.app.post('/api/register', json={
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'john@example.com',
            'password': 'Password123',
            'height_cm': 175,
            'weight_kg': 70
        })
        
        # Login
        response = self.app.post('/api/login', json={
            'email': 'john@example.com',
            'password': 'Password123'
        })
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('user_id', data)
        self.assertEqual(data['first_name'], 'John')

    def test_login_invalid_credentials(self):
        """Test login with invalid credentials"""
        response = self.app.post('/api/login', json={
            'email': 'nonexistent@example.com',
            'password': 'wrongpassword'
        })
        self.assertEqual(response.status_code, 401)

    def test_login_missing_fields(self):
        """Test login with missing fields"""
        response = self.app.post('/api/login', json={
            'email': 'john@example.com'
        })
        self.assertEqual(response.status_code, 400)

if __name__ == '__main__':
    unittest.main()