"""
==============================================================================
FILE: models/ai_predictions.py
ROLE: AI Predictions Data Models
PURPOSE: Pydantic models for price predictions, market forecasting, and
         trend analysis.

INTEGRATION POINTS:
    - PredictionEngine: Price forecasting
    - AIAnalyticsService: Market analysis
    - AIPredictionsAPI: Prediction endpoints
    - FrontendAI: Prediction dashboard

AUTHOR: AI Investor Team
CREATED: 2026-01-21
LAST_MODIFIED: 2026-01-21
==============================================================================
"""

from pydantic import BaseModel, Field
from datetime import datetime
from typing import Dict, List, Optional
from enum import Enum


class PredictionType(str, Enum):
    """Prediction types."""
    PRICE = "price"
    TREND = "trend"
    VOLATILITY = "volatility"
    MARKET_REGIME = "market_regime"


class PricePrediction(BaseModel):
    """Price prediction result."""
    prediction_id: str
    symbol: str
    predicted_price: float
    confidence: float = Field(..., ge=0, le=1)
    prediction_date: datetime
    time_horizon: str  # "1d", "1w", "1m", "3m", "1y"
    confidence_interval: Dict[str, float] = {}  # {lower: value, upper: value}
    model_version: str


class TrendPrediction(BaseModel):
    """Trend prediction result."""
    prediction_id: str
    symbol: str
    trend_direction: str  # "bullish", "bearish", "neutral"
    trend_strength: float = Field(..., ge=0, le=1)
    predicted_change: float  # Percentage change
    time_horizon: str
    confidence: float


class MarketRegime(BaseModel):
    """Market regime detection."""
    regime_id: str
    regime_type: str  # "bull", "bear", "sideways", "volatile"
    confidence: float
    detected_date: datetime
    expected_duration: Optional[str] = None
    
    @property
    def regime(self) -> str:
        """Alias for regime_type for test compatibility."""
        return self.regime_type


class SentimentAnalysisResult(BaseModel):
    """Sentiment analysis result."""
    symbol: Optional[str] = None
    overall_sentiment: float
    positive_score: float
    negative_score: float
    neutral_score: float = 0.0
    sentiment_label: str = "neutral"
    confidence: float = 0.0
    analysis_date: datetime = Field(default_factory=datetime.utcnow)
