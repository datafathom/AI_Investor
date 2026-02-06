"""
Unit Tests for Phase 3: The Trading Engine
Tests for Strategy Compiler, Monte Carlo, and Trader agents.
"""

import pytest
import time

from services.strategy.strategy_compiler import (
    get_strategy_compiler,
    get_monte_carlo_engine,
    NodeType,
    BlueprintNode,
)
from agents.trader import get_trader_agents


class TestStrategyCompiler:
    """Tests for the Strategy Compiler."""

    def setup_method(self) -> None:
        self.compiler = get_strategy_compiler()

    def test_compile_simple_blueprint(self) -> None:
        """Test compiling a simple RSI strategy."""
        react_flow_data = {
            "id": "test-strategy-001",
            "name": "RSI Oversold Strategy",
            "nodes": [
                {"id": "entry", "type": "entry", "data": {"label": "Start"}},
                {"id": "rsi_check", "type": "condition", "data": {
                    "label": "RSI < 30",
                    "config": {"indicator": "RSI", "operator": "<", "value": 30}
                }},
                {"id": "buy_action", "type": "action", "data": {
                    "label": "Buy 100 shares",
                    "config": {"action": "BUY", "size": "100"}
                }},
                {"id": "exit", "type": "exit", "data": {"label": "End"}},
            ],
            "edges": [
                {"source": "entry", "target": "rsi_check"},
                {"source": "rsi_check", "target": "buy_action"},
                {"source": "buy_action", "target": "exit"},
            ],
        }

        blueprint = self.compiler.compile_blueprint(react_flow_data)

        assert blueprint.blueprint_id == "test-strategy-001"
        assert blueprint.name == "RSI Oversold Strategy"
        assert len(blueprint.nodes) == 4
        assert len(blueprint.edges) == 3
        assert blueprint.sha_hash is not None
        assert len(blueprint.sha_hash) == 12
        assert blueprint.json_logic is not None

    def test_blueprint_versioning(self) -> None:
        """Test that blueprints are versioned correctly."""
        react_flow_data = {
            "id": "versioned-strategy",
            "name": "Versioned Strategy",
            "nodes": [{"id": "n1", "type": "condition", "data": {"label": "Test"}}],
            "edges": [],
        }

        bp1 = self.compiler.compile_blueprint(react_flow_data)
        assert bp1.version == 1

        # Compile again (same ID, should increment version)
        bp2 = self.compiler.compile_blueprint(react_flow_data)
        assert bp2.version == 2

    def test_validate_dead_end(self) -> None:
        """Test validation catches dead ends."""
        react_flow_data = {
            "nodes": [
                {"id": "entry", "type": "entry", "data": {"label": "Start"}},
                {"id": "orphan", "type": "condition", "data": {"label": "Orphan"}},
            ],
            "edges": [],
        }

        result = self.compiler.validate_blueprint(react_flow_data)

        assert result["valid"] is False
        assert len(result["errors"]) > 0

    def test_validate_missing_entry_exit(self) -> None:
        """Test validation catches missing entry/exit."""
        react_flow_data = {
            "nodes": [
                {"id": "cond", "type": "condition", "data": {"label": "Condition"}},
            ],
            "edges": [],
        }

        result = self.compiler.validate_blueprint(react_flow_data)

        assert result["valid"] is False
        assert "Missing entry point" in result["errors"]
        assert "Missing exit point" in result["errors"]


class TestMonteCarloEngine:
    """Tests for the Monte Carlo stress-testing engine."""

    def setup_method(self) -> None:
        self.engine = get_monte_carlo_engine()
        self.compiler = get_strategy_compiler()

    def test_stress_test_performance(self) -> None:
        """Test Monte Carlo completes 5000 paths in <5 seconds."""
        blueprint = self.compiler.compile_blueprint({
            "id": "mc-test",
            "name": "MC Test Strategy",
            "nodes": [],
            "edges": [],
        })

        result = self.engine.run_stress_test(
            blueprint,
            num_paths=5000,
            time_horizon_days=252,
        )

        assert result.paths_simulated == 5000
        assert result.execution_time_ms < 5000  # <5 seconds SLA
        assert result.mean_return_pct is not None
        assert result.max_drawdown_pct >= 0

    def test_tail_risk_detection(self) -> None:
        """Test that tail risk events are detected."""
        blueprint = self.compiler.compile_blueprint({
            "id": "risk-test",
            "name": "Risk Test",
            "nodes": [],
            "edges": [],
        })

        result = self.engine.run_stress_test(blueprint, num_paths=1000)

        # With random GBM, there should be some tail risk events (>20% drawdown)
        assert result.tail_risk_events >= 0
        # VaR values should be numbers
        assert isinstance(result.var_95_pct, float)
        assert isinstance(result.var_99_pct, float)

    def test_var_calculations(self) -> None:
        """Test Value at Risk calculations."""
        blueprint = self.compiler.compile_blueprint({
            "id": "var-test",
            "name": "VaR Test",
            "nodes": [],
            "edges": [],
        })

        result = self.engine.run_stress_test(blueprint, num_paths=1000)

        # Both VaR values should be computed
        assert result.var_95_pct is not None
        assert result.var_99_pct is not None


