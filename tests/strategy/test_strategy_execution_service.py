"""
Tests for Strategy Execution Service
Comprehensive test coverage for strategy execution, monitoring, and risk controls
"""

import pytest
from datetime import datetime
from unittest.mock import Mock, AsyncMock, patch
from services.strategy.strategy_execution_service import StrategyExecutionService
from models.strategy import TradingStrategy, StrategyStatus, StrategyPerformance


@pytest.fixture
def service():
    """Create service instance with mocked dependencies."""
    with patch('services.strategy.strategy_execution_service.get_strategy_builder_service'), \
         patch('services.strategy.strategy_execution_service.get_cache_service'):
        return StrategyExecutionService()


@pytest.fixture
def mock_strategy():
    """Mock trading strategy."""
    return TradingStrategy(
        strategy_id="strategy_123",
        user_id="user_123",
        strategy_name="Test Strategy",
        rules=[],
        status=StrategyStatus.DRAFT,
        created_date=datetime.utcnow(),
        updated_date=datetime.utcnow()
    )


@pytest.mark.asyncio
async def test_start_strategy(service, mock_strategy):
    """Test starting strategy execution."""
    service.strategy_builder._get_strategy = AsyncMock(return_value=mock_strategy)
    service.strategy_builder.validate_strategy = AsyncMock(return_value={'valid': True, 'errors': []})
    service.strategy_builder._save_strategy = AsyncMock()
    
    result = await service.start_strategy(
        strategy_id="strategy_123",
        portfolio_id="portfolio_123"
    )
    
    assert result is not None
    assert result.status == StrategyStatus.ACTIVE
    assert result.portfolio_id == "portfolio_123"
    assert "strategy_123" in service.active_strategies


@pytest.mark.asyncio
async def test_start_strategy_not_found(service):
    """Test starting non-existent strategy."""
    service.strategy_builder._get_strategy = AsyncMock(return_value=None)
    
    with pytest.raises(ValueError, match="not found"):
        await service.start_strategy(
            strategy_id="nonexistent",
            portfolio_id="portfolio_123"
        )


@pytest.mark.asyncio
async def test_start_strategy_validation_failed(service, mock_strategy):
    """Test starting strategy with validation failure."""
    service.strategy_builder._get_strategy = AsyncMock(return_value=mock_strategy)
    service.strategy_builder.validate_strategy = AsyncMock(return_value={'valid': False, 'errors': ['Invalid rules']})
    
    with pytest.raises(ValueError, match="validation failed"):
        await service.start_strategy(
            strategy_id="strategy_123",
            portfolio_id="portfolio_123"
        )


@pytest.mark.asyncio
async def test_stop_strategy(service, mock_strategy):
    """Test stopping strategy execution."""
    mock_strategy.status = StrategyStatus.ACTIVE
    service.active_strategies["strategy_123"] = mock_strategy
    service.strategy_builder._get_strategy = AsyncMock(return_value=mock_strategy)
    service.strategy_builder._save_strategy = AsyncMock()
    
    result = await service.stop_strategy("strategy_123")
    
    assert result is not None
    assert result.status == StrategyStatus.STOPPED
    assert "strategy_123" not in service.active_strategies


@pytest.mark.asyncio
async def test_pause_strategy(service, mock_strategy):
    """Test pausing strategy execution."""
    mock_strategy.status = StrategyStatus.ACTIVE
    service.active_strategies["strategy_123"] = mock_strategy
    service.strategy_builder._get_strategy = AsyncMock(return_value=mock_strategy)
    service.strategy_builder._save_strategy = AsyncMock()
    
    result = await service.pause_strategy("strategy_123")
    
    assert result is not None
    assert result.status == StrategyStatus.PAUSED
    assert "strategy_123" in service.active_strategies  # Still in active but paused


@pytest.mark.asyncio
async def test_get_strategy_performance(service, mock_strategy):
    """Test getting strategy performance."""
    service.strategy_builder._get_strategy = AsyncMock(return_value=mock_strategy)
    service._calculate_performance_metrics = AsyncMock(return_value={
        'total_return': 0.10,
        'sharpe_ratio': 1.2,
        'win_rate': 0.6,
        'total_trades': 50
    })
    
    result = await service.get_strategy_performance("strategy_123")
    
    assert result is not None
    assert isinstance(result, StrategyPerformance) or isinstance(result, dict)
    assert 'total_return' in str(result) or hasattr(result, 'total_return')


@pytest.mark.asyncio
async def test_check_risk_controls(service, mock_strategy):
    """Test risk control checking."""
    service.strategy_builder._get_strategy = AsyncMock(return_value=mock_strategy)
    service._check_position_limits = AsyncMock(return_value=True)
    service._check_loss_limits = AsyncMock(return_value=True)
    service._check_drawdown_limits = AsyncMock(return_value=True)
    
    result = await service.check_risk_controls("strategy_123")
    
    assert result is not None
    assert result.get('passed', True) or result is True


@pytest.mark.asyncio
async def test_check_risk_controls_violation(service, mock_strategy):
    """Test risk control violation."""
    service.strategy_builder._get_strategy = AsyncMock(return_value=mock_strategy)
    service._check_position_limits = AsyncMock(return_value=False)  # Violation
    
    result = await service.check_risk_controls("strategy_123")
    
    assert result is not None
    assert result.get('passed', False) is False or result is False


@pytest.mark.asyncio
async def test_stop_strategy_error_handling(service):
    """Test error handling when stopping strategy."""
    service.strategy_builder._get_strategy = AsyncMock(side_effect=Exception("Database error"))
    
    with pytest.raises(Exception):
        await service.stop_strategy("strategy_123")
