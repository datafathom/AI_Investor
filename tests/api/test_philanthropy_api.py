"""
Tests for Philanthropy API Endpoints
Phase 6: API Endpoint Tests
"""

import pytest
from unittest.mock import patch, MagicMock, AsyncMock
from fastapi.testclient import TestClient
from fastapi import FastAPI
from web.api.philanthropy_api import router


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
def mock_donation_service():
    """Mock DonationService."""
    with patch('web.api.philanthropy_api.get_donation_service') as mock:
        service = AsyncMock()
        from services.philanthropy.donation_service import DonationRecord
        mock_record = DonationRecord(
            id='donation_1',
            amount=1000.0,
            status='completed',
            tax_savings_est=250.0
        )
        service.route_excess_alpha.return_value = mock_record
        service.get_donation_history.return_value = [mock_record]
        service.get_impact_summary.return_value = {
            'donated_ytd': 5000.0,
            'tax_savings': 1250.0,
            'effective_cost': 3750.0
        }
        mock.return_value = service
        yield service


def test_trigger_donation_success(client, mock_donation_service):
    """Test successful donation routing."""
    response = client.post('/donate',
                          json={
                              'amount': 1000.0,
                              'allocations': [{'category': 'Climate', 'percentage': 40}]
                          })
    
    assert response.status_code == 200
    data = response.get_json()
    assert 'transaction_id' in data
    assert 'status' in data


def test_get_donation_history_success(client, mock_donation_service):
    """Test successful donation history retrieval."""
    response = client.get('/history')
    
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)


def test_get_impact_summary_success(client, mock_donation_service):
    """Test successful impact summary retrieval."""
    response = client.get('/impact-summary')
    
    assert response.status_code == 200
    data = response.get_json()
    assert 'donated_ytd' in data or 'tax_savings' in data
