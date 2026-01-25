"""
Tests for Charting Service
Comprehensive test coverage for chart data preparation and multi-timeframe support
"""

import pytest
from datetime import datetime, timedelta
from unittest.mock import Mock, AsyncMock, patch
import pandas as pd
from services.charting.charting_service import ChartingService, ChartType, Timeframe


@pytest.fixture
def service():
    """Create service instance with mocked dependencies."""
    with patch('services.charting.charting_service.AlphaVantageClient'), \
         patch('services.charting.charting_service.get_cache_service'):
        return ChartingService()


@pytest.fixture
def mock_ohlcv_data():
    """Mock OHLCV data."""
    dates = pd.date_range(start='2024-01-01', periods=100, freq='D')
    return pd.DataFrame({
        'open': [150.0] * 100,
        'high': [155.0] * 100,
        'low': [145.0] * 100,
        'close': [152.0] * 100,
        'volume': [1000000] * 100
    }, index=dates)


@pytest.mark.asyncio
async def test_get_chart_data_candlestick(service, mock_ohlcv_data):
    """Test getting candlestick chart data."""
    service.market_data_client.get_historical_data = AsyncMock(return_value=mock_ohlcv_data)
    service.cache_service.get = AsyncMock(return_value=None)
    service.cache_service.set = AsyncMock()
    
    result = await service.get_chart_data(
        symbol="AAPL",
        timeframe="1day",
        chart_type="candlestick"
    )
    
    assert result is not None
    assert 'data' in result or hasattr(result, 'data')
    assert 'chart_type' in result or hasattr(result, 'chart_type')


@pytest.mark.asyncio
async def test_get_chart_data_with_indicators(service, mock_ohlcv_data):
    """Test getting chart data with indicators."""
    service.market_data_client.get_historical_data = AsyncMock(return_value=mock_ohlcv_data)
    service.cache_service.get = AsyncMock(return_value=None)
    service.cache_service.set = AsyncMock()
    service._calculate_indicators = AsyncMock(return_value={
        'RSI': pd.Series([50.0] * 100),
        'MACD': pd.Series([0.5] * 100)
    })
    
    result = await service.get_chart_data(
        symbol="AAPL",
        timeframe="1day",
        chart_type="candlestick",
        indicators=['RSI', 'MACD']
    )
    
    assert result is not None
    assert 'indicators' in result or hasattr(result, 'indicators')


@pytest.mark.asyncio
async def test_get_chart_data_different_timeframes(service, mock_ohlcv_data):
    """Test getting chart data for different timeframes."""
    service.market_data_client.get_historical_data = AsyncMock(return_value=mock_ohlcv_data)
    service.cache_service.get = AsyncMock(return_value=None)
    service.cache_service.set = AsyncMock()
    
    timeframes = ["1min", "5min", "1day", "1week"]
    for timeframe in timeframes:
        result = await service.get_chart_data(
            symbol="AAPL",
            timeframe=timeframe
        )
        assert result is not None


@pytest.mark.asyncio
async def test_get_chart_data_different_types(service, mock_ohlcv_data):
    """Test getting different chart types."""
    service.market_data_client.get_historical_data = AsyncMock(return_value=mock_ohlcv_data)
    service.cache_service.get = AsyncMock(return_value=None)
    service.cache_service.set = AsyncMock()
    
    chart_types = ["candlestick", "line", "area", "heikin_ashi"]
    for chart_type in chart_types:
        result = await service.get_chart_data(
            symbol="AAPL",
            chart_type=chart_type
        )
        assert result is not None
