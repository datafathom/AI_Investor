"""
Tests for Social Trading Service
Comprehensive test coverage for trader profiles, rankings, and follow system
"""

import pytest
from datetime import datetime
from unittest.mock import Mock, AsyncMock, patch
from services.social_trading.social_trading_service import SocialTradingService
from models.social_trading import TraderProfile, TraderRanking


@pytest.fixture
def service():
    """Create service instance with mocked dependencies."""
    with patch('services.social_trading.social_trading_service.get_cache_service'):
        return SocialTradingService()


@pytest.mark.asyncio
async def test_create_trader_profile(service):
    """Test trader profile creation."""
    service._save_profile = AsyncMock()
    
    result = await service.create_trader_profile(
        user_id="user_123",
        display_name="Trader John",
        bio="Experienced trader",
        is_public=True
    )
    
    assert result is not None
    assert isinstance(result, TraderProfile)
    assert result.user_id == "user_123"
    assert result.display_name == "Trader John"
    assert result.is_public is True


@pytest.mark.asyncio
async def test_get_top_traders(service):
    """Test getting top traders leaderboard."""
    service._get_trader_rankings = AsyncMock(return_value=[
        TraderProfile(
            trader_id="trader_1",
            user_id="user_1",
            display_name="Top Trader",
            ranking=TraderRanking.PLATINUM,
            total_return=0.25,
            sharpe_ratio=2.0,
            is_public=True,
            created_date=datetime.utcnow()
        )
    ])
    
    result = await service.get_top_traders(limit=10)
    
    assert result is not None
    assert len(result) == 1
    assert result[0].ranking == TraderRanking.PLATINUM


@pytest.mark.asyncio
async def test_follow_trader(service):
    """Test following a trader."""
    service._save_follow = AsyncMock(return_value=True)
    
    result = await service.follow_trader(
        user_id="user_123",
        trader_id="trader_456"
    )
    
    assert result is True
    service._save_follow.assert_called_once()


@pytest.mark.asyncio
async def test_unfollow_trader(service):
    """Test unfollowing a trader."""
    service._remove_follow = AsyncMock(return_value=True)
    
    result = await service.unfollow_trader(
        user_id="user_123",
        trader_id="trader_456"
    )
    
    assert result is True


@pytest.mark.asyncio
async def test_get_followed_traders(service):
    """Test getting followed traders."""
    service._get_follows = AsyncMock(return_value=[
        {'trader_id': 'trader_1', 'followed_date': datetime.utcnow()},
        {'trader_id': 'trader_2', 'followed_date': datetime.utcnow()},
    ])
    
    result = await service.get_followed_traders("user_123")
    
    assert result is not None
    assert len(result) == 2
