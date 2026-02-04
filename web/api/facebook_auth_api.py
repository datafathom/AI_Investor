"""
==============================================================================
FILE: web/api/facebook_auth_api.py
ROLE: Facebook OAuth REST API (FastAPI)
PURPOSE: RESTful endpoints for Facebook OAuth authentication flow.
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

router = APIRouter(prefix="/api/v1/facebook_auth", tags=["Facebook Auth"])


def _get_facebook_auth_service():
    """Lazy-load Facebook Auth service."""
    from services.auth.facebook_auth import get_facebook_auth_service
    return get_facebook_auth_service()


def get_facebook_auth_provider():
    return _get_facebook_auth_service()


# In-memory state store (should be Redis in production)
_oauth_states: Dict[str, Dict[str, Any]] = {}


class CallbackRequest(BaseModel):
    code: str
    state: str
    error: Optional[str] = None


class LongLivedTokenRequest(BaseModel):
    access_token: str


class RevokeRequest(BaseModel):
    access_token: str


@router.get("/login")
async def initiate_login(
    scopes: Optional[str] = Query(None),
    redirect: bool = Query(False, alias="redirect")
):
    """
    Initiate Facebook OAuth login flow.
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
        auth_service = _get_facebook_auth_service()
        auth_url = auth_service.get_authorization_url(state=state, scopes=scope_list)
        
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
        logger.exception("Failed to initiate Facebook login")
        return JSONResponse(status_code=500, content={"success": False, "detail": str(e)})


@router.get("/callback")
async def handle_callback_get(
    code: Optional[str] = Query(None),
    state: Optional[str] = Query(None),
    error: Optional[str] = Query(None)
):
    """Handle Facebook OAuth callback via GET."""
    return await _process_callback(code, state, error)


@router.post("/callback")
async def handle_callback_post(request: CallbackRequest):
    """Handle Facebook OAuth callback via POST."""
    return await _process_callback(request.code, request.state, request.error)


async def _process_callback(code: Optional[str], state: Optional[str], error: Optional[str]):
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
        auth_service = _get_facebook_auth_service()
        token_info = await auth_service.exchange_code_for_tokens(code, state)
        
        profile = await auth_service.get_user_profile(token_info.access_token)
        
        from services.system.social_auth_service import get_social_auth_service
        social_auth = get_social_auth_service()
        
        user_result = social_auth.handle_callback("facebook", code)
        
        logger.info(f"Facebook OAuth successful for user: {profile.email or profile.name}")
        
        return {
            "success": True,
            "data": {
                "user": {
                    "id": user_result.get("user", {}).get("id"),
                    "username": user_result.get("user", {}).get("username"),
                    "email": profile.email,
                    "name": profile.name,
                    "picture": profile.picture,
                    "facebook_id": profile.facebook_id
                },
                "tokens": {
                    "access_token": token_info.access_token,
                    "expires_at": token_info.expires_at.isoformat() if token_info.expires_at else None
                },
                "session_token": user_result.get("token")
            }
        }
    except Exception as e:
        logger.exception("Facebook OAuth callback failed")
        return JSONResponse(status_code=500, content={"success": False, "detail": str(e)})


@router.post("/long-lived-token")
async def exchange_long_lived_token(request: LongLivedTokenRequest):
    """Exchange short-lived token for long-lived token (60 days)."""
    try:
        auth_service = _get_facebook_auth_service()
        token_info = await auth_service.exchange_for_long_lived_token(request.access_token)
        
        return {
            "success": True,
            "data": {
                "access_token": token_info.access_token,
                "expires_at": token_info.expires_at.isoformat() if token_info.expires_at else None
            }
        }
    except Exception as e:
        logger.exception("Long-lived token exchange failed")
        return JSONResponse(status_code=500, content={"success": False, "detail": str(e)})


@router.post("/revoke")
async def revoke_token(request: RevokeRequest):
    """Revoke Facebook access token."""
    try:
        auth_service = _get_facebook_auth_service()
        revoked = await auth_service.revoke_token(request.access_token)
        
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
