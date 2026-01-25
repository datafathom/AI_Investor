"""
==============================================================================
FILE: web/api/google_auth_api.py
ROLE: Google OAuth REST API
PURPOSE: RESTful endpoints for Google OAuth authentication flow.

INTEGRATION POINTS:
    - GoogleAuthService: OAuth flow management
    - AuthAPI: Session management
    - UserService: Profile sync

ENDPOINTS:
    GET /api/v1/auth/google/login - Initiate OAuth flow
    POST /api/v1/auth/google/callback - Handle OAuth callback
    POST /api/v1/auth/google/refresh - Refresh access token
    POST /api/v1/auth/google/revoke - Revoke tokens

AUTHOR: AI Investor Team
CREATED: 2026-01-21
==============================================================================
"""

from flask import Blueprint, request, jsonify, redirect, session
import logging
import asyncio
import secrets
from typing import Optional, Dict, Any

logger = logging.getLogger(__name__)

google_auth_bp = Blueprint('google_auth', __name__, url_prefix='/api/v1/auth/google')


def _run_async(coro):
    """Helper to run async functions in sync context."""
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    return loop.run_until_complete(coro)


def _get_google_auth_service():
    """Lazy-load Google Auth service."""
    from services.auth.google_auth import get_google_auth_service
    return get_google_auth_service()


# In-memory state store (should be Redis in production)
_oauth_states: Dict[str, Dict[str, Any]] = {}


# =============================================================================
# Initiate OAuth Flow
# =============================================================================

@google_auth_bp.route('/login', methods=['GET'])
def initiate_login():
    """
    Initiate Google OAuth login flow.
    
    Query Params:
        scopes: Comma-separated list of scopes (optional)
        redirect_uri: Custom redirect URI (optional)
        
    Returns:
        JSON with authorization URL or redirects directly
    """
    try:
        scopes_param = request.args.get('scopes', '')
        scopes = scopes_param.split(',') if scopes_param else None
        
        # Generate CSRF state token
        state = secrets.token_urlsafe(32)
        
        # Store state for verification
        _oauth_states[state] = {
            "scopes": scopes,
            "created_at": asyncio.get_event_loop().time() if asyncio.get_event_loop().is_running() else 0
        }
        
        # Get authorization URL
        auth_service = _get_google_auth_service()
        auth_url = auth_service.get_authorization_url(
            state=state,
            scopes=scopes,
            access_type="offline",  # Request refresh token
            prompt="consent"
        )
        
        # Return URL or redirect based on request
        if request.args.get('redirect') == 'true':
            return redirect(auth_url)
        
        return jsonify({
            "authorization_url": auth_url,
            "state": state
        })
        
    except Exception as e:
        logger.error(f"Failed to initiate Google login: {e}", exc_info=True)
        return jsonify({
            "error": "Failed to initiate Google login",
            "message": str(e)
        }), 500


# =============================================================================
# OAuth Callback Handler
# =============================================================================

@google_auth_bp.route('/callback', methods=['GET', 'POST'])
def handle_callback():
    """
    Handle Google OAuth callback.
    
    Query Params (GET) or Body (POST):
        code: Authorization code
        state: CSRF state token
        error: Error code (if OAuth failed)
        
    Returns:
        JSON with user info and session token
    """
    try:
        # Get parameters from query string or body
        if request.method == 'GET':
            code = request.args.get('code')
            state = request.args.get('state')
            error = request.args.get('error')
        else:
            data = request.json or {}
            code = data.get('code')
            state = data.get('state')
            error = data.get('error')
        
        if error:
            return jsonify({
                "error": "OAuth authorization failed",
                "error_code": error
            }), 400
        
        if not code:
            return jsonify({
                "error": "Missing authorization code"
            }), 400
        
        if not state:
            return jsonify({
                "error": "Missing state parameter"
            }), 400
        
        # Verify state token
        if state not in _oauth_states:
            return jsonify({
                "error": "Invalid state token"
            }), 400
        
        state_data = _oauth_states.pop(state)  # Remove used state
        
        # Exchange code for tokens
        auth_service = _get_google_auth_service()
        token_info = _run_async(auth_service.exchange_code_for_tokens(code, state))
        
        # Get user profile
        profile = _run_async(auth_service.get_user_profile(token_info.access_token))
        
        # Link or create user account
        from services.system.social_auth_service import get_social_auth_service
        social_auth = get_social_auth_service()
        
        # Create or link account
        # In production, this would check database for existing Google-linked account
        user_result = social_auth.handle_callback("google", code)
        
        # Store tokens (in production, encrypt and store in database)
        # For now, return in response (frontend should store securely)
        
        logger.info(f"Google OAuth successful for user: {profile.email}")
        
        return jsonify({
            "success": True,
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
        })
        
    except Exception as e:
        logger.error(f"Google OAuth callback failed: {e}", exc_info=True)
        return jsonify({
            "error": "OAuth callback failed",
            "message": str(e)
        }), 500


