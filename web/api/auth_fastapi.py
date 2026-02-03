"""
FastAPI Authentication API - Identity & Session Management
Migrated from Flask web/api/auth_api.py
"""

from fastapi import APIRouter, HTTPException, Depends, Request
from pydantic import BaseModel, EmailStr
from typing import Optional, Dict, Any
import logging
from web.auth_utils import generate_token
from services.communication.email_service import get_email_service
from services.system.social_auth_service import get_social_auth_service

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/auth", tags=["Authentication"])

# --- Request Models ---

class LoginRequest(BaseModel):
    email: str
    password: str

class RegisterRequest(BaseModel):
    email: EmailStr
    password: str

class MFASetupResponse(BaseModel):
    secret: str
    provisioning_uri: str

class MFAVerifyRequest(BaseModel):
    code: str
    secret: str

class SocialCallbackRequest(BaseModel):
    code: str

# --- Endpoints ---

@router.post("/login")
async def login(request_data: LoginRequest):
    """
    Login endpoint with support for standard DB lookup and developer fallback.
    """
    email = request_data.email.strip()
    password = request_data.password.strip()

    # 1. HARDCODED ADMIN FALLBACK (Development/Infrastructure-Free Mode)
    if email == 'admin' and password == 'makeMoney':
        logger.info("AUTH_FALLBACK_ACTIVE: Success for admin user (FastAPI)")
        user_data = {
            "id": 0, "email": "admin@example.com", "username": "admin",
            "role": "admin", "is_verified": True
        }
        token = generate_token(user_id=user_data["id"], role=user_data["role"])
        return {
            'token': token,
            'user': user_data
        }

    social_service = get_social_auth_service()
    user_data = None
    
    # 2. Database Lookup (Standard Flow)
    try:
        with social_service.db.pg_cursor() as cur:
            cur.execute("""
                SELECT id, email, username, role, is_verified, password_hash, organization_id 
                FROM users WHERE username = %s OR LOWER(email) = LOWER(%s);
            """, (email, email))
            user = cur.fetchone()
            if user:
                user_data = {
                    "id": user[0], "email": user[1], "username": user[2],
                    "role": user[3], "is_verified": user[4], "password_hash": user[5],
                    "organization_id": user[6]
                }
    except Exception as e:
        logger.warning(f"Login DB connection unavailable: {e}")

    # 3. Standard Password Verification
    provided_hash = f"mock_hash_{password[::-1]}"
    if user_data:
        stored_hash = user_data.get("password_hash")
        if stored_hash == provided_hash:
            token = generate_token(user_id=user_data["id"], role=user_data["role"])
            return {
                'token': token,
                'user': {
                    'id': user_data["id"],
                    'username': user_data["username"],
                    'email': user_data["email"],
                    'role': user_data["role"],
                    'orgId': user_data.get("organization_id")
                }
            }
    
    raise HTTPException(status_code=401, detail="Invalid credentials")

@router.post("/register")
async def register(request_data: RegisterRequest):
    email = request_data.email.strip()
    password = request_data.password.strip()
    
    social_service = get_social_auth_service()
    existing_user = social_service._get_user_by_email(email)
    
    if not existing_user:
        try:
            res = social_service.handle_callback(provider='email', code=f"email:{email}")
            
            if 'user' in res and res['user']:
                user_record = res['user']
            else:
                user_record = social_service._get_user_by_email(email)
            
            if not user_record:
                logger.error(f"Failed to create user record for {email}")
                raise HTTPException(status_code=500, detail="Failed to create user")

            pwd_success = social_service.set_password(email, password, user_id=user_record['id'])
            if not pwd_success:
                logger.error(f"Failed to set password for {email} (ID: {user_record['id']})")
                raise HTTPException(status_code=500, detail="Failed to set password")
                
        except Exception as e:
            if "duplicate key" in str(e) or "UniqueViolation" in str(e):
                raise HTTPException(status_code=409, detail="User already exists. Please log in.")
            
            logger.error(f"Registration failed for {email}: {e}")
            raise HTTPException(status_code=500, detail=str(e))
    else:
        user_record = existing_user

    if not user_record:
        raise HTTPException(status_code=500, detail="Internal registration error - record missing")

    # Send Verification Email
    try:
        verification_url = f"http://localhost:5050/api/auth/verify-email?email={email}&token=mock_verify_token"
        email_service = get_email_service()
        email_service.send_transactional_email(
            to=email,
            template='email_verification',
            context={'verification_url': verification_url}
        )
    except Exception as e:
        logger.error(f"Failed to send verification email to {email}: {e}")
        pass

    return {
        'message': 'User registered successfully. Please check your email for verification.',
        'user': {
            'id': user_record["id"],
            'username': user_record["username"],
            'email': email
        }
    }

@router.get("/verify-email")
async def verify_email(email: str, token: str):
    if token != 'mock_verify_token':
        raise HTTPException(status_code=400, detail="Invalid verification request")
        
    success = get_social_auth_service().verify_email(email)
    if success:
        from fastapi.responses import HTMLResponse
        return HTMLResponse(content="Email Verified! You can now log in.", status_code=200)
    raise HTTPException(status_code=404, detail="User not found")

@router.post("/mfa/setup", response_model=MFASetupResponse)
async def mfa_setup():
    from services.system.totp_service import get_totp_service
    service = get_totp_service()
    secret = service.generate_new_secret()
    uri = service.get_provisioning_uri(secret, "admin")
    return MFASetupResponse(secret=secret, provisioning_uri=uri)

@router.post("/mfa/verify")
async def mfa_verify(data: MFAVerifyRequest):
    from services.system.totp_service import get_totp_service
    service = get_totp_service()
    is_valid = service.verify_code(data.secret, data.code)
    if is_valid:
        return {"valid": True, "message": "MFA Verified"}
    raise HTTPException(status_code=401, detail="Invalid Code")

@router.get("/social/login/{provider}")
async def social_login(provider: str):
    url = get_social_auth_service().initiate_auth_flow(provider)
    return {"redirect_url": url}

@router.post("/social/callback/{provider}")
async def social_callback(provider: str, data: SocialCallbackRequest):
    try:
        result = get_social_auth_service().handle_callback(provider, data.code)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
