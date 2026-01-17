
import jwt
import datetime
from functools import wraps
from flask import request, jsonify, g
import os

# Configuration
SECRET_KEY = os.getenv('SECRET_KEY', 'default_secret_key_change_me')
ALGORITHM = 'HS256'

def generate_token(user_id, tenant_id='default', expiration_minutes=60*24):
    """
    Generate a JWT token for a user.
    """
    payload = {
        'sub': str(user_id),
        'tenant_id': tenant_id,
        'iat': datetime.datetime.utcnow(),
        'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=expiration_minutes)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def decode_token(token):
    """
    Decode and verify a JWT token.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

def login_required(f):
    """
    Decorator to protect routes with JWT authentication.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return jsonify({'error': 'Missing or invalid token'}), 401
        
        token = auth_header.split(' ')[1]
        payload = decode_token(token)
        
        if not payload:
            return jsonify({'error': 'Invalid or expired token'}), 401
            
        # Store user info in flask global context
        g.user_id = payload.get('sub')
        g.tenant_id = payload.get('tenant_id')
        
        return f(*args, **kwargs)
    return decorated_function
