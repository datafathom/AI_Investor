"""
Tests for Consolidated Wave APIs
"""

import pytest
from unittest.mock import MagicMock, AsyncMock
from fastapi import FastAPI
from fastapi.testclient import TestClient
from web.api.wave_apis import all_routers, get_monte_carlo_provider, get_compliance_provider


@pytest.fixture
def api_app():
    """Create FastAPI app with all wave routers."""
    app = FastAPI()
    for router in all_routers:
        app.include_router(router)
    return app


@pytest.fixture
def client(api_app):
    """Create test client."""
    return TestClient(api_app)


@pytest.fixture
def mock_monte_carlo(api_app):
    """Mock Monte Carlo service."""
    service = MagicMock()
    res = MagicMock()
    res.paths = [[100, 105], [100, 95]]
    res.quantiles = {"50%": 102}
    res.ruin_probability = 0.05
    res.median_final = 1000000
    service.run_gbm_simulation.return_value = res
    
    api_app.dependency_overrides[get_monte_carlo_provider] = lambda: service
    return service


@pytest.fixture
def mock_compliance(api_app):
    """Mock Compliance service."""
    service = MagicMock()
    service.get_compliance_score.return_value = 95
    service.get_sar_alerts.return_value = []
    service.get_audit_logs.return_value = []
    
    api_app.dependency_overrides[get_compliance_provider] = lambda: service
    return service


def test_monte_carlo_simulation_success(client, mock_monte_carlo):
    """Test Monte Carlo endpoint."""
    from web.auth_utils import get_current_user
    client.app.dependency_overrides[get_current_user] = lambda: {"user_id": "test_user"}
    
    payload = {"initial_value": 1000000, "mu": 0.08, "sigma": 0.15}
    response = client.post('/api/v1/backtest/monte-carlo', json=payload)
    
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert 'paths' in data['data']


def test_compliance_overview_success(client, mock_compliance):
    """Test compliance overview endpoint."""
    from web.auth_utils import get_current_user
    client.app.dependency_overrides[get_current_user] = lambda: {"user_id": "test_user"}
    
    response = client.get('/api/v1/compliance/overview')
    
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert data['data']['compliance_score'] == 95


def test_system_health_success(client):
    """Test system health endpoint."""
    from web.auth_utils import get_current_user
    client.app.dependency_overrides[get_current_user] = lambda: {"user_id": "test_user"}
    
    # We use the default mock if not overridden
    response = client.get('/api/v1/system/health')
    
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
