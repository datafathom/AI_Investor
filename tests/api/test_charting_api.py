"""
Tests for Charting API Endpoints
Phase 5: Advanced Charting & Technical Analysis
"""

import pytest
from unittest.mock import AsyncMock
from fastapi import FastAPI
from fastapi.testclient import TestClient
from web.api.charting_api import router, get_charting_service, get_technical_analysis_service


@pytest.fixture
def api_app(mock_charting_service, mock_technical_analysis_service):
    """Create FastAPI app for testing."""
    app = FastAPI()
    app.include_router(router)
    app.dependency_overrides[get_charting_service] = lambda: mock_charting_service
    app.dependency_overrides[get_technical_analysis_service] = lambda: mock_technical_analysis_service
    return app


@pytest.fixture
def client(api_app):
    """Create test client."""
    return TestClient(api_app)


@pytest.fixture
def mock_charting_service():
    """Mock ChartingService."""
    service = AsyncMock()
    return service


@pytest.fixture
def mock_technical_analysis_service():
    """Mock TechnicalAnalysisService."""
    service = AsyncMock()
    return service


def test_get_chart_data_success(client, mock_charting_service):
    """Test successful chart data retrieval."""
    mock_chart_data = {
        'symbol': 'AAPL',
        'timeframe': '1day',
        'data': [],
        'indicators': {}
    }
    mock_charting_service.get_chart_data.return_value = mock_chart_data
    
    response = client.get('/api/v1/charting/data?symbol=AAPL&timeframe=1day&chart_type=candlestick')
    
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert data['data']['symbol'] == 'AAPL'


def test_get_patterns_success(client, mock_charting_service, mock_technical_analysis_service):
    """Test successful pattern recognition."""
    mock_chart_data = {
        'symbol': 'AAPL',
        'timeframe': '1day',
        'data': [{'open': 150, 'high': 151, 'low': 149, 'close': 150.5, 'volume': 1000}]
    }
    mock_charting_service.get_chart_data.return_value = mock_chart_data
    
    mock_patterns = [
        {'pattern': 'head_and_shoulders', 'confidence': 0.85, 'signal': 'bearish'}
    ]
    mock_technical_analysis_service.recognize_patterns.return_value = mock_patterns
    
    response = client.get('/api/v1/charting/patterns?symbol=AAPL')
    
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True


def test_get_signals_success(client, mock_charting_service, mock_technical_analysis_service):
    """Test successful trading signals generation."""
    mock_chart_data = {
        'symbol': 'AAPL',
        'timeframe': '1day',
        'data': [{'open': 150, 'high': 151, 'low': 149, 'close': 150.5, 'volume': 1000}]
    }
    mock_charting_service.get_chart_data.return_value = mock_chart_data
    
    mock_signals = {
        'buy_signals': 2,
        'sell_signals': 1,
        'hold_signals': 0,
        'overall_signal': 'buy'
    }
    mock_technical_analysis_service.generate_signals.return_value = mock_signals
    
    response = client.get('/api/v1/charting/signals?symbol=AAPL')
    
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
