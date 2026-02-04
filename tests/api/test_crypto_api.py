"""
Tests for Crypto API Endpoints
Phase 6: API Endpoint Tests
"""

import pytest
from unittest.mock import MagicMock, AsyncMock
from fastapi import FastAPI
from fastapi.testclient import TestClient
from web.api.crypto_api import router, get_crypto_provider


@pytest.fixture
def api_app():
    """Create FastAPI app for testing."""
    app = FastAPI()
    app.include_router(router)
    return app


@pytest.fixture
def client(api_app):
    """Create test client."""
    return TestClient(api_app)


@pytest.fixture
def mock_crypto_client(api_app):
    """Mock CryptoCompare client."""
    service = AsyncMock()
    # Mocking price is synchronous in some contexts, but let's assume AsyncMock is safer
    api_app.dependency_overrides[get_crypto_provider] = lambda: service
    return service


def test_get_crypto_price_success(client, mock_crypto_client):
    """Test successful crypto price retrieval."""
    mock_prices = {
        'BTC': {'USD': 50000.0, 'EUR': 45000.0},
        'ETH': {'USD': 3000.0, 'EUR': 2700.0}
    }
    
    mock_crypto_client.get_price.return_value = mock_prices
    
    response = client.get('/api/v1/market/crypto/price?symbols=BTC,ETH&currencies=USD,EUR&mock=false')
    
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert 'BTC' in data['data']
    assert 'ETH' in data['data']


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
    
    mock_crypto_client.get_top_exchanges_volume.return_value = mock_volumes
    
    response = client.get('/api/v1/market/crypto/volume/BTC?mock=false')
    
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert isinstance(data['data'], list)
    assert data['data'][0]['exchange'] == 'Binance'
