"""
Tests for Tax Optimization API Endpoints
Phase 4: Enhanced Tax-Loss Harvesting & Optimization
"""

import pytest
from unittest.mock import AsyncMock, patch
from flask import Flask
from web.api.tax_optimization_api import tax_optimization_bp


@pytest.fixture
def app():
    """Create Flask app for testing."""
    app = Flask(__name__)
    app.config['TESTING'] = True
    app.register_blueprint(tax_optimization_bp)
    return app


@pytest.fixture
def client(app):
    """Create test client."""
    return app.test_client()


@pytest.fixture
def mock_harvest_service():
    """Mock EnhancedTaxHarvestingService."""
    with patch('web.api.tax_optimization_api.get_enhanced_harvest_service') as mock:
        service = AsyncMock()
        mock.return_value = service
        yield service


@pytest.fixture
def mock_tax_optimization_service():
    """Mock TaxOptimizationService."""
    with patch('web.api.tax_optimization_api.get_tax_optimization_service') as mock:
        service = AsyncMock()
        mock.return_value = service
        yield service


@pytest.mark.asyncio
async def test_get_harvest_opportunities_success(client, mock_harvest_service):
    """Test successful harvest opportunities retrieval."""
    from models.tax import HarvestOpportunity, HarvestCandidate
    
    mock_opportunities = [
        HarvestOpportunity(
            candidate=HarvestCandidate(
                ticker='AAPL',
                unrealized_loss=-500.0,
                cost_basis=150.0,
                current_value=145.0
            ),
            tax_savings=125.0,
            net_benefit=100.0,
            replacement_suggestions=[],
            wash_sale_risk=False,
            rank=1
        )
    ]
    mock_harvest_service.identify_harvest_opportunities.return_value = mock_opportunities
    
    response = client.get('/api/tax/harvest/opportunities/portfolio_1?min_loss_dollar=500')
    
    assert response.status_code == 200
    data = response.get_json()
    assert data['success'] is True
    assert len(data['data']) == 1
    assert data['data'][0]['candidate']['ticker'] == 'AAPL'


@pytest.mark.asyncio
async def test_analyze_batch_harvest_success(client, mock_harvest_service):
    """Test successful batch harvest analysis."""
    from models.tax import BatchHarvestResult
    
    mock_result = BatchHarvestResult(
        portfolio_id='portfolio_1',
        total_tax_savings=1000.0,
        total_net_benefit=800.0,
        opportunities_count=5
    )
    mock_harvest_service.batch_harvest_analysis.return_value = mock_result
    
    response = client.post('/api/tax/harvest/batch/portfolio_1', json={})
    
    assert response.status_code == 200
    data = response.get_json()
    assert data['success'] is True


@pytest.mark.asyncio
async def test_execute_harvest_success(client, mock_harvest_service):
    """Test successful harvest execution."""
    from models.tax import HarvestExecutionResult
    
    mock_result = HarvestExecutionResult(
        portfolio_id='portfolio_1',
        executed_trades=[],
        realized_loss=-500.0,
        tax_savings=125.0
    )
    mock_harvest_service.execute_harvest.return_value = mock_result
    
    response = client.post('/api/tax/harvest/execute/portfolio_1',
                          json={'opportunities': []})
    
    assert response.status_code == 200
    data = response.get_json()
    assert data['success'] is True


@pytest.mark.asyncio
async def test_optimize_lot_selection_success(client, mock_tax_optimization_service):
    """Test successful lot selection optimization."""
    from models.tax import LotSelectionResult
    
    mock_result = LotSelectionResult(
        portfolio_id='portfolio_1',
        selected_lots=[],
        total_tax_impact=0.0
    )
    mock_tax_optimization_service.optimize_lot_selection.return_value = mock_result
    
    response = client.post('/api/tax/optimize/lot_selection/portfolio_1',
                          json={'method': 'highest_cost', 'target_amount': 1000.0})
    
    assert response.status_code == 200
    data = response.get_json()
    assert data['success'] is True


@pytest.mark.asyncio
async def test_project_year_end_tax_success(client, mock_tax_optimization_service):
    """Test successful year-end tax projection."""
    from models.tax import YearEndTaxProjection
    
    mock_projection = YearEndTaxProjection(
        portfolio_id='portfolio_1',
        estimated_taxable_gains=5000.0,
        estimated_tax_liability=1200.0
    )
    mock_tax_optimization_service.project_year_end_tax.return_value = mock_projection
    
    response = client.post('/api/tax/optimize/project/portfolio_1', json={})
    
    assert response.status_code == 200
    data = response.get_json()
    assert data['success'] is True


@pytest.mark.asyncio
async def test_optimize_withdrawal_success(client, mock_tax_optimization_service):
    """Test successful withdrawal optimization."""
    from models.tax import WithdrawalOptimization
    
    mock_optimization = WithdrawalOptimization(
        portfolio_id='portfolio_1',
        recommended_withdrawal=10000.0,
        tax_efficient_sources=[]
    )
    mock_tax_optimization_service.optimize_withdrawal.return_value = mock_optimization
    
    response = client.post('/api/tax/optimize/withdrawal/portfolio_1',
                          json={'target_amount': 10000.0})
    
    assert response.status_code == 200
    data = response.get_json()
    assert data['success'] is True
