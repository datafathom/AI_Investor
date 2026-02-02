"""
Tests for AI Predictions API Endpoints
Phase 22: AI Predictions & Forecasting
"""

import pytest
from unittest.mock import AsyncMock, patch
from flask import Flask
from web.api.ai_predictions_api import ai_predictions_bp
from datetime import datetime, timezone


@pytest.fixture
def app():
    """Create Flask app for testing."""
    app = Flask(__name__)
    app.config['TESTING'] = True
    app.register_blueprint(ai_predictions_bp)
    return app


@pytest.fixture
def client(app):
    """Create test client."""
    return app.test_client()


@pytest.fixture
def mock_prediction_engine():
    """Mock PredictionEngine."""
    with patch('web.api.ai_predictions_api.get_prediction_engine') as mock:
        engine = AsyncMock()
        mock.return_value = engine
        yield engine


@pytest.fixture
def mock_ai_analytics_service():
    """Mock AIAnalyticsService."""
    with patch('web.api.ai_predictions_api.get_ai_analytics_service') as mock:
        service = AsyncMock()
        mock.return_value = service
        yield service


def test_predict_price_success(client, mock_prediction_engine):
    """Test successful price prediction."""
    from models.ai_predictions import PricePrediction
    
    from datetime import datetime
    mock_prediction = PricePrediction(
        prediction_id='pred_1',
        symbol='AAPL',
        predicted_price=150.0,
        current_price=145.0,
        confidence=0.85,
        prediction_date=datetime.now(timezone.utc),
        time_horizon='1m',
        model_version='v1.0'
    )
    mock_prediction_engine.predict_price.return_value = mock_prediction
    
    response = client.post('/api/ai-predictions/price',
                          json={
                              'symbol': 'AAPL',
                              'time_horizon': '1m',
                              'model_version': 'v1.0'
                          })
    
    assert response.status_code == 200
    data = response.get_json()
    assert data['success'] is True
    assert data['data']['symbol'] == 'AAPL'


def test_predict_price_missing_symbol(client):
    """Test price prediction without symbol."""
    response = client.post('/api/ai-predictions/price', json={})
    
    assert response.status_code == 400
    data = response.get_json()
    assert data['success'] is False


def test_predict_trend_success(client, mock_prediction_engine):
    """Test successful trend prediction."""
    from models.ai_predictions import TrendPrediction
    
    mock_trend = TrendPrediction(
        prediction_id='trend_1',
        symbol='AAPL',
        trend_direction='bullish',
        trend_strength=0.8,
        predicted_change=5.0,
        confidence=0.75,
        time_horizon='1m'
    )
    mock_prediction_engine.predict_trend.return_value = mock_trend
    
    response = client.post('/api/ai-predictions/trend',
                          json={'symbol': 'AAPL', 'time_horizon': '1m'})
    
    assert response.status_code == 200
    data = response.get_json()
    assert data['success'] is True


def test_get_market_regime_success(client, mock_ai_analytics_service):
    """Test successful market regime detection."""
    from models.ai_predictions import MarketRegime
    
    from datetime import datetime
    mock_regime = MarketRegime(
        regime_id='reg_1',
        regime_type='bull',
        confidence=0.8,
        detected_date=datetime.now(timezone.utc),
        indicators={}
    )
    mock_ai_analytics_service.detect_market_regime.return_value = mock_regime
    
    response = client.get('/api/ai-predictions/regime?symbol=AAPL')
    
    assert response.status_code == 200
    data = response.get_json()
    assert data['success'] is True
