"""
Tests for Health API Endpoints
"""

import pytest
from unittest.mock import MagicMock, AsyncMock
from fastapi import FastAPI
from fastapi.testclient import TestClient
from web.api.health_api import router, get_health_check_provider, get_system_health_provider


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
def mock_health_service(api_app):
    """Mock HealthCheckService."""
    service = MagicMock()
    service.check_postgres.return_value = {'status': 'UP', 'latency_ms': 10}
    service.check_redis.return_value = {'status': 'UP', 'latency_ms': 5}
    api_app.dependency_overrides[get_health_check_provider] = lambda: service
    return service


@pytest.fixture
def mock_system_health_service(api_app):
    """Mock SystemHealthService."""
    service = MagicMock()
    service.get_health_status.return_value = {'cpu_usage': 20, 'memory_usage': 40}
    api_app.dependency_overrides[get_system_health_provider] = lambda: service
    return service


def test_health_check_success(client):
    """Test basic health check."""
    response = client.get('/health')
    
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert data['data']['status'] == 'healthy'


def test_readiness_check_success(client, mock_health_service):
    """Test readiness check success."""
    response = client.get('/health/readiness')
    
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert data['data']['status'] == 'ready'


def test_readiness_check_failure(api_app, client, mock_health_service):
    """Test readiness check failure when dependency is DOWN."""
    mock_health_service.check_postgres.return_value = {'status': 'DOWN'}
    
    response = client.get('/health/readiness')
    
    assert response.status_code == 503
    data = response.json()
    assert data['success'] is False
    assert data['data']['status'] == 'not_ready'


def test_liveness_check_success(client):
    """Test liveness check."""
    response = client.get('/health/liveness')
    
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert data['data']['status'] == 'alive'


def test_detailed_health_success(client, mock_health_service, mock_system_health_service):
    """Test detailed health check."""
    response = client.get('/health/detailed')
    
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert 'system' in data['data']['checks']
