
import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from fastapi import FastAPI
from fastapi.testclient import TestClient
from web.api.binance_api import router, get_binance_service
from web.auth_utils import get_current_user

@pytest.fixture
def api_app(mock_binance_service):
    """Create FastAPI app for testing."""
    app = FastAPI()
    app.include_router(router)
    app.dependency_overrides[get_binance_service] = lambda: mock_binance_service
    app.dependency_overrides[get_current_user] = lambda: {"id": "user_1", "role": "user"}
    return app

@pytest.fixture
def client(api_app):
    """Create test client."""
    return TestClient(api_app)

@pytest.fixture
def mock_binance_service():
    """Mock Binance Service."""
    service = AsyncMock()
    service.get_ticker.return_value = {
        'symbol': 'BTCUSDT',
        'price': '50000.00',
        'priceChangePercent': '2.5'
    }
    service.get_order_book.return_value = {
        'bids': [[50000, 1.0]],
        'asks': [[50001, 1.0]]
    }
    service.place_order.return_value = {'orderId': 12345, 'status': 'NEW'}
    return service

def test_get_ticker_success(client, mock_binance_service):
    """Test successful ticker retrieval."""
    response = client.get('/api/v1/binance/ticker/BTCUSDT')
    
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert data['data']['symbol'] == 'BTCUSDT'

def test_get_order_book_success(client, mock_binance_service):
    """Test successful order book retrieval."""
    response = client.get('/api/v1/binance/depth/BTCUSDT?limit=5')
    
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert 'bids' in data['data']

def test_place_order_success(client, mock_binance_service):
    """Test successful order placement."""
    response = client.post('/api/v1/binance/order',
                          json={
                              'symbol': 'BTCUSDT',
                              'side': 'BUY',
                              'quantity': 0.001
                          })
    
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert data['data']['orderId'] == 12345
