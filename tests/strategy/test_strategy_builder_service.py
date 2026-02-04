"""
Tests for Strategy Builder Service
Comprehensive test coverage for strategy creation, rules, and validation
"""

import pytest
from datetime import timezone, datetime
from unittest.mock import Mock, AsyncMock, patch
from services.strategy.strategy_builder_service import StrategyBuilderService
from schemas.strategy import TradingStrategy, StrategyRule, StrategyStatus


@pytest.fixture
def service():
    """Create service instance with mocked dependencies."""
    with patch('services.strategy.strategy_builder_service.get_cache_service'):
        return StrategyBuilderService()


@pytest.fixture
def mock_rules():
    """Mock strategy rules."""
    return [
        {
            'condition_type': 'price',
            'condition': {'symbol': 'AAPL', 'operator': '>', 'value': 150.0},
            'action': {'type': 'buy', 'quantity': 100}
        }
    ]


@pytest.mark.asyncio
async def test_create_strategy(service, mock_rules):
    """Test strategy creation."""
    service._save_strategy = AsyncMock()
    
    result = await service.create_strategy(
        user_id="user_123",
        strategy_name="Test Strategy",
        description="Test description",
        rules=mock_rules
    )
    
    assert result is not None
    assert isinstance(result, TradingStrategy)
    assert result.user_id == "user_123"
    assert result.strategy_name == "Test Strategy"
    assert result.status == StrategyStatus.DRAFT
    assert len(result.rules) == 1


@pytest.mark.asyncio
async def test_create_strategy_no_rules(service):
    """Test strategy creation without rules."""
    service._save_strategy = AsyncMock()
    
    result = await service.create_strategy(
        user_id="user_123",
        strategy_name="Empty Strategy"
    )
    
    assert result is not None
    assert len(result.rules) == 0


@pytest.mark.asyncio
async def test_add_rule(service):
    """Test adding rule to strategy."""
    strategy = TradingStrategy(
        strategy_id="strategy_123",
        user_id="user_123",
        strategy_name="Test Strategy",
        rules=[],
        status=StrategyStatus.DRAFT,
        created_date=datetime.now(timezone.utc),
        updated_date=datetime.now(timezone.utc)
    )
    
    service._get_strategy = AsyncMock(return_value=strategy)
    service._save_strategy = AsyncMock()
    
    result = await service.add_rule(
        strategy_id="strategy_123",
        condition_type="price",
        condition={'symbol': 'AAPL', 'operator': '>', 'value': 150.0},
        action={'type': 'buy', 'quantity': 100},
        priority=1
    )
    
    assert result is not None
    assert isinstance(result, StrategyRule)
    assert result.condition_type == "price"


@pytest.mark.asyncio
async def test_validate_strategy(service):
    """Test strategy validation."""
    strategy = TradingStrategy(
        strategy_id="strategy_123",
        user_id="user_123",
        strategy_name="Test Strategy",
        rules=[
            StrategyRule(
                rule_id="rule_1",
                condition_type="price",
                condition={'symbol': 'AAPL', 'operator': '>', 'value': 150.0},
                action={'type': 'buy', 'quantity': 100}
            )
        ],
        status=StrategyStatus.DRAFT,
        created_date=datetime.now(timezone.utc),
        updated_date=datetime.now(timezone.utc)
    )
    
    service._get_strategy = AsyncMock(return_value=strategy)
    service._validate_rules = AsyncMock(return_value={'valid': True, 'errors': []})
    service._validate_risk_controls = AsyncMock(return_value={'valid': True, 'errors': []})
    
    result = await service.validate_strategy("strategy_123")
    
    assert result is not None
    assert result['valid'] is True


@pytest.mark.asyncio
async def test_validate_strategy_invalid(service):
    """Test strategy validation with invalid rules."""
    strategy = TradingStrategy(
        strategy_id="strategy_123",
        user_id="user_123",
        strategy_name="Test Strategy",
        rules=[],
        status=StrategyStatus.DRAFT,
        created_date=datetime.now(timezone.utc),
        updated_date=datetime.now(timezone.utc)
    )
    
    service._get_strategy = AsyncMock(return_value=strategy)
    service._validate_rules = AsyncMock(return_value={'valid': False, 'errors': ['No rules defined']})
    
    result = await service.validate_strategy("strategy_123")
    
    assert result is not None
    assert result['valid'] is False
    assert len(result['errors']) > 0


@pytest.mark.asyncio
async def test_get_strategy_templates(service):
    """Test getting strategy templates."""
    templates = service.get_strategy_templates()
    
    assert templates is not None
    assert len(templates) > 0


@pytest.mark.asyncio
async def test_create_strategy_from_template(service):
    """Test creating strategy from template."""
    service._save_strategy = AsyncMock()
    service._get_template = Mock(return_value={
        'name': 'Momentum Strategy',
        'rules': [
            {'condition_type': 'price', 'condition': {}, 'action': {}}
        ]
    })
    
    result = await service.create_strategy_from_template(
        user_id="user_123",
        template_name="momentum",
        parameters={'symbol': 'AAPL'}
    )
    
    assert result is not None
    assert isinstance(result, TradingStrategy)


@pytest.mark.asyncio
async def test_add_rule_error_handling(service):
    """Test error handling when adding rule."""
    service._get_strategy = AsyncMock(return_value=None)
    
    with pytest.raises(ValueError, match="not found"):
        await service.add_rule(
            strategy_id="nonexistent",
            condition_type="price",
            condition={},
            action={}
        )


@pytest.mark.asyncio
async def test_create_strategy_error_handling(service):
    """Test error handling in strategy creation."""
    service._save_strategy = AsyncMock(side_effect=Exception("Database error"))
    
    with pytest.raises(Exception):
        await service.create_strategy(
            user_id="user_123",
            strategy_name="Error Strategy"
        )
