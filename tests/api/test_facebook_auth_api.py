"""
Tests for Facebook Auth API Endpoints
Phase 6: API Endpoint Tests
"""

import pytest
from unittest.mock import patch, MagicMock, AsyncMock
from flask import Flask
from web.api.facebook_auth_api import facebook_auth_bp


@pytest.fixture
def app():
    """Create Flask app for testing."""
    app = Flask(__name__)
    app.config['TESTING'] = True
    app.register_blueprint(facebook_auth_bp)
    return app


@pytest.fixture
def client(app):
    """Create test client."""
    return app.test_client()


@pytest.fixture
def mock_facebook_auth_service():
    """Mock FacebookAuthService."""
    with patch('web.api.facebook_auth_api.get_facebook_auth_service') as mock:
        service = AsyncMock()
        service.get_authorization_url.return_value = 'https://facebook.com/oauth'
        service.handle_callback.return_value = {'access_token': 'token_123', 'user_id': 'user_1'}
        mock.return_value = service
        yield service


def test_initiate_login_success(client, mock_facebook_auth_service):
    """Test successful login initiation."""
    response = client.get('/api/v1/auth/facebook/login')
    
    assert response.status_code in [200, 302]  # May redirect
    data = response.get_json() if response.is_json else {}
    if 'redirect_url' in data:
        assert 'facebook.com' in data['redirect_url']


def test_callback_success(client, mock_facebook_auth_service):
    """Test successful OAuth callback."""
    response = client.get('/api/v1/auth/facebook/callback?code=test_code&state=test_state')
    
    assert response.status_code in [200, 302]  # May redirect
