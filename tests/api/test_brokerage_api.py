"""
Tests for Brokerage API Endpoints
Phase 6: API Endpoint Tests
"""

import pytest
from unittest.mock import patch, MagicMock
from flask import Flask
from web.api.brokerage_api import brokerage_bp


@pytest.fixture
def app():
    """Create Flask app for testing."""
    app = Flask(__name__)
    app.config['TESTING'] = True
    app.register_blueprint(brokerage_bp)
    return app


@pytest.fixture
def client(app):
    """Create test client."""
    return app.test_client()


@pytest.fixture
def mock_brokerage_service():
    """Mock BrokerageService."""
    with patch('web.api.brokerage_api.get_brokerage_service') as mock:
        service = MagicMock()
        service.get_status.return_value = {
            'connected': True,
            'provider': 'test_provider',
            'account_id': 'account_1'
        }
        service.get_supported_providers.return_value = [
            'test_provider',
            'another_provider'
        ]
        service.get_positions.return_value = [
            {'symbol': 'AAPL', 'quantity': 100, 'price': 150.0}
        ]
        service.connect_with_keys.return_value = True
        mock.return_value = service
        yield service


def test_get_brokerage_status_success(client, mock_brokerage_service):
    """Test successful brokerage status retrieval."""
    with patch('web.api.brokerage_api.login_required', lambda f: f):
        response = client.get('/api/v1/brokerage/status')
        
        assert response.status_code == 200
        data = response.get_json()
        assert data['connected'] is True
        assert 'provider' in data


def test_get_supported_providers_success(client, mock_brokerage_service):
    """Test successful providers list retrieval."""
    with patch('web.api.brokerage_api.login_required', lambda f: f):
        response = client.get('/api/v1/brokerage/providers')
        
        assert response.status_code == 200
        data = response.get_json()
        assert isinstance(data, list)
        assert len(data) > 0


def test_get_brokerage_positions_success(client, mock_brokerage_service):
    """Test successful positions retrieval."""
    with patch('web.api.brokerage_api.login_required', lambda f: f):
        response = client.get('/api/v1/brokerage/positions')
        
        assert response.status_code == 200
        data = response.get_json()
        assert isinstance(data, list)
        assert len(data) > 0


def test_connect_brokerage_success(client, mock_brokerage_service):
    """Test successful brokerage connection."""
    with patch('web.api.brokerage_api.login_required', lambda f: f):
        with patch('web.api.brokerage_api.requires_role', lambda role: lambda f: f):
            response = client.post('/api/v1/brokerage/connect',
                                  json={
                                      'api_key': 'test_key',
                                      'secret_key': 'test_secret',
                                      'base_url': 'https://api.test.com'
                                  })
            
            assert response.status_code == 200
            data = response.get_json()
            assert data['status'] == 'success'


def test_connect_brokerage_missing_credentials(client):
    """Test brokerage connection with missing credentials."""
    with patch('web.api.brokerage_api.login_required', lambda f: f):
        with patch('web.api.brokerage_api.requires_role', lambda role: lambda f: f):
            response = client.post('/api/v1/brokerage/connect',
                                  json={'api_key': 'test_key'})
            
            assert response.status_code == 400
            data = response.get_json()
            assert 'error' in data
