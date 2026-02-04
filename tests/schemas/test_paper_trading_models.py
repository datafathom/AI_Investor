"""
Tests for Paper Trading Pydantic Models
Phase 7: Model Validation Tests
"""

import pytest
from datetime import datetime
from pydantic import ValidationError
from schemas.paper_trading import (
    PaperOrder,
    VirtualPortfolio,
    SimulationResult
)


class TestPaperOrder:
    """Tests for PaperOrder model."""
    
    def test_valid_paper_order(self):
        """Test valid paper order creation."""
        order = PaperOrder(
            order_id='order_1',
            user_id='user_1',
            symbol='AAPL',
            quantity=100,
            order_type='market',
            price=None,
            status='pending',
            filled_price=None,
            filled_quantity=0,
            commission=0.0,
            slippage=0.0,
            created_date=datetime.now()
        )
        assert order.order_id == 'order_1'
        assert order.symbol == 'AAPL'
        assert order.quantity == 100
        assert order.order_type == 'market'
    
    def test_paper_order_with_limit_price(self):
        """Test paper order with limit price."""
        order = PaperOrder(
            order_id='order_1',
            user_id='user_1',
            symbol='AAPL',
            quantity=100,
            order_type='limit',
            price=150.0,
            status='pending',
            filled_price=None,
            filled_quantity=0,
            commission=0.0,
            slippage=0.0,
            created_date=datetime.now()
        )
        assert order.price == 150.0
        assert order.order_type == 'limit'


class TestVirtualPortfolio:
    """Tests for VirtualPortfolio model."""
    
    def test_valid_virtual_portfolio(self):
        """Test valid virtual portfolio creation."""
        portfolio = VirtualPortfolio(
            portfolio_id='portfolio_1',
            user_id='user_1',
            portfolio_name='Paper Trading Portfolio',
            initial_cash=100000.0,
            current_cash=95000.0,
            total_value=100000.0,
            positions={},
            created_date=datetime.now(),
            updated_date=datetime.now()
        )
        assert portfolio.portfolio_id == 'portfolio_1'
        assert portfolio.initial_cash == 100000.0
        assert portfolio.current_cash == 95000.0
    
    def test_virtual_portfolio_with_positions(self):
        """Test virtual portfolio with positions."""
        positions = {
            'AAPL': {
                'quantity': 100,
                'avg_price': 150.0,
                'current_price': 155.0
            }
        }
        portfolio = VirtualPortfolio(
            portfolio_id='portfolio_1',
            user_id='user_1',
            portfolio_name='Paper Trading Portfolio',
            initial_cash=100000.0,
            current_cash=85000.0,
            total_value=100500.0,
            positions=positions,
            created_date=datetime.now(),
            updated_date=datetime.now()
        )
        assert len(portfolio.positions) == 1
        assert portfolio.positions['AAPL']['quantity'] == 100


class TestSimulationResult:
    """Tests for SimulationResult model."""
    
    def test_valid_simulation_result(self):
        """Test valid simulation result creation."""
        result = SimulationResult(
            simulation_id='sim_1',
            strategy_name='Test Strategy',
            start_date=datetime(2024, 1, 1),
            end_date=datetime(2024, 12, 31),
            initial_capital=100000.0,
            final_capital=115000.0,
            total_return=0.15,
            sharpe_ratio=1.5,
            max_drawdown=0.05,
            win_rate=0.6,
            trades=[]
        )
        assert result.simulation_id == 'sim_1'
        assert result.total_return == 0.15
        assert result.sharpe_ratio == 1.5
        assert result.win_rate == 0.6
