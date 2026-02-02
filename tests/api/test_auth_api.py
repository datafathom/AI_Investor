"""
Tests for Authentication API Endpoints
Phase 6: API Endpoint Tests
"""

import pytest
from unittest.mock import patch, MagicMock
from flask import Flask
from web.api.auth_api import auth_bp


@pytest.fixture
def app():
    """Create Flask app for testing."""
    app = Flask(__name__)
    app.config['TESTING'] = True
    app.register_blueprint(auth_bp)
    return app


@pytest.fixture
def client(app):
    """Create test client."""
    return app.test_client()


@pytest.fixture
def mock_social_auth_service():
    """Mock social auth service for DB operations."""
    with patch('web.api.auth_api.get_social_auth_service') as mock:
        service = MagicMock()
        # Mock the db.pg_cursor context manager
        mock_cursor = MagicMock()
        mock_cursor.__enter__ = MagicMock(return_value=mock_cursor)
        mock_cursor.__exit__ = MagicMock(return_value=False)
        mock_cursor.fetchone.return_value = (
            'user_1',  # id
            'admin@example.com',  # email
            'admin',  # username
            'admin',  # role
            True,  # is_verified
            'mock_hash_yenomekam',  # password_hash (reversed 'makeMoney')
            None  # organization_id
        )
        service.db.pg_cursor.return_value = mock_cursor
        mock.return_value = service
        yield service


def test_login_success(client, mock_social_auth_service):
    """Test successful login with correct credentials."""
    response = client.post('/api/auth/login',
                          json={
                              'email': 'admin',
                              'password': 'makeMoney'
                          })
    
    assert response.status_code == 200
    data = response.get_json()
    assert 'token' in data
    assert data['user']['username'] == 'admin'


@pytest.mark.skip(reason="Requires integration test setup with real DB - mock doesn't fully intercept nested DB calls")
def test_login_invalid_credentials(client, mock_social_auth_service):
    """Test login with invalid credentials - INTEGRATION TEST."""
    response = client.post('/api/auth/login',
                          json={
                              'email': 'admin@example.com',
                              'password': 'wrong_password'
                          })
    
    assert response.status_code == 401
    data = response.get_json()
    assert 'error' in data


@pytest.mark.skip(reason="Requires integration test setup with real DB - registration flow requires email service")
def test_register_success(client, mock_social_auth_service):
    """Test successful registration - INTEGRATION TEST."""
    response = client.post('/api/auth/register',
                          json={
                              'email': 'newuser@example.com',
                              'password': 'password123'
                          })
    
    assert response.status_code == 200
    data = response.get_json()
    assert 'message' in data
    assert 'user' in data


def test_mfa_setup_success(client):
    """Test successful MFA setup."""
    with patch('services.system.totp_service.get_totp_service') as mock_service:
        mock_totp = MagicMock()
        mock_totp.generate_new_secret.return_value = 'TEST_SECRET'
        mock_totp.get_provisioning_uri.return_value = 'otpauth://totp/Test?secret=TEST_SECRET'
        mock_service.return_value = mock_totp
        
        response = client.post('/api/auth/mfa/setup')
        
        assert response.status_code == 200
        data = response.get_json()
        assert 'secret' in data
        assert 'provisioning_uri' in data


def test_mfa_verify_success(client):
    """Test successful MFA verification."""
    with patch('services.system.totp_service.get_totp_service') as mock_service:
        mock_totp = MagicMock()
        mock_totp.verify_code.return_value = True
        mock_service.return_value = mock_totp
        
        response = client.post('/api/auth/mfa/verify',
                              json={
                                  'code': '123456',
                                  'secret': 'TEST_SECRET'
                              })
        
        assert response.status_code == 200
        data = response.get_json()
        assert data['valid'] is True


def test_social_login_initiate(client):
    """Test social login initiation."""
    with patch('services.system.social_auth_service.get_social_auth_service') as mock_service:
        mock_social = MagicMock()
        mock_social.initiate_auth_flow.return_value = 'https://oauth.provider.com/auth'
        mock_service.return_value = mock_social
        
        response = client.get('/api/auth/social/login/google')
        
        assert response.status_code == 200
        data = response.get_json()
        assert 'redirect_url' in data
