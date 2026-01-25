"""
Tests for Cash API Flask Endpoints
Phase 6: API Endpoint Tests
"""

import pytest
from unittest.mock import patch, MagicMock, AsyncMock
from flask import Flask
from web.api.cash_api_flask import cash_bp


@pytest.fixture
def app():
    """Create Flask app for testing."""
    app = Flask(__name__)
    app.config['TESTING'] = True
    app.register_blueprint(cash_bp)
    return app


@pytest.fixture
def client(app):
    """Create test client."""
    return app.test_client()


@pytest.fixture
def mock_fx_service():
    """Mock FXService."""
    with patch('web.api.cash_api_flask.get_fx_service') as mock:
        service = AsyncMock()
        from services.trading.fx_service import CurrencyBalance, FXRate
        mock_balances = [
            CurrencyBalance(
                currency='USD',
                amount=100000.0,
                amount_usd=100000.0,
                interest_rate=0.05,
                allocation_pct=1.0
            )
        ]
        service.get_balances.return_value = mock_balances
        mock_rates = [
            FXRate(
                pair='EUR/USD',
                base='EUR',
                quote='USD',
                rate=1.10,
                bid=1.0995,
                ask=1.1005,
                spread_bps=10.0,
                change_24h=0.01,
                timestamp=None
            )
        ]
        service.get_fx_rates.return_value = mock_rates
        service.get_total_value_usd.return_value = 100000.0
        from services.trading.fx_service import ConversionResult
        mock_conversion = ConversionResult(
            from_currency='USD',
            to_currency='EUR',
            amount=1000.0,
            converted_amount=909.09,
            rate=1.10,
            success=True,
            error_message=None
        )
        service.execute_conversion.return_value = mock_conversion
        mock.return_value = service
        yield service


def test_get_cash_dashboard_success(client, mock_fx_service):
    """Test successful cash dashboard retrieval."""
    response = client.get('/dashboard')
    
    assert response.status_code == 200
    data = response.get_json()
    assert 'balances' in data
    assert 'fx_rates' in data
    assert 'total_value_usd' in data


def test_get_fx_rates_success(client, mock_fx_service):
    """Test successful FX rates retrieval."""
    response = client.get('/fx/rates')
    
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, dict)


def test_convert_currency_success(client, mock_fx_service):
    """Test successful currency conversion."""
    response = client.post('/fx/convert',
                          json={
                              'from_currency': 'USD',
                              'to_currency': 'EUR',
                              'amount': 1000.0
                          })
    
    assert response.status_code == 200
    data = response.get_json()
    assert data['success'] is True
    assert 'rate' in data


def test_convert_currency_missing_params(client):
    """Test currency conversion with missing parameters."""
    response = client.post('/fx/convert',
                          json={'from_currency': 'USD'})
    
    assert response.status_code == 400
    data = response.get_json()
    assert 'error' in data
