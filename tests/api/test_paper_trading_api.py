import pytest
from unittest.mock import AsyncMock, patch
from flask import Flask
from datetime import datetime, timezone
from web.api.paper_trading_api import paper_trading_bp, simulation_bp


@pytest.fixture
def app():
    """Create Flask app for testing."""
    app = Flask(__name__)
    app.config['TESTING'] = True
    app.register_blueprint(paper_trading_bp)
    app.register_blueprint(simulation_bp)
    return app


@pytest.fixture
def client(app):
    """Create test client."""
    return app.test_client()


@pytest.fixture
def mock_paper_trading_service():
    """Mock PaperTradingService."""
    with patch('web.api.paper_trading_api.get_paper_trading_service') as mock:
        service = AsyncMock()
        mock.return_value = service
        yield service


@pytest.fixture
def mock_simulation_service():
    """Mock SimulationService."""
    with patch('web.api.paper_trading_api.get_simulation_service') as mock:
        service = AsyncMock()
        mock.return_value = service
        yield service


def test_create_virtual_portfolio_success(client, mock_paper_trading_service):
    """Test successful virtual portfolio creation."""
    from models.paper_trading import VirtualPortfolio
    
    mock_portfolio = VirtualPortfolio(
        portfolio_id='portfolio_1',
        user_id='user_1',
        portfolio_name='Paper Trading Portfolio',
        initial_cash=100000.0,
        current_cash=100000.0,
        total_value=100000.0,
        positions={},
        created_date=datetime.now(timezone.utc),
        updated_date=datetime.now(timezone.utc)
    )
    mock_paper_trading_service.create_virtual_portfolio.return_value = mock_portfolio
    
    response = client.post('/api/paper-trading/portfolio/create',
                          json={
                              'user_id': 'user_1',
                              'portfolio_name': 'Paper Trading Portfolio',
                              'initial_cash': 100000.0
                          })
    
    assert response.status_code == 200
    data = response.get_json()
    assert data['success'] is True
    assert data['data']['portfolio_id'] == 'portfolio_1'


def test_create_virtual_portfolio_missing_user_id(client):
    """Test portfolio creation without user_id."""
    response = client.post('/api/paper-trading/portfolio/create',
                          json={'portfolio_name': 'Test'})
    
    assert response.status_code == 400
    data = response.get_json()
    assert data['success'] is False


def test_get_portfolio_success(client, mock_paper_trading_service):
    """Test successful portfolio retrieval."""
    from models.paper_trading import VirtualPortfolio
    
    mock_portfolio = VirtualPortfolio(
        portfolio_id='portfolio_1',
        user_id='user_1',
        portfolio_name='Paper Trading Portfolio',
        initial_cash=100000.0,
        current_cash=100000.0,
        total_value=100000.0,
        positions={},
        created_date=datetime.now(timezone.utc),
        updated_date=datetime.now(timezone.utc)
    )
    mock_paper_trading_service._get_portfolio.return_value = mock_portfolio
    
    response = client.get('/api/paper-trading/portfolio/portfolio_1')
    
    assert response.status_code == 200
    data = response.get_json()
    assert data['success'] is True


def test_execute_paper_order_success(client, mock_paper_trading_service):
    """Test successful paper order execution."""
    from models.paper_trading import PaperOrder
    
    mock_order = PaperOrder(
        order_id='order_1',
        user_id='user_1',
        symbol='AAPL',
        quantity=10,
        order_type='market',
        status='filled',
        filled_price=150.0,
        filled_quantity=10,
        created_date=datetime.now(timezone.utc)
    )
    mock_paper_trading_service.execute_paper_order.return_value = mock_order
    
    order_data = {
        'portfolio_id': 'portfolio_1',
        'symbol': 'AAPL',
        'side': 'buy',
        'quantity': 10,
        'order_type': 'market'
    }
    
    response = client.post('/api/paper-trading/order/execute', json=order_data)
    
    assert response.status_code == 200
    data = response.get_json()
    assert data['success'] is True


def test_get_performance_success(client, mock_paper_trading_service):
    """Test successful performance retrieval."""
    # API returns a dict directly from service
    mock_performance = {
        'total_return': 0.15,
        'sharpe_ratio': 1.5,
        'max_drawdown': 0.05
    }
    mock_paper_trading_service.get_portfolio_performance.return_value = mock_performance
    
    response = client.get('/api/paper-trading/portfolio/portfolio_1/performance')
    
    assert response.status_code == 200
    data = response.get_json()
    assert data['success'] is True
    assert data['data']['total_return'] == 0.15


def test_run_simulation_success(client, mock_simulation_service):
    """Test successful simulation run."""
    from models.paper_trading import SimulationResult
    
    mock_result = SimulationResult(
        simulation_id='sim_1',
        strategy_name='strategy_1',
        start_date=datetime(2024, 1, 1, tzinfo=timezone.utc),
        end_date=datetime(2024, 12, 31, tzinfo=timezone.utc),
        initial_capital=100000.0,
        final_capital=120000.0,
        total_return=0.20,
        sharpe_ratio=1.8,
        max_drawdown=0.05,
        win_rate=0.6,
        trades=[]
    )
    mock_simulation_service.run_historical_simulation.return_value = mock_result
    
    response = client.post('/api/simulation/run',
                          json={
                              'strategy_name': 'strategy_1',
                              'start_date': '2024-01-01',
                              'end_date': '2024-12-31'
                          })
    
    assert response.status_code == 200
    data = response.get_json()
    assert data['success'] is True
