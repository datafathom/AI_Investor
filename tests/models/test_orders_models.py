"""
Tests for Orders Pydantic Models
Phase 7: Model Validation Tests
"""

import pytest
from datetime import datetime
from pydantic import ValidationError
from models.orders import (
    OrderType,
    OrderStatus,
    TrailingStopOrder,
    BracketOrder,
    ConditionalOrder,
    ExecutionStrategy,
    ExecutionResult
)


class TestOrderEnums:
    """Tests for order enums."""
    
    def test_order_type_enum(self):
        """Test order type enum values."""
        assert OrderType.MARKET == "market"
        assert OrderType.LIMIT == "limit"
        assert OrderType.STOP == "stop"
        assert OrderType.TRAILING_STOP == "trailing_stop"
        assert OrderType.BRACKET == "bracket"
        assert OrderType.OCO == "oco"
    
    def test_order_status_enum(self):
        """Test order status enum values."""
        assert OrderStatus.PENDING == "pending"
        assert OrderStatus.FILLED == "filled"
        assert OrderStatus.CANCELLED == "cancelled"
        assert OrderStatus.REJECTED == "rejected"
    
    def test_execution_strategy_enum(self):
        """Test execution strategy enum values."""
        assert ExecutionStrategy.MARKET == "market"
        assert ExecutionStrategy.TWAP == "twap"
        assert ExecutionStrategy.VWAP == "vwap"
        assert ExecutionStrategy.IS == "implementation_shortfall"
        assert ExecutionStrategy.ICEBERG == "iceberg"


class TestTrailingStopOrder:
    """Tests for TrailingStopOrder model."""
    
    def test_valid_trailing_stop_order(self):
        """Test valid trailing stop order creation."""
        order = TrailingStopOrder(
            order_id='order_1',
            symbol='AAPL',
            quantity=100,
            trailing_type='percentage',
            trailing_value=5.0,
            initial_stop_price=145.0,
            current_stop_price=147.0,
            highest_price=150.0
        )
        assert order.order_id == 'order_1'
        assert order.trailing_type == 'percentage'
        assert order.trailing_value == 5.0


class TestBracketOrder:
    """Tests for BracketOrder model."""
    
    def test_valid_bracket_order(self):
        """Test valid bracket order creation."""
        bracket = BracketOrder(
            bracket_id='bracket_1',
            entry_order_id='entry_1',
            profit_target_order_id='profit_1',
            stop_loss_order_id='stop_1',
            profit_target_price=160.0,
            stop_loss_price=140.0
        )
        assert bracket.bracket_id == 'bracket_1'
        assert bracket.profit_target_price == 160.0
        assert bracket.stop_loss_price == 140.0


class TestConditionalOrder:
    """Tests for ConditionalOrder model."""
    
    def test_valid_conditional_order(self):
        """Test valid conditional order creation."""
        order = ConditionalOrder(
            order_id='order_1',
            symbol='AAPL',
            quantity=100,
            order_type='market',
            condition_type='price',
            condition_value=150.0,
            triggered=False
        )
        assert order.order_id == 'order_1'
        assert order.condition_type == 'price'
        assert order.condition_value == 150.0
        assert order.triggered is False


class TestExecutionResult:
    """Tests for ExecutionResult model."""
    
    def test_valid_execution_result(self):
        """Test valid execution result creation."""
        result = ExecutionResult(
            execution_id='exec_1',
            order_id='order_1',
            filled_quantity=100,
            average_price=150.0,
            execution_time=datetime.now(),
            execution_strategy='twap',
            market_impact=0.001
        )
        assert result.execution_id == 'exec_1'
        assert result.filled_quantity == 100
        assert result.average_price == 150.0
        assert result.execution_strategy == 'twap'
