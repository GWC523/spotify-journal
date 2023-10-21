from flask import Blueprint, request, jsonify

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    data = request.get_json()

    if 'username' not in data or 'password' not in data:
        return jsonify({'error': 'Invalid request. Missing username or password.'}), 400
    
    # Get username and password from the JSON data
    username = data['username']
    password = data['password']

    if username == 'example' and password == 'password':
        return jsonify({'message': 'Login successful'}), 200
    else:
        return jsonify({'error': 'Invalid credentials'}), 401
    
@auth.route('/sign-up', methods=['GET', 'POST'])
def signup():
    # Get the JSON data from the request body
    data = request.get_json()

    # Check if the required fields are present in the JSON data
    if 'username' not in data or 'password' not in data:
        return jsonify({'error': 'Invalid request. Missing username or password.'}), 400

    # Get username and password from the JSON data
    email = data['email']
    username = data['username']
    firstName = data['firstName']
    lastName = data['lastName']
    password = data['password']

    #Add checker for the params




