"""
Tests for Paper Trading API Endpoints
"""

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from web.api.paper_trading_api import router
from web.auth_utils import get_current_user


@pytest.fixture
def api_app():
    """Create FastAPI app for testing."""
    app = FastAPI()
    app.include_router(router)
    # Mock current user
    app.dependency_overrides[get_current_user] = lambda: {'id': 'user_1', 'email': 'test@example.com'}
    return app


@pytest.fixture
def client(api_app):
    """Create test client."""
    return TestClient(api_app)


def test_get_portfolio_summary_success(client):
    """Test getting portfolio summary."""
    response = client.get('/api/v1/paper-trading/portfolio')
    
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert data['data']['portfolio_id'] == "paper_001"


def test_get_portfolio_by_id_success(client):
    """Test getting portfolio by ID."""
    response = client.get('/api/v1/paper-trading/portfolio/paper_001')
    
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True


def test_create_virtual_portfolio_success(client):
    """Test creating virtual portfolio."""
    payload = {"user_id": "user_1", "portfolio_name": "New Port", "initial_cash": 50000.0}
    response = client.post('/api/v1/paper-trading/portfolio/create', json=payload)
    
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert data['data']['cash'] == 50000.0


def test_get_trades_success(client):
    """Test getting trades."""
    response = client.get('/api/v1/paper-trading/trades?limit=5')
    
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert len(data['data']) <= 5


def test_execute_paper_order_success(client):
    """Test executing paper order."""
    payload = {"portfolio_id": "paper_001", "symbol": "AAPL", "quantity": 10, "order_type": "market"}
    response = client.post('/api/v1/paper-trading/order/execute', json=payload)
    
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert data['data']['symbol'] == "AAPL"


def test_get_portfolio_performance_success(client):
    """Test getting performance."""
    response = client.get('/api/v1/paper-trading/portfolio/paper_001/performance')
    
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert 'sharpe_ratio' in data['data']


def test_run_simulation_success(client):
    """Test running simulation."""
    payload = {
        "strategy_name": "SMA Crossover",
        "start_date": "2025-01-01",
        "end_date": "2025-12-31",
        "initial_capital": 100000.0
    }
    response = client.post('/api/v1/paper-trading/simulation/run', json=payload)
    
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert data['data']['total_return'] == 15.0
