from fastapi import APIRouter
import uuid
from typing import List, Optional
from pydantic import BaseModel
from web.auth_utils import generate_token

router = APIRouter(prefix="/api/v1/auth", tags=["Auth"])

class ApiKey(BaseModel):
    name: str
    scopes: List[str]

class AuthRequest(BaseModel):
    email: str
    password: str

import os

# Configuration from environment
ADMIN_USER = os.getenv('ADMIN_USER', 'admin')
ADMIN_PASS = os.getenv('ADMIN_PASSWORD', 'makeMoney')
TEST_USER = os.getenv('TEST_USER_EMAIL', 'test@aiinvestor.com')
TEST_PASS = os.getenv('TEST_USER_PASSWORD', 'test_pass_123')

# In-memory user store for dev/testing
_users_db = {
    ADMIN_USER: {
        "id": "admin-001",
        "email": ADMIN_USER,
        "password": ADMIN_PASS,
        "role": "admin",
        "verified": True
    },
    TEST_USER: {
        "id": "demo-user-001",
        "email": TEST_USER,
        "password": TEST_PASS,
        "role": "admin",
        "verified": True
    }
}

@router.post('/register')
async def register_user(auth: AuthRequest):
    """Registration disabled for now to restrict accounts."""
    return {"success": False, "detail": "Registration is currently restricted to pre-defined accounts."}

@router.post('/login')
async def login_user(auth: AuthRequest):
    """Login with email/password and receive JWT token."""
    # Check if user exists
    user = _users_db.get(auth.email)
    
    if not user:
        return {"success": False, "detail": "Invalid credentials"}
    
    # Verify password (in prod, use hashing!)
    if auth.password != user["password"]:
        return {"success": False, "detail": "Invalid credentials"}
    
    if not user.get("verified"):
        return {"success": False, "detail": "Account not verified"}
    
    # In prod, verify password hash
    token = generate_token(user["id"], role=user.get("role", "trader"))
    
    return {
        "success": True,
        "token": token,
        "user": {
            "id": user["id"],
            "email": auth.email,
            "role": user.get("role", "trader")
        }
    }

@router.get('/verify/{email}')
async def verify_account(email: str):
    """Verify an account via email."""
    if email in _users_db:
        _users_db[email]["verified"] = True
        return {"success": True, "message": f"Account {email} verified successfully"}
    return {"success": False, "detail": "User not found"}

@router.get('/sessions')
async def get_active_sessions():
    """List active user sessions."""
    return {"success": True, "data": [
        {"id": "sess_01", "device": "Chrome / Windows", "ip": "192.168.1.50", "location": "New York, US", "current": True, "expires": "2h"},
        {"id": "sess_02", "device": "Mobile App / iOS", "ip": "10.0.0.1", "location": "New York, US", "current": False, "expires": "5d"}
    ]}

@router.delete('/sessions/{id}')
async def kill_session(id: str):
    """Terminate a session."""
    return {"success": True, "data": {"status": "TERMINATED"}}

@router.get('/api-keys')
async def list_api_keys():
    """List generated API keys."""
    return {"success": True, "data": [
        {"id": "key_01", "name": "Trading Bot A", "prefix": "sk_live_...", "created": "2025-01-15", "last_used": "2 mins ago"},
        {"id": "key_02", "name": "Data Scraper", "prefix": "sk_test_...", "created": "2025-02-01", "last_used": "1 hour ago"}
    ]}

@router.post('/api-keys')
async def create_api_key(key: ApiKey):
    """Create a new API key."""
    return {"success": True, "data": {
        "id": str(uuid.uuid4()),
        "key": f"sk_live_{uuid.uuid4().hex[:24]}", # Show once
        "name": key.name
    }}

@router.delete('/api-keys/{id}')
async def revoke_api_key(id: str):
    """Revoke an API key."""
    return {"success": True, "data": {"status": "REVOKED"}}
