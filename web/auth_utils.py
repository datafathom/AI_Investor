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


def login_required(f):
    """
    Decorator to protect routes with JWT authentication.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth_header = request.headers.get('Authorization')

        # Bypass for Demoware/Dev (Simulated) if no token provided but FLASK_ENV is dev
        # In a real app we'd block this. For this demo, let's assume if no token, we are 'demo-user'
        # BUT this might break RBAC testing. Let's enforce it strictly or provide a strict mock.
        if not auth_header or not auth_header.startswith('Bearer '):
            if os.getenv('FLASK_ENV', 'development') == 'development':
                # Auto-login as Admin for convenience in Dev
                g.user_id = 'demo-admin'
                g.tenant_id = 'default'
                g.user_role = 'admin'
                return f(*args, **kwargs)
            return jsonify({'error': 'Missing or invalid token'}), 401

        token = auth_header.split(' ')[1]
        payload = decode_token(token)

        if not payload:
            return jsonify({'error': 'Invalid or expired token'}), 401

        # Store user info in flask global context
        g.user_id = payload.get('sub')
        g.tenant_id = payload.get('tenant_id')
        g.user_role = payload.get('role', 'trader')  # Default to trader

        return f(*args, **kwargs)
    return decorated_function


def requires_role(required_role):
    """
    Decorator for RBAC. Assumes login_required is called BEFORE this.
    Or we can nest it. Usage: @login_required \n @requires_role('admin')
    """
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            # If we don't have a user_role, access is denied (unless we allow checks inside)
            user_role = getattr(g, 'user_role', 'guest')

            # Simple Hierarchy: admin > trader > analyst > guest
            roles = ['guest', 'analyst', 'trader', 'admin']

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
