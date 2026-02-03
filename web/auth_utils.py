"""
Auth Utils Module
Provides JWT generation, decoding, and Flask decorators for RBAC.
"""

import datetime
import os
from functools import wraps

import jwt
from flask import request, jsonify, g

# Configuration
SECRET_KEY = os.getenv('SECRET_KEY', 'default_secret_key_change_me')
ALGORITHM = 'HS256'


def generate_token(user_id, tenant_id='default', role='trader', expiration_minutes=60*24):
    """
    Generate a JWT token for a user.
    """
    payload = {
        'sub': str(user_id),
        'tenant_id': tenant_id,
        'role': role,
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


import asyncio

def login_required(f):
    """
    Decorator to protect routes with JWT authentication.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if request.method == 'OPTIONS':
            return f(*args, **kwargs)
            
        auth_header = request.headers.get('Authorization')

        if not auth_header or not auth_header.startswith('Bearer '):
            if os.getenv('FLASK_ENV', 'development') == 'development':
                g.user_id = 'demo-admin'
                g.tenant_id = 'default'
                g.user_role = 'admin'
                # Sync refactor: No longer using asyncio.run
                return f(*args, **kwargs)
            return jsonify({'error': 'Missing or invalid token'}), 401

        token = auth_header.split(' ')[1]
        payload = decode_token(token)

        if not payload:
            return jsonify({'error': 'Invalid or expired token'}), 401

        g.user_id = payload.get('sub')
        g.tenant_id = payload.get('tenant_id')
        g.user_role = payload.get('role', 'trader')

        if asyncio.iscoroutinefunction(f):
             # For Flask routes, if we are in an async context (like under an async worker), 
             # simply returning the coroutine might work if Flask expects it.
             # However, since this decorator is sync, we must ensure it's awaited.
             # In Flask 2.0+, if the view is async, Flask awaits it.
             # If we wrap it in a sync decorator that returns a coroutine, Flask STILL awaits it IF the decorator is also async.
             return f(*args, **kwargs)
        return f(*args, **kwargs)
    
    # If the original function was async, we should make the wrapper async too
    if asyncio.iscoroutinefunction(f):
        @wraps(f)
        async def async_decorated_function(*args, **kwargs):
            if request.method == 'OPTIONS':
                return await f(*args, **kwargs)
                
            auth_header = request.headers.get('Authorization')
            if not auth_header or not auth_header.startswith('Bearer '):
                if os.getenv('FLASK_ENV', 'development') == 'development':
                    g.user_id = 'demo-admin'
                    g.tenant_id = 'default'
                    g.user_role = 'admin'
                    return await f(*args, **kwargs)
                return jsonify({'error': 'Missing or invalid token'}), 401
            token = auth_header.split(' ')[1]
            payload = decode_token(token)
            if not payload:
                return jsonify({'error': 'Invalid or expired token'}), 401
            g.user_id = payload.get('sub')
            g.tenant_id = payload.get('tenant_id')
            g.user_role = payload.get('role', 'trader')
            return await f(*args, **kwargs)
        return async_decorated_function
        
    return decorated_function


def requires_role(required_role):
    """
    Decorator for RBAC. Assumes login_required is called BEFORE this.
    """
    def decorator(f):
        if asyncio.iscoroutinefunction(f):
            @wraps(f)
            async def async_wrapper(*args, **kwargs):
                user_role = getattr(g, 'user_role', 'guest')
                roles = ['guest', 'analyst', 'trader', 'advisor', 'admin', 'super_admin']
                try:
                    user_level = roles.index(user_role)
                    required_level = roles.index(required_role)
                except ValueError:
                    return jsonify({'error': 'Invalid Role Configuration'}), 403
                if user_level < required_level:
                    return jsonify({'error': f'Forbidden: Requires {required_role} access'}), 403
                return await f(*args, **kwargs)
            return async_wrapper
        else:
            @wraps(f)
            def wrapper(*args, **kwargs):
                user_role = getattr(g, 'user_role', 'guest')
                roles = ['guest', 'analyst', 'trader', 'advisor', 'admin', 'super_admin']
                try:
                    user_level = roles.index(user_role)
                    required_level = roles.index(required_role)
                except ValueError:
                    return jsonify({'error': 'Invalid Role Configuration'}), 403
                if user_level < required_level:
                    return jsonify({'error': f'Forbidden: Requires {required_role} access'}), 403
                return f(*args, **kwargs)
            return wrapper
    return decorator


# --- Phase 09: Supply Chain Security (Placeholder) ---
def verify_sbom_integrity():
    """Placeholder for Phase 09 SBOM verification logic."""
    return True
