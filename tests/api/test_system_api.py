"""
Tests for System API Endpoints
"""

import pytest
from unittest.mock import MagicMock, AsyncMock
from fastapi import FastAPI
from fastapi.testclient import TestClient
from web.api.system_api import (
    router,
    get_secret_manager_provider,
    get_totp_provider,
    get_system_health_service,
    get_audit_integrity_provider,
    get_governor_provider
)


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
def mock_health(api_app):
    """Mock SystemHealthService."""
    service = AsyncMock()
    service.get_health_status.return_value = {
        "kafka": {"details": {"lag": 0}}
    }
    service.restart_service.return_value = True
    
    api_app.dependency_overrides[get_system_health_service] = lambda: service
    return service


@pytest.fixture
def mock_secrets(api_app):
    """Mock SecretManager."""
    sm = MagicMock()
    sm.get_status.return_value = {"status": "Active", "engine": "Env"}
    
    api_app.dependency_overrides[get_secret_manager_provider] = lambda: sm
    return sm


@pytest.fixture
def mock_totp(api_app):
    """Mock TotpService."""
    totp = MagicMock()
    totp.verify_code.return_value = True
    
    api_app.dependency_overrides[get_totp_provider] = lambda: totp
    return totp


@pytest.fixture
def mock_audit(api_app):
    """Mock AuditIntegrityService."""
    service = AsyncMock()
    service.get_audit_stream.return_value = [{"event": "login"}]
    
    api_app.dependency_overrides[get_audit_integrity_provider] = lambda: service
    return service


@pytest.fixture
def mock_governor(api_app):
    """Mock ApiGovernor."""
    governor = MagicMock()
    governor.get_all_stats.return_value = {"user1": 10}
    
    api_app.dependency_overrides[get_governor_provider] = lambda: governor
    return governor


def test_get_secrets_status_minimal_success(client, mock_secrets):
    """Test getting minimal secrets status."""
    response = client.get('/api/v1/system/secrets')
    
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert data['data']['status'] == "Healthy"


def test_get_secrets_status_full_success(client, mock_secrets, mock_totp):
    """Test getting full secrets status with MFA."""
    payload = {"mfa_code": "123456"}
    response = client.post('/api/v1/system/secrets', json=payload)
    
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert data['data']['mfa_verified'] is True


def test_get_secrets_status_full_invalid_mfa(client, mock_secrets, mock_totp):
    """Test full secrets status with invalid MFA."""
    mock_totp.verify_code.return_value = False
    payload = {"mfa_code": "wrong"}
    response = client.post('/api/v1/system/secrets', json=payload)
    
    assert response.status_code == 401
    data = response.json()
    assert data['success'] is False


def test_get_system_health_success(client, mock_health):
    """Test system health."""
    response = client.get('/api/v1/system/health')
    
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True


def test_restart_service_success(client, mock_health):
    """Test restarting service."""
    response = client.post('/api/v1/system/restart/kafka')
    
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True


def test_get_kafka_lag_success(client, mock_health):
    """Test getting Kafka lag."""
    response = client.get('/api/v1/system/kafka/lag')
    
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert data['data']['lag'] == 0


def test_log_frontend_error_success(client):
    """Test logging frontend error."""
    payload = {"error": "UI Hang", "stack": "trace", "context": {"browser": "chrome"}}
    response = client.post('/api/v1/system/error', json=payload)
    
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True


def test_get_audit_stream_success(client, mock_audit):
    """Test getting audit stream."""
    response = client.get('/api/v1/system/audit/stream')
    
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert len(data['data']) == 1


def test_get_api_quotas_success(client, mock_governor):
    """Test getting API quotas."""
    response = client.get('/api/v1/system/quotas')
    
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True


def test_get_supply_chain_health_success(client):
    """Test supply chain health."""
    response = client.get('/api/v1/system/supply-chain')
    
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert data['data']['status'] == "Healthy"
