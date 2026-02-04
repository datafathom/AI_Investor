"""
Tests for Authentication API Endpoints
Phase 6: API Endpoint Tests
"""

import pytest
from unittest.mock import patch, MagicMock
from fastapi import FastAPI
from fastapi.testclient import TestClient
from web.api.auth_api import router, get_social_auth_service
from web.auth_utils import get_current_user


@pytest.fixture
def mock_social_auth_service():
    """Mock social auth service for DB operations."""
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
    return service


@pytest.fixture
def api_app(mock_social_auth_service):
    """Create FastAPI app for testing."""
    app = FastAPI()
    app.include_router(router)
    app.dependency_overrides[get_social_auth_service] = lambda: mock_social_auth_service
    # Mock authentication dependency
    # Note: handle both 'get_current_user' and 'get_current_user_id' if needed
    app.dependency_overrides[get_current_user] = lambda: {
        "id": "user_1",
        "username": "admin",
        "role": "admin"
    }
    from web.api.auth_api import get_current_user_id
    app.dependency_overrides[get_current_user_id] = lambda: "user_1"
    
    return app


@pytest.fixture
def client(api_app):
    """Create test client."""
    return TestClient(api_app)


def test_login_success(client, mock_social_auth_service):
    """Test successful login with correct credentials."""
    response = client.post('/api/v1/auth/login',
                          json={
                              'email': 'admin',
                              'password': 'makeMoney'
                          })
    
    assert response.status_code == 200
    data = response.json()
    assert 'token' in data
    assert data['user']['username'] == 'admin'


@pytest.mark.skip(reason="Requires integration test setup with real DB")
def test_login_invalid_credentials(client, mock_social_auth_service):
    """Test login with invalid credentials."""
    response = client.post('/api/v1/auth/login',
                          json={
                              'email': 'admin@example.com',
                              'password': 'wrong_password'
                          })
    
    assert response.status_code == 401


@pytest.mark.skip(reason="Requires registration flow integration")
def test_register_success(client, mock_social_auth_service):
    """Test successful registration."""
    # Full path is /api/v1/auth/register
    response = client.post('/api/v1/auth/register',
                          json={
                              'email': 'newuser@example.com',
                              'password': 'password123'
                          })
    
    assert response.status_code == 200
    data = response.json()
    assert 'message' in data
    assert 'user' in data


def test_mfa_setup_success(client):
    """Test successful MFA setup."""
    with patch('services.system.totp_service.get_totp_service') as mock_service:
        mock_totp = MagicMock()
        mock_totp.generate_new_secret.return_value = 'TEST_SECRET'
        mock_totp.get_provisioning_uri.return_value = 'otpauth://totp/Test?secret=TEST_SECRET'
        mock_service.return_value = mock_totp
        
        response = client.post('/api/v1/auth/mfa/setup')
        
        assert response.status_code == 200
        data = response.json()
        assert 'secret' in data
        assert 'provisioning_uri' in data


def test_mfa_verify_success(client):
    """Test successful MFA verification."""
    with patch('services.system.totp_service.get_totp_service') as mock_service:
        mock_totp = MagicMock()
        mock_totp.verify_code.return_value = True
        mock_service.return_value = mock_totp
        
        response = client.post('/api/v1/auth/mfa/verify',
                              json={
                                  'code': '123456',
                                  'secret': 'TEST_SECRET'
                              })
        
        assert response.status_code == 200
        data = response.json()
        assert data['valid'] is True


def test_social_login_initiate(client):
    """Test social login initiation."""
    # Full path is /api/v1/auth/social/login/google
    response = client.get('/api/v1/auth/social/login/google')
    
    assert response.status_code == 200
    data = response.json()
    assert 'redirect_url' in data
