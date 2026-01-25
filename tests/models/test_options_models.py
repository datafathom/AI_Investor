"""
Tests for Options Pydantic Models
Phase 7: Model Validation Tests
"""

import pytest
from datetime import datetime
from pydantic import ValidationError
from models.options import (
    OptionType,
    OptionAction,
    OptionLeg,
    OptionsStrategy,
    Greeks,
    StrategyGreeks,
    StrategyPnL,
    StrategyAnalysis
)


class TestOptionEnums:
    """Tests for option enums."""
    
    def test_option_type_enum(self):
        """Test option type enum values."""
        assert OptionType.CALL == "call"
        assert OptionType.PUT == "put"
    
    def test_option_action_enum(self):
        """Test option action enum values."""
        assert OptionAction.BUY == "buy"
        assert OptionAction.SELL == "sell"


class TestOptionLeg:
    """Tests for OptionLeg model."""
    
    def test_valid_option_leg(self):
        """Test valid option leg creation."""
        leg = OptionLeg(
            symbol="AAPL",
            option_type=OptionType.CALL,
            action=OptionAction.BUY,
            strike=150.0,
            expiration=datetime(2024, 12, 31),
            quantity=10,
            premium=5.0
        )
        assert leg.symbol == "AAPL"
        assert leg.strike == 150.0
        assert leg.quantity == 10
    
    def test_option_leg_optional_premium(self):
        """Test option leg without premium."""
        leg = OptionLeg(
            symbol="AAPL",
            option_type=OptionType.CALL,
            action=OptionAction.BUY,
            strike=150.0,
            expiration=datetime(2024, 12, 31),
            quantity=10
        )
        assert leg.premium is None


class TestOptionsStrategy:
    """Tests for OptionsStrategy model."""
    
    def test_valid_options_strategy(self):
        """Test valid options strategy creation."""
        strategy = OptionsStrategy(
            strategy_id="strategy_1",
            strategy_name="Covered Call",
            underlying_symbol="AAPL",
            legs=[],
            net_cost=500.0,
            max_profit=1000.0,
            max_loss=-500.0,
            breakeven_points=[145.0, 155.0],
            created_date=datetime.now(),
            strategy_type="covered_call"
        )
        assert strategy.strategy_id == "strategy_1"
        assert strategy.net_cost == 500.0
        assert strategy.max_profit == 1000.0


class TestGreeks:
    """Tests for Greeks model."""
    
    def test_valid_greeks(self):
        """Test valid Greeks creation."""
        greeks = Greeks(
            delta=0.5,
            gamma=0.02,
            theta=-0.01,
            vega=0.15,
            rho=0.05
        )
        assert greeks.delta == 0.5
        assert greeks.gamma == 0.02
        assert greeks.theta == -0.01
    
    def test_greeks_optional_rho(self):
        """Test Greeks without rho."""
        greeks = Greeks(
            delta=0.5,
            gamma=0.02,
            theta=-0.01,
            vega=0.15
        )
        assert greeks.rho is None


class TestStrategyGreeks:
    """Tests for StrategyGreeks model."""
    
    def test_valid_strategy_greeks(self):
        """Test valid strategy Greeks creation."""
        strategy_greeks = StrategyGreeks(
            strategy_id="strategy_1",
            total_delta=0.5,
            total_gamma=0.02,
            total_theta=-0.01,
            total_vega=0.15,
            leg_greeks={}
        )
        assert strategy_greeks.strategy_id == "strategy_1"
        assert strategy_greeks.total_delta == 0.5


class TestStrategyPnL:
    """Tests for StrategyPnL model."""
    
    def test_valid_strategy_pnl(self):
        """Test valid strategy P&L creation."""
        pnl = StrategyPnL(
            strategy_id="strategy_1",
            underlying_price=150.0,
            days_to_expiration=30,
            profit_loss=100.0,
            profit_loss_pct=0.1,
            intrinsic_value=50.0,
            time_value=50.0
        )
        assert pnl.strategy_id == "strategy_1"
        assert pnl.profit_loss == 100.0
