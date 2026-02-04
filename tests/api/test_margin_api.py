"""
Tests for Margin API Endpoints
"""

import pytest
from unittest.mock import MagicMock, AsyncMock
from fastapi import FastAPI
from fastapi.testclient import TestClient
from web.api.margin_api import router, get_margin_provider


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
def mock_margin_service(api_app):
    """Mock Margin Service."""
    service = AsyncMock()
    
    # Mock MarginStatus
    status = MagicMock()
    status.margin_buffer = 0.25
    status.margin_used = 100000.0
    status.margin_available = 400000.0
    status.liquidation_distance = 0.15
    status.maintenance_margin = 0.10
    service.get_margin_status.return_value = status
    
    # Mock DeleveragePlan
    plan = MagicMock()
    plan.positions_to_close = ["AAPL", "TSLA"]
    plan.total_to_sell = 50000.0
    plan.new_buffer = 0.35
    plan.urgency = "high"
    service.generate_deleverage_plan.return_value = plan
    
    service.check_danger_zone.return_value = True
    
    api_app.dependency_overrides[get_margin_provider] = lambda: service
    return service


def test_get_margin_status_success(client, mock_margin_service):
    """Test getting margin status."""
    response = client.get('/api/v1/margin/status')
    
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert data['data']['buffer'] == 0.25


def test_generate_deleverage_plan_success(client, mock_margin_service):
    """Test generating deleverage plan."""
    response = client.post('/api/v1/margin/deleverage', json={'target_buffer': 0.35})
    
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert data['data']['new_buffer'] == 0.35


def test_check_danger_zone_success(client, mock_margin_service):
    """Test checking danger zone."""
    response = client.get('/api/v1/margin/danger-zone')
    
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert data['data']['is_danger'] is True
