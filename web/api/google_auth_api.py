"""
==============================================================================
FILE: web/api/google_auth_api.py
ROLE: Google OAuth REST API (FastAPI)
PURPOSE: RESTful endpoints for Google OAuth authentication flow.
==============================================================================
"""

from fastapi import APIRouter, HTTPException, Query, Request, Header, Depends
from fastapi.responses import RedirectResponse, JSONResponse
from pydantic import BaseModel
import logging
import asyncio
import secrets
from typing import Optional, Dict, Any

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/google_auth", tags=["Google Auth"])


def _get_google_auth_service():
    """Lazy-load Google Auth service."""
    from services.auth.google_auth import get_google_auth_service
    return get_google_auth_service()


def get_google_auth_provider():
    return _get_google_auth_service()


# In-memory state store (should be Redis in production)
_oauth_states: Dict[str, Dict[str, Any]] = {}


class CallbackRequest(BaseModel):
    code: str
    state: str
    error: Optional[str] = None


class RefreshRequest(BaseModel):
    refresh_token: str


class RevokeRequest(BaseModel):
    token: str


@router.get("/login")
async def initiate_login(
    scopes: Optional[str] = Query(None),
    redirect: bool = Query(False, alias="redirect"),
    auth_service = Depends(get_google_auth_provider)
):
    """
    Initiate Google OAuth login flow.
    """
    try:
        scope_list = scopes.split(',') if scopes else None
        
        # Generate CSRF state token
        state = secrets.token_urlsafe(32)
        
        # Store state for verification
        _oauth_states[state] = {
            "scopes": scope_list,
            "created_at": asyncio.get_event_loop().time() if asyncio.get_event_loop().is_running() else 0
        }
        
        # Get authorization URL
        auth_url = auth_service.get_authorization_url(
            state=state,
            scopes=scope_list,
            access_type="offline",
            prompt="consent"
        )
        
        if redirect:
            return RedirectResponse(auth_url)
        
        return {
            "success": True,
            "data": {
                "authorization_url": auth_url,
                "state": state
            }
        }
    except Exception as e:
        logger.exception("Failed to initiate Google login")
        return JSONResponse(status_code=500, content={"success": False, "detail": str(e)})


@router.get("/callback")
async def handle_callback_get(
    code: Optional[str] = Query(None),
    state: Optional[str] = Query(None),
    error: Optional[str] = Query(None),
    auth_service = Depends(get_google_auth_provider)
):
    """Handle Google OAuth callback via GET."""
    return await _process_callback(code, state, error, auth_service)


@router.post("/callback")
async def handle_callback_post(
    request: CallbackRequest,
    auth_service = Depends(get_google_auth_provider)
):
    """Handle Google OAuth callback via POST."""
    return await _process_callback(request.code, request.state, request.error, auth_service)


async def _process_callback(
    code: Optional[str],
    state: Optional[str],
    error: Optional[str],
    auth_service
):
    if error:
        return JSONResponse(status_code=400, content={"success": False, "detail": f"OAuth authorization failed: {error}"})
    
    if not code:
        return JSONResponse(status_code=400, content={"success": False, "detail": "Missing authorization code"})
    
    if not state:
        return JSONResponse(status_code=400, content={"success": False, "detail": "Missing state parameter"})
    
    if state not in _oauth_states:
        return JSONResponse(status_code=400, content={"success": False, "detail": "Invalid state token"})
    
    _oauth_states.pop(state)
    
    try:
        token_info = await auth_service.exchange_code_for_tokens(code, state)
        
        profile = await auth_service.get_user_profile(token_info.access_token)
        
        from services.system.social_auth_service import get_social_auth_service
        social_auth = get_social_auth_service()
        
        user_result = social_auth.handle_callback("google", code)
        
        logger.info(f"Google OAuth successful for user: {profile.email}")
        
        return {
            "success": True,
            "data": {
                "user": {
                    "id": user_result.get("user", {}).get("id"),
                    "username": user_result.get("user", {}).get("username"),
                    "email": profile.email,
                    "name": profile.name,
                    "picture": profile.picture,
                    "verified_email": profile.verified_email
                },
                "tokens": {
                    "access_token": token_info.access_token,
                    "refresh_token": token_info.refresh_token,
                    "expires_at": token_info.expires_at.isoformat(),
                    "scopes": token_info.scopes
                },
                "session_token": user_result.get("token")
            }
        }
    except Exception as e:
        logger.exception("Google OAuth callback failed")
        return JSONResponse(status_code=500, content={"success": False, "detail": str(e)})


@router.post("/refresh")
async def refresh_token(
    request: RefreshRequest,
    auth_service = Depends(get_google_auth_provider)
):
    """Refresh expired access token."""
    try:
        token_info = await auth_service.refresh_access_token(request.refresh_token)
        
        return {
            "success": True,
            "data": {
                "access_token": token_info.access_token,
                "expires_at": token_info.expires_at.isoformat(),
                "scopes": token_info.scopes
            }
        }
    except Exception as e:
        logger.exception("Token refresh failed")
        return JSONResponse(status_code=500, content={"success": False, "detail": str(e)})


@router.post("/revoke")
async def revoke_token(
    request: RevokeRequest,
    auth_service = Depends(get_google_auth_provider)
):
    """Revoke Google access/refresh token."""
    try:
        revoked = await auth_service.revoke_token(request.token)
        
        if revoked:
            return {
                "success": True,
                "data": {
                    "message": "Token revoked successfully"
                }
            }
        else:
            return JSONResponse(status_code=500, content={"success": False, "detail": "Failed to revoke token"})
    except HTTPException:
        raise
    except Exception as e:
        logger.exception("Token revocation failed")
        return JSONResponse(status_code=500, content={"success": False, "detail": str(e)})


@router.get("/profile")
async def get_profile(
    authorization: str = Header(...),
    auth_service = Depends(get_google_auth_provider)
):
    """Get current user's Google profile."""
    try:
        if not authorization.startswith('Bearer '):
            raise HTTPException(status_code=401, detail="Missing or invalid Authorization header")
        
        access_token = authorization[7:]
        
        profile = await auth_service.get_user_profile(access_token)
        
        return {
            "success": True,
            "data": {
                "google_id": profile.google_id,
                "email": profile.email,
                "name": profile.name,
                "picture": profile.picture,
                "verified_email": profile.verified_email,
                "locale": profile.locale
            }
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.exception("Failed to get profile")
        return JSONResponse(status_code=500, content={"success": False, "detail": str(e)})
