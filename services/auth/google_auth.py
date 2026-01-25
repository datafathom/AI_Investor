"""
==============================================================================
FILE: services/auth/google_auth.py
ROLE: Google OAuth Authentication Service
PURPOSE: Handles Google OAuth2 flow for SSO login and provides access tokens
         for Google APIs (Gmail, Calendar, YouTube, Drive).

INTEGRATION POINTS:
    - AuthAPI: OAuth callback handling
    - UserService: Profile sync and account linking
    - GmailService: Email sending (requires gmail.send scope)
    - CalendarService: Event creation (requires calendar scope)
    - YouTubeService: Video monitoring (requires youtube.readonly scope)

SCOPES SUPPORTED:
    - openid, email, profile (basic SSO)
    - https://www.googleapis.com/auth/calendar (Calendar API)
    - https://www.googleapis.com/auth/gmail.send (Gmail sending)
    - https://www.googleapis.com/auth/youtube.readonly (YouTube read)

AUTHOR: AI Investor Team
CREATED: 2026-01-21
==============================================================================
"""

import logging
import asyncio
import json
from typing import Dict, Any, Optional, List
from datetime import datetime, timedelta
from dataclasses import dataclass

logger = logging.getLogger(__name__)

try:
    from google.auth.transport.requests import Request
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import Flow
    from googleapiclient.discovery import build
    GOOGLE_LIBS_AVAILABLE = True
except ImportError:
    GOOGLE_LIBS_AVAILABLE = False
    logger.warning("Google OAuth libraries not installed. Install with: pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client")


@dataclass
class GoogleUserProfile:
    """Google user profile data"""
    google_id: str
    email: str
    name: str
    picture: Optional[str] = None
    verified_email: bool = False
    locale: Optional[str] = None


@dataclass
class TokenInfo:
    """OAuth token information"""
    access_token: str
    refresh_token: Optional[str]
    expires_at: datetime
    scopes: List[str]
    token_type: str = "Bearer"


