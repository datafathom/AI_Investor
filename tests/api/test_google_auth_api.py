import pytest
from datetime import datetime
from unittest.mock import MagicMock, AsyncMock, patch
from fastapi import FastAPI
from fastapi.testclient import TestClient
from web.api.google_auth_api import router, get_google_auth_provider
import web.api.google_auth_api as google_auth_module
from services.auth.google_auth import TokenInfo, GoogleUserProfile


@pytest.fixture
def api_app():
    """Create FastAPI app for testing."""
    app = FastAPI()
    app.include_router(router)
    return app


@pytest.fixture
def client(api_app):
    """Create test client."""
    return TestClient(api_app)


@pytest.fixture
def mock_google_auth_service(api_app):
    """Mock GoogleAuthService."""
    service = AsyncMock()
    service.get_authorization_url = MagicMock(return_value='https://accounts.google.com/oauth')
    service.exchange_code_for_tokens.return_value = TokenInfo(
        access_token='token_123',
        refresh_token='refresh_123',
        expires_at=datetime(2024, 1, 1),
        scopes=['email']
    )
    service.get_user_profile.return_value = GoogleUserProfile(
        email='test@example.com',
        name='Test User',
        picture='pic_url',
        verified_email=True,
        google_id='google_123',
        locale='en'
    )
    service.refresh_access_token.return_value = TokenInfo(
        access_token='new_token_123',
        refresh_token='refresh_123',
        expires_at=datetime(2024, 1, 1),
        scopes=['email']
    )
    service.revoke_token.return_value = True
    api_app.dependency_overrides[get_google_auth_provider] = lambda: service
    return service


def test_initiate_login_success(client, mock_google_auth_service):
    """Test successful login initiation."""
    response = client.get('/api/v1/google_auth/login')
    
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert 'authorization_url' in data['data']
    assert 'state' in data['data']


def test_callback_success(client, mock_google_auth_service):
    """Test successful OAuth callback."""
    # Add state to allowed states
    google_auth_module._oauth_states['test_state'] = {'scopes': None, 'created_at': 0}
    
    with patch('services.system.social_auth_service.get_social_auth_service') as mock_social:
        social_service = MagicMock()
        social_service.handle_callback.return_value = {
            'user': {'id': 'user_1', 'username': 'testuser'},
            'token': 'session_token_123'
        }
        mock_social.return_value = social_service
        
        response = client.post('/api/v1/google_auth/callback',
                              json={'code': 'test_code', 'state': 'test_state'})
        
        assert response.status_code == 200
        data = response.json()
        assert data['success'] is True
        assert data['data']['user']['email'] == 'test@example.com'


def test_refresh_token_success(client, mock_google_auth_service):
    """Test successful token refresh."""
    response = client.post('/api/v1/google_auth/refresh',
                          json={'refresh_token': 'refresh_token_123'})
    
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert data['data']['access_token'] == 'new_token_123'


def test_revoke_token_success(client, mock_google_auth_service):
    """Test successful token revocation."""
    response = client.post('/api/v1/google_auth/revoke',
                          json={'token': 'token_to_revoke'})
    
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert data['data']['message'] == 'Token revoked successfully'


def test_get_profile_success(client, mock_google_auth_service):
    """Test successful profile retrieval."""
    response = client.get('/api/v1/google_auth/profile',
                          headers={'Authorization': 'Bearer token_123'})
    
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert data['data']['email'] == 'test@example.com'
