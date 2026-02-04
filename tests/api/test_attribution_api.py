
import pytest
from unittest.mock import AsyncMock, patch
from fastapi import FastAPI
from fastapi.testclient import TestClient
from web.api.attribution_api import router
from datetime import datetime, timezone
from web.auth_utils import get_current_user

@pytest.fixture
def api_app(mock_attribution_service):
    """Create FastAPI app for testing."""
    app = FastAPI()
    app.include_router(router)
    from web.api.attribution_api import get_attribution_service
    app.dependency_overrides[get_attribution_service] = lambda: mock_attribution_service
    app.dependency_overrides[get_current_user] = lambda: {"id": "user_1", "role": "user"}
    return app

@pytest.fixture
def client(api_app):
    """Create test client."""
    return TestClient(api_app)

@pytest.fixture
def mock_attribution_service():
    """Mock AttributionServiceInstance."""
    from unittest.mock import MagicMock
    service = MagicMock()
    service.get_available_benchmarks.return_value = [{'id': 'sp500', 'name': 'S&P 500'}]
    
    from services.analysis.attribution_service import BrinsonAttribution, DateRange
    mock_result = BrinsonAttribution(
        portfolio_id='portfolio_1',
        benchmark_id='sp500',
        period=DateRange(start='2024-01-01', end='2024-12-31'),
        total_active_return=0.05,
        total_allocation_effect=0.02,
        total_selection_effect=0.03,
        total_interaction_effect=0.0,
        sector_attributions=[],
        regime_shifts=[],
        calculated_at=datetime.now(timezone.utc).isoformat()
    )
    service.calculate_brinson_attribution = AsyncMock(return_value=mock_result)
    service.compare_benchmarks = AsyncMock(return_value={'comparison': 'result'})
    service.get_sector_allocation_effect = AsyncMock(return_value=0.02)
    service.get_selection_effect = AsyncMock(return_value=0.03)
    return service

def test_get_attribution_success(client, mock_attribution_service):
    """Test successful attribution retrieval."""
    response = client.get('/api/v1/attribution/portfolio_1?benchmark=sp500&start=2024-01-01&end=2024-12-31')
    
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert 'data' in data

def test_get_benchmarks_success(client, mock_attribution_service):
    """Test successful benchmarks retrieval."""
    response = client.get('/api/v1/attribution/benchmarks')
    
    assert response.status_code == 200
    data = response.json()
    assert 'success' in data or isinstance(data, list)

def test_compare_benchmarks_success(client, mock_attribution_service):
    """Test successful benchmark comparison."""
    response = client.post('/api/v1/attribution/compare',
                          json={
                              'portfolio_id': 'portfolio_1',
                              'benchmarks': ['sp500', 'nasdaq']
                          })
    
    assert response.status_code == 200
    data = response.json()
    assert 'success' in data or 'comparison' in data
