"""
Tests for Institutional API Endpoints
Phase: Institutional Features & Professional Tools
"""

import pytest
from unittest.mock import AsyncMock, MagicMock
from fastapi import FastAPI
from fastapi.testclient import TestClient
from datetime import timezone, datetime
from web.api.institutional_api import router, get_institutional_service, get_professional_tools_service
from web.auth_utils import get_current_user
from schemas.institutional import Client, WhiteLabelConfig


@pytest.fixture
def api_app(mock_service):
    """Create FastAPI app for testing."""
    app = FastAPI()
    app.include_router(router)
    app.dependency_overrides[get_institutional_service] = lambda: mock_service
    app.dependency_overrides[get_current_user] = lambda: {"id": "user_1", "role": "advisor"}
    return app


@pytest.fixture
def client(api_app):
    """Create test client."""
    return TestClient(api_app)


@pytest.fixture
def mock_service():
    """Mock InstitutionalService fixture."""
    service = AsyncMock()
    return service


def test_create_client_success(client, mock_service):
    """Test successful client creation via API."""
    now = datetime.now(timezone.utc)
    mock_service.create_client.return_value = Client(
        client_id='client_123',
        advisor_id='advisor_1',
        client_name='Test Client',
        portfolio_ids=[],
        created_date=now,
        updated_date=now
    )
    
    response = client.post('/api/v1/institutional/client/create',
                          json={
                              'advisor_id': 'advisor_1',
                              'client_name': 'Test Client'
                          })
    
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert data['data']['client_name'] == 'Test Client'


def test_get_fee_analytics(client, mock_service):
    """Test fee analytics endpoint."""
    mock_service.get_revenue_forecast.return_value = {
        'current_fees': 1250000.0,
        'projected_fees': 1306250.0,
        'growth_rate': 0.045
    }
    
    response = client.get('/api/v1/institutional/analytics/fees')
    
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert data['data']['current_fees'] == 1250000.0


def test_get_risk_analytics(client, mock_service):
    """Test risk analytics endpoint."""
    mock_service.get_client_risk_profile.return_value = {
        'volatility_score': 15.5,
        'health_status': 'Healthy'
    }
    
    response = client.get('/api/v1/institutional/analytics/risk/client_123')
    
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert data['data']['volatility_score'] == 15.5


def test_configure_white_label(client, mock_service):
    """Test white-label configuration."""
    now = datetime.now(timezone.utc)
    mock_service.configure_white_label.return_value = WhiteLabelConfig(
        config_id='cfg_123',
        organization_id='org_1',
        branding_name='Test Brand',
        created_date=now,
        updated_date=now
    )
    
    response = client.post('/api/v1/institutional/whitelabel/configure',
                          json={'organization_id': 'org_1', 'branding_name': 'Test Brand'})
    
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert data['data']['branding_name'] == 'Test Brand'
