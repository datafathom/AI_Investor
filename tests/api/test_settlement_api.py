"""
Tests for Settlement API Endpoints
Phase 6: API Endpoint Tests
"""

import pytest
from unittest.mock import patch, MagicMock
from flask import Flask
from web.api.settlement_api import settlement_bp


@pytest.fixture
def app():
    """Create Flask app for testing."""
    app = Flask(__name__)
    app.config['TESTING'] = True
    app.register_blueprint(settlement_bp)
    return app


@pytest.fixture
def client(app):
    """Create test client."""
    return app.test_client()


@pytest.fixture
def mock_settlement_service():
    """Mock SettlementService."""
    with patch('web.api.settlement_api.get_settlement_service') as mock:
        service = MagicMock()
        service.get_balance_summary.return_value = {
            'cash': 100000.0,
            'settled': 95000.0,
            'pending': 5000.0
        }
        service.get_rates.return_value = {'USD': 1.0, 'EUR': 0.85}
        service.convert_currency.return_value = {
            'status': 'SUCCESS',
            'from': 'USD',
            'to': 'EUR',
            'amount': 1000.0,
            'converted': 850.0
        }
        mock.return_value = service
        yield service


def test_get_balances_success(client, mock_settlement_service):
    """Test successful balances retrieval."""
    with patch('web.api.settlement_api.login_required', lambda f: f):
        with patch('web.api.settlement_api.requires_role', lambda role: lambda f: f):
            response = client.get('/api/v1/settlement/balances')
            
            assert response.status_code == 200
            data = response.get_json()
            assert 'cash' in data or 'settled' in data


def test_get_rates_success(client, mock_settlement_service):
    """Test successful rates retrieval."""
    with patch('web.api.settlement_api.login_required', lambda f: f):
        with patch('services.system.cache_service.get_cache_service') as mock_cache:
            mock_cache.return_value.get.return_value = None
            response = client.get('/api/v1/settlement/rates')
            
            assert response.status_code == 200
            data = response.get_json()
            assert 'USD' in data or 'rates' in data


def test_convert_currency_success(client, mock_settlement_service):
    """Test successful currency conversion."""
    with patch('web.api.settlement_api.login_required', lambda f: f):
        with patch('web.api.settlement_api.requires_role', lambda role: lambda f: f):
            response = client.post('/api/v1/settlement/convert',
                                  json={
                                      'from': 'USD',
                                      'to': 'EUR',
                                      'amount': 1000.0
                                  })
            
            assert response.status_code == 200
            data = response.get_json()
            assert data['status'] == 'SUCCESS' or 'converted' in data


def test_convert_currency_missing_params(client):
    """Test currency conversion with missing parameters."""
    with patch('web.api.settlement_api.login_required', lambda f: f):
        with patch('web.api.settlement_api.requires_role', lambda role: lambda f: f):
            response = client.post('/api/v1/settlement/convert',
                                  json={'from': 'USD'})
            
            assert response.status_code == 400
            data = response.get_json()
            assert 'error' in data
