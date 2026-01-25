"""
Tests for Performance Attribution Service
"""

import pytest
from datetime import datetime, timedelta
from unittest.mock import Mock, AsyncMock, patch
from services.analytics.performance_attribution_service import PerformanceAttributionService
from models.analytics import AttributionResult, AttributionType


@pytest.fixture
def service():
    """Create service instance with mocked dependencies."""
    with patch('services.analytics.performance_attribution_service.get_portfolio_aggregator'), \
         patch('services.analytics.performance_attribution_service.get_cache_service'), \
         patch('services.analytics.performance_attribution_service.AlphaVantageClient'):
        return PerformanceAttributionService()


@pytest.fixture
def mock_portfolio_data():
    """Mock portfolio holdings data."""
    return {
        'holdings': [
            {'symbol': 'AAPL', 'quantity': 100, 'cost_basis': 150.0, 'sector': 'Technology'},
            {'symbol': 'MSFT', 'quantity': 50, 'cost_basis': 300.0, 'sector': 'Technology'},
            {'symbol': 'JPM', 'quantity': 200, 'cost_basis': 150.0, 'sector': 'Financials'},
        ],
        'transactions': [],
        'cash': 10000.0
    }


@pytest.mark.asyncio
async def test_calculate_attribution_basic(service, mock_portfolio_data):
    """Test basic attribution calculation."""
    start_date = datetime(2024, 1, 1)
    end_date = datetime(2024, 12, 31)
    
    service.portfolio_aggregator.get_portfolio = AsyncMock(return_value=mock_portfolio_data)
    service.cache_service.get = AsyncMock(return_value=None)
    service.cache_service.set = AsyncMock()
    service.market_data_client.get_historical_data = AsyncMock(return_value={
        'AAPL': [{'date': '2024-01-01', 'close': 150.0}, {'date': '2024-12-31', 'close': 180.0}],
        'MSFT': [{'date': '2024-01-01', 'close': 300.0}, {'date': '2024-12-31', 'close': 350.0}],
        'JPM': [{'date': '2024-01-01', 'close': 150.0}, {'date': '2024-12-31', 'close': 160.0}],
    })
    
    result = await service.calculate_attribution(
        portfolio_id="test_portfolio",
        start_date=start_date,
        end_date=end_date
    )
    
    assert result is not None
    assert isinstance(result, AttributionResult)
    assert result.total_return is not None


@pytest.mark.asyncio
async def test_calculate_attribution_with_benchmark(service, mock_portfolio_data):
    """Test attribution calculation with benchmark."""
    start_date = datetime(2024, 1, 1)
    end_date = datetime(2024, 12, 31)
    
    service.portfolio_aggregator.get_portfolio = AsyncMock(return_value=mock_portfolio_data)
    service.cache_service.get = AsyncMock(return_value=None)
    service.cache_service.set = AsyncMock()
    service.market_data_client.get_historical_data = AsyncMock(return_value={
        'AAPL': [{'date': '2024-01-01', 'close': 150.0}, {'date': '2024-12-31', 'close': 180.0}],
        'MSFT': [{'date': '2024-01-01', 'close': 300.0}, {'date': '2024-12-31', 'close': 350.0}],
        'JPM': [{'date': '2024-01-01', 'close': 150.0}, {'date': '2024-12-31', 'close': 160.0}],
        'SPY': [{'date': '2024-01-01', 'close': 400.0}, {'date': '2024-12-31', 'close': 440.0}],
    })
    
    result = await service.calculate_attribution(
        portfolio_id="test_portfolio",
        start_date=start_date,
        end_date=end_date,
        benchmark="SPY"
    )
    
    assert result is not None
    assert result.benchmark_comparison is not None


@pytest.mark.asyncio
async def test_calculate_attribution_cached(service):
    """Test that cached attribution is returned when available."""
    start_date = datetime(2024, 1, 1)
    end_date = datetime(2024, 12, 31)
    
    cached_result = AttributionResult(
        portfolio_id="test_portfolio",
        start_date=start_date,
        end_date=end_date,
        total_return=0.15,
        attribution_breakdowns=[],
        holding_attributions=[],
        benchmark_comparison=None,
        calculation_metadata=None
    )
    
    service.cache_service.get = AsyncMock(return_value=cached_result)
    
    result = await service.calculate_attribution(
        portfolio_id="test_portfolio",
        start_date=start_date,
        end_date=end_date
    )
    
    assert result == cached_result
    service.portfolio_aggregator.get_portfolio.assert_not_called()


@pytest.mark.asyncio
async def test_calculate_attribution_by_sector(service, mock_portfolio_data):
    """Test sector-level attribution."""
    start_date = datetime(2024, 1, 1)
    end_date = datetime(2024, 12, 31)
    
    service.portfolio_aggregator.get_portfolio = AsyncMock(return_value=mock_portfolio_data)
    service.cache_service.get = AsyncMock(return_value=None)
    service.cache_service.set = AsyncMock()
    service.market_data_client.get_historical_data = AsyncMock(return_value={
        'AAPL': [{'date': '2024-01-01', 'close': 150.0}, {'date': '2024-12-31', 'close': 180.0}],
        'MSFT': [{'date': '2024-01-01', 'close': 300.0}, {'date': '2024-12-31', 'close': 350.0}],
        'JPM': [{'date': '2024-01-01', 'close': 150.0}, {'date': '2024-12-31', 'close': 160.0}],
    })
    
    result = await service.calculate_attribution_by_sector(
        portfolio_id="test_portfolio",
        start_date=start_date,
        end_date=end_date
    )
    
    assert result is not None
    assert len(result) > 0


@pytest.mark.asyncio
async def test_calculate_holding_contributions(service, mock_portfolio_data):
    """Test holding contribution calculation."""
    start_date = datetime(2024, 1, 1)
    end_date = datetime(2024, 12, 31)
    
    service.portfolio_aggregator.get_portfolio = AsyncMock(return_value=mock_portfolio_data)
    service.market_data_client.get_historical_data = AsyncMock(return_value={
        'AAPL': [{'date': '2024-01-01', 'close': 150.0}, {'date': '2024-12-31', 'close': 180.0}],
        'MSFT': [{'date': '2024-01-01', 'close': 300.0}, {'date': '2024-12-31', 'close': 350.0}],
        'JPM': [{'date': '2024-01-01', 'close': 150.0}, {'date': '2024-12-31', 'close': 160.0}],
    })
    
    result = await service.calculate_holding_contributions(
        portfolio_id="test_portfolio",
        start_date=start_date,
        end_date=end_date
    )
    
    assert result is not None
    assert len(result) > 0
    assert all('symbol' in contrib for contrib in result)


@pytest.mark.asyncio
async def test_calculate_attribution_error_handling(service):
    """Test error handling in attribution calculation."""
    start_date = datetime(2024, 1, 1)
    end_date = datetime(2024, 12, 31)
    
    service.portfolio_aggregator.get_portfolio = AsyncMock(side_effect=Exception("Portfolio not found"))
    
    with pytest.raises(Exception):
        await service.calculate_attribution(
            portfolio_id="nonexistent",
            start_date=start_date,
            end_date=end_date
        )
