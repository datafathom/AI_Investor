"""
Tests for Optimization API Endpoints
"""

import pytest
from unittest.mock import MagicMock, AsyncMock
from fastapi import FastAPI
from fastapi.testclient import TestClient
from web.api.optimization_api import router, get_optimizer_provider, get_rebalancing_provider
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


@pytest.fixture
def mock_optimizer(api_app):
    """Mock Optimizer Service."""
    service = AsyncMock()
    
    result = MagicMock()
    result.model_dump.return_value = {"weights": {"AAPL": 0.6, "MSFT": 0.4}, "sharpe": 1.2}
    service.optimize.return_value = result
    
    api_app.dependency_overrides[get_optimizer_provider] = lambda: service
    return service


@pytest.fixture
def mock_rebalancing(api_app):
    """Mock Rebalancing Service."""
    service = AsyncMock()
    
    service.check_rebalancing_needed.return_value = True
    
    recommendation = MagicMock()
    recommendation.model_dump.return_value = {"trades": [{"symbol": "AAPL", "side": "SELL", "quantity": 10}]}
    service.generate_rebalancing_recommendation.return_value = recommendation
    
    history_item = MagicMock()
    history_item.model_dump.return_value = {"id": "reb_123", "timestamp": "2026-02-03T10:00:00"}
    service.execute_rebalancing.return_value = history_item
    service.get_rebalancing_history.return_value = [history_item]
    
    api_app.dependency_overrides[get_rebalancing_provider] = lambda: service
    return service


def test_optimize_portfolio_success(client, mock_optimizer):
    """Test optimizing portfolio."""
    payload = {
        "objective": "maximize_sharpe",
        "method": "mean_variance"
    }
    response = client.post('/api/v1/optimization/optimize/port_123', json=payload)
    
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert data['data']['sharpe'] == 1.2


def test_check_rebalancing_success(client, mock_rebalancing):
    """Test checking rebalancing."""
    response = client.get('/api/v1/optimization/rebalancing/check/port_123?threshold=0.05')
    
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert data['data']['needs_rebalancing'] is True


def test_recommend_rebalancing_success(client, mock_rebalancing):
    """Test recommending rebalancing."""
    payload = {"strategy": "threshold"}
    response = client.post('/api/v1/optimization/rebalancing/recommend/port_123', json=payload)
    
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert len(data['data']['trades']) == 1


def test_execute_rebalancing_success(client, mock_rebalancing):
    """Test executing rebalancing."""
    payload = {
        "recommendation": {
            "portfolio_id": "port_123",
            "current_weights": {"AAPL": 0.5},
            "target_weights": {"AAPL": 0.6},
            "recommended_trades": [{"symbol": "AAPL", "action": "BUY", "quantity": 10, "price": 150.0}],
            "drift_percentage": 0.1,
            "estimated_cost": 5.0,
            "estimated_tax_impact": 0.0,
            "requires_approval": True,
            "recommendation_date": "2026-02-03T10:00:00"
        },
        "approved": True
    }
    response = client.post('/api/v1/optimization/rebalancing/execute/port_123', json=payload)
    
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert data['data']['id'] == "reb_123"


def test_get_rebalancing_history_success(client, mock_rebalancing):
    """Test getting rebalancing history."""
    response = client.get('/api/v1/optimization/rebalancing/history/port_123')
    
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert len(data['data']) == 1
