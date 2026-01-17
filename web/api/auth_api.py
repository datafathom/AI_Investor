
from flask import Blueprint, jsonify, request
from web.auth_utils import generate_token

auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    # Mock Authentication for Verification
    if username == 'admin' and password == 'admin':
        token = generate_token(user_id=1, tenant_id='default')
        return jsonify({
            'token': token,
            'user': {
                'id': 1,
                'username': 'admin',
                'role': 'admin'
            }
        })
    
    return jsonify({'error': 'Invalid credentials'}), 401

@auth_bp.route('/register', methods=['POST'])
def register():
    # Mock Registration
    return jsonify({
        'message': 'User registered successfully',
        'user': {
            'id': 2,
            'username': request.get_json().get('username')
        }
    })
