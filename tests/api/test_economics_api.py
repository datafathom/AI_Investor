"""
Tests for Economics API Endpoints
"""

import pytest
from unittest.mock import MagicMock, AsyncMock
from fastapi import FastAPI
from fastapi.testclient import TestClient
from web.api.economics_api import router, get_clew_index_provider


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
def mock_clew_service(api_app):
    """Mock CLEW Index service."""
    service = MagicMock()
    service.calculate_current_index.return_value = 1.25
    service.get_uhnwi_inflation_rate.return_value = 0.08
    api_app.dependency_overrides[get_clew_index_provider] = lambda: service
    return service


def test_get_clew_index_success(client, mock_clew_service):
    """Test successful CLEW index retrieval."""
    response = client.get('/api/v1/economics/clew')
    
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert data['data']['current_index'] == 1.25
    assert data['data']['inflation_rate'] == 0.08


def test_get_cpi_data_success(client):
    """Test successful CPI data retrieval."""
    response = client.get('/api/v1/economics/cpi')
    
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert data['data']['current_rate'] == 0.032
