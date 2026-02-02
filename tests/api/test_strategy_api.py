import pytest
from unittest.mock import AsyncMock, patch
from flask import Flask
from datetime import datetime, timezone
from web.api.strategy_api import strategy_bp


@pytest.fixture
def app():
    """Create Flask app for testing."""
    app = Flask(__name__)
    app.config['TESTING'] = True
    app.register_blueprint(strategy_bp)
    return app


@pytest.fixture
def client(app):
    """Create test client."""
    return app.test_client()


@pytest.fixture
def mock_strategy_builder_service():
    """Mock StrategyBuilderService."""
    with patch('web.api.strategy_api.get_strategy_builder_service') as mock:
        service = AsyncMock()
        mock.return_value = service
        yield service


@pytest.fixture
def mock_strategy_execution_service():
    """Mock StrategyExecutionService."""
    with patch('web.api.strategy_api.get_strategy_execution_service') as mock:
        service = AsyncMock()
        mock.return_value = service
        yield service


def test_create_strategy_success(client, mock_strategy_builder_service):
    """Test successful strategy creation."""
    from models.strategy import TradingStrategy
    
    mock_strategy = TradingStrategy(
        strategy_id='strategy_1',
        user_id='user_1',
        strategy_name='Test Strategy',
        description='Test description',
        rules=[],
        created_date=datetime.now(timezone.utc),
        updated_date=datetime.now(timezone.utc)
    )
    mock_strategy_builder_service.create_strategy.return_value = mock_strategy
    
    response = client.post('/api/strategy/create',
                          json={
                              'user_id': 'user_1',
                              'strategy_name': 'Test Strategy',
                              'description': 'Test description'
                          })
    
    assert response.status_code == 200
    data = response.get_json()
    assert data['success'] is True
    assert data['data']['strategy_name'] == 'Test Strategy'


def test_create_strategy_missing_params(client):
    """Test strategy creation with missing parameters."""
    response = client.post('/api/strategy/create', json={'user_id': 'user_1'})
    
    assert response.status_code == 400
    data = response.get_json()
    assert data['success'] is False


def test_get_strategy_success(client, mock_strategy_builder_service):
    """Test successful strategy retrieval."""
    from models.strategy import TradingStrategy
    
    mock_strategy = TradingStrategy(
        strategy_id='strategy_1',
        user_id='user_1',
        strategy_name='Test Strategy',
        rules=[],
        created_date=datetime.now(timezone.utc),
        updated_date=datetime.now(timezone.utc)
    )
    mock_strategy_builder_service._get_strategy.return_value = mock_strategy
    
    response = client.get('/api/strategy/strategy_1')
    
    assert response.status_code == 200
    data = response.get_json()
    assert data['success'] is True


def test_get_strategy_not_found(client, mock_strategy_builder_service):
    """Test strategy retrieval when not found."""
    mock_strategy_builder_service._get_strategy.return_value = None
    
    response = client.get('/api/strategy/strategy_1')
    
    assert response.status_code == 404
    data = response.get_json()
    assert data['success'] is False


def test_start_strategy_success(client, mock_strategy_execution_service):
    """Test successful strategy start."""
    from models.strategy import StrategyExecution
    
    mock_execution = StrategyExecution(
        execution_id='exec_1',
        strategy_id='strategy_1',
        rule_id='rule_1',
        action_taken='buy',
        execution_time=datetime.now(timezone.utc),
        result='success'
    )
    mock_strategy_execution_service.start_strategy.return_value = mock_execution
    
    response = client.post('/api/strategy/strategy_1/start', 
                          json={'portfolio_id': 'portfolio_1'})
    
    assert response.status_code == 200
    data = response.get_json()
    assert data['success'] is True


def test_stop_strategy_success(client, mock_strategy_execution_service):
    """Test successful strategy stop."""
    from models.strategy import TradingStrategy, StrategyStatus
    mock_strategy = TradingStrategy(
        strategy_id='strategy_1',
        user_id='user_1',
        strategy_name='Test Strategy',
        status=StrategyStatus.STOPPED,
        created_date=datetime.now(timezone.utc),
        updated_date=datetime.now(timezone.utc)
    )
    mock_strategy_execution_service.stop_strategy.return_value = mock_strategy
    response = client.post('/api/strategy/strategy_1/stop')
    
    assert response.status_code == 200
    data = response.get_json()
    assert data['success'] is True


def test_get_strategy_performance_success(client, mock_strategy_execution_service):
    """Test successful performance retrieval."""
    from models.strategy import StrategyPerformance, StrategyStatus
    
    mock_performance = StrategyPerformance(
        strategy_id='strategy_1',
        total_trades=10,
        winning_trades=7,
        losing_trades=3,
        win_rate=0.7,
        total_pnl=1500.0,
        sharpe_ratio=1.5,
        max_drawdown=0.05,
        current_status=StrategyStatus.ACTIVE
    )
    mock_strategy_execution_service.get_strategy_performance.return_value = mock_performance
    
    response = client.get('/api/strategy/strategy_1/performance')
    
    assert response.status_code == 200
    data = response.get_json()
    assert data['success'] is True
    assert data['data']['total_pnl'] == 1500.0
