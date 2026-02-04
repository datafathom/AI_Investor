"""
Tests for Square API Endpoints
"""

import pytest
from unittest.mock import MagicMock, AsyncMock
from fastapi import FastAPI
from fastapi.testclient import TestClient
from web.api.square_api import router, get_square_provider


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
def mock_client(api_app):
    """Mock Square Client."""
    service = AsyncMock()
    service.get_merchant_stats.return_value = {"total_sales": 1000.0}
    service.get_catalog.return_value = [{"id": "item1", "name": "Coffee"}]
    service.get_transactions.return_value = [{"id": "tx1", "amount": 5.0}]
    service.get_refunds.return_value = [{"id": "ref1", "amount": 2.0}]
    
    api_app.dependency_overrides[get_square_provider] = lambda: service
    return service


def test_get_stats_success(client, mock_client):
    """Test getting stats."""
    response = client.get('/api/v1/square/merchant/square/stats')
    
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert data['data']['total_sales'] == 1000.0


def test_get_catalog_success(client, mock_client):
    """Test getting catalog."""
    response = client.get('/api/v1/square/merchant/square/catalog')
    
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert data['data'][0]['name'] == "Coffee"


def test_get_transactions_success(client, mock_client):
    """Test getting transactions."""
    response = client.get('/api/v1/square/transactions?start_date=2024-01-01')
    
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert len(data['data']['transactions']) == 1


def test_get_refunds_success(client, mock_client):
    """Test getting refunds."""
    response = client.get('/api/v1/square/refunds')
    
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert len(data['data']['refunds']) == 1
