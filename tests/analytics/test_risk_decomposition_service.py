"""
Tests for Risk Decomposition Service
Comprehensive test coverage for all methods and edge cases
"""

import pytest
from datetime import datetime, timedelta
from unittest.mock import Mock, AsyncMock, patch, MagicMock
from services.analytics.risk_decomposition_service import RiskDecompositionService
from models.analytics import FactorRiskDecomposition, ConcentrationRiskAnalysis, CorrelationAnalysis, TailRiskContributions


@pytest.fixture
def service():
    """Create service instance with mocked dependencies."""
    with patch('services.analytics.risk_decomposition_service.get_portfolio_aggregator'), \
         patch('services.analytics.risk_decomposition_service.get_cache_service'), \
         patch('services.analytics.risk_decomposition_service.MonteCarloEngine'):
        return RiskDecompositionService()


@pytest.fixture
def mock_portfolio_data():
    """Mock portfolio holdings data."""
    return {
        'holdings': [
            {'symbol': 'AAPL', 'quantity': 100, 'weight': 0.4, 'sector': 'Technology', 'geography': 'US'},
            {'symbol': 'MSFT', 'quantity': 50, 'weight': 0.3, 'sector': 'Technology', 'geography': 'US'},
            {'symbol': 'JPM', 'quantity': 200, 'weight': 0.2, 'sector': 'Financials', 'geography': 'US'},
            {'symbol': 'TSLA', 'quantity': 50, 'weight': 0.1, 'sector': 'Consumer Discretionary', 'geography': 'US'},
        ],
        'total_value': 100000.0
    }


@pytest.mark.asyncio
async def test_decompose_factor_risk_basic(service, mock_portfolio_data):
    """Test basic factor risk decomposition."""
    service.portfolio_aggregator.get_portfolio = AsyncMock(return_value=mock_portfolio_data)
    service.cache_service.get = Mock(return_value=None)
    service.cache_service.set = Mock()
    service._get_portfolio_data = AsyncMock(return_value=mock_portfolio_data)
    service._calculate_factor_exposures = AsyncMock(return_value=[])
    service._calculate_portfolio_volatility = AsyncMock(return_value=0.15)
    
    result = await service.decompose_factor_risk(
        portfolio_id="test_portfolio",
        factor_model="fama_french",
        lookback_days=252
    )
    
    assert result is not None
    assert isinstance(result, FactorRiskDecomposition)
    assert result.portfolio_id == "test_portfolio"
    assert result.factor_model == "fama_french"
    assert result.total_risk == 0.15
    service.cache_service.set.assert_called_once()


@pytest.mark.asyncio
async def test_decompose_factor_risk_cached(service):
    """Test that cached factor risk is returned when available."""
    cached_data = {
        'portfolio_id': 'test_portfolio',
        'factor_model': 'fama_french',
        'total_risk': 0.15,
        'factor_exposures': [],
        'idiosyncratic_risk': 0.045,
        'r_squared': 0.7
    }
    
    service.cache_service.get = Mock(return_value=cached_data)
    
    result = await service.decompose_factor_risk(
        portfolio_id="test_portfolio",
        factor_model="fama_french"
    )
    
    assert result is not None
    assert result.total_risk == 0.15
    service.portfolio_aggregator.get_portfolio.assert_not_called()


@pytest.mark.asyncio
async def test_calculate_concentration_risk(service, mock_portfolio_data):
    """Test concentration risk calculation."""
    service._get_portfolio_data = AsyncMock(return_value=mock_portfolio_data)
    
    result = await service.calculate_concentration_risk(
        portfolio_id="test_portfolio",
        dimensions=["holding", "sector"]
    )
    
    assert result is not None
    assert isinstance(result, ConcentrationRiskAnalysis)
    assert result.by_holding is not None
    assert result.by_sector is not None


