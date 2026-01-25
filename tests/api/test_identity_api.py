"""
Tests for Identity API Endpoints
Phase 6: API Endpoint Tests
"""

import pytest
from unittest.mock import patch, MagicMock
from flask import Flask
from web.api.identity_api import identity_api


@pytest.fixture
def app():
    """Create Flask app for testing."""
    app = Flask(__name__)
    app.config['TESTING'] = True
    app.register_blueprint(identity_api)
    return app


@pytest.fixture
def client(app):
    """Create test client."""
    return app.test_client()


@pytest.fixture
def mock_identity_service():
    """Mock IdentityService."""
    with patch('web.api.identity_api.identity_service') as mock:
        service = MagicMock()
        service.get_identity_profile.return_value = {
            'user_id': 'user_1',
            'trust_score': 0.95,
            'verified': True
        }
        service.reconcile_identity.return_value = {
            'user_id': 'user_1',
            'trust_score': 0.95
        }
        mock.return_value = service
        yield service


def test_get_profile_success(client, mock_identity_service):
    """Test successful profile retrieval."""
    with patch('web.api.identity_api.login_required', lambda f: f):
        with patch('web.api.identity_api.g') as mock_g:
            mock_g.user_id = 'user_1'
            response = client.get('/profile')
            
            assert response.status_code == 200
            data = response.get_json()
            assert 'user_id' in data or 'trust_score' in data


def test_reconcile_success(client, mock_identity_service):
    """Test successful identity reconciliation."""
    with patch('web.api.identity_api.login_required', lambda f: f):
        with patch('web.api.identity_api.g') as mock_g:
            mock_g.user_id = 'user_1'
            response = client.post('/reconcile')
            
            assert response.status_code == 200
            data = response.get_json()
            assert 'message' in data or 'data' in data


def test_manual_verify_success(client):
    """Test successful manual verification."""
    with patch('web.api.identity_api.login_required', lambda f: f):
        response = client.post('/manual-verify')
        
        assert response.status_code == 200
        data = response.get_json()
        assert 'message' in data
