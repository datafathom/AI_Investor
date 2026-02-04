"""
Tests for Social Trading Pydantic Models
Phase 7: Model Validation Tests
"""

import pytest
from datetime import datetime
from pydantic import ValidationError
from schemas.social_trading import (
    TraderRanking,
    TraderProfile,
    CopyTradingConfig,
    CopyTrade
)


class TestTraderRankingEnum:
    """Tests for TraderRanking enum."""
    
    def test_trader_ranking_enum(self):
        """Test trader ranking enum values."""
        assert TraderRanking.BRONZE == "bronze"
        assert TraderRanking.SILVER == "silver"
        assert TraderRanking.GOLD == "gold"
        assert TraderRanking.PLATINUM == "platinum"
        assert TraderRanking.DIAMOND == "diamond"


class TestTraderProfile:
    """Tests for TraderProfile model."""
    
    def test_valid_trader_profile(self):
        """Test valid trader profile creation."""
        profile = TraderProfile(
            trader_id='trader_1',
            user_id='user_1',
            display_name='Top Trader',
            bio='Experienced trader',
            ranking=TraderRanking.GOLD,
            total_return=0.25,
            sharpe_ratio=1.8,
            win_rate=0.65,
            followers_count=100,
            is_public=True,
            created_date=datetime.now()
        )
        assert profile.trader_id == 'trader_1'
        assert profile.ranking == TraderRanking.GOLD
        assert profile.total_return == 0.25
        assert profile.sharpe_ratio == 1.8
    
    def test_trader_profile_defaults(self):
        """Test trader profile with default values."""
        profile = TraderProfile(
            trader_id='trader_1',
            user_id='user_1',
            display_name='Test Trader',
            created_date=datetime.now()
        )
        assert profile.ranking == TraderRanking.BRONZE
        assert profile.total_return == 0.0
        assert profile.is_public is True


class TestCopyTradingConfig:
    """Tests for CopyTradingConfig model."""
    
    def test_valid_copy_trading_config(self):
        """Test valid copy trading config creation."""
        config = CopyTradingConfig(
            config_id='config_1',
            follower_id='user_1',
            trader_id='trader_1',
            allocation_percentage=10.0,
            risk_multiplier=1.0,
            max_position_size=1000.0,
            is_active=True,
            created_date=datetime.now(),
            updated_date=datetime.now()
        )
        assert config.config_id == 'config_1'
        assert config.allocation_percentage == 10.0
        assert config.risk_multiplier == 1.0
    
    def test_copy_trading_config_allocation_validation(self):
        """Test copy trading config allocation percentage validation."""
        # Should fail if percentage > 100
        with pytest.raises(ValidationError):
            CopyTradingConfig(
                config_id='config_1',
                follower_id='user_1',
                trader_id='trader_1',
                allocation_percentage=150.0,
                created_date=datetime.now(),
                updated_date=datetime.now()
            )


class TestCopyTrade:
    """Tests for CopyTrade model."""
    
    def test_valid_copy_trade(self):
        """Test valid copy trade creation."""
        copy_trade = CopyTrade(
            copy_trade_id='copy_1',
            config_id='config_1',
            original_trade_id='trade_1',
            symbol='AAPL',
            quantity=10,
            price=150.0,
            executed_date=datetime.now(),
            status='executed'
        )
        assert copy_trade.copy_trade_id == 'copy_1'
        assert copy_trade.symbol == 'AAPL'
        assert copy_trade.status == 'executed'