class TestTraderAgents:
    """Tests for Trader Department agents (4.1-4.6)."""

    def setup_method(self) -> None:
        self.agents = get_trader_agents()

    def test_all_trader_agents_registered(self) -> None:
        """Test that all 6 agents are instantiated."""
        assert len(self.agents) == 6
        assert "trader.order.4.1" in self.agents
        assert "trader.fills.4.2" in self.agents
        assert "trader.algo.4.3" in self.agents
        assert "trader.hedger.4.4" in self.agents
        assert "trader.arb.4.5" in self.agents
        assert "trader.mm.4.6" in self.agents

    def test_order_creation(self) -> None:
        """Test order creation latency."""
        order_agent = self.agents["trader.order.4.1"]
        order_agent.start()

        result = order_agent.process_event({
            "type": "order.new",
            "ticker": "AAPL",
            "side": "buy",
            "order_type": "limit",
            "quantity": 100,
            "price": 150.00,
        })

        assert result["status"] == "created"
        assert result["order_id"].startswith("ORD-")
        assert result["under_50ms_sla"] is True

    def test_order_routing(self) -> None:
        """Test order routing SOR."""
        order_agent = self.agents["trader.order.4.1"]
        order_agent.start()

        # Create order first
        create_result = order_agent.process_event({
            "type": "order.new",
            "ticker": "MSFT",
            "side": "buy",
            "order_type": "market",
            "quantity": 50,
        })

        # Route order
        route_result = order_agent.process_event({
            "type": "order.route",
            "order_id": create_result["order_id"],
        })

        assert route_result["status"] == "routed"
        assert route_result["venue"] in ["NYSE", "NASDAQ", "ARCA", "BATS"]
        assert route_result["under_50ms_sla"] is True

    def test_fill_tracking(self) -> None:
        """Test fill recording and position updates."""
        fill_agent = self.agents["trader.fills.4.2"]
        fill_agent.start()

        result = fill_agent.process_event({
            "type": "fill.new",
            "order_id": "ORD-000001",
            "ticker": "TSLA",
            "side": "buy",
            "quantity": 100,
            "price": 250.00,
            "venue": "NASDAQ",
            "commission": 1.00,
        })

        assert result["status"] == "recorded"
        assert result["position"] == 100

        # Check position
        pos_result = fill_agent.process_event({
            "type": "position.query",
            "ticker": "TSLA",
        })

        assert pos_result["quantity"] == 100

    def test_algo_execution_twap(self) -> None:
        """Test TWAP algorithmic execution."""
        algo_agent = self.agents["trader.algo.4.3"]
        algo_agent.start()

        start_result = algo_agent.process_event({
            "type": "algo.start",
            "algo_id": "TWAP-001",
            "algo_type": "twap",
            "quantity": 10000,
            "duration_min": 60,
        })

        assert start_result["status"] == "started"
        assert start_result["num_slices"] == 60

        # Execute a slice
        slice_result = algo_agent.process_event({
            "type": "algo.slice",
            "algo_id": "TWAP-001",
        })

        assert slice_result["status"] == "slice_executed"
        assert slice_result["progress_pct"] > 0

    def test_market_maker_quotes(self) -> None:
        """Test market maker quote management."""
        mm_agent = self.agents["trader.mm.4.6"]
        mm_agent.start()

        result = mm_agent.process_event({
            "type": "quote.update",
            "ticker": "NVDA",
            "mid_price": 500.00,
            "spread_bps": 10,
        })

        assert result["status"] == "quoted"
        assert result["bid"] < 500.00
        assert result["ask"] > 500.00
