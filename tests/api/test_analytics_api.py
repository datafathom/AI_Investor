"""
Tests for Analytics API Endpoints
Phase 1: Performance Attribution & Risk Decomposition
"""

import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from flask import Flask
from datetime import datetime
from web.api.analytics_api import analytics_bp


@pytest.fixture
def app():
    """Create Flask app for testing."""
    app = Flask(__name__)
    app.config['TESTING'] = True
    app.register_blueprint(analytics_bp)
    return app


@pytest.fixture
def client(app):
    """Create test client."""
    return app.test_client()


@pytest.fixture
def mock_attribution_service():
    """Mock PerformanceAttributionService."""
    with patch('web.api.analytics_api.get_attribution_service') as mock:
        service = AsyncMock()
        mock.return_value = service
        yield service


@pytest.fixture
def mock_risk_service():
    """Mock RiskDecompositionService."""
    with patch('web.api.analytics_api.get_risk_decomposition_service') as mock:
        service = AsyncMock()
        mock.return_value = service
        yield service


@pytest.mark.asyncio
async def test_get_attribution_success(client, mock_attribution_service):
    """Test successful attribution calculation."""
    from models.analytics import PerformanceAttribution
    
    mock_attribution = PerformanceAttribution(
        portfolio_id='portfolio_1',
        total_return=15.5,
        benchmark_return=12.0,
        active_return=3.5,
        breakdown=[]
    )
    mock_attribution_service.calculate_attribution.return_value = mock_attribution
    
    response = client.get('/api/analytics/attribution/portfolio_1?start_date=2024-01-01&end_date=2024-12-31')
    
    assert response.status_code == 200
    data = response.get_json()
    assert data['success'] is True
    assert 'data' in data
    assert data['data']['total_return'] == 15.5


@pytest.mark.asyncio
async def test_get_attribution_with_benchmark(client, mock_attribution_service):
    """Test attribution with benchmark."""
    from models.analytics import PerformanceAttribution
    
    mock_attribution = PerformanceAttribution(
        portfolio_id='portfolio_1',
        total_return=15.5,
        benchmark_return=12.0,
        active_return=3.5,
        breakdown=[]
    )
    mock_attribution_service.calculate_attribution.return_value = mock_attribution
    
    response = client.get('/api/analytics/attribution/portfolio_1?benchmark=SPY')
    
    assert response.status_code == 200
    mock_attribution_service.calculate_attribution.assert_called_once()
    call_args = mock_attribution_service.calculate_attribution.call_args
    assert call_args[1]['benchmark'] == 'SPY'


@pytest.mark.asyncio
async def test_get_attribution_error(client, mock_attribution_service):
    """Test attribution error handling."""
    mock_attribution_service.calculate_attribution.side_effect = Exception('Service error')
    
    response = client.get('/api/analytics/attribution/portfolio_1')
    
    assert response.status_code == 500
    data = response.get_json()
    assert data['success'] is False
    assert 'error' in data


@pytest.mark.asyncio
async def test_get_contribution_success(client, mock_attribution_service):
    """Test successful contribution calculation."""
    from models.analytics import HoldingContribution
    
    mock_contributions = [
        HoldingContribution(
            symbol='AAPL',
            contribution=2.5,
            weight=0.3
        )
    ]
    mock_attribution_service.calculate_contribution.return_value = mock_contributions
    
    response = client.get('/api/analytics/contribution/portfolio_1')
    
    assert response.status_code == 200
    data = response.get_json()
    assert data['success'] is True
    assert len(data['data']) == 1
    assert data['data'][0]['symbol'] == 'AAPL'


@pytest.mark.asyncio
async def test_get_factor_risk_success(client, mock_risk_service):
    """Test successful factor risk decomposition."""
    from models.analytics import FactorRiskDecomposition
    
    mock_risk = FactorRiskDecomposition(
        portfolio_id='portfolio_1',
        total_risk=0.18,
        factor_risks=[]
    )
    mock_risk_service.decompose_factor_risk.return_value = mock_risk
    
    response = client.get('/api/analytics/risk/factor/portfolio_1?factor_model=fama_french')
    
    assert response.status_code == 200
    data = response.get_json()
    assert data['success'] is True
    assert data['data']['total_risk'] == 0.18


@pytest.mark.asyncio
async def test_get_concentration_risk_success(client, mock_risk_service):
    """Test successful concentration risk calculation."""
    from models.analytics import ConcentrationRisk
    
    mock_concentration = ConcentrationRisk(
        portfolio_id='portfolio_1',
        herfindahl_index=0.25,
        dimension_risks={}
    )
    mock_risk_service.calculate_concentration_risk.return_value = mock_concentration
    
    response = client.get('/api/analytics/risk/concentration/portfolio_1?dimensions=holding,sector')
    
    assert response.status_code == 200
    data = response.get_json()
    assert data['success'] is True


@pytest.mark.asyncio
async def test_get_correlation_success(client, mock_risk_service):
    """Test successful correlation analysis."""
    from models.analytics import CorrelationAnalysis
    
    mock_correlation = CorrelationAnalysis(
        portfolio_id='portfolio_1',
        avg_correlation=0.6,
        correlation_matrix={}
    )
    mock_risk_service.analyze_correlation.return_value = mock_correlation
    
    response = client.get('/api/analytics/risk/correlation/portfolio_1?lookback_days=252')
    
    assert response.status_code == 200
    data = response.get_json()
    assert data['success'] is True


@pytest.mark.asyncio
async def test_get_tail_risk_success(client, mock_risk_service):
    """Test successful tail risk calculation."""
    from models.analytics import TailRiskContributions
    
    mock_tail_risk = TailRiskContributions(
        portfolio_id='portfolio_1',
        var_95=0.05,
        cvar_95=0.07,
        contributions={}
    )
    mock_risk_service.calculate_tail_risk_contributions.return_value = mock_tail_risk
    
    response = client.get('/api/analytics/risk/tail/portfolio_1?confidence_level=0.95&method=historical')
    
    assert response.status_code == 200
    data = response.get_json()
    assert data['success'] is True
    assert data['data']['var_95'] == 0.05
