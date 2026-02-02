"""
Tests for Performance Attribution Service
"""

import pytest
from datetime import datetime, timedelta, timezone
from unittest.mock import Mock, AsyncMock, patch
from services.analytics.performance_attribution_service import PerformanceAttributionService
from models.analytics import AttributionResult, AttributionType, CalculationMetadata


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
            {'symbol': 'AAPL', 'quantity': 100, 'cost_basis': 150.0, 'value': 180.0, 'sector': 'Technology'},
            {'symbol': 'MSFT', 'quantity': 50, 'cost_basis': 300.0, 'value': 350.0, 'sector': 'Technology'},
            {'symbol': 'JPM', 'quantity': 200, 'cost_basis': 150.0, 'value': 160.0, 'sector': 'Financials'},
        ],
        'transactions': [],
        'cash': 10000.0
    }


@pytest.mark.asyncio
async def test_calculate_attribution_basic(service, mock_portfolio_data):
    """Test basic attribution calculation."""
    start_date = datetime(2024, 1, 1, tzinfo=timezone.utc)
    end_date = datetime(2024, 12, 31, tzinfo=timezone.utc)
    
    service.portfolio_aggregator.get_portfolio = AsyncMock(return_value=mock_portfolio_data)
    service.cache_service.get = Mock(return_value=None)  # Sync method
    service.cache_service.set = Mock()  # Sync method
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
    start_date = datetime(2024, 1, 1, tzinfo=timezone.utc)
    end_date = datetime(2024, 12, 31, tzinfo=timezone.utc)
    
    service.portfolio_aggregator.get_portfolio = AsyncMock(return_value=mock_portfolio_data)
    service.cache_service.get = Mock(return_value=None)
    service.cache_service.set = Mock()
    service.market_data_client.get_historical_data = AsyncMock(return_value={
        'AAPL': [{'date': '2024-01-01', 'close': 150.0}, {'date': '2024-12-31', 'close': 180.0}],
        'MSFT': [{'date': '2024-01-01', 'close': 300.0}, {'date': '2024-12-31', 'close': 350.0}],
        'JPM': [{'date': '2024-01-01', 'close': 150.0}, {'date': '2024-12-31', 'close': 160.0}],
        'SPY': [{'date': '2024-01-01', 'close': 400.0}, {'date': '2024-12-31', 'close': 440.0}],
        'SPY': [{'date': '2024-01-01', 'close': 400.0}, {'date': '2024-12-31', 'close': 440.0}],
    })
    
    local_mock_data = {
        'holdings': [
            {'symbol': 'AAPL', 'quantity': 100, 'cost_basis': 150.0, 'value': 180.0, 'sector': 'Technology'},
            {'symbol': 'MSFT', 'quantity': 50, 'cost_basis': 300.0, 'value': 350.0, 'sector': 'Technology'},
            {'symbol': 'JPM', 'quantity': 200, 'cost_basis': 150.0, 'value': 160.0, 'sector': 'Financials'},
        ]
    }
    service.portfolio_aggregator.get_portfolio = AsyncMock(return_value=local_mock_data)
    
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
    start_date = datetime(2024, 1, 1, tzinfo=timezone.utc)
    end_date = datetime(2024, 12, 31, tzinfo=timezone.utc)
    
    cached_result = AttributionResult(
        portfolio_id="test_portfolio",
        period_start=start_date,
        period_end=end_date,
        total_return=1500.0,
        total_return_pct=0.15,
        attribution_by_asset_class={},
        attribution_by_sector={},
        attribution_by_geography={},
        attribution_by_holding=[],
        calculation_metadata=CalculationMetadata(
            calculation_method='Modified Dietz',
            calculation_date=datetime.now(timezone.utc),
            data_quality='high',
            missing_data_points=0,
            cache_hit=True
        )
    )
    
    service.cache_service.get = Mock(return_value=cached_result.model_dump())
    service.portfolio_aggregator.get_portfolio = AsyncMock()  # Should not be called
    
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
    start_date = datetime(2024, 1, 1, tzinfo=timezone.utc)
    end_date = datetime(2024, 12, 31, tzinfo=timezone.utc)
    
    service.portfolio_aggregator.get_portfolio = AsyncMock(return_value=mock_portfolio_data)
    service.cache_service.get = Mock(return_value=None)
    service.cache_service.set = Mock()
    service.market_data_client.get_historical_data = AsyncMock(return_value={
        'AAPL': [{'date': '2024-01-01', 'close': 150.0}, {'date': '2024-12-31', 'close': 180.0}],
        'MSFT': [{'date': '2024-01-01', 'close': 300.0}, {'date': '2024-12-31', 'close': 350.0}],
        'JPM': [{'date': '2024-01-01', 'close': 150.0}, {'date': '2024-12-31', 'close': 160.0}],
    })
    
    local_mock_data = {
        'holdings': [
            {'symbol': 'AAPL', 'quantity': 100, 'cost_basis': 150.0, 'value': 180.0, 'sector': 'Technology'},
            {'symbol': 'MSFT', 'quantity': 50, 'cost_basis': 300.0, 'value': 350.0, 'sector': 'Technology'},
            {'symbol': 'JPM', 'quantity': 200, 'cost_basis': 150.0, 'value': 160.0, 'sector': 'Financials'},
        ]
    }
    service.portfolio_aggregator.get_portfolio = AsyncMock(return_value=local_mock_data)
    
    # Access private method for testing
    result = await service._calculate_sector_attribution(
        portfolio_data=local_mock_data,
        start_date=start_date,
        end_date=end_date
    )
    
    assert result is not None
    assert len(result) > 0