# =============================================================================
# Refresh Token Endpoint
# =============================================================================

@google_auth_bp.route('/refresh', methods=['POST'])
def refresh_token():
    """
    Refresh expired access token.
    
    Request Body:
        {
            "refresh_token": "refresh_token_string"
        }
        
    Returns:
        JSON with new access token
    """
    try:
        data = request.json or {}
        refresh_token = data.get('refresh_token')
        
        if not refresh_token:
            return jsonify({
                "error": "Missing refresh_token"
            }), 400
        
        auth_service = _get_google_auth_service()
        token_info = _run_async(auth_service.refresh_access_token(refresh_token))
        
        return jsonify({
            "access_token": token_info.access_token,
            "expires_at": token_info.expires_at.isoformat(),
            "scopes": token_info.scopes
        })
        
    except Exception as e:
        logger.error(f"Token refresh failed: {e}", exc_info=True)
        return jsonify({
            "error": "Token refresh failed",
            "message": str(e)
        }), 500


# =============================================================================
# Revoke Token Endpoint
# =============================================================================

@google_auth_bp.route('/revoke', methods=['POST'])
def revoke_token():
    """
    Revoke Google access/refresh token.
    
    Request Body:
        {
            "token": "access_token_or_refresh_token"
        }
        
    Returns:
        JSON confirmation
    """
    try:
        data = request.json or {}
        token = data.get('token')
        
        if not token:
            return jsonify({
                "error": "Missing token"
            }), 400
        
        auth_service = _get_google_auth_service()
        revoked = _run_async(auth_service.revoke_token(token))
        
        if revoked:
            return jsonify({
                "success": True,
                "message": "Token revoked successfully"
            })
        else:
            return jsonify({
                "error": "Failed to revoke token"
            }), 500
        
    except Exception as e:
        logger.error(f"Token revocation failed: {e}", exc_info=True)
        return jsonify({
            "error": "Token revocation failed",
            "message": str(e)
        }), 500


# =============================================================================
# Profile Endpoint
# =============================================================================

@google_auth_bp.route('/profile', methods=['GET'])
def get_profile():
    """
    Get current user's Google profile.
    
    Headers:
        Authorization: Bearer {access_token}
        
    Returns:
        JSON with user profile
    """
    try:
        auth_header = request.headers.get('Authorization', '')
        if not auth_header.startswith('Bearer '):
            return jsonify({
                "error": "Missing or invalid Authorization header"
            }), 401
        
        access_token = auth_header[7:]  # Remove "Bearer " prefix
        
        auth_service = _get_google_auth_service()
        profile = _run_async(auth_service.get_user_profile(access_token))
        
        return jsonify({
            "google_id": profile.google_id,
            "email": profile.email,
            "name": profile.name,
            "picture": profile.picture,
            "verified_email": profile.verified_email,
            "locale": profile.locale
        })
        
    except Exception as e:
        logger.error(f"Failed to get profile: {e}", exc_info=True)
        return jsonify({
            "error": "Failed to retrieve profile",
            "message": str(e)
        }), 500
