"""
==============================================================================
FILE: services/auth/facebook_auth.py
ROLE: Facebook OAuth Authentication Service
PURPOSE: Handles Facebook OAuth2 flow for SSO login and provides access tokens
         for Facebook Graph API (hype ingestion, profile data).

INTEGRATION POINTS:
    - AuthAPI: OAuth callback handling
    - UserService: Profile sync and account linking
    - FacebookHypeService: Social sentiment monitoring (requires pages_read_engagement)

SCOPES SUPPORTED:
    - email (basic profile email)
    - public_profile (name, picture)
    - pages_read_engagement (read page posts for hype tracking)
    - pages_show_list (list user's pages)

AUTHOR: AI Investor Team
CREATED: 2026-01-21
==============================================================================
"""

import logging
import asyncio
import httpx
from typing import Dict, Any, Optional
from datetime import datetime, timedelta
from dataclasses import dataclass

logger = logging.getLogger(__name__)


@dataclass
class FacebookUserProfile:
    """Facebook user profile data"""
    facebook_id: str
    name: str
    email: Optional[str] = None
    picture: Optional[str] = None
    verified: bool = False


@dataclass
class TokenInfo:
    """OAuth token information"""
    access_token: str
    expires_at: Optional[datetime] = None
    token_type: str = "Bearer"


