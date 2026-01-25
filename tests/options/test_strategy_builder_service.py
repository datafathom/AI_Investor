"""
Tests for Options Strategy Builder Service
Comprehensive test coverage for strategy creation, validation, and templates
"""

import pytest
from datetime import datetime
from unittest.mock import Mock, AsyncMock, patch
from services.options.strategy_builder_service import OptionsStrategyBuilderService
from models.options import OptionsStrategy, OptionLeg, OptionType, OptionAction


@pytest.fixture
def service():
    """Create service instance with mocked dependencies."""
    with patch('services.options.strategy_builder_service.get_cache_service'):
        return OptionsStrategyBuilderService()


@pytest.fixture
def mock_legs():
    """Mock option legs."""
    return [
        {
            'symbol': 'AAPL',
            'option_type': OptionType.CALL,
            'action': OptionAction.BUY,
            'quantity': 1,
            'strike': 150.0,
            'expiration': datetime(2024, 12, 20),
            'premium': 5.0
        }
    ]


@pytest.mark.asyncio
async def test_create_strategy_basic(service, mock_legs):
    """Test basic strategy creation."""
    service.validate_strategy = AsyncMock(return_value={'valid': True, 'errors': []})
    service._calculate_net_cost = AsyncMock(return_value=500.0)
    service._calculate_risk_reward = AsyncMock(return_value=(1000.0, -500.0, [155.0]))
    service._save_strategy = AsyncMock()
    
    result = await service.create_strategy(
        strategy_name="Test Strategy",
        underlying_symbol="AAPL",
        legs=mock_legs,
        strategy_type="custom"
    )
    
    assert result is not None
    assert isinstance(result, OptionsStrategy)
    assert result.strategy_name == "Test Strategy"
    assert result.underlying_symbol == "AAPL"
    assert len(result.legs) == 1


@pytest.mark.asyncio
async def test_create_strategy_invalid(service, mock_legs):
    """Test strategy creation with invalid strategy."""
    service.validate_strategy = AsyncMock(return_value={'valid': False, 'errors': ['Invalid leg configuration']})
    
    with pytest.raises(ValueError, match="Invalid strategy"):
        await service.create_strategy(
            strategy_name="Invalid Strategy",
            underlying_symbol="AAPL",
            legs=mock_legs
        )


@pytest.mark.asyncio
async def test_create_strategy_from_template(service):
    """Test strategy creation from template."""
    service.validate_strategy = AsyncMock(return_value={'valid': True, 'errors': []})
    service._calculate_net_cost = AsyncMock(return_value=500.0)
    service._calculate_risk_reward = AsyncMock(return_value=(1000.0, -500.0, [155.0]))
    service._save_strategy = AsyncMock()
    service._covered_call_template = Mock(return_value=[
        {'symbol': 'AAPL', 'option_type': OptionType.CALL, 'action': OptionAction.SELL, 'quantity': 1, 'strike': 150.0, 'expiration': datetime(2024, 12, 20), 'premium': 5.0}
    ])
    
    result = await service.create_strategy_from_template(
        template_name="covered_call",
        underlying_symbol="AAPL",
        stock_price=145.0,
        strike=150.0
    )
    
    assert result is not None
    assert result.strategy_type == "covered_call"


@pytest.mark.asyncio
async def test_validate_strategy(service, mock_legs):
    """Test strategy validation."""
    service._validate_legs = AsyncMock(return_value={'valid': True, 'errors': []})
    service._validate_strategy_logic = AsyncMock(return_value={'valid': True, 'errors': []})
    
    legs = [OptionLeg(**leg) for leg in mock_legs]
    result = await service.validate_strategy(legs)
    
    assert result is not None
    assert result['valid'] is True


@pytest.mark.asyncio
async def test_validate_strategy_invalid_legs(service):
    """Test strategy validation with invalid legs."""
    service._validate_legs = AsyncMock(return_value={'valid': False, 'errors': ['Invalid expiration date']})
    
    legs = [OptionLeg(
        symbol='AAPL',
        option_type=OptionType.CALL,
        action=OptionAction.BUY,
        quantity=1,
        strike=150.0,
        expiration=datetime(2023, 1, 1),  # Past date
        premium=5.0
    )]
    
    result = await service.validate_strategy(legs)
    assert result['valid'] is False
    assert len(result['errors']) > 0


@pytest.mark.asyncio
async def test_get_strategy_templates(service):
    """Test getting available strategy templates."""
    templates = service.get_strategy_templates()
    
    assert templates is not None
    assert len(templates) > 0
    assert "covered_call" in templates
    assert "protective_put" in templates


@pytest.mark.asyncio
async def test_calculate_net_cost(service, mock_legs):
    """Test net cost calculation."""
    legs = [OptionLeg(**leg) for leg in mock_legs]
    result = await service._calculate_net_cost(legs)
    
    assert result is not None
    assert isinstance(result, (int, float))


@pytest.mark.asyncio
async def test_calculate_risk_reward(service, mock_legs):
    """Test risk/reward calculation."""
    legs = [OptionLeg(**leg) for leg in mock_legs]
    max_profit, max_loss, breakeven = await service._calculate_risk_reward(legs)
    
    assert max_profit is not None
    assert max_loss is not None
    assert breakeven is not None
    assert isinstance(breakeven, list)


@pytest.mark.asyncio
async def test_create_strategy_error_handling(service):
    """Test error handling in strategy creation."""
    service.validate_strategy = AsyncMock(side_effect=Exception("Validation error"))
    
    with pytest.raises(Exception):
        await service.create_strategy(
            strategy_name="Error Strategy",
            underlying_symbol="AAPL",
            legs=[]
        )
