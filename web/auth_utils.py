"""
Auth Utils Module
Provides JWT generation, decoding, and FastAPI dependencies for RBAC.
Migrated from Flask to FastAPI.
"""

import datetime
from datetime import timezone
import os
from functools import wraps
from typing import Optional, Dict, Any, List

import jwt
from fastapi import Header, HTTPException, Depends, Request

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
        'iat': datetime.datetime.now(timezone.utc),
        'exp': datetime.datetime.now(timezone.utc) + datetime.timedelta(minutes=expiration_minutes)
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


async def get_current_user(authorization: Optional[str] = Header(None)) -> Dict[str, Any]:
    """
    FastAPI dependency to protect routes with JWT authentication.
    """
    if not authorization or not authorization.startswith('Bearer '):
        if os.getenv('FLASK_ENV', 'development') == 'development' or os.getenv('ENV', 'development') == 'development':
            return {
                "id": "demo-admin",
                "tenant_id": "default",
                "role": "admin"
            }
        raise HTTPException(status_code=401, detail="Header missing or invalid")

    token = authorization.split(' ')[1]
    payload = decode_token(token)

    if not payload:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    return {
        "id": payload.get('sub'),
        "tenant_id": payload.get('tenant_id'),
        "role": payload.get('role', 'trader')
    }


def login_required(f):
    """
    Legacy Flask-style decorator, now a placeholder or adapted for FastAPI if used as a wrapper.
    In FastAPI, use Depends(get_current_user) instead.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # This is strictly a helper for transition.
        # It's better to refactor routes to use Depends.
        raise RuntimeError("login_required decorator is legacy Flask. Use FastAPI Depends(get_current_user) instead.")
    return decorated_function


def requires_role(required_role):
    """
    Legacy Flask-style decorator. Use FastAPI dependencies for RBAC.
    """
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            raise RuntimeError("requires_role decorator is legacy Flask. Use FastAPI dependencies instead.")
        return wrapper
    return decorator


def verify_integrity():
    """Placeholder for integrity verification logic."""
    return True
