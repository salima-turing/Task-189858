
from flask import Flask, request, jsonify
app = Flask(__name__)

@app.route('/validate_input', methods=['POST'])
def validate_input():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    name = data.get('name')
    age = data.get('age')

    if not name or len(name) < 3:
        return jsonify({'error': 'Name is required and must be at least 3 characters long'}), 400

    try:
        age = int(age)
        if age < 0 or age > 150:
            return jsonify({'error': 'Age must be between 0 and 150'}), 400
    except ValueError:
        return jsonify({'error': 'Age must be an integer'}), 400
    return jsonify({'message': 'Input is valid'}), 200

if __name__ == '__main__':
    app.run(debug=True)
