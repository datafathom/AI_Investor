"""
Tests for Prediction Engine
Comprehensive test coverage for price forecasting and trend prediction
"""

import pytest
from datetime import timezone, datetime, timedelta
from unittest.mock import Mock, AsyncMock, patch
from services.ai_predictions.prediction_engine import PredictionEngine
from schemas.ai_predictions import PricePrediction, TrendPrediction


@pytest.fixture
def service():
    """Create service instance with mocked dependencies."""
    with patch('services.ai_predictions.prediction_engine.get_cache_service'):
        return PredictionEngine()


@pytest.mark.asyncio
async def test_predict_price(service):
    """Test price prediction."""
    service._get_current_price = AsyncMock(return_value=150.0)
    service.cache_service.get = Mock(return_value=None)
    service.cache_service.set = Mock()
    
    result = await service.predict_price(
        symbol="AAPL",
        time_horizon="1m",
        model_version="v1.0"
    )
    
    assert result is not None
    assert isinstance(result, PricePrediction)
    assert result.symbol == "AAPL"
    assert result.predicted_price is not None
    assert result.confidence is not None


@pytest.mark.asyncio
async def test_predict_price_different_horizons(service):
    """Test price prediction with different time horizons."""
    service._get_current_price = AsyncMock(return_value=150.0)
    service.cache_service.get = Mock(return_value=None)
    service.cache_service.set = Mock()
    
    horizons = ["1d", "1w", "1m", "3m", "1y"]
    for horizon in horizons:
        result = await service.predict_price(
            symbol="AAPL",
            time_horizon=horizon
        )
        assert result is not None
        assert result.time_horizon == horizon


@pytest.mark.asyncio
async def test_predict_trend(service):
    """Test trend prediction."""
    service._get_current_price = AsyncMock(return_value=150.0)
    service._analyze_trend = AsyncMock(return_value="bullish")
    
    result = await service.predict_trend(
        symbol="AAPL",
        time_horizon="1m"
    )
    
    assert result is not None
    assert isinstance(result, TrendPrediction)
    assert result.symbol == "AAPL"
    assert result.trend_direction is not None


@pytest.mark.asyncio
async def test_predict_price_cached(service):
    """Test cached price prediction."""
    cached_data = {
        'prediction_id': 'pred_123',
        'symbol': 'AAPL',
        'predicted_price': 157.5,
        'confidence': 0.75,
        'prediction_date': datetime.now(timezone.utc),
        'time_horizon': '1m',
        'model_version': 'v1.0'
    }
    service.cache_service.get = Mock(return_value=cached_data)
    service._get_current_price = AsyncMock()
    
    result = await service.predict_price("AAPL", "1m")
    
    assert result is not None
    assert result.predicted_price == 157.5
    service._get_current_price.assert_not_called()
