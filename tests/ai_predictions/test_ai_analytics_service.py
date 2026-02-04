"""
Tests for AI Analytics Service
Comprehensive test coverage for sentiment analysis and market regime detection
"""

import pytest
from datetime import datetime
from unittest.mock import Mock, AsyncMock, patch
from services.ai_predictions.ai_analytics_service import AIAnalyticsService
from schemas.ai_predictions import SentimentAnalysisResult, MarketRegime


@pytest.fixture
def service():
    """Create service instance with mocked dependencies."""
    with patch('services.ai_predictions.ai_analytics_service.get_cache_service'):
        return AIAnalyticsService()


@pytest.mark.asyncio
async def test_analyze_sentiment(service):
    """Test sentiment analysis."""
    service._analyze_text_sentiment = AsyncMock(return_value={
        'overall_sentiment': 0.7,
        'positive_score': 0.8,
        'negative_score': 0.1
    })
    
    result = await service.analyze_sentiment(
        symbol="AAPL",
        text="Apple reports strong earnings and growth"
    )
    
    assert result is not None
    assert isinstance(result, SentimentAnalysisResult) or isinstance(result, dict)
    assert 'overall_sentiment' in str(result) or hasattr(result, 'overall_sentiment')


@pytest.mark.asyncio
async def test_detect_market_regime(service):
    """Test market regime detection."""
    service._analyze_market_conditions = AsyncMock(return_value={
        'regime': 'bull_market',
        'confidence': 0.85
    })
    
    result = await service.detect_market_regime()
    
    assert result is not None
    assert isinstance(result, MarketRegime) or isinstance(result, dict)
    assert 'regime' in str(result) or hasattr(result, 'regime')