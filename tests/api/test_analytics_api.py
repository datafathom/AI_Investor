import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from flask import Flask
from datetime import datetime, timezone
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


def test_get_attribution_success(client, mock_attribution_service):
    """Test successful attribution calculation."""
    from models.analytics import AttributionResult, CalculationMetadata
    
    mock_attribution = AttributionResult(
        portfolio_id='portfolio_1',
        period_start=datetime.now(timezone.utc),
        period_end=datetime.now(timezone.utc),
        total_return=1500.0,
        total_return_pct=15.5,
        attribution_by_asset_class={},
        attribution_by_sector={},
        attribution_by_geography={},
        attribution_by_holding=[],
        calculation_metadata=CalculationMetadata(
            calculation_method='brinson',
            calculation_date=datetime.now(timezone.utc),
            data_quality='high',
            missing_data_points=0
        )
    )
    mock_attribution_service.calculate_attribution.return_value = mock_attribution
    
    response = client.get('/api/analytics/attribution/portfolio_1?start_date=2024-01-01&end_date=2024-12-31')
    
    assert response.status_code == 200
    data = response.get_json()
    assert data['success'] is True
    assert 'data' in data
    assert data['data']['total_return_pct'] == 15.5


def test_get_attribution_with_benchmark(client, mock_attribution_service):
    """Test attribution with benchmark."""
    from models.analytics import AttributionResult, CalculationMetadata
    
    mock_attribution = AttributionResult(
        portfolio_id='portfolio_1',
        period_start=datetime.now(timezone.utc),
        period_end=datetime.now(timezone.utc),
        total_return=1500.0,
        total_return_pct=15.5,
        attribution_by_asset_class={},
        attribution_by_sector={},
        attribution_by_geography={},
        attribution_by_holding=[],
        calculation_metadata=CalculationMetadata(
            calculation_method='brinson',
            calculation_date=datetime.now(timezone.utc),
            data_quality='high',
            missing_data_points=0
        )
    )
    mock_attribution_service.calculate_attribution.return_value = mock_attribution
    
    response = client.get('/api/analytics/attribution/portfolio_1?benchmark=SPY')
    
    assert response.status_code == 200
    mock_attribution_service.calculate_attribution.assert_called_once()


def test_get_attribution_error(client, mock_attribution_service):
    """Test attribution error handling."""
    mock_attribution_service.calculate_attribution.side_effect = Exception('Service error')
    
    response = client.get('/api/analytics/attribution/portfolio_1')
    
    assert response.status_code == 500
    data = response.get_json()
    assert data['success'] is False
    assert 'error' in data


def test_get_contribution_success(client, mock_attribution_service):
    """Test successful contribution calculation."""
    from models.analytics import HoldingContribution
    
    mock_contributions = [
        HoldingContribution(
            symbol='AAPL',
            name='Apple',
            weight=0.3,
            return_pct=10.0,
            contribution_absolute=2.5,
            contribution_pct=2.5,
            rank=1
        )
    ]
    mock_attribution_service.calculate_contribution.return_value = mock_contributions
    
    response = client.get('/api/analytics/contribution/portfolio_1')
    
    assert response.status_code == 200
    data = response.get_json()
    assert data['success'] is True
    assert len(data['data']) == 1
    assert data['data'][0]['symbol'] == 'AAPL'


def test_get_factor_risk_success(client, mock_risk_service):
    """Test successful factor risk decomposition."""
    from models.analytics import FactorRiskDecomposition
    
    mock_risk = FactorRiskDecomposition(
        portfolio_id='portfolio_1',
        factor_model='fama_french',
        total_risk=0.18,
        factor_exposures=[],
        idiosyncratic_risk=0.05,
        r_squared=0.85
    )
    mock_risk_service.decompose_factor_risk.return_value = mock_risk
    
    response = client.get('/api/analytics/risk/factor/portfolio_1?factor_model=fama_french')
    
    assert response.status_code == 200
    data = response.get_json()
    assert data['success'] is True
    assert data['data']['total_risk'] == 0.18


def test_get_concentration_risk_success(client, mock_risk_service):
    """Test successful concentration risk calculation."""
    from models.analytics import ConcentrationRiskAnalysis, ConcentrationMetric
    
    mock_concentration = ConcentrationRiskAnalysis(
        portfolio_id='portfolio_1',
        by_holding=ConcentrationMetric(
            dimension='holding',
            herfindahl_hirschman_index=0.25,
            top_5_concentration=0.5,
            top_10_concentration=0.8,
            max_weight=0.1,
            max_weight_symbol='AAPL'
        ),
        by_sector=ConcentrationMetric(
            dimension='sector',
            herfindahl_hirschman_index=0.3,
            top_5_concentration=0.6,
            top_10_concentration=0.9,
            max_weight=0.2,
            max_weight_symbol='IT'
        ),
        by_geography=ConcentrationMetric(
            dimension='geography',
            herfindahl_hirschman_index=0.4,
            top_5_concentration=0.7,
            top_10_concentration=1.0,
            max_weight=0.5,
            max_weight_symbol='US'
        ),
        by_asset_class=ConcentrationMetric(
            dimension='asset_class',
            herfindahl_hirschman_index=0.5,
            top_5_concentration=0.8,
            top_10_concentration=1.0,
            max_weight=0.6,
            max_weight_symbol='Equity'
        )
    )
    mock_risk_service.calculate_concentration_risk.return_value = mock_concentration
    
    response = client.get('/api/analytics/risk/concentration/portfolio_1?dimensions=holding,sector')
    
    assert response.status_code == 200
    data = response.get_json()
    assert data['success'] is True


def test_get_correlation_success(client, mock_risk_service):
    """Test successful correlation analysis."""
    from models.analytics import CorrelationAnalysis
    
    mock_correlation = CorrelationAnalysis(
        portfolio_id='portfolio_1',
        correlation_matrix={},
        average_correlation=0.6,
        diversification_ratio=1.5,
        highly_correlated_pairs=[]
    )
    mock_risk_service.analyze_correlation.return_value = mock_correlation
    
    response = client.get('/api/analytics/risk/correlation/portfolio_1?lookback_days=252')
    
    assert response.status_code == 200
    data = response.get_json()
    assert data['success'] is True


def test_get_tail_risk_success(client, mock_risk_service):
    """Test successful tail risk calculation."""
    from models.analytics import TailRiskContributions
    
    mock_tail_risk = TailRiskContributions(
        portfolio_id='portfolio_1',
        confidence_level=0.95,
        portfolio_var=0.05,
        portfolio_cvar=0.07,
        contributions=[],
        method='historical'
    )
    mock_risk_service.calculate_tail_risk_contributions.return_value = mock_tail_risk
    
    response = client.get('/api/analytics/risk/tail/portfolio_1?confidence_level=0.95&method=historical')
    
    assert response.status_code == 200
    data = response.get_json()
    assert data['success'] is True
    assert data['data']['portfolio_var'] == 0.05
