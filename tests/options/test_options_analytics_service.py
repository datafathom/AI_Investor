"""
Tests for Options Analytics Service
Comprehensive test coverage for Greeks, P&L analysis, and probability calculations
"""

import pytest
from datetime import datetime
from unittest.mock import Mock, AsyncMock, patch
from services.options.options_analytics_service import OptionsAnalyticsService
from schemas.options import OptionsStrategy, OptionLeg, OptionType, OptionAction, StrategyGreeks, Greeks, StrategyPnL, StrategyAnalysis


@pytest.fixture
def service():
    """Create service instance with mocked dependencies."""
    with patch('services.options.options_analytics_service.get_cache_service'):
        return OptionsAnalyticsService()


@pytest.fixture
def mock_strategy():
    """Mock options strategy."""
    return OptionsStrategy(
        strategy_id="test_strategy",
        strategy_name="Test Strategy",
        strategy_type="custom",
        created_date=datetime.now(),
        underlying_symbol="AAPL",
        legs=[
            OptionLeg(
                symbol="AAPL",
                option_type=OptionType.CALL,
                action=OptionAction.BUY,
                quantity=1,
                strike=150.0,
                expiration=datetime(2024, 12, 20),
                premium=5.0
            )
        ],
        net_cost=500.0,
        max_profit=1000.0,
        max_loss=-500.0
    )


@pytest.mark.asyncio
async def test_calculate_greeks(service, mock_strategy):
    """Test Greeks calculation."""
    service._calculate_leg_greeks = AsyncMock(return_value=Greeks(
        delta=0.5,
        gamma=0.02,
        theta=-0.05,
        vega=0.15,
        rho=0.01
    ))
    
    result = await service.calculate_greeks(
        strategy=mock_strategy,
        underlying_price=145.0,
        days_to_expiration=30,
        volatility=0.20
    )
    
    assert result is not None
    assert isinstance(result, StrategyGreeks)
    assert result.strategy_id == "test_strategy"
    assert result.total_delta is not None


@pytest.mark.asyncio
async def test_calculate_pnl_analysis(service, mock_strategy):
    """Test P&L analysis calculation."""
    service._calculate_leg_value = AsyncMock(return_value=100.0)
    
    result = await service.calculate_pnl(
        strategy=mock_strategy,
        underlying_price=145.0,
        days_to_expiration=30
    )
    
    assert result is not None
    assert isinstance(result, StrategyPnL)
    assert result.profit_loss is not None


@pytest.mark.asyncio
async def test_analyze_strategy(service, mock_strategy):
    """Test full strategy analysis (covers probability and IV)."""
    service.calculate_greeks = AsyncMock(return_value=Mock(spec=StrategyGreeks))
    service.calculate_pnl = AsyncMock(return_value=Mock(spec=StrategyPnL))
    service._calculate_probability_profit = AsyncMock(return_value=0.55)
    
    result = await service.analyze_strategy(
        strategy=mock_strategy,
        underlying_price=145.0,
        days_to_expiration=30,
        volatility=0.20
    )
    
    assert result is not None
    assert isinstance(result, StrategyAnalysis)
    assert result.probability_profit == 0.55


@pytest.mark.asyncio
async def test_calculate_greeks_multiple_legs(service):
    """Test Greeks calculation with multiple legs."""
    strategy = OptionsStrategy(
        strategy_id="multi_leg",
        strategy_name="Multi Leg",
        strategy_type="condor",
        created_date=datetime.now(),
        underlying_symbol="AAPL",
        legs=[
            OptionLeg(
                symbol="AAPL", 
                option_type=OptionType.CALL, 
                action=OptionAction.BUY, 
                quantity=1, 
                strike=150.0, 
                expiration=datetime(2024, 12, 20), 
                premium=5.0
            ),
            OptionLeg(
                symbol="AAPL", 
                option_type=OptionType.CALL, 
                action=OptionAction.SELL, 
                quantity=1, 
                strike=155.0, 
                expiration=datetime(2024, 12, 20), 
                premium=3.0
            ),
        ],
        net_cost=200.0,
        max_profit=500.0,
        max_loss=-200.0
    )
    
    service._calculate_leg_greeks = AsyncMock(side_effect=[
        Greeks(delta=0.5, gamma=0.02, theta=-0.05, vega=0.15, rho=0.01),
        Greeks(delta=0.3, gamma=0.01, theta=-0.03, vega=0.10, rho=0.005),
    ])
    
    result = await service.calculate_greeks(
        strategy=strategy,
        underlying_price=145.0,
        days_to_expiration=30
    )
    
    assert result is not None
    assert len(result.leg_greeks) == 2


@pytest.mark.asyncio
async def test_calculate_greeks_error_handling(service, mock_strategy):
    """Test error handling in Greeks calculation."""
    service._calculate_leg_greeks = AsyncMock(side_effect=Exception("Calculation error"))
    
    with pytest.raises(Exception):
        await service.calculate_greeks(
            strategy=mock_strategy,
            underlying_price=145.0,
            days_to_expiration=30
        )
