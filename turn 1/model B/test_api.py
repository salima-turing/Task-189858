import unittest
from app import app
from faker import Faker


class TestAPI(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.fake = Faker()

    def test_validate_input_with_synthetic_data(self):
        for _ in range(100):  # Generate 100 test cases with synthetic data
            data = {
                'name': self.fake.name(),
                'age': self.fake.random_int(min=0, max=150)
            }
            response = self.app.post('/validate_input', json=data)
            self.assertEqual(response.status_code, 200)

            # Test edge cases by modifying the data
            data['name'] = ''
            response = self.app.post('/validate_input', json=data)
            self.assertEqual(response.status_code, 400)
            data['name'] = 'a' * 2  # Name should be at least 3 characters long
            response = self.app.post('/validate_input', json=data)
            self.assertEqual(response.status_code, 400)
            data['age'] = -1  # Age should be between 0 and 150
            response = self.app.post('/validate_input', json=data)
            self.assertEqual(response.status_code, 400)
            data['age'] = 151  # Age should be between 0 and 150
            response = self.app.post('/validate_input', json=data)
            self.assertEqual(response.status_code, 400)
            data['age'] = 'non-integer'  # Age should be an integer
            response = self.app.post('/validate_input', json=data)
            self.assertEqual(response.status_code, 400)


if __name__ == '__main__':
    unittest.main()
