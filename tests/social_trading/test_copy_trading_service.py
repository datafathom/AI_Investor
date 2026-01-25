"""
Tests for Copy Trading Service
Comprehensive test coverage for copy trading configuration and execution
"""

import pytest
from datetime import datetime
from unittest.mock import Mock, AsyncMock, patch
from services.social_trading.copy_trading_service import CopyTradingService
from models.social_trading import CopyTradingConfig, CopyTrade


@pytest.fixture
def service():
    """Create service instance with mocked dependencies."""
    with patch('services.social_trading.copy_trading_service.get_social_trading_service'), \
         patch('services.social_trading.copy_trading_service.get_cache_service'):
        return CopyTradingService()


@pytest.mark.asyncio
async def test_create_copy_config(service):
    """Test copy trading configuration creation."""
    service._save_config = AsyncMock()
    
    result = await service.create_copy_config(
        follower_id="user_123",
        trader_id="trader_456",
        allocation_percentage=0.2,
        risk_multiplier=1.0
    )
    
    assert result is not None
    assert isinstance(result, CopyTradingConfig)
    assert result.follower_id == "user_123"
    assert result.trader_id == "trader_456"
    assert result.allocation_percentage == 0.2
    assert result.is_active is True


@pytest.mark.asyncio
async def test_execute_copy_trade(service):
    """Test executing a copy trade."""
    config = CopyTradingConfig(
        config_id="config_123",
        follower_id="user_123",
        trader_id="trader_456",
        allocation_percentage=0.2,
        risk_multiplier=1.0,
        is_active=True,
        created_date=datetime.utcnow(),
        updated_date=datetime.utcnow()
    )
    
    service.active_configs["config_123"] = config
    service._get_trader_trade = AsyncMock(return_value={
        'symbol': 'AAPL',
        'action': 'buy',
        'quantity': 100,
        'price': 150.0
    })
    service._execute_follower_trade = AsyncMock(return_value={
        'trade_id': 'trade_123',
        'status': 'filled'
    })
    service._record_copy_trade = AsyncMock()
    
    result = await service.execute_copy_trade(
        config_id="config_123",
        trader_trade_id="trader_trade_123"
    )
    
    assert result is not None
    assert isinstance(result, CopyTrade) or isinstance(result, dict)


@pytest.mark.asyncio
async def test_stop_copy_trading(service):
    """Test stopping copy trading."""
    config = CopyTradingConfig(
        config_id="config_123",
        follower_id="user_123",
        trader_id="trader_456",
        allocation_percentage=0.2,
        risk_multiplier=1.0,
        is_active=True,
        created_date=datetime.utcnow(),
        updated_date=datetime.utcnow()
    )
    
    service.active_configs["config_123"] = config
    service._get_config = AsyncMock(return_value=config)
    service._save_config = AsyncMock()
    
    result = await service.stop_copy_trading("config_123")
    
    assert result is not None
    assert result.is_active is False
    assert "config_123" not in service.active_configs
