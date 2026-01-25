"""
Tests for Options API Endpoints
Phase 6: Options Strategy Builder & Analytics
"""

import pytest
from unittest.mock import AsyncMock, patch
from flask import Flask
from datetime import datetime
from web.api.options_api import options_bp


@pytest.fixture
def app():
    """Create Flask app for testing."""
    app = Flask(__name__)
    app.config['TESTING'] = True
    app.register_blueprint(options_bp)
    return app


@pytest.fixture
def client(app):
    """Create test client."""
    return app.test_client()


@pytest.fixture
def mock_strategy_builder_service():
    """Mock OptionsStrategyBuilderService."""
    with patch('web.api.options_api.get_strategy_builder_service') as mock:
        service = AsyncMock()
        mock.return_value = service
        yield service


@pytest.fixture
def mock_analytics_service():
    """Mock OptionsAnalyticsService."""
    with patch('web.api.options_api.get_options_analytics_service') as mock:
        service = AsyncMock()
        mock.return_value = service
        yield service


@pytest.mark.asyncio
async def test_create_strategy_success(client, mock_strategy_builder_service):
    """Test successful strategy creation."""
    from models.options import OptionsStrategy
    
    mock_strategy = OptionsStrategy(
        strategy_id='strategy_1',
        strategy_name='Test Strategy',
        underlying_symbol='AAPL',
        legs=[],
        strategy_type='custom'
    )
    mock_strategy_builder_service.create_strategy.return_value = mock_strategy
    
    response = client.post('/api/options/strategy/create',
                          json={
                              'strategy_name': 'Test Strategy',
                              'underlying_symbol': 'AAPL',
                              'legs': []
                          })
    
    assert response.status_code == 200
    data = response.get_json()
    assert data['success'] is True
    assert data['data']['strategy_name'] == 'Test Strategy'


@pytest.mark.asyncio
async def test_create_strategy_missing_params(client):
    """Test strategy creation with missing parameters."""
    response = client.post('/api/options/strategy/create',
                          json={'strategy_name': 'Test'})
    
    assert response.status_code == 400
    data = response.get_json()
    assert data['success'] is False


@pytest.mark.asyncio
async def test_create_from_template_success(client, mock_strategy_builder_service):
    """Test successful template-based strategy creation."""
    from models.options import OptionsStrategy
    
    mock_strategy = OptionsStrategy(
        strategy_id='strategy_1',
        strategy_name='Covered Call',
        underlying_symbol='AAPL',
        legs=[],
        strategy_type='covered_call'
    )
    mock_strategy_builder_service.create_from_template.return_value = mock_strategy
    
    response = client.post('/api/options/strategy/template',
                          json={
                              'template_name': 'covered_call',
                              'underlying_symbol': 'AAPL',
                              'current_price': 150.0,
                              'expiration': '2024-12-31'
                          })
    
    assert response.status_code == 200
    data = response.get_json()
    assert data['success'] is True


@pytest.mark.asyncio
async def test_get_greeks_success(client, mock_analytics_service):
    """Test successful Greeks calculation."""
    from models.options import Greeks
    
    mock_greeks = Greeks(
        strategy_id='strategy_1',
        delta=0.5,
        gamma=0.02,
        theta=-0.01,
        vega=0.15,
        rho=0.05
    )
    mock_analytics_service.calculate_greeks.return_value = mock_greeks
    
    response = client.get('/api/options/strategy/strategy_1/greeks')
    
    assert response.status_code == 200
    data = response.get_json()
    assert data['success'] is True
    assert data['data']['delta'] == 0.5


@pytest.mark.asyncio
async def test_get_pnl_success(client, mock_analytics_service):
    """Test successful P&L analysis."""
    from models.options import PnLAnalysis
    
    mock_pnl = PnLAnalysis(
        strategy_id='strategy_1',
        current_pnl=100.0,
        max_profit=500.0,
        max_loss=-200.0,
        breakeven_prices=[145.0, 155.0]
    )
    mock_analytics_service.calculate_pnl.return_value = mock_pnl
    
    response = client.get('/api/options/strategy/strategy_1/pnl')
    
    assert response.status_code == 200
    data = response.get_json()
    assert data['success'] is True
    assert data['data']['current_pnl'] == 100.0


@pytest.mark.asyncio
async def test_analyze_strategy_success(client, mock_analytics_service):
    """Test successful strategy analysis."""
    from models.options import StrategyAnalysis
    
    mock_analysis = StrategyAnalysis(
        strategy_id='strategy_1',
        risk_reward_ratio=2.0,
        probability_profit=0.65,
        expected_return=150.0
    )
    mock_analytics_service.analyze_strategy.return_value = mock_analysis
    
    response = client.post('/api/options/strategy/strategy_1/analyze', json={})
    
    assert response.status_code == 200
    data = response.get_json()
    assert data['success'] is True
