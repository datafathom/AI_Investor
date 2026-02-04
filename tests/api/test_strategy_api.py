"""
Tests for Strategy API Endpoints
"""

import pytest
from unittest.mock import MagicMock, AsyncMock
from fastapi import FastAPI
from fastapi.testclient import TestClient
from web.api.strategy_api import router, get_strategy_builder_provider, get_strategy_execution_provider


@pytest.fixture
def api_app():
    """Create FastAPI app merchant testing."""
    app = FastAPI()
    app.include_router(router)
    return app


@pytest.fixture
def client(api_app):
    """Create test client."""
    return TestClient(api_app)


@pytest.fixture
def mock_builder(api_app):
    """Mock Strategy Builder Service."""
    service = AsyncMock()
    
    strategy = MagicMock()
    strategy.model_dump.return_value = {"id": "s1", "name": "Strategy 1"}
    
    rule = MagicMock()
    rule.model_dump.return_value = {"id": "r1", "condition": "price > 100"}
    
    service.create_strategy.return_value = strategy
    service.get_strategy_templates.return_value = [{"id": "t1", "name": "MA Crossover"}]
    service._get_strategy.return_value = strategy
    service.add_rule.return_value = rule
    service.validate_strategy.return_value = {"valid": True, "errors": []}
    
    api_app.dependency_overrides[get_strategy_builder_provider] = lambda: service
    return service


@pytest.fixture
def mock_execution(api_app):
    """Mock Strategy Execution Service."""
    service = AsyncMock()
    
    strategy = MagicMock()
    strategy.model_dump.return_value = {"id": "s1", "status": "running"}
    
    performance = MagicMock()
    performance.model_dump.return_value = {"sharpe": 1.5, "return": 0.2}
    
    drift = MagicMock()
    drift.model_dump.return_value = {"drift_score": 0.05}
    
    service.start_strategy.return_value = strategy
    service.stop_strategy.return_value = strategy
    service.pause_strategy.return_value = strategy
    service.get_strategy_performance.return_value = performance
    service.calculate_model_drift.return_value = drift
    
    api_app.dependency_overrides[get_strategy_execution_provider] = lambda: service
    return service


def test_create_strategy_success(client, mock_builder):
    """Test creating strategy."""
    from web.auth_utils import get_current_user
    client.app.dependency_overrides[get_current_user] = lambda: {"user_id": "test_user"}
    
    payload = {"user_id": "u1", "strategy_name": "Strategy 1"}
    response = client.post('/api/v1/strategy/create', json=payload)
    
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert data['data']['name'] == "Strategy 1"


def test_get_templates_success(client, mock_builder):
    """Test getting templates."""
    from web.auth_utils import get_current_user
    client.app.dependency_overrides[get_current_user] = lambda: {"user_id": "test_user"}
    
    response = client.get('/api/v1/strategy/templates')
    
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert len(data['data']) == 1


def test_get_strategy_success(client, mock_builder):
    """Test getting strategy."""
    from web.auth_utils import get_current_user
    client.app.dependency_overrides[get_current_user] = lambda: {"user_id": "test_user"}
    
    response = client.get('/api/v1/strategy/s1')
    
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert data['data']['id'] == "s1"


def test_start_strategy_success(client, mock_execution):
    """Test starting strategy."""
    from web.auth_utils import get_current_user
    client.app.dependency_overrides[get_current_user] = lambda: {"user_id": "test_user"}
    
    payload = {"portfolio_id": "p1"}
    response = client.post('/api/v1/strategy/s1/start', json=payload)
    
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert data['data']['status'] == "running"
