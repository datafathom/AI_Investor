"""
==============================================================================
Unit Tests - PortfolioManager
==============================================================================
Tests the dual-portfolio management system.
==============================================================================
"""
import pytest

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.portfolio_manager import (
    PortfolioManager, PortfolioType, ConvictionLevel, Position, Portfolio
)


class TestPortfolioManager:
    """Test suite for PortfolioManager dual-portfolio system."""
    
    def test_initialization(self) -> None:
        """Test PortfolioManager initializes with correct allocations."""
        pm = PortfolioManager(total_capital=100000, defensive_allocation=0.60)
        
        assert pm.defensive.cash == 60000
        assert pm.aggressive.cash == 40000
        assert pm.get_combined_value() == 100000
    
    def test_custom_allocation(self) -> None:
        """Test custom defensive/aggressive split."""
        pm = PortfolioManager(total_capital=100000, defensive_allocation=0.70)
        
        assert pm.defensive.cash == 70000
        assert pm.aggressive.cash == 30000
    
    def test_add_defensive_position(self) -> None:
        """Test adding a position to defensive portfolio."""
        pm = PortfolioManager(total_capital=100000)
        
        result = pm.add_position(
            portfolio_type=PortfolioType.DEFENSIVE,
            symbol='VXX',
            quantity=10,
            price=20.0
        )
        
        assert result['success'] is True
        assert len(pm.defensive.positions) == 1
        assert pm.defensive.cash == 60000 - 200
    
    def test_add_aggressive_position(self) -> None:
        """Test adding a position to aggressive portfolio."""
        pm = PortfolioManager(total_capital=100000)
        
        result = pm.add_position(
            portfolio_type=PortfolioType.AGGRESSIVE,
            symbol='NVDA',
            quantity=5,
            price=500.0,
            conviction=ConvictionLevel.HIGH
        )
        
        assert result['success'] is True
        assert len(pm.aggressive.positions) == 1
    
    def test_insufficient_cash(self) -> None:
        """Test rejection when insufficient cash."""
        pm = PortfolioManager(total_capital=10000)
        
        result = pm.add_position(
            portfolio_type=PortfolioType.AGGRESSIVE,
            symbol='NVDA',
            quantity=100,
            price=500.0
        )
        
        assert result['success'] is False
        assert 'Insufficient' in result['reason']
    
    def test_add_sure_thing(self) -> None:
        """Test adding a sure-thing leveraged play."""
        pm = PortfolioManager(total_capital=100000)
        
        result = pm.add_sure_thing(
            symbol='NVDA',
            thesis='CUDA moat for AI/ML market',
            capital_percentage=0.10,
            leverage=2.0
        )
        
        assert result['success'] is True
        assert result['position']['conviction'] == 'SURE_THING'
        assert result['position']['leverage'] == 2.0
    
    def test_add_hedge(self) -> None:
        """Test adding a hedging position."""
        pm = PortfolioManager(total_capital=100000)
        
        result = pm.add_hedge(
            symbol='VXX',
            hedge_type='VIX_CALL',
            quantity=50,
            price=20.0
        )
        
        assert result['success'] is True
        assert 'Hedge' in pm.defensive.positions[0].thesis
    
    def test_combined_pnl(self) -> None:
        """Test combined P&L calculation."""
        pm = PortfolioManager(total_capital=100000)
        
        # Add position and simulate price change
        pm.add_position(
            portfolio_type=PortfolioType.AGGRESSIVE,
            symbol='NVDA',
            quantity=10,
            price=100.0
        )
        
        # Update price (simulated gain)
        pm.aggressive.positions[0].current_price = 110.0
        
        assert pm.get_combined_pnl() == 100.0  # 10 shares * $10 gain
    
    def test_rebalance_check(self) -> None:
        """Test rebalance detection."""
        pm = PortfolioManager(total_capital=100000)
        
        rebalance = pm.rebalance()
        
        assert 'action' in rebalance
        assert 'current' in rebalance
        assert 'target' in rebalance
    
    def test_portfolio_summary(self) -> None:
        """Test summary includes all required fields."""
        pm = PortfolioManager(total_capital=100000)
        
        summary = pm.get_summary()
        
        assert 'total_value' in summary
        assert 'defensive' in summary
        assert 'aggressive' in summary
        assert summary['defensive']['value'] == 60000
        assert summary['aggressive']['value'] == 40000


class TestPosition:
    """Test suite for Position dataclass."""
    
    def test_market_value(self) -> None:
        """Test market value calculation."""
        pos = Position(
            symbol='NVDA',
            quantity=10,
            entry_price=100.0,
            current_price=110.0,
            portfolio_type=PortfolioType.AGGRESSIVE
        )
        
        assert pos.market_value == 1100.0
    
    def test_pnl_calculation(self) -> None:
        """Test P&L calculation."""
        pos = Position(
            symbol='NVDA',
            quantity=10,
            entry_price=100.0,
            current_price=120.0,
            portfolio_type=PortfolioType.AGGRESSIVE
        )
        
        assert pos.pnl == 200.0
        assert pos.pnl_percent == 0.2
