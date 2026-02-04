"""
Tests for Strategy Pydantic Models
Phase 7: Model Validation Tests
"""

import pytest
from datetime import datetime
from pydantic import ValidationError
from schemas.strategy import (
    StrategyStatus,
    ConditionType,
    StrategyRule,
    TradingStrategy,
    StrategyExecution,
    StrategyPerformance
)


class TestStrategyEnums:
    """Tests for strategy enums."""
    
    def test_strategy_status_enum(self):
        """Test strategy status enum values."""
        assert StrategyStatus.DRAFT == "draft"
        assert StrategyStatus.ACTIVE == "active"
        assert StrategyStatus.PAUSED == "paused"
        assert StrategyStatus.STOPPED == "stopped"
    
    def test_condition_type_enum(self):
        """Test condition type enum values."""
        assert ConditionType.PRICE == "price"
        assert ConditionType.VOLUME == "volume"
        assert ConditionType.INDICATOR == "indicator"


class TestStrategyRule:
    """Tests for StrategyRule model."""
    
    def test_valid_strategy_rule(self):
        """Test valid strategy rule creation."""
        rule = StrategyRule(
            rule_id="rule_1",
            condition_type=ConditionType.PRICE,
            condition={"symbol": "AAPL", "operator": ">", "value": 150.0},
            action={"type": "buy", "quantity": 10},
            priority=1
        )
        assert rule.rule_id == "rule_1"
        assert rule.condition_type == ConditionType.PRICE
        assert rule.priority == 1
    
    def test_strategy_rule_default_priority(self):
        """Test strategy rule with default priority."""
        rule = StrategyRule(
            rule_id="rule_1",
            condition_type=ConditionType.PRICE,
            condition={},
            action={}
        )
        assert rule.priority == 0


class TestTradingStrategy:
    """Tests for TradingStrategy model."""
    
    def test_valid_trading_strategy(self):
        """Test valid trading strategy creation."""
        strategy = TradingStrategy(
            strategy_id="strategy_1",
            user_id="user_1",
            strategy_name="Test Strategy",
            description="Test description",
            rules=[],
            status=StrategyStatus.DRAFT,
            risk_limits={"max_loss": 1000.0},
            created_date=datetime.now(),
            updated_date=datetime.now()
        )
        assert strategy.strategy_id == "strategy_1"
        assert strategy.status == StrategyStatus.DRAFT


class TestStrategyExecution:
    """Tests for StrategyExecution model."""
    
    def test_valid_strategy_execution(self):
        """Test valid strategy execution creation."""
        execution = StrategyExecution(
            execution_id="exec_1",
            strategy_id="strategy_1",
            rule_id="rule_1",
            action_taken="buy",
            order_id="order_1",
            execution_time=datetime.now(),
            result="success"
        )
        assert execution.execution_id == "exec_1"
        assert execution.result == "success"


class TestStrategyPerformance:
    """Tests for StrategyPerformance model."""
    
    def test_valid_strategy_performance(self):
        """Test valid strategy performance creation."""
        performance = StrategyPerformance(
            strategy_id="strategy_1",
            total_trades=100,
            winning_trades=60,
            losing_trades=40,
            win_rate=0.6,
            total_pnl=5000.0,
            sharpe_ratio=1.5,
            max_drawdown=0.1,
            current_status=StrategyStatus.ACTIVE
        )
        assert performance.strategy_id == "strategy_1"
        assert performance.win_rate == 0.6
        assert performance.total_pnl == 5000.0
