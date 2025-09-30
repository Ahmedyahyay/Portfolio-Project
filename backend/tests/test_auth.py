import unittest
from app import app, db
from models import User

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

    def test_register(self):
        response = self.app.post('/api/register', json={
            'email': 'test@example.com',
            'password': 'testpass',
            'height': 170,
            'weight': 90
        })
        self.assertEqual(response.status_code, 201)

    def test_login(self):
        with app.app_context():
            user = User(email='test2@example.com', password_hash='hash', height=170, weight=90)
            db.session.add(user)
            db.session.commit()
        response = self.app.post('/api/login', json={
            'email': 'test2@example.com',
            'password': 'wrongpass'
        })
        self.assertEqual(response.status_code, 401)

if __name__ == '__main__':
    unittest.main()