@pytest.mark.asyncio
async def test_calculate_holding_contributions(service, mock_portfolio_data):
    """Test holding contribution calculation."""
    start_date = datetime(2024, 1, 1, tzinfo=timezone.utc)
    end_date = datetime(2024, 12, 31, tzinfo=timezone.utc)
    
    service.market_data_client.get_historical_data = AsyncMock(return_value={
        'AAPL': [{'date': '2024-01-01', 'close': 150.0}, {'date': '2024-12-31', 'close': 180.0}],
        'MSFT': [{'date': '2024-01-01', 'close': 300.0}, {'date': '2024-12-31', 'close': 350.0}],
        'JPM': [{'date': '2024-01-01', 'close': 150.0}, {'date': '2024-12-31', 'close': 160.0}],
    })
    
    local_mock_data = {
        'holdings': [
            {'symbol': 'AAPL', 'quantity': 100, 'cost_basis': 150.0, 'value': 180.0, 'sector': 'Technology'},
            {'symbol': 'MSFT', 'quantity': 50, 'cost_basis': 300.0, 'value': 350.0, 'sector': 'Technology'},
            {'symbol': 'JPM', 'quantity': 200, 'cost_basis': 150.0, 'value': 160.0, 'sector': 'Financials'},
        ]
    }
    service.portfolio_aggregator.get_portfolio = AsyncMock(return_value=local_mock_data)
    
    result = await service.calculate_holding_contributions(
        portfolio_id="test_portfolio",
        start_date=start_date,
        end_date=end_date
    )
    
    assert result is not None
    assert result is not None
    assert len(result) > 0
    assert all(contrib.symbol for contrib in result)


@pytest.mark.asyncio
async def test_calculate_attribution_error_handling(service):
    """Test error handling in attribution calculation."""
    start_date = datetime(2024, 1, 1, tzinfo=timezone.utc)
    end_date = datetime(2024, 12, 31, tzinfo=timezone.utc)
    
    service.portfolio_aggregator.get_portfolio = AsyncMock(side_effect=Exception("Portfolio not found"))
    service.cache_service.get = Mock(return_value=None)
    
    with pytest.raises(Exception):
        await service.calculate_attribution(
            portfolio_id="nonexistent",
            start_date=start_date,
            end_date=end_date
        )
