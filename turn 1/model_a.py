import unittest
from flask import Flask, request, jsonify
import requests
import json
from faker import Faker

app = Flask(__name__)


@app.route('/api/data', methods=['POST'])
def handle_data():
    try:
        data = request.get_json()
        name = data.get('name')
        age = data.get('age')

        if not isinstance(name, str) or len(name.strip()) == 0:
            return jsonify(error="Name is required and must be a string"), 400

        if not isinstance(age, int) or age < 0:
            return jsonify(error="Age must be a non-negative integer"), 400

        return jsonify(message="Data received successfully", data=data), 200
    except for KeyError:
        return jsonify(error="Invalid data format"), 400


if __name__ == '__main__':
    app.run(debug=True)


class TestAPIWithSyntheticData(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.fake = Faker()

    def test_valid_data(self):
        data = {'name': self.fake.name(), 'age': self.fake.pyint(min_value=0, max_value=100)}
        response = self.app.post('/api/data', json=data)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Data received successfully', response.data)

    def test_empty_name(self):
        data = {'name': '', 'age': self.fake.pyint()}
        response = self.app.post('/api/data', json=data)
        self.assertEqual(response.status_code, 400)
        self.assertIn(b'Name is required and must be a string', response.data)

    def test_non_string_name(self):
        data = {'name': self.fake.pyint(), 'age': self.fake.pyint()}
        response = self.app.post('/api/data', json=data)
        self.assertEqual(response.status_code, 400)
        self.assertIn(b'Name is required and must be a string', response.data)

    def test_negative_age(self):
        data = {'name': self.fake.name(), 'age': -self.fake.pyint()}
        response = self.app.post('/api/data', json=data)
        self.assertEqual(response.status_code, 400)
        self.assertIn(b'Age must be a non-negative integer', response.data)

    def test_missing_age(self):
        data = {'name': self.fake.name()}
        response = self.app.post('/api/data', json=data)
        self.assertEqual(response.status_code, 400)
        self.assertIn(b'Invalid data format', response.data)


if __name__ == '__main__':
    unittest.main()