class FacebookAuthService:
    """
    Facebook OAuth2 authentication service.
    Handles OAuth flow, token management, and profile retrieval.
    """
    
    # OAuth2 endpoints
    AUTHORIZATION_BASE_URL = "https://www.facebook.com/v18.0/dialog/oauth"
    TOKEN_URL = "https://graph.facebook.com/v18.0/oauth/access_token"
    TOKEN_EXCHANGE_URL = "https://graph.facebook.com/v18.0/oauth/access_token"
    USERINFO_URL = "https://graph.facebook.com/v18.0/me"
    LONG_LIVED_TOKEN_URL = "https://graph.facebook.com/v18.0/oauth/access_token"
    
    # OAuth2 scopes
    SCOPES = [
        "email",
        "public_profile",
        "pages_read_engagement",  # For hype ingestion
        "pages_show_list"  # List user's pages
    ]
    
    def __init__(
        self,
        app_id: Optional[str] = None,
        app_secret: Optional[str] = None,
        redirect_uri: Optional[str] = None,
        mock: bool = False
    ):
        """
        Initialize Facebook OAuth service.
        
        Args:
            app_id: Facebook App ID
            app_secret: Facebook App Secret
            redirect_uri: OAuth redirect URI
            mock: Use mock mode if True
        """
        self.mock = mock
        self.app_id = app_id
        self.app_secret = app_secret
        self.redirect_uri = redirect_uri
    
    def get_authorization_url(
        self,
        state: Optional[str] = None,
        scopes: Optional[list] = None
    ) -> str:
        """
        Generate Facebook OAuth authorization URL.
        
        Args:
            state: CSRF protection state token
            scopes: List of scopes to request (defaults to full)
            
        Returns:
            Authorization URL
        """
        if self.mock:
            return f"https://mock-facebook-auth.com/authorize?state={state or 'mock_state'}"
        
        if not self.app_id or not self.redirect_uri:
            raise RuntimeError("Facebook OAuth not configured. Check app credentials.")
        
        requested_scopes = scopes or self.SCOPES
        scope_string = ",".join(requested_scopes)
        
        params = {
            "client_id": self.app_id,
            "redirect_uri": self.redirect_uri,
            "scope": scope_string,
            "response_type": "code"
        }
        
        if state:
            params["state"] = state
        
        query_string = "&".join([f"{k}={v}" for k, v in params.items()])
        return f"{self.AUTHORIZATION_BASE_URL}?{query_string}"
    
    async def exchange_code_for_tokens(
        self,
        authorization_code: str,
        state: Optional[str] = None
    ) -> TokenInfo:
        """
        Exchange authorization code for access token.
        
        Args:
            authorization_code: OAuth authorization code from callback
            state: CSRF state token (should match request)
            
        Returns:
            TokenInfo with access token and expiration
        """
        if self.mock:
            await asyncio.sleep(0.2)
            return TokenInfo(
                access_token="mock_access_token",
                expires_at=datetime.now() + timedelta(hours=2)
            )
        
        if not self.app_id or not self.app_secret or not self.redirect_uri:
            raise RuntimeError("Facebook OAuth not configured.")
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    self.TOKEN_URL,
                    params={
                        "client_id": self.app_id,
                        "client_secret": self.app_secret,
                        "redirect_uri": self.redirect_uri,
                        "code": authorization_code
                    }
                )
                response.raise_for_status()
                data = response.json()
                
                access_token = data.get("access_token")
                expires_in = data.get("expires_in", 7200)  # Default 2 hours
                
                expires_at = datetime.now() + timedelta(seconds=expires_in) if expires_in else None
                
                return TokenInfo(
                    access_token=access_token,
                    expires_at=expires_at
                )
        except Exception as e:
            logger.error(f"Token exchange failed: {e}")
            raise RuntimeError(f"Failed to exchange code for tokens: {str(e)}")
    
    async def exchange_for_long_lived_token(
        self,
        short_lived_token: str
    ) -> TokenInfo:
        """
        Exchange short-lived token for long-lived token (60 days).
        
        Args:
            short_lived_token: Short-lived access token
            
        Returns:
            TokenInfo with long-lived token
        """
        if self.mock:
            await asyncio.sleep(0.2)
            return TokenInfo(
                access_token="mock_long_lived_token",
                expires_at=datetime.now() + timedelta(days=60)
            )
        
        if not self.app_secret:
            raise RuntimeError("Facebook App Secret not configured.")
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    self.LONG_LIVED_TOKEN_URL,
                    params={
                        "grant_type": "fb_exchange_token",
                        "client_id": self.app_id,
                        "client_secret": self.app_secret,
                        "fb_exchange_token": short_lived_token
                    }
                )
                response.raise_for_status()
                data = response.json()
                
                access_token = data.get("access_token")
                expires_in = data.get("expires_in", 5184000)  # 60 days
                
                expires_at = datetime.now() + timedelta(seconds=expires_in)
                
                return TokenInfo(
                    access_token=access_token,
                    expires_at=expires_at
                )
        except Exception as e:
            logger.error(f"Long-lived token exchange failed: {e}")
            raise RuntimeError(f"Failed to exchange for long-lived token: {str(e)}")
    
    async def get_user_profile(self, access_token: str) -> FacebookUserProfile:
        """
        Retrieve user profile from Facebook Graph API.
        
        Args:
            access_token: Valid Facebook access token
            
        Returns:
            FacebookUserProfile with user information
        """
        if self.mock:
            await asyncio.sleep(0.1)
            return FacebookUserProfile(
                facebook_id="mock_facebook_id_123",
                name="Mock User",
                email="user@example.com",
                picture="https://via.placeholder.com/150",
                verified=False
            )
        
        try:
            async with httpx.AsyncClient() as client:
                # Get basic profile
                response = await client.get(
                    self.USERINFO_URL,
                    params={
                        "access_token": access_token,
                        "fields": "id,name,email,picture"
                    }
                )
                response.raise_for_status()
                data = response.json()
                
                # Get picture URL separately
                picture_url = None
                if "picture" in data:
                    picture_data = data["picture"]
                    if isinstance(picture_data, dict) and "data" in picture_data:
                        picture_url = picture_data["data"].get("url")
                
                return FacebookUserProfile(
                    facebook_id=data.get("id", ""),
                    name=data.get("name", ""),
                    email=data.get("email"),
                    picture=picture_url,
                    verified=False  # Facebook doesn't provide verified status in basic API
                )
        except Exception as e:
            logger.error(f"Failed to get user profile: {e}")
            raise RuntimeError(f"Failed to retrieve user profile: {str(e)}")
    
    async def revoke_token(self, access_token: str) -> bool:
        """
        Revoke access token.
        
        Args:
            access_token: Access token to revoke
            
        Returns:
            True if revoked successfully
        """
        if self.mock:
            logger.info(f"[MOCK] Revoked token: {access_token[:20]}...")
            return True
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.delete(
                    "https://graph.facebook.com/v18.0/me/permissions",
                    params={"access_token": access_token}
                )
                response.raise_for_status()
                return True
        except Exception as e:
            logger.error(f"Token revocation failed: {e}")
            return False


# Singleton instance
_facebook_auth_service: Optional[FacebookAuthService] = None


def get_facebook_auth_service(mock: bool = True) -> FacebookAuthService:
    """
    Get singleton Facebook OAuth service instance.
    
    Args:
        mock: Use mock mode if True
        
    Returns:
        FacebookAuthService instance
    """
    global _facebook_auth_service
    
    if _facebook_auth_service is None:
        from config.environment_manager import get_settings
        settings = get_settings()
        
        app_id = getattr(settings, 'FACEBOOK_APP_ID', None)
        app_secret = getattr(settings, 'FACEBOOK_APP_SECRET', None)
        redirect_uri = getattr(settings, 'FACEBOOK_REDIRECT_URI', 'http://localhost:3000/auth/facebook/callback')
        
        # Default to mock if credentials not provided
        use_mock = mock or not app_id or not app_secret
        
        _facebook_auth_service = FacebookAuthService(
            app_id=app_id,
            app_secret=app_secret,
            redirect_uri=redirect_uri,
            mock=use_mock
        )
        logger.info(f"Facebook Auth service initialized (mock={use_mock})")
    
    return _facebook_auth_service