@pytest.mark.asyncio
async def test_calculate_concentration_risk_empty_portfolio(service):
    """Test concentration risk with empty portfolio."""
    service._get_portfolio_data = AsyncMock(return_value={'holdings': []})
    
    result = await service.calculate_concentration_risk(
        portfolio_id="empty_portfolio"
    )
    
    assert result is not None
    assert result.by_holding.max_weight == 0.0


@pytest.mark.asyncio
async def test_calculate_correlation_analysis(service, mock_portfolio_data):
    """Test correlation analysis calculation."""
    service._get_portfolio_data = AsyncMock(return_value=mock_portfolio_data)
    service._get_returns_data = AsyncMock(return_value={
        'AAPL': [0.01, 0.02, -0.01, 0.03],
        'MSFT': [0.015, 0.018, -0.008, 0.025],
        'JPM': [0.005, 0.01, -0.005, 0.02],
    })
    
    result = await service.calculate_correlation_analysis(
        portfolio_id="test_portfolio",
        lookback_days=252
    )
    
    assert result is not None
    assert isinstance(result, CorrelationAnalysis)


@pytest.mark.asyncio
async def test_calculate_tail_risk_contributions(service, mock_portfolio_data):
    """Test tail risk contributions calculation."""
    service._get_portfolio_data = AsyncMock(return_value=mock_portfolio_data)
    service._get_returns_data = AsyncMock(return_value={
        'AAPL': [0.01, 0.02, -0.01, 0.03],
        'MSFT': [0.015, 0.018, -0.008, 0.025],
    })
    service.monte_carlo.simulate = AsyncMock(return_value=[[-0.05, -0.03, -0.08, -0.02]])
    
    result = await service.calculate_tail_risk_contributions(
        portfolio_id="test_portfolio",
        confidence_level=0.95
    )
    
    assert result is not None
    assert isinstance(result, TailRiskContributions)


@pytest.mark.asyncio
async def test_decompose_factor_risk_different_models(service, mock_portfolio_data):
    """Test factor risk decomposition with different factor models."""
    service._get_portfolio_data = AsyncMock(return_value=mock_portfolio_data)
    service.cache_service.get = Mock(return_value=None)
    service.cache_service.set = Mock()
    service._calculate_factor_exposures = AsyncMock(return_value=[])
    service._calculate_portfolio_volatility = AsyncMock(return_value=0.15)
    
    models = ["fama_french", "barra", "custom"]
    for model in models:
        result = await service.decompose_factor_risk(
            portfolio_id="test_portfolio",
            factor_model=model
        )
        assert result.factor_model == model


@pytest.mark.asyncio
async def test_calculate_concentration_risk_all_dimensions(service, mock_portfolio_data):
    """Test concentration risk with all dimensions."""
    service._get_portfolio_data = AsyncMock(return_value=mock_portfolio_data)
    
    result = await service.calculate_concentration_risk(
        portfolio_id="test_portfolio",
        dimensions=["holding", "sector", "geography", "asset_class"]
    )
    
    assert result is not None
    assert result.by_holding is not None
    assert result.by_sector is not None
    assert result.by_geography is not None
    assert result.by_asset_class is not None


@pytest.mark.asyncio
async def test_decompose_factor_risk_error_handling(service):
    """Test error handling in factor risk decomposition."""
    service._get_portfolio_data = AsyncMock(side_effect=Exception("Portfolio not found"))
    
    with pytest.raises(Exception):
        await service.decompose_factor_risk(
            portfolio_id="nonexistent"
        )


@pytest.mark.asyncio
async def test_calculate_concentration_risk_single_holding(service):
    """Test concentration risk with single holding."""
    single_holding_data = {
        'holdings': [
            {'symbol': 'AAPL', 'quantity': 100, 'weight': 1.0, 'sector': 'Technology'}
        ]
    }
    service._get_portfolio_data = AsyncMock(return_value=single_holding_data)
    
    result = await service.calculate_concentration_risk(
        portfolio_id="single_holding_portfolio"
    )
    
    assert result is not None
    # Single holding should have high concentration
    assert result.by_holding is not None
    assert result.by_holding.max_weight == 1.0
