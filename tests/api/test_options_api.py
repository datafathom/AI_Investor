import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from flask import Flask
from datetime import datetime, timezone
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


@pytest.fixture
def mock_cache_service():
    """Mock CacheService."""
    with patch('services.system.cache_service.get_cache_service') as mock:
        service = MagicMock()
        mock.return_value = service
        yield service


def test_create_strategy_success(client, mock_strategy_builder_service):
    """Test successful strategy creation."""
    from models.options import OptionsStrategy
    
    mock_strategy = OptionsStrategy(
        strategy_id='strategy_1',
        strategy_name='Test Strategy',
        underlying_symbol='AAPL',
        legs=[],
        net_cost=100.0,
        strategy_type='custom',
        created_date=datetime.now(timezone.utc)
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


def test_create_strategy_missing_params(client):
    """Test strategy creation with missing parameters."""
    response = client.post('/api/options/strategy/create',
                          json={'strategy_name': 'Test'})
    
    assert response.status_code == 400
    data = response.get_json()
    assert data['success'] is False


def test_create_from_template_success(client, mock_strategy_builder_service):
    """Test successful template-based strategy creation."""
    from models.options import OptionsStrategy
    
    mock_strategy = OptionsStrategy(
        strategy_id='strategy_1',
        strategy_name='Covered Call',
        underlying_symbol='AAPL',
        legs=[],
        net_cost=50.0,
        strategy_type='covered_call',
        created_date=datetime.now(timezone.utc)
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


def test_get_greeks_success(client, mock_analytics_service, mock_cache_service):
    """Test successful Greeks calculation."""
    from models.options import Greeks, OptionsStrategy
    
    mock_strategy = OptionsStrategy(
        strategy_id='strategy_1',
        strategy_name='Test Strategy',
        underlying_symbol='AAPL',
        legs=[],
        net_cost=100.0,
        strategy_type='custom',
        created_date=datetime.now(timezone.utc)
    )
    mock_cache_service.get.return_value = mock_strategy.model_dump()
    
    mock_greeks = Greeks(
        delta=0.5,
        gamma=0.02,
        theta=-0.01,
        vega=0.15,
        rho=0.05
    )
    mock_analytics_service.calculate_greeks.return_value = mock_greeks
    
    response = client.get('/api/options/strategy/strategy_1/greeks?underlying_price=150.0')
    
    assert response.status_code == 200
    data = response.get_json()
    assert data['success'] is True
    assert data['data']['delta'] == 0.5


def test_get_pnl_success(client, mock_analytics_service, mock_cache_service):
    """Test successful P&L analysis."""
    from models.options import StrategyPnL, OptionsStrategy
    
    mock_strategy = OptionsStrategy(
        strategy_id='strategy_1',
        strategy_name='Test Strategy',
        underlying_symbol='AAPL',
        legs=[],
        net_cost=100.0,
        strategy_type='custom',
        created_date=datetime.now(timezone.utc)
    )
    mock_cache_service.get.return_value = mock_strategy.model_dump()
    
    mock_pnl = StrategyPnL(
        strategy_id='strategy_1',
        underlying_price=150.0,
        days_to_expiration=30,
        profit_loss=100.0,
        profit_loss_pct=0.05,
        intrinsic_value=50.0,
        time_value=50.0
    )
    mock_analytics_service.calculate_pnl.return_value = mock_pnl
    
    response = client.get('/api/options/strategy/strategy_1/pnl?underlying_price=150.0')
    
    assert response.status_code == 200
    data = response.get_json()
    assert data['success'] is True
    assert data['data']['profit_loss'] == 100.0


def test_analyze_strategy_success(client, mock_analytics_service, mock_cache_service):
    """Test successful strategy analysis."""
    from models.options import StrategyAnalysis, OptionsStrategy, StrategyGreeks, StrategyPnL
    
    mock_strategy = OptionsStrategy(
        strategy_id='strategy_1',
        strategy_name='Test Strategy',
        underlying_symbol='AAPL',
        legs=[],
        net_cost=100.0,
        strategy_type='custom',
        created_date=datetime.now(timezone.utc)
    )
    mock_cache_service.get.return_value = mock_strategy.model_dump()
    
    mock_greeks = StrategyGreeks(
        strategy_id='strategy_1',
        total_delta=0.5,
        total_gamma=0.02,
        total_theta=-0.01,
        total_vega=0.15
    )
    
    mock_pnl = StrategyPnL(
        strategy_id='strategy_1',
        underlying_price=150.0,
        days_to_expiration=30,
        profit_loss=100.0,
        profit_loss_pct=0.05,
        intrinsic_value=50.0,
        time_value=50.0
    )
    
    mock_analysis = StrategyAnalysis(
        strategy=mock_strategy,
        greeks=mock_greeks,
        pnl=mock_pnl,
        probability_profit=0.65
    )
    mock_analytics_service.analyze_strategy.return_value = mock_analysis
    
    response = client.post('/api/options/strategy/strategy_1/analyze', 
                          json={'underlying_price': 150.0})
    
    assert response.status_code == 200
    data = response.get_json()
    assert data['success'] is True
