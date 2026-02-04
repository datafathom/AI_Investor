"""
Tests for Tax Optimization API Endpoints
"""

import pytest
from unittest.mock import MagicMock, AsyncMock
from fastapi import FastAPI
from fastapi.testclient import TestClient
from web.api.tax_optimization_api import (
    router,
    get_enhanced_harvest_provider,
    get_tax_optimization_provider
)


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
def mock_harvest(api_app):
    """Mock EnhancedTaxHarvestingService."""
    service = AsyncMock()
    
    candidate = MagicMock()
    candidate.ticker = "AAPL"
    candidate.unrealized_loss = 1000.0
    candidate.cost_basis = 5000.0
    candidate.current_value = 4000.0
    
    opp = MagicMock()
    opp.candidate = candidate
    opp.tax_savings = 300.0
    opp.net_benefit = 250.0
    opp.replacement_suggestions = ["MSFT"]
    opp.wash_sale_risk = False
    opp.rank = 1
    
    service.identify_harvest_opportunities.return_value = [opp]
    
    result = MagicMock()
    result.total_tax_savings = 300.0
    result.total_net_benefit = 250.0
    result.trades_required = 1
    result.requires_approval = False
    result.opportunities = [opp]
    
    service.batch_harvest_analysis.return_value = result
    service.execute_harvest.return_value = {"status": "executed"}
    
    api_app.dependency_overrides[get_enhanced_harvest_provider] = lambda: service
    return service


@pytest.fixture
def mock_optimize(api_app):
    """Mock TaxOptimizationService."""
    service = AsyncMock()
    service.optimize_lot_selection.return_value = {"lots": []}
    service.project_year_end_tax.return_value = {"projected_bill": 5000.0}
    service.optimize_withdrawal_sequence.return_value = {"sequence": []}
    
    api_app.dependency_overrides[get_tax_optimization_provider] = lambda: service
    return service


def test_get_harvest_opportunities_success(client, mock_harvest):
    """Test getting harvest opportunities."""
    from web.auth_utils import get_current_user
    client.app.dependency_overrides[get_current_user] = lambda: {"user_id": "test_user"}
    
    response = client.get('/api/v1/tax_optimization/harvest/opportunities/p1')
    
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert data['data'][0]['candidate']['ticker'] == "AAPL"


def test_analyze_batch_harvest_success(client, mock_harvest):
    """Test analyzing batch harvest."""
    from web.auth_utils import get_current_user
    client.app.dependency_overrides[get_current_user] = lambda: {"user_id": "test_user"}
    
    payload = {"opportunities": []}
    response = client.post('/api/v1/tax_optimization/harvest/batch/p1', json=payload)
    
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert data['data']['total_tax_savings'] == 300.0


def test_execute_harvest_success(client, mock_harvest):
    """Test executing harvest."""
    from web.auth_utils import get_current_user
    client.app.dependency_overrides[get_current_user] = lambda: {"user_id": "test_user"}
    
    payload = {
        "opportunity": {
            "candidate": {
                "ticker": "AAPL",
                "position_id": "pos1",
                "unrealized_loss": 1000.0,
                "cost_basis": 5000.0,
                "current_value": 4000.0,
                "holding_period_days": 100,
                "is_long_term": False,
                "tax_savings_estimate": 300.0,
                "wash_sale_risk": False
            },
            "wash_sale_risk": False,
            "requires_approval": False
        },
        "approved": True
    }
    response = client.post('/api/v1/tax_optimization/harvest/execute/p1', json=payload)
    
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert data['data']['status'] == "executed"


def test_optimize_lot_selection_success(client, mock_optimize):
    """Test optimizing lot selection."""
    from web.auth_utils import get_current_user
    client.app.dependency_overrides[get_current_user] = lambda: {"user_id": "test_user"}
    
    payload = {"symbol": "AAPL", "quantity": 10}
    response = client.post('/api/v1/tax_optimization/optimize/lot_selection/p1', json=payload)
    
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True


def test_project_tax_success(client, mock_optimize):
    """Test projecting tax."""
    from web.auth_utils import get_current_user
    client.app.dependency_overrides[get_current_user] = lambda: {"user_id": "test_user"}
    
    payload = {"planned_transactions": []}
    response = client.post('/api/v1/tax_optimization/optimize/project/p1', json=payload)
    
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert data['data']['projected_bill'] == 5000.0


def test_optimize_withdrawal_success(client, mock_optimize):
    """Test optimizing withdrawal."""
    from web.auth_utils import get_current_user
    client.app.dependency_overrides[get_current_user] = lambda: {"user_id": "test_user"}
    
    payload = {"withdrawal_amount": 1000.0}
    response = client.post('/api/v1/tax_optimization/optimize/withdrawal/p1', json=payload)
    
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
