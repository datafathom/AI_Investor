"""
Tests for Corporate API Endpoints
Phase 6: API Endpoint Tests
"""

import pytest
from unittest.mock import patch, MagicMock, AsyncMock
from fastapi.testclient import TestClient
from fastapi import FastAPI
from web.api.corporate_api import router, get_corporate_service


@pytest.fixture
def app(mock_corporate_service):
    """Create FastAPI app for testing."""
    app = FastAPI()
    app.include_router(router)
    app.dependency_overrides[get_corporate_service] = lambda: mock_corporate_service
    return app


@pytest.fixture
def client(app):
    """Create test client."""
    return TestClient(app)


@pytest.fixture
def mock_corporate_service():
    """Mock CorporateService."""
    service = AsyncMock()
    from services.trading.corporate_service import EarningsEvent, CorporateAction
    mock_earnings = EarningsEvent(
        ticker='AAPL',
        date='2024-12-31',
        time='after_market',
        estimated_eps=2.5,
        estimated_revenue='100B'
    )
    service.get_earnings_calendar.return_value = [mock_earnings]
    mock_action = CorporateAction(
        ticker='AAPL',
        type='dividend',
        ex_date='2024-12-15',
        details='$0.25 per share'
    )
    service.get_corporate_actions.return_value = [mock_action]
    return service



def test_get_earnings_success(client, mock_corporate_service):
    """Test successful earnings calendar retrieval."""
    response = client.get('/api/v1/corporate/earnings?days=30')
    
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert isinstance(data['data'], list)
    assert len(data['data']) > 0


def test_list_actions_success(client, mock_corporate_service):
    """Test successful corporate actions retrieval."""
    response = client.get('/api/v1/corporate/actions')
    
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert isinstance(data['data'], list)
