"""
Tests for Homeostasis API Endpoints
Phase 6: API Endpoint Tests
"""

import pytest
from unittest.mock import patch, MagicMock
from flask import Flask
from web.api.homeostasis_api import homeostasis_api


@pytest.fixture
def app():
    """Create Flask app for testing."""
    app = Flask(__name__)
    app.config['TESTING'] = True
    app.register_blueprint(homeostasis_api)
    return app


@pytest.fixture
def client(app):
    """Create test client."""
    return app.test_client()


@pytest.fixture
def mock_homeostasis_service():
    """Mock HomeostasisService."""
    with patch('web.api.homeostasis_api.homeostasis_service') as mock:
        service = MagicMock()
        service.get_homeostasis_status.return_value = {
            'net_worth': 100000.0,
            'target': 100000.0,
            'excess': 0.0
        }
        service.update_net_worth.return_value = None
        mock.return_value = service
        yield service


@pytest.fixture
def mock_philanthropy_service():
    """Mock PhilanthropyService."""
    with patch('web.api.homeostasis_api.philanthropy_service') as mock:
        service = MagicMock()
        service.donate_excess_alpha.return_value = None
        mock.return_value = service
        yield service


def test_get_status_success(client, mock_homeostasis_service):
    """Test successful status retrieval."""
    with patch('web.api.homeostasis_api.g') as mock_g:
        mock_g.get.return_value = 'default'
        response = client.get('/status')
        
        assert response.status_code == 200
        data = response.get_json()
        assert 'net_worth' in data or 'status' in data


def test_update_metrics_success(client, mock_homeostasis_service):
    """Test successful metrics update."""
    with patch('web.api.homeostasis_api.g') as mock_g:
        mock_g.get.return_value = 'default'
        response = client.post('/update',
                              json={'net_worth': 110000.0})
        
        assert response.status_code == 200
        data = response.get_json()
        assert 'net_worth' in data or 'status' in data


def test_manual_donate_success(client, mock_philanthropy_service):
    """Test successful manual donation."""
    with patch('web.api.homeostasis_api.g') as mock_g:
        mock_g.get.return_value = 'default'
        response = client.post('/donate',
                              json={'amount': 1000.0})
        
        assert response.status_code == 200
        data = response.get_json()
        assert data['status'] == 'success'
        assert 'amount' in data
