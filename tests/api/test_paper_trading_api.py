"""
Tests for Paper Trading API Endpoints
Phase 14: Paper Trading & Simulation
"""

import pytest
from unittest.mock import AsyncMock, patch
from flask import Flask
from datetime import datetime
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


@pytest.mark.asyncio
async def test_create_virtual_portfolio_success(client, mock_paper_trading_service):
    """Test successful virtual portfolio creation."""
    from models.trading import VirtualPortfolio
    
    mock_portfolio = VirtualPortfolio(
        portfolio_id='portfolio_1',
        user_id='user_1',
        portfolio_name='Paper Trading Portfolio',
        cash_balance=100000.0,
        positions={}
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


@pytest.mark.asyncio
async def test_create_virtual_portfolio_missing_user_id(client):
    """Test portfolio creation without user_id."""
    response = client.post('/api/paper-trading/portfolio/create',
                          json={'portfolio_name': 'Test'})
    
    assert response.status_code == 400
    data = response.get_json()
    assert data['success'] is False


@pytest.mark.asyncio
async def test_get_portfolio_success(client, mock_paper_trading_service):
    """Test successful portfolio retrieval."""
    from models.trading import VirtualPortfolio
    
    mock_portfolio = VirtualPortfolio(
        portfolio_id='portfolio_1',
        user_id='user_1',
        portfolio_name='Paper Trading Portfolio',
        cash_balance=100000.0,
        positions={}
    )
    mock_paper_trading_service.get_virtual_portfolio.return_value = mock_portfolio
    
    response = client.get('/api/paper-trading/portfolio/portfolio_1')
    
    assert response.status_code == 200
    data = response.get_json()
    assert data['success'] is True


@pytest.mark.asyncio
async def test_execute_paper_order_success(client, mock_paper_trading_service):
    """Test successful paper order execution."""
    from models.trading import PaperOrder, PaperOrderExecution
    
    mock_execution = PaperOrderExecution(
        order_id='order_1',
        portfolio_id='portfolio_1',
        executed_at=datetime.now(),
        fill_price=150.0,
        quantity=10
    )
    mock_paper_trading_service.execute_paper_order.return_value = mock_execution
    
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


@pytest.mark.asyncio
async def test_get_performance_success(client, mock_paper_trading_service):
    """Test successful performance retrieval."""
    from models.trading import PortfolioPerformance
    
    mock_performance = PortfolioPerformance(
        portfolio_id='portfolio_1',
        total_return=0.15,
        sharpe_ratio=1.5,
        max_drawdown=0.05
    )
    mock_paper_trading_service.get_portfolio_performance.return_value = mock_performance
    
    response = client.get('/api/paper-trading/portfolio/portfolio_1/performance')
    
    assert response.status_code == 200
    data = response.get_json()
    assert data['success'] is True
    assert data['data']['total_return'] == 0.15


@pytest.mark.asyncio
async def test_run_simulation_success(client, mock_simulation_service):
    """Test successful simulation run."""
    from models.trading import SimulationResult
    
    mock_result = SimulationResult(
        simulation_id='sim_1',
        strategy_id='strategy_1',
        start_date=datetime(2024, 1, 1),
        end_date=datetime(2024, 12, 31),
        total_return=0.20,
        sharpe_ratio=1.8
    )
    mock_simulation_service.run_historical_simulation.return_value = mock_result
    
    response = client.post('/api/simulation/run',
                          json={
                              'strategy_id': 'strategy_1',
                              'start_date': '2024-01-01',
                              'end_date': '2024-12-31'
                          })
    
    assert response.status_code == 200
    data = response.get_json()
    assert data['success'] is True
