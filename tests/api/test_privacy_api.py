"""
Tests for Privacy API Endpoints
Phase 6: API Endpoint Tests
"""

import pytest
from unittest.mock import patch, MagicMock
from flask import Flask
from web.api.privacy_api import privacy_bp


@pytest.fixture
def app():
    """Create Flask app for testing."""
    app = Flask(__name__)
    app.config['TESTING'] = True
    app.register_blueprint(privacy_bp)
    return app


@pytest.fixture
def client(app):
    """Create test client."""
    return app.test_client()


@pytest.fixture
def mock_privacy_service():
    """Mock PrivacyService."""
    with patch('web.api.privacy_api.get_privacy_service') as mock:
        service = MagicMock()
        service.export_user_data.return_value = {'user_id': 'user_1', 'data': {}}
        service.delete_user_account.return_value = True
        mock.return_value = service
        yield service


def test_export_data_success(client, mock_privacy_service):
    """Test successful data export."""
    with patch('web.api.privacy_api.login_required', lambda f: f):
        with patch('web.api.privacy_api.g') as mock_g:
            mock_g.user_id = 'user_1'
            response = client.get('/api/v1/privacy/export')
            
            assert response.status_code == 200
            assert response.content_type == 'application/json'


def test_delete_account_success(client, mock_privacy_service):
    """Test successful account deletion."""
    with patch('web.api.privacy_api.login_required', lambda f: f):
        with patch('web.api.privacy_api.g') as mock_g:
            mock_g.user_id = 'user_1'
            response = client.delete('/api/v1/privacy/forget-me')
            
            assert response.status_code == 200
            data = response.get_json()
            assert 'message' in data
