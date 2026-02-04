
import pytest
from unittest.mock import AsyncMock, patch
from fastapi import FastAPI
from fastapi.testclient import TestClient
from web.api.analytics_api import router, get_attribution_service, get_risk_decomposition_service
from web.auth_utils import get_current_user
from datetime import datetime, timezone

@pytest.fixture
def api_app(mock_attribution_service, mock_risk_service):
    """Create FastAPI app for testing."""
    app = FastAPI()
    app.include_router(router)
    app.dependency_overrides[get_attribution_service] = lambda: mock_attribution_service
    app.dependency_overrides[get_risk_decomposition_service] = lambda: mock_risk_service
    app.dependency_overrides[get_current_user] = lambda: {"id": "user_1", "role": "user"}
    return app


@pytest.fixture
def client(api_app):
    """Create test client."""
    return TestClient(api_app)


@pytest.fixture
def mock_attribution_service():
    """Mock PerformanceAttributionService."""
    from unittest.mock import MagicMock
    service = MagicMock()
    service.calculate_attribution = AsyncMock()
    service.calculate_holding_contributions = AsyncMock()
    return service


@pytest.fixture
def mock_risk_service():
    """Mock RiskDecompositionService."""
    from unittest.mock import MagicMock
    service = MagicMock()
    service.decompose_factor_risk = AsyncMock()
    service.calculate_concentration_risk = AsyncMock()
    service.analyze_correlation = AsyncMock()
    service.calculate_tail_risk_contributions = AsyncMock()
    return service


def test_get_attribution_success(client, mock_attribution_service):
    """Test successful attribution calculation."""
    from schemas.analytics import AttributionResult, CalculationMetadata
    
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
    
    response = client.get('/api/v1/analytics/attribution/portfolio_1?start_date=2024-01-01&end_date=2024-12-31')
    
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert 'data' in data
    assert data['data']['total_return_pct'] == 15.5


def test_get_attribution_with_benchmark(client, mock_attribution_service):
    """Test attribution with benchmark."""
    from schemas.analytics import AttributionResult, CalculationMetadata
    
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
    
    response = client.get('/api/v1/analytics/attribution/portfolio_1?benchmark=SPY')
    
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    mock_attribution_service.calculate_attribution.assert_called_once()


def test_get_attribution_error(client, mock_attribution_service):
    """Test attribution error handling."""
    mock_attribution_service.calculate_attribution.side_effect = Exception('Service error')
    
    response = client.get('/api/v1/analytics/attribution/portfolio_1')
    
    assert response.status_code == 500
    data = response.json()
    assert data['success'] is False


def test_get_contribution_success(client, mock_attribution_service):
    """Test successful contribution calculation."""
    from schemas.analytics import HoldingContribution
    
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
    mock_attribution_service.calculate_holding_contributions.return_value = mock_contributions
    
    response = client.get('/api/v1/analytics/contribution/portfolio_1')
    
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert len(data['data']) == 1
    assert data['data'][0]['symbol'] == 'AAPL'


def test_get_factor_risk_success(client, mock_risk_service):
    """Test successful factor risk decomposition."""
    from schemas.analytics import FactorRiskDecomposition
    
    mock_risk = FactorRiskDecomposition(
        portfolio_id='portfolio_1',
        factor_model='fama_french',
        total_risk=0.18,
        factor_exposures=[],
        idiosyncratic_risk=0.05,
        r_squared=0.85
    )
    mock_risk_service.decompose_factor_risk.return_value = mock_risk
    
    response = client.get('/api/v1/analytics/risk/factor/portfolio_1?factor_model=fama_french')
    
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert data['data']['total_risk'] == 0.18


def test_get_concentration_risk_success(client, mock_risk_service):
    """Test successful concentration risk calculation."""
    from schemas.analytics import ConcentrationRiskAnalysis, ConcentrationMetric
    
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
    
    response = client.get('/api/v1/analytics/risk/concentration/portfolio_1?dimensions=holding,sector')
    
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True


def test_get_correlation_success(client, mock_risk_service):
    """Test successful correlation analysis."""
    from schemas.analytics import CorrelationAnalysis
    
    mock_correlation = CorrelationAnalysis(
        portfolio_id='portfolio_1',
        correlation_matrix={},
        average_correlation=0.6,
        diversification_ratio=1.5,
        highly_correlated_pairs=[]
    )
    mock_risk_service.analyze_correlation.return_value = mock_correlation
    
    response = client.get('/api/v1/analytics/risk/correlation/portfolio_1?lookback_days=252')
    
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True


def test_get_tail_risk_success(client, mock_risk_service):
    """Test successful tail risk calculation."""
    from schemas.analytics import TailRiskContributions
    
    mock_tail_risk = TailRiskContributions(
        portfolio_id='portfolio_1',
        confidence_level=0.95,
        portfolio_var=0.05,
        portfolio_cvar=0.07,
        contributions=[],
        method='historical'
    )
    mock_risk_service.calculate_tail_risk_contributions.return_value = mock_tail_risk
    
    response = client.get('/api/v1/analytics/risk/tail/portfolio_1?confidence_level=0.95&method=historical')
    
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert data['data']['portfolio_var'] == 0.05
