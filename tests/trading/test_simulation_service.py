"""
Tests for Simulation Service
Comprehensive test coverage for historical replay and backtesting
"""

import pytest
from datetime import datetime, timedelta, timezone
from unittest.mock import Mock, AsyncMock, patch
from services.trading.simulation_service import SimulationService
from schemas.paper_trading import SimulationResult


@pytest.fixture
def service():
    """Create service instance with mocked dependencies."""
    with patch('services.trading.simulation_service.get_paper_trading_service'), \
         patch('services.trading.simulation_service.get_cache_service'):
        return SimulationService()


@pytest.mark.asyncio
async def test_run_historical_simulation(service):
    """Test historical simulation execution."""
    mock_portfolio = Mock(portfolio_id="sim_portfolio")
    service.paper_trading.create_virtual_portfolio = AsyncMock(return_value=mock_portfolio)
    service._simulate_strategy = AsyncMock(return_value=[
        {'symbol': 'AAPL', 'action': 'buy', 'quantity': 100, 'price': 150.0, 'date': datetime(2024, 1, 1, tzinfo=timezone.utc)},
        {'symbol': 'AAPL', 'action': 'sell', 'quantity': 100, 'price': 160.0, 'date': datetime(2024, 6, 1, tzinfo=timezone.utc)},
    ])
    service.paper_trading.get_portfolio_performance = AsyncMock(return_value={
        'total_return': 6.67,
        'total_value': 106670.0
    })
    service._calculate_sharpe_ratio = AsyncMock(return_value=1.2)
    service._calculate_max_drawdown = AsyncMock(return_value=0.05)
    service._calculate_win_rate = AsyncMock(return_value=0.6)
    service._save_simulation = AsyncMock()
    
    start_date = datetime(2024, 1, 1, tzinfo=timezone.utc)
    end_date = datetime(2024, 12, 31, tzinfo=timezone.utc)
    
    result = await service.run_historical_simulation(
        strategy_name="Test Strategy",
        start_date=start_date,
        end_date=end_date,
        initial_capital=100000.0
    )
    
    assert result is not None
    assert isinstance(result, SimulationResult)
    assert result.strategy_name == "Test Strategy"
    assert result.start_date == start_date
    assert result.end_date == end_date
    assert result.initial_capital == 100000.0


@pytest.mark.asyncio
async def test_run_historical_simulation_with_config(service):
    """Test historical simulation with strategy configuration."""
    mock_portfolio = Mock(portfolio_id="sim_portfolio")
    service.paper_trading.create_virtual_portfolio = AsyncMock(return_value=mock_portfolio)
    service._simulate_strategy = AsyncMock(return_value=[])
    service.paper_trading.get_portfolio_performance = AsyncMock(return_value={
        'total_return': 0.0,
        'total_value': 100000.0
    })
    service._calculate_sharpe_ratio = AsyncMock(return_value=0.0)
    service._calculate_max_drawdown = AsyncMock(return_value=0.0)
    service._calculate_win_rate = AsyncMock(return_value=0.0)
    service._save_simulation = AsyncMock()
    
    config = {'max_position_size': 0.1, 'stop_loss': 0.05}
    
    result = await service.run_historical_simulation(
        strategy_name="Test Strategy",
        start_date=datetime(2024, 1, 1, tzinfo=timezone.utc),
        end_date=datetime(2024, 12, 31, tzinfo=timezone.utc),
        initial_capital=100000.0,
        strategy_config=config
    )
    
    assert result is not None
    service._simulate_strategy.assert_called_once()


@pytest.mark.asyncio
async def test_get_simulation_results(service):
    """Test retrieving simulation results."""
    service._get_simulations_from_db = AsyncMock(return_value=[
        {
            'simulation_id': 'sim_1',
            'strategy_name': 'Strategy 1',
            'total_return': 0.10,
            'sharpe_ratio': 1.2
        },
        {
            'simulation_id': 'sim_2',
            'strategy_name': 'Strategy 2',
            'total_return': 0.15,
            'sharpe_ratio': 1.5
        },
    ])
    
    result = await service.get_simulation_results(
        user_id="user_123",
        limit=10
    )
    
    assert result is not None
    assert len(result) == 2


@pytest.mark.asyncio
async def test_compare_simulations(service):
    """Test comparing multiple simulations."""
    simulations = [
        SimulationResult(
            simulation_id="sim_1",
            strategy_name="Strategy 1",
            start_date=datetime(2024, 1, 1, tzinfo=timezone.utc),
            end_date=datetime(2024, 12, 31, tzinfo=timezone.utc),
            initial_capital=100000.0,
            final_capital=110000.0,
            total_return=0.10,
            sharpe_ratio=1.2,
            max_drawdown=0.05,
            win_rate=0.6
        ),
        SimulationResult(
            simulation_id="sim_2",
            strategy_name="Strategy 2",
            start_date=datetime(2024, 1, 1, tzinfo=timezone.utc),
            end_date=datetime(2024, 12, 31, tzinfo=timezone.utc),
            initial_capital=100000.0,
            final_capital=115000.0,
            total_return=0.15,
            sharpe_ratio=1.5,
            max_drawdown=0.03,
            win_rate=0.65
        ),
    ]
    
    result = await service.compare_simulations(simulations)
    
    assert result is not None
    assert 'best_return' in result or hasattr(result, 'best_return')
    assert 'best_sharpe' in result or hasattr(result, 'best_sharpe')


@pytest.mark.asyncio
async def test_run_historical_simulation_error_handling(service):
    """Test error handling in simulation."""
    service.paper_trading.create_virtual_portfolio = AsyncMock(side_effect=Exception("Error"))
    
    with pytest.raises(Exception):
        await service.run_historical_simulation(
            strategy_name="Error Strategy",
            start_date=datetime(2024, 1, 1, tzinfo=timezone.utc),
            end_date=datetime(2024, 12, 31, tzinfo=timezone.utc)
        )
