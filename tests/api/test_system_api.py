"""
Tests for System API Endpoints
Phase 6: API Endpoint Tests
"""

import pytest
from unittest.mock import patch, MagicMock, AsyncMock
from fastapi.testclient import TestClient
from fastapi import FastAPI
from web.api.system_api import router


@pytest.fixture
def app():
    """Create FastAPI app for testing."""
    app = FastAPI()
    app.include_router(router)
    return app


@pytest.fixture
def client(app):
    """Create test client."""
    return TestClient(app)


@pytest.fixture
def mock_secret_manager():
    """Mock SecretManager."""
    with patch('web.api.system_api.get_secret_manager') as mock:
        manager = MagicMock()
        manager.get_status.return_value = {
            'status': 'Active',
            'engine': 'env'
        }
        mock.return_value = manager
        yield manager


@pytest.fixture
def mock_system_health_service():
    """Mock SystemHealthService."""
    with patch('web.api.system_api.get_system_health_service') as mock:
        service = AsyncMock()
        from services.security.system_health_service import ComponentHealth
        mock_health = {
            'overall': ComponentHealth(
                status='healthy',
                message='All systems operational',
                details={}
            ),
            'kafka': ComponentHealth(
                status='healthy',
                message='Kafka operational',
                details={'lag': 0}
            )
        }
        service.get_health_status.return_value = mock_health
        service.restart_service.return_value = True
        mock.return_value = service
        yield service


def test_get_secrets_status_success(client, mock_secret_manager):
    """Test successful secrets status retrieval."""
    response = client.get('/api/v1/system/secrets')
    
    assert response.status_code == 200
    data = response.get_json()
    assert 'status' in data
    assert 'engine' in data


def test_get_system_health_success(client, mock_system_health_service):
    """Test successful system health retrieval."""
    response = client.get('/api/v1/system/health')
    
    assert response.status_code == 200
    data = response.get_json()
    assert 'overall' in data or 'status' in data


def test_restart_service_success(client, mock_system_health_service):
    """Test successful service restart."""
    response = client.post('/api/v1/system/restart/test_service')
    
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == 'success'
    assert 'message' in data


def test_get_kafka_lag_success(client, mock_system_health_service):
    """Test successful Kafka lag retrieval."""
    response = client.get('/api/v1/system/kafka/lag')
    
    assert response.status_code == 200
    data = response.get_json()
    assert 'lag' in data or 'details' in data
