"""
Tests for Homeostasis API Endpoints
"""

import pytest
from unittest.mock import MagicMock, AsyncMock
from fastapi import FastAPI
from fastapi.testclient import TestClient
from web.api.homeostasis_api import router, get_homeostasis_provider, get_philanthropy_provider


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
def mock_homeostasis_service(api_app):
    """Mock HomeostasisService."""
    service = MagicMock()
    service.get_homeostasis_status.return_value = {'net_worth': 1000000, 'excess_alpha': 50000}
    api_app.dependency_overrides[get_homeostasis_provider] = lambda: service
    return service


@pytest.fixture
def mock_philanthropy_service(api_app):
    """Mock PhilanthropyService."""
    service = MagicMock()
    api_app.dependency_overrides[get_philanthropy_provider] = lambda: service
    return service


def test_get_status_success(client, mock_homeostasis_service):
    """Test getting homeostasis status."""
    response = client.get('/api/v1/homeostasis/status')
    
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert data['data']['net_worth'] == 1000000


def test_update_metrics_success(client, mock_homeostasis_service):
    """Test updating net worth."""
    response = client.post('/api/v1/homeostasis/update',
                           json={'net_worth': 1100000})
    
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    mock_homeostasis_service.update_net_worth.assert_called_once_with('default', 1100000)


def test_manual_donate_success(client, mock_philanthropy_service):
    """Test manual donation."""
    response = client.post('/api/v1/homeostasis/donate',
                           json={'amount': 10000})
    
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert data['data']['amount'] == 10000
    mock_philanthropy_service.donate_excess_alpha.assert_called_once_with('default', 10000)
