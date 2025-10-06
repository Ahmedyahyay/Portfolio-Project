import unittest
import json
from app import app

class BMITestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    def test_bmi_calculation_success(self):
        """Test successful BMI calculation"""
        response = self.app.post('/api/bmi', json={
            'height_cm': 175,
            'weight_kg': 70
        })
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertAlmostEqual(data['bmi'], 22.86, places=1)
        self.assertFalse(data['eligibility'])
        self.assertIn('message', data)

    def test_bmi_obese_range(self):
        """Test BMI calculation for obese range"""
        response = self.app.post('/api/bmi', json={
            'height_cm': 170,
            'weight_kg': 100
        })
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertAlmostEqual(data['bmi'], 34.6, places=1)
        self.assertTrue(data['eligibility'])
        self.assertIn('overweight', data['message'].lower())

    def test_bmi_validation_errors(self):
        """Test BMI validation errors"""
        # Test missing height
        response = self.app.post('/api/bmi', json={
            'weight_kg': 70
        })
        self.assertEqual(response.status_code, 400)

        # Test invalid height range
        response = self.app.post('/api/bmi', json={
            'height_cm': 0,
            'weight_kg': 70
        })
        self.assertEqual(response.status_code, 400)

        # Test invalid weight range
        response = self.app.post('/api/bmi', json={
            'height_cm': 175,
            'weight_kg': 600
        })
        self.assertEqual(response.status_code, 400)

    def test_bmi_invalid_data_types(self):
        """Test BMI with invalid data types"""
        response = self.app.post('/api/bmi', json={
            'height_cm': 'invalid',
            'weight_kg': 70
        })
        self.assertEqual(response.status_code, 400)

if __name__ == '__main__':
    unittest.main()
