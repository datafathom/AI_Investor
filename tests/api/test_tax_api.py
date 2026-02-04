"""
Tests for Tax API Endpoints
"""

import pytest
from unittest.mock import MagicMock, AsyncMock
from fastapi import FastAPI
from fastapi.testclient import TestClient
from web.api.tax_api import router, get_taxbit_provider


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
    """Mock TaxBit Client."""
    service = AsyncMock()
    service.get_harvesting_opportunities.return_value = [{"symbol": "BTC", "loss": 500.0}]
    
    api_app.dependency_overrides[get_taxbit_provider] = lambda: service
    return service


def test_get_opportunities_success(client, mock_client):
    """Test getting tax loss harvesting opportunities."""
    from web.auth_utils import get_current_user
    client.app.dependency_overrides[get_current_user] = lambda: {"user_id": "test_user"}
    
    response = client.get('/api/v1/tax_api/tax/harvesting/opportunities')
    
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert data['data'][0]['symbol'] == "BTC"