class GoogleAuthService:
    """
    Google OAuth2 authentication service.
    Handles OAuth flow, token management, and profile retrieval.
    """
    
    # OAuth2 scopes
    SCOPES = {
        "basic": [
            "openid",
            "https://www.googleapis.com/auth/userinfo.email",
            "https://www.googleapis.com/auth/userinfo.profile"
        ],
        "calendar": [
            "https://www.googleapis.com/auth/calendar"
        ],
        "gmail": [
            "https://www.googleapis.com/auth/gmail.send"
        ],
        "youtube": [
            "https://www.googleapis.com/auth/youtube.readonly"
        ],
        "full": [
            "openid",
            "https://www.googleapis.com/auth/userinfo.email",
            "https://www.googleapis.com/auth/userinfo.profile",
            "https://www.googleapis.com/auth/calendar",
            "https://www.googleapis.com/auth/gmail.send",
            "https://www.googleapis.com/auth/youtube.readonly"
        ]
    }
    
    # OAuth2 endpoints
    AUTHORIZATION_BASE_URL = "https://accounts.google.com/o/oauth2/v2/auth"
    TOKEN_URL = "https://oauth2.googleapis.com/token"
    REVOKE_URL = "https://oauth2.googleapis.com/revoke"
    USERINFO_URL = "https://www.googleapis.com/oauth2/v2/userinfo"
    
    def __init__(
        self,
        client_id: Optional[str] = None,
        client_secret: Optional[str] = None,
        redirect_uri: Optional[str] = None,
        mock: bool = False
    ):
        """
        Initialize Google OAuth service.
        
        Args:
            client_id: Google OAuth client ID
            client_secret: Google OAuth client secret
            redirect_uri: OAuth redirect URI
            mock: Use mock mode if True
        """
        self.mock = mock
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri
        
        if not mock and GOOGLE_LIBS_AVAILABLE and client_id and client_secret:
            # Configure OAuth flow
            self.flow = Flow.from_client_config(
                {
                    "web": {
                        "client_id": client_id,
                        "client_secret": client_secret,
                        "auth_uri": self.AUTHORIZATION_BASE_URL,
                        "token_uri": self.TOKEN_URL,
                        "redirect_uris": [redirect_uri] if redirect_uri else []
                    }
                },
                scopes=self.SCOPES["full"],
                redirect_uri=redirect_uri
            )
        else:
            self.flow = None
            if not GOOGLE_LIBS_AVAILABLE:
                logger.warning("Google OAuth libraries not available. Using mock mode.")
                self.mock = True
    
    def get_authorization_url(
        self,
        state: Optional[str] = None,
        scopes: Optional[List[str]] = None,
        access_type: str = "offline",
        prompt: str = "consent"
    ) -> str:
        """
        Generate Google OAuth authorization URL.
        
        Args:
            state: CSRF protection state token
            scopes: List of scopes to request (defaults to full)
            access_type: "offline" for refresh token, "online" for access token only
            prompt: "consent" to force consent screen, "none" for silent auth
            
        Returns:
            Authorization URL
        """
        if self.mock:
            return f"https://mock-google-auth.com/authorize?state={state or 'mock_state'}"
        
        if not self.flow:
            raise RuntimeError("Google OAuth not configured. Check client credentials.")
        
        # Set scopes
        requested_scopes = scopes or self.SCOPES["full"]
        self.flow.scopes = requested_scopes
        
        # Generate authorization URL
        auth_url, _ = self.flow.authorization_url(
            access_type=access_type,
            include_granted_scopes=True,
            state=state,
            prompt=prompt
        )
        
        return auth_url
    
    async def exchange_code_for_tokens(
        self,
        authorization_code: str,
        state: Optional[str] = None
    ) -> TokenInfo:
        """
        Exchange authorization code for access and refresh tokens.
        
        Args:
            authorization_code: OAuth authorization code from callback
            state: CSRF state token (should match request)
            
        Returns:
            TokenInfo with access token, refresh token, and expiration
        """
        if self.mock:
            await asyncio.sleep(0.2)  # Simulate API call
            return TokenInfo(
                access_token="mock_access_token",
                refresh_token="mock_refresh_token",
                expires_at=datetime.now() + timedelta(hours=1),
                scopes=self.SCOPES["full"]
            )
        
        if not self.flow:
            raise RuntimeError("Google OAuth not configured.")
        
        try:
            # Exchange code for tokens
            self.flow.fetch_token(code=authorization_code)
            credentials = self.flow.credentials
            
            return TokenInfo(
                access_token=credentials.token,
                refresh_token=credentials.refresh_token,
                expires_at=credentials.expiry if credentials.expiry else datetime.now() + timedelta(hours=1),
                scopes=credentials.scopes or []
            )
        except Exception as e:
            logger.error(f"Token exchange failed: {e}")
            raise RuntimeError(f"Failed to exchange code for tokens: {str(e)}")
    
    async def get_user_profile(self, access_token: str) -> GoogleUserProfile:
        """
        Retrieve user profile from Google API.
        
        Args:
            access_token: Valid Google access token
            
        Returns:
            GoogleUserProfile with user information
        """
        if self.mock:
            await asyncio.sleep(0.1)
            return GoogleUserProfile(
                google_id="mock_google_id_123",
                email="user@example.com",
                name="Mock User",
                picture="https://via.placeholder.com/150",
                verified_email=True,
                locale="en"
            )
        
        try:
            import httpx
            
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    self.USERINFO_URL,
                    headers={"Authorization": f"Bearer {access_token}"}
                )
                response.raise_for_status()
                data = response.json()
                
                return GoogleUserProfile(
                    google_id=data.get("id", ""),
                    email=data.get("email", ""),
                    name=data.get("name", ""),
                    picture=data.get("picture"),
                    verified_email=data.get("verified_email", False),
                    locale=data.get("locale")
                )
        except Exception as e:
            logger.error(f"Failed to get user profile: {e}")
            raise RuntimeError(f"Failed to retrieve user profile: {str(e)}")
    
    async def refresh_access_token(self, refresh_token: str) -> TokenInfo:
        """
        Refresh expired access token using refresh token.
        
        Args:
            refresh_token: Valid refresh token
            
        Returns:
            New TokenInfo with refreshed access token
        """
        if self.mock:
            await asyncio.sleep(0.1)
            return TokenInfo(
                access_token="mock_refreshed_token",
                refresh_token=refresh_token,  # Refresh token doesn't change
                expires_at=datetime.now() + timedelta(hours=1),
                scopes=self.SCOPES["full"]
            )
        
        if not GOOGLE_LIBS_AVAILABLE:
            raise RuntimeError("Google OAuth libraries not available.")
        
        try:
            credentials = Credentials(
                token=None,
                refresh_token=refresh_token,
                token_uri=self.TOKEN_URL,
                client_id=self.client_id,
                client_secret=self.client_secret
            )
            
            # Refresh token
            credentials.refresh(Request())
            
            return TokenInfo(
                access_token=credentials.token,
                refresh_token=credentials.refresh_token,
                expires_at=credentials.expiry if credentials.expiry else datetime.now() + timedelta(hours=1),
                scopes=credentials.scopes or []
            )
        except Exception as e:
            logger.error(f"Token refresh failed: {e}")
            raise RuntimeError(f"Failed to refresh token: {str(e)}")
    
    async def revoke_token(self, token: str) -> bool:
        """
        Revoke access or refresh token.
        
        Args:
            token: Access or refresh token to revoke
            
        Returns:
            True if revoked successfully
        """
        if self.mock:
            logger.info(f"[MOCK] Revoked token: {token[:20]}...")
            return True
        
        try:
            import httpx
            
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    self.REVOKE_URL,
                    params={"token": token}
                )
                response.raise_for_status()
                return True
        except Exception as e:
            logger.error(f"Token revocation failed: {e}")
            return False
    
    def get_incremental_auth_url(
        self,
        existing_scopes: List[str],
        additional_scopes: List[str],
        state: Optional[str] = None
    ) -> str:
        """
        Generate authorization URL for incremental scope addition.
        
        Args:
            existing_scopes: Already granted scopes
            additional_scopes: New scopes to request
            state: CSRF protection state
            
        Returns:
            Authorization URL for additional scopes
        """
        all_scopes = list(set(existing_scopes + additional_scopes))
        return self.get_authorization_url(
            state=state,
            scopes=all_scopes,
            prompt="consent"  # Force consent for new scopes
        )


# Singleton instance
_google_auth_service: Optional[GoogleAuthService] = None


def get_google_auth_service(mock: bool = True) -> GoogleAuthService:
    """
    Get singleton Google OAuth service instance.
    
    Args:
        mock: Use mock mode if True
        
    Returns:
        GoogleAuthService instance
    """
    global _google_auth_service
    
    if _google_auth_service is None:
        from config.environment_manager import get_settings
        settings = get_settings()
        
        client_id = getattr(settings, 'GOOGLE_CLIENT_ID', None)
        client_secret = getattr(settings, 'GOOGLE_CLIENT_SECRET', None)
        redirect_uri = getattr(settings, 'GOOGLE_REDIRECT_URI', 'http://localhost:3000/auth/google/callback')
        
        # Default to mock if credentials not provided
        use_mock = mock or not client_id or not client_secret
        
        _google_auth_service = GoogleAuthService(
            client_id=client_id,
            client_secret=client_secret,
            redirect_uri=redirect_uri,
            mock=use_mock
        )
        logger.info(f"Google Auth service initialized (mock={use_mock})")
    
    return _google_auth_service
