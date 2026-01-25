"""
Tests for Margin API Endpoints
Phase 6: API Endpoint Tests
"""

import pytest
from unittest.mock import patch, MagicMock, AsyncMock
from fastapi.testclient import TestClient
from fastapi import FastAPI
from web.api.margin_api import router


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
def mock_margin_service():
    """Mock MarginService."""
    with patch('web.api.margin_api.get_margin_service') as mock:
        service = AsyncMock()
        from services.risk.margin_service import MarginStatus
        mock_status = MarginStatus(
            margin_buffer=10000.0,
            margin_used=5000.0,
            margin_available=5000.0,
            liquidation_distance=0.5,
            maintenance_margin=2500.0
        )
        service.get_margin_status.return_value = mock_status
        from services.risk.margin_service import DeleveragePlan
        mock_plan = DeleveragePlan(
            positions_to_close=[],
            total_to_sell=0.0,
            new_buffer=15000.0,
            urgency='low'
        )
        service.generate_deleverage_plan.return_value = mock_plan
        mock.return_value = service
        yield service


def test_get_margin_status_success(client, mock_margin_service):
    """Test successful margin status retrieval."""
    response = client.get('/api/v1/margin/status?portfolio_id=portfolio_1')
    
    assert response.status_code == 200
    data = response.get_json()
    assert 'buffer' in data
    assert 'used' in data
    assert 'available' in data


def test_generate_deleverage_plan_success(client, mock_margin_service):
    """Test successful deleverage plan generation."""
    response = client.post('/api/v1/margin/deleverage',
                          json={'target_buffer': 15000.0})
    
    assert response.status_code == 200
    data = response.get_json()
    assert 'status' in data
    assert 'plan' in data
