"""
==============================================================================
FILE: web/api/facebook_auth_api.py
ROLE: Facebook OAuth REST API
PURPOSE: RESTful endpoints for Facebook OAuth authentication flow.

INTEGRATION POINTS:
    - FacebookAuthService: OAuth flow management
    - AuthAPI: Session management
    - UserService: Profile sync

ENDPOINTS:
    GET /api/v1/auth/facebook/login - Initiate OAuth flow
    GET/POST /api/v1/auth/facebook/callback - Handle OAuth callback
    POST /api/v1/auth/facebook/long-lived-token - Exchange for long-lived token
    POST /api/v1/auth/facebook/revoke - Revoke tokens

AUTHOR: AI Investor Team
CREATED: 2026-01-21
==============================================================================
"""

from flask import Blueprint, request, jsonify, redirect
import logging
import asyncio
import secrets
from typing import Optional, Dict, Any

logger = logging.getLogger(__name__)

facebook_auth_bp = Blueprint('facebook_auth', __name__, url_prefix='/api/v1/auth/facebook')


def _run_async(coro):
    """Helper to run async functions in sync context."""
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    return loop.run_until_complete(coro)


def _get_facebook_auth_service():
    """Lazy-load Facebook Auth service."""
    from services.auth.facebook_auth import get_facebook_auth_service
    return get_facebook_auth_service()


# In-memory state store (should be Redis in production)
_oauth_states: Dict[str, Dict[str, Any]] = {}


# =============================================================================
# Initiate OAuth Flow
# =============================================================================

@facebook_auth_bp.route('/login', methods=['GET'])
def initiate_login():
    """
    Initiate Facebook OAuth login flow.
    
    Query Params:
        scopes: Comma-separated list of scopes (optional)
        redirect: If true, redirects directly to Facebook
        
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
        auth_service = _get_facebook_auth_service()
        auth_url = auth_service.get_authorization_url(state=state, scopes=scopes)
        
        # Return URL or redirect based on request
        if request.args.get('redirect') == 'true':
            return redirect(auth_url)
        
        return jsonify({
            "authorization_url": auth_url,
            "state": state
        })
        
    except Exception as e:
        logger.error(f"Failed to initiate Facebook login: {e}", exc_info=True)
        return jsonify({
            "error": "Failed to initiate Facebook login",
            "message": str(e)
        }), 500


# =============================================================================
# OAuth Callback Handler
# =============================================================================

@facebook_auth_bp.route('/callback', methods=['GET', 'POST'])
def handle_callback():
    """
    Handle Facebook OAuth callback.
    
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
        auth_service = _get_facebook_auth_service()
        token_info = _run_async(auth_service.exchange_code_for_tokens(code, state))
        
        # Get user profile
        profile = _run_async(auth_service.get_user_profile(token_info.access_token))
        
        # Link or create user account
        from services.system.social_auth_service import get_social_auth_service
        social_auth = get_social_auth_service()
        
        # Create or link account
        user_result = social_auth.handle_callback("facebook", code)
        
        logger.info(f"Facebook OAuth successful for user: {profile.email or profile.name}")
        
        return jsonify({
            "success": True,
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
        })
        
    except Exception as e:
        logger.error(f"Facebook OAuth callback failed: {e}", exc_info=True)
        return jsonify({
            "error": "OAuth callback failed",
            "message": str(e)
        }), 500


# =============================================================================
# Exchange for Long-Lived Token
# =============================================================================

@facebook_auth_bp.route('/long-lived-token', methods=['POST'])
def exchange_long_lived_token():
    """
    Exchange short-lived token for long-lived token (60 days).
    
    Request Body:
        {
            "access_token": "short_lived_token"
        }
        
    Returns:
        JSON with long-lived token
    """
    try:
        data = request.json or {}
        short_lived_token = data.get('access_token')
        
        if not short_lived_token:
            return jsonify({
                "error": "Missing access_token"
            }), 400
        
        auth_service = _get_facebook_auth_service()
        token_info = _run_async(auth_service.exchange_for_long_lived_token(short_lived_token))
        
        return jsonify({
            "access_token": token_info.access_token,
            "expires_at": token_info.expires_at.isoformat() if token_info.expires_at else None
        })
        
    except Exception as e:
        logger.error(f"Long-lived token exchange failed: {e}", exc_info=True)
        return jsonify({
            "error": "Token exchange failed",
            "message": str(e)
        }), 500


# =============================================================================
# Revoke Token Endpoint
# =============================================================================

@facebook_auth_bp.route('/revoke', methods=['POST'])
def revoke_token():
    """
    Revoke Facebook access token.
    
    Request Body:
        {
            "access_token": "access_token_to_revoke"
        }
        
    Returns:
        JSON confirmation
    """
    try:
        data = request.json or {}
        access_token = data.get('access_token')
        
        if not access_token:
            return jsonify({
                "error": "Missing access_token"
            }), 400
        
        auth_service = _get_facebook_auth_service()
        revoked = _run_async(auth_service.revoke_token(access_token))
        
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
