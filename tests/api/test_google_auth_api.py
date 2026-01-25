"""
Tests for Google Auth API Endpoints
Phase 6: API Endpoint Tests
"""

import pytest
from unittest.mock import patch, MagicMock, AsyncMock
from flask import Flask
from web.api.google_auth_api import google_auth_bp


@pytest.fixture
def app():
    """Create Flask app for testing."""
    app = Flask(__name__)
    app.config['TESTING'] = True
    app.register_blueprint(google_auth_bp)
    return app


@pytest.fixture
def client(app):
    """Create test client."""
    return app.test_client()


@pytest.fixture
def mock_google_auth_service():
    """Mock GoogleAuthService."""
    with patch('web.api.google_auth_api._get_google_auth_service') as mock:
        service = AsyncMock()
        service.get_authorization_url.return_value = 'https://accounts.google.com/oauth'
        service.handle_callback.return_value = {'access_token': 'token_123', 'user_id': 'user_1'}
        service.refresh_token.return_value = {'access_token': 'new_token_123'}
        service.revoke_tokens.return_value = True
        mock.return_value = service
        yield service


def test_initiate_login_success(client, mock_google_auth_service):
    """Test successful login initiation."""
    response = client.get('/api/v1/auth/google/login')
    
    assert response.status_code in [200, 302]  # May redirect
    data = response.get_json() if response.is_json else {}
    if 'redirect_url' in data:
        assert 'google.com' in data['redirect_url']


def test_callback_success(client, mock_google_auth_service):
    """Test successful OAuth callback."""
    response = client.post('/api/v1/auth/google/callback',
                          json={'code': 'test_code', 'state': 'test_state'})
    
    assert response.status_code in [200, 302]  # May redirect


def test_refresh_token_success(client, mock_google_auth_service):
    """Test successful token refresh."""
    response = client.post('/api/v1/auth/google/refresh',
                          json={'refresh_token': 'refresh_token_123'})
    
    assert response.status_code == 200
    data = response.get_json()
    assert 'access_token' in data or 'token' in data
