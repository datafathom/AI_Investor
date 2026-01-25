"""
Tests for Legal API Endpoints
Phase 6: API Endpoint Tests
"""

import pytest
from unittest.mock import patch, MagicMock
from flask import Flask
from web.api.legal_api import legal_bp


@pytest.fixture
def app():
    """Create Flask app for testing."""
    app = Flask(__name__)
    app.config['TESTING'] = True
    app.register_blueprint(legal_bp)
    return app


@pytest.fixture
def client(app):
    """Create test client."""
    return app.test_client()


@pytest.fixture
def mock_legal_service():
    """Mock LegalComplianceService."""
    with patch('web.api.legal_api.get_legal_compliance_service') as mock:
        service = MagicMock()
        service.get_user_consent_status.return_value = {
            'tos_accepted': True,
            'tos_version': '1.0',
            'privacy_accepted': True
        }
        service.accept_agreement.return_value = True
        mock.return_value = service
        yield service


def test_get_consent_status_success(client, mock_legal_service):
    """Test successful consent status retrieval."""
    with patch('web.api.legal_api.login_required', lambda f: f):
        with patch('web.api.legal_api.g') as mock_g:
            mock_g.user_id = 'user_1'
            response = client.get('/api/v1/legal/status')
            
            assert response.status_code == 200
            data = response.get_json()
            assert 'tos_accepted' in data or 'consent' in data


def test_accept_agreement_success(client, mock_legal_service):
    """Test successful agreement acceptance."""
    with patch('web.api.legal_api.login_required', lambda f: f):
        with patch('web.api.legal_api.g') as mock_g:
            mock_g.user_id = 'user_1'
            response = client.post('/api/v1/legal/accept',
                                  json={'type': 'TOS', 'version': '1.0'})
            
            assert response.status_code == 200
            data = response.get_json()
            assert 'message' in data


def test_accept_agreement_missing_params(client):
    """Test agreement acceptance with missing parameters."""
    with patch('web.api.legal_api.login_required', lambda f: f):
        with patch('web.api.legal_api.g') as mock_g:
            mock_g.user_id = 'user_1'
            response = client.post('/api/v1/legal/accept',
                                  json={'type': 'TOS'})
            
            assert response.status_code == 400
            data = response.get_json()
            assert 'error' in data
