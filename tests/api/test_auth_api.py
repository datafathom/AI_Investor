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


def test_login_success(client):
    """Test successful login."""
    response = client.post('/api/auth/login',
                          json={
                              'username': 'admin',
                              'password': 'admin'
                          })
    
    assert response.status_code == 200
    data = response.get_json()
    assert 'token' in data
    assert data['user']['username'] == 'admin'


def test_login_invalid_credentials(client):
    """Test login with invalid credentials."""
    response = client.post('/api/auth/login',
                          json={
                              'username': 'admin',
                              'password': 'wrong_password'
                          })
    
    assert response.status_code == 401
    data = response.get_json()
    assert 'error' in data


def test_register_success(client):
    """Test successful registration."""
    response = client.post('/api/auth/register',
                          json={
                              'username': 'newuser',
                              'password': 'password123',
                              'email': 'newuser@example.com'
                          })
    
    assert response.status_code == 200
    data = response.get_json()
    assert data['message'] == 'User registered successfully'
    assert data['user']['username'] == 'newuser'


def test_mfa_setup_success(client):
    """Test successful MFA setup."""
    with patch('web.api.auth_api.get_totp_service') as mock_service:
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
    with patch('web.api.auth_api.get_totp_service') as mock_service:
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
    with patch('web.api.auth_api.get_social_auth_service') as mock_service:
        mock_social = MagicMock()
        mock_social.initiate_auth_flow.return_value = 'https://oauth.provider.com/auth'
        mock_service.return_value = mock_social
        
        response = client.get('/api/auth/social/login/google')
        
        assert response.status_code == 200
        data = response.get_json()
        assert 'redirect_url' in data
