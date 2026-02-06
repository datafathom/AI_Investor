"""
FastAPI Authentication API - Identity & Session Management
 web/api/auth_api.py
"""

from fastapi import APIRouter, HTTPException, Depends, Request, Query
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, EmailStr
from typing import Optional, Dict, Any
import logging
from web.auth_utils import generate_token, login_required
from services.communication.email_service import get_email_service
from services.system.social_auth_service import get_social_auth_service

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/auth", tags=["Authentication"])

# --- Request Models ---

class LoginRequest(BaseModel):
    email: str
    password: str

class RegisterRequest(BaseModel):
    email: str # Not strictly EmailStr to match Flask's permissive check if needed
    password: str

class MFASetupResponse(BaseModel):
    secret: str
    provisioning_uri: str

class MFAVerifyRequest(BaseModel):
    code: str
    secret: str

class SocialCallbackRequest(BaseModel):
    code: str

class AddPasswordRequest(BaseModel):
    password: str

# --- Dependency ---

async def get_current_user_id(request: Request):
    # This should match how your security middleare works
    # For now, we simulate what login_required does
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Unauthorized")
    token = auth_header.split(" ")[1]
    # In a real app, you'd decode token here
    # For now, we assume user_id is injected or available
    return "demo-user"

# --- Endpoints ---

@router.post("/login")
async def login(request_data: LoginRequest):
    """
    Login endpoint with support for standard DB lookup and developer fallback.
    """
    logger.info("AUTH_DEBUG: /login endpoint hit (FastAPI)")
    email = request_data.email.strip()
    password = request_data.password.strip()

    # 1. HARDCODED ADMIN FALLBACK
    if email == 'admin' and password == 'makeMoney':
        logger.info("AUTH_FALLBACK_ACTIVE: Success for admin user")
        user_data = {
            "id": 0, "email": "admin@example.com", "username": "admin",
            "role": "admin", "is_verified": True
        }
        token = generate_token(user_id=user_data["id"], role=user_data["role"])
        return {
            'token': token,
            'user': user_data
        }

    # 2. Database Lookup
    user_data = None
    try:
        social_service = get_social_auth_service()
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
        logger.warning(f"AUTH_FAIL: DB connection unavailable during login for {email}: {e}")
        # If DB is down and it's not the admin fallback (already handled), 
        # we can't verify standard users.
        if email != 'admin':
             raise HTTPException(
                 status_code=503, 
                 detail="Security service temporarily unavailable. Please try again later."
             )

    # 3. Standard Password Verification
    if user_data:
        provided_hash = f"mock_hash_{password[::-1]}"
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
    
    if not email or not password:
        raise HTTPException(status_code=400, detail="Email and password required")

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
        return HTMLResponse(content="Email Verified! You can now log in.", status_code=200)
    raise HTTPException(status_code=404, detail="User not found")

@router.post("/add-password")
async def add_password(
    request_data: AddPasswordRequest,
    user_id: str = Depends(get_current_user_id)
):
    password = request_data.password
    if not password:
        raise HTTPException(status_code=400, detail="Password required")
        
    social_service = get_social_auth_service()
    # In a real app, you'd use the user_id from token
    # For now, we match Flask's logic
    user_record = social_service._get_user_by_id(user_id) if user_id != "demo-user" else social_service._get_user_by_email("admin@example.com")
            
    if not user_record:
        raise HTTPException(status_code=404, detail="User session invalid")
        
    success = social_service.set_password(user_record["email"], password)
    if success:
        return {"message": "Password added successfully. You can now login via email or social provider."}
    raise HTTPException(status_code=500, detail="Failed to set password")

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

