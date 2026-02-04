"""
Tests for Philanthropy API Endpoints
"""

import pytest
from unittest.mock import MagicMock, AsyncMock
from fastapi import FastAPI
from fastapi.testclient import TestClient
from web.api.philanthropy_api import router, get_donation_provider, get_esg_provider, get_portfolio_manager_provider


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
def mock_donation_service(api_app):
    """Mock Donation Service."""
    service = AsyncMock()
    
    record = MagicMock()
    record.id = "don_123"
    record.status = "completed"
    record.tax_savings_est = 50.0
    record.model_dump.return_value = {"id": "don_123", "amount": 100.0}
    
    service.route_excess_alpha.return_value = record
    service.get_donation_history.return_value = [record]
    service.get_tax_impact_summary.return_value = {
        "total_donated_ytd": 1000.0,
        "estimated_tax_savings": 300.0,
        "effective_cost": 700.0
    }
    
    api_app.dependency_overrides[get_donation_provider] = lambda: service
    return service


@pytest.fixture
def mock_esg_service(api_app):
    """Mock ESG Service."""
    service = AsyncMock()
    
    scores = MagicMock()
    scores.composite = 85.0
    scores.model_dump.return_value = {"composite": 85.0}
    
    service.get_portfolio_esg_scores.return_value = scores
    service.detect_sin_stocks.return_value = []
    
    footprint = MagicMock()
    footprint.model_dump.return_value = {"tons_co2": 12.5}
    service.calculate_carbon_footprint.return_value = footprint
    service.get_alpha_vs_carbon_data.return_value = []
    
    api_app.dependency_overrides[get_esg_provider] = lambda: service
    return service


@pytest.fixture
def mock_portfolio_manager(api_app):
    """Mock Portfolio Manager."""
    pm = MagicMock()
    
    pos = MagicMock()
    pos.symbol = "AAPL"
    
    pm.defensive.positions = [pos]
    pm.aggressive.positions = []
    
    api_app.dependency_overrides[get_portfolio_manager_provider] = lambda: pm
    return pm


def test_trigger_donation_success(client, mock_donation_service):
    """Test triggering donation."""
    payload = {"amount": 100.0, "allocations": [{"category": "Climate", "percentage": 100}]}
    response = client.post('/api/v1/philanthropy/donate', json=payload)
    
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert data['data']['transaction_id'] == "don_123"


def test_get_donation_history_success(client, mock_donation_service):
    """Test getting donation history."""
    response = client.get('/api/v1/philanthropy/history')
    
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert len(data['data']) == 1


def test_get_impact_summary_success(client, mock_donation_service):
    """Test getting impact summary."""
    response = client.get('/api/v1/philanthropy/summary')
    
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert data['data']['donated_ytd'] == 1000.0


def test_get_esg_metrics_success(client, mock_esg_service, mock_portfolio_manager):
    """Test getting ESG metrics."""
    response = client.get('/api/v1/philanthropy/esg')
    
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert data['data']['karma_score'] == 76.5 # 85 * 0.9 = 76.5


def test_get_carbon_data_success(client, mock_esg_service, mock_portfolio_manager):
    """Test getting carbon data."""
    response = client.get('/api/v1/philanthropy/carbon?portfolio_value=1000000')
    
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert 'footprint' in data['data']
