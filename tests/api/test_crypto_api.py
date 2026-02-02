"""
Tests for Crypto API Endpoints
Phase 6: API Endpoint Tests
"""

import pytest
from unittest.mock import patch, MagicMock
from flask import Flask
from web.api.crypto_api import crypto_api_bp


@pytest.fixture
def app():
    """Create Flask app for testing."""
    app = Flask(__name__)
    app.config['TESTING'] = True
    app.register_blueprint(crypto_api_bp)
    return app


@pytest.fixture
def client(app):
    """Create test client."""
    return app.test_client()


@pytest.fixture
def mock_crypto_client():
    """Mock CryptoCompare client."""
    with patch('web.api.crypto_api.get_crypto_client') as mock:
        client = MagicMock()
        mock.return_value = client
        yield client


def test_get_crypto_price_success(client, mock_crypto_client):
    """Test successful crypto price retrieval."""
    mock_prices = {
        'BTC': {'USD': 50000.0, 'EUR': 45000.0},
        'ETH': {'USD': 3000.0, 'EUR': 2700.0}
    }
    
    async def mock_get_price(symbols, currencies):
        return mock_prices
    
    mock_crypto_client.get_price = mock_get_price
    
    response = client.get('/api/v1/market/crypto/price?symbols=BTC,ETH&currencies=USD,EUR&mock=false')
    
    assert response.status_code == 200
    data = response.get_json()
    assert 'BTC' in data
    assert 'ETH' in data


def test_get_crypto_volume_success(client, mock_crypto_client):
    """Test successful crypto volume retrieval."""
    from services.data.crypto_compare_service import ExchangeVolume
    
    mock_volumes = [
        ExchangeVolume(
            exchange='Binance',
            volume_24h=1000000.0,
            market_share=25.5
        )
    ]
    
    async def mock_get_volume(symbol):
        return mock_volumes
    
    mock_crypto_client.get_top_exchanges_volume = mock_get_volume
    
    response = client.get('/api/v1/market/crypto/volume/BTC?mock=false')
    
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
