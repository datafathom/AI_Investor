"""
Tests for AI Predictions Pydantic Models
Phase 7: Model Validation Tests
"""

import pytest
from datetime import datetime
from pydantic import ValidationError
from models.ai_predictions import (
    PredictionType,
    PricePrediction,
    TrendPrediction,
    MarketRegime
)


class TestPredictionTypeEnum:
    """Tests for PredictionType enum."""
    
    def test_prediction_type_enum(self):
        """Test prediction type enum values."""
        assert PredictionType.PRICE == "price"
        assert PredictionType.TREND == "trend"
        assert PredictionType.VOLATILITY == "volatility"
        assert PredictionType.MARKET_REGIME == "market_regime"


class TestPricePrediction:
    """Tests for PricePrediction model."""
    
    def test_valid_price_prediction(self):
        """Test valid price prediction creation."""
        prediction = PricePrediction(
            prediction_id='pred_1',
            symbol='AAPL',
            predicted_price=150.0,
            confidence=0.85,
            prediction_date=datetime.now(),
            time_horizon='1m',
            confidence_interval={'lower': 145.0, 'upper': 155.0},
            model_version='v1.0'
        )
        assert prediction.prediction_id == 'pred_1'
        assert prediction.predicted_price == 150.0
        assert prediction.confidence == 0.85
    
    def test_price_prediction_confidence_validation(self):
        """Test price prediction confidence validation."""
        # Should fail if confidence > 1
        with pytest.raises(ValidationError):
            PricePrediction(
                prediction_id='pred_1',
                symbol='AAPL',
                predicted_price=150.0,
                confidence=1.5,
                prediction_date=datetime.now(),
                time_horizon='1m',
                model_version='v1.0'
            )


class TestTrendPrediction:
    """Tests for TrendPrediction model."""
    
    def test_valid_trend_prediction(self):
        """Test valid trend prediction creation."""
        prediction = TrendPrediction(
            prediction_id='trend_1',
            symbol='AAPL',
            trend_direction='bullish',
            trend_strength=0.75,
            predicted_change=0.05,
            time_horizon='1m',
            confidence=0.8
        )
        assert prediction.prediction_id == 'trend_1'
        assert prediction.trend_direction == 'bullish'
        assert prediction.trend_strength == 0.75
        assert prediction.predicted_change == 0.05
    
    def test_trend_prediction_strength_validation(self):
        """Test trend prediction strength validation."""
        # Should fail if trend_strength > 1
        with pytest.raises(ValidationError):
            TrendPrediction(
                prediction_id='trend_1',
                symbol='AAPL',
                trend_direction='bullish',
                trend_strength=1.5,
                predicted_change=0.05,
                time_horizon='1m',
                confidence=0.8
            )


class TestMarketRegime:
    """Tests for MarketRegime model."""
    
    def test_valid_market_regime(self):
        """Test valid market regime creation."""
        regime = MarketRegime(
            regime_id='regime_1',
            regime_type='bull',
            confidence=0.8,
            detected_date=datetime.now(),
            expected_duration='3-6 months'
        )
        assert regime.regime_id == 'regime_1'
        assert regime.regime_type == 'bull'
        assert regime.confidence == 0.8
    
    def test_market_regime_optional_duration(self):
        """Test market regime with optional duration."""
        regime = MarketRegime(
            regime_id='regime_1',
            regime_type='bear',
            confidence=0.75,
            detected_date=datetime.now()
        )
        assert regime.expected_duration is None
