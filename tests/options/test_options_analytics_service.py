"""
Tests for Options Analytics Service
Comprehensive test coverage for Greeks, P&L analysis, and probability calculations
"""

import pytest
from datetime import datetime
from unittest.mock import Mock, AsyncMock, patch
from services.options.options_analytics_service import OptionsAnalyticsService
from models.options import OptionsStrategy, OptionLeg, OptionType, OptionAction, StrategyGreeks


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
    service._calculate_leg_greeks = AsyncMock(return_value=Mock(
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
    service._calculate_pnl_at_price = AsyncMock(return_value=100.0)
    
    result = await service.calculate_pnl_analysis(
        strategy=mock_strategy,
        underlying_price=145.0,
        days_to_expiration=30
    )
    
    assert result is not None
    assert 'pnl_at_expiration' in result or hasattr(result, 'pnl_at_expiration')


@pytest.mark.asyncio
async def test_calculate_probability(service, mock_strategy):
    """Test probability calculation."""
    service._calculate_probability_itm = AsyncMock(return_value=0.35)
    service._calculate_probability_profit = AsyncMock(return_value=0.25)
    
    result = await service.calculate_probability(
        strategy=mock_strategy,
        underlying_price=145.0,
        days_to_expiration=30,
        target_price=150.0
    )
    
    assert result is not None
    assert 'probability_itm' in result or hasattr(result, 'probability_itm')


@pytest.mark.asyncio
async def test_calculate_implied_volatility(service, mock_strategy):
    """Test implied volatility calculation."""
    service._calculate_iv = AsyncMock(return_value=0.22)
    
    result = await service.calculate_implied_volatility(
        strategy=mock_strategy,
        underlying_price=145.0,
        market_price=5.0
    )
    
    assert result is not None
    assert isinstance(result, (int, float))


@pytest.mark.asyncio
async def test_calculate_greeks_multiple_legs(service):
    """Test Greeks calculation with multiple legs."""
    strategy = OptionsStrategy(
        strategy_id="multi_leg",
        strategy_name="Multi Leg",
        underlying_symbol="AAPL",
        legs=[
            OptionLeg("AAPL", OptionType.CALL, OptionAction.BUY, 1, 150.0, datetime(2024, 12, 20), 5.0),
            OptionLeg("AAPL", OptionType.CALL, OptionAction.SELL, 1, 155.0, datetime(2024, 12, 20), 3.0),
        ],
        net_cost=200.0,
        max_profit=500.0,
        max_loss=-200.0
    )
    
    service._calculate_leg_greeks = AsyncMock(side_effect=[
        Mock(delta=0.5, gamma=0.02, theta=-0.05, vega=0.15, rho=0.01),
        Mock(delta=0.3, gamma=0.01, theta=-0.03, vega=0.10, rho=0.005),
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
