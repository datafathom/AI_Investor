
import pytest
from unittest.mock import AsyncMock, patch
from fastapi import FastAPI
from fastapi.testclient import TestClient
from web.api.ai_predictions_api import router, get_prediction_engine, get_ai_analytics_service
from web.auth_utils import get_current_user
from datetime import datetime, timezone

@pytest.fixture
def api_app(mock_prediction_engine, mock_ai_analytics_service):
    """Create FastAPI app for testing."""
    app = FastAPI()
    app.include_router(router)
    app.dependency_overrides[get_prediction_engine] = lambda: mock_prediction_engine
    app.dependency_overrides[get_ai_analytics_service] = lambda: mock_ai_analytics_service
    app.dependency_overrides[get_current_user] = lambda: {"id": "user_1", "role": "user"}
    return app


@pytest.fixture
def client(api_app):
    """Create test client."""
    return TestClient(api_app)


@pytest.fixture
def mock_prediction_engine():
    """Mock PredictionEngine."""
    engine = AsyncMock()
    return engine


@pytest.fixture
def mock_ai_analytics_service():
    """Mock AIAnalyticsService."""
    service = AsyncMock()
    return service


def test_predict_price_success(client, mock_prediction_engine):
    """Test successful price prediction."""
    from schemas.ai_predictions import PricePrediction
    
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
    
    response = client.post('/api/v1/ai-predictions/price',
                          json={
                              'symbol': 'AAPL',
                              'time_horizon': '1m',
                              'model_version': 'v1.0'
                          })
    
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert data['data']['symbol'] == 'AAPL'


def test_predict_price_missing_symbol(client):
    """Test price prediction without symbol."""
    response = client.post('/api/v1/ai-predictions/price', json={})
    
    assert response.status_code in [400, 422]
    # data = response.json()
    # assert data['success'] is False


def test_predict_trend_success(client, mock_prediction_engine):
    """Test successful trend prediction."""
    from schemas.ai_predictions import TrendPrediction
    
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
    
    response = client.post('/api/v1/ai-predictions/trend',
                          json={'symbol': 'AAPL', 'time_horizon': '1m'})
    
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True


def test_get_market_regime_success(client, mock_ai_analytics_service):
    """Test successful market regime detection."""
    from schemas.ai_predictions import MarketRegime
    
    from datetime import datetime
    mock_regime = MarketRegime(
        regime_id='reg_1',
        regime_type='bull',
        confidence=0.8,
        detected_date=datetime.now(timezone.utc),
        indicators={}
    )
    mock_ai_analytics_service.detect_market_regime.return_value = mock_regime
    
    response = client.get('/api/v1/ai-predictions/regime?symbol=AAPL')
    
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
