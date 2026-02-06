"""
Unit Tests for Orchestrator Agents
Phase 1 Implementation: The Sovereign Kernel
"""

import pytest
from datetime import datetime

from agents.orchestrator.orchestrator_agents import (
    SynthesizerAgent,
    CommandInterpreterAgent,
    TrafficControllerAgent,
    LayoutMorphologistAgent,
    RedTeamSentryAgent,
    ContextWeaverAgent,
    get_orchestrator_agents,
)


class TestSynthesizerAgent:
    """Tests for Agent 1.1: The Synthesizer."""

    def setup_method(self) -> None:
        self.agent = SynthesizerAgent()
        self.agent.start()

    def test_agent_initialization(self) -> None:
        """Test agent initializes with correct name."""
        assert self.agent.name == "orchestrator.synthesizer.1.1"
        assert self.agent.is_active is True

    def test_aggregate_agent_log(self) -> None:
        """Test log aggregation."""
        event = {"type": "agent.log", "agent_id": "trader.4.1", "message": "Trade executed"}
        result = self.agent.process_event(event)
        
        assert result is not None
        assert result["status"] == "aggregated"
        assert result["agent_id"] == "trader.4.1"

    def test_validate_ledger_totals_within_tolerance(self) -> None:
        """Test ledger validation passes within 0.01% tolerance."""
        event = {
            "type": "ledger.summary",
            "total": 1000000.00,
            "briefing_total": 1000000.05,  # 0.000005% variance
        }
        result = self.agent.process_event(event)
        
        assert result["status"] == "validated"
        assert result["within_tolerance"] is True

    def test_validate_ledger_totals_outside_tolerance(self) -> None:
        """Test ledger validation fails outside tolerance."""
        event = {
            "type": "ledger.summary",
            "total": 1000000.00,
            "briefing_total": 1000200.00,  # 0.02% variance
        }
        result = self.agent.process_event(event)
        
        assert result["status"] == "mismatch"
        assert result["within_tolerance"] is False

    def test_generate_briefing(self) -> None:
        """Test briefing generation."""
        event = {"type": "briefing.request", "date": "2026-02-05"}
        result = self.agent.process_event(event)
        
        assert result["status"] == "generated"
        assert "briefing_hash" in result
        assert len(result["briefing_hash"]) == 64


class TestCommandInterpreterAgent:
    """Tests for Agent 1.2: The Command Interpreter."""

    def setup_method(self) -> None:
        self.agent = CommandInterpreterAgent()
        self.agent.start()

    def test_interpret_buy_command(self) -> None:
        """Test interpretation of a BUY command."""
        event = {"type": "command.text", "text": "Buy 100 shares of AAPL"}
        result = self.agent.process_event(event)
        
        assert result["status"] == "interpreted"
        assert result["structured_call"]["verb"] == "BUY"
        assert "AAPL" in result["structured_call"]["tickers"]

    def test_interpret_sell_command_with_amount(self) -> None:
        """Test interpretation of a SELL command with amount."""
        event = {"type": "command.text", "text": "Sell $5,000 of MSFT"}
        result = self.agent.process_event(event)
        
        assert result["structured_call"]["verb"] == "SELL"
        assert "MSFT" in result["structured_call"]["tickers"]
        assert 5000.0 in result["structured_call"]["amounts"]

    def test_accuracy_feedback(self) -> None:
        """Test accuracy tracking."""
        # Record some feedback
        for correct in [True, True, True, False, True]:
            self.agent.process_event({"type": "accuracy.feedback", "correct": correct})
        
        result = self.agent.process_event({"type": "accuracy.feedback", "correct": True})
        
        assert result["current_accuracy"] == 83.33333333333334  # 5/6


class TestTrafficControllerAgent:
    """Tests for Agent 1.3: The Traffic Controller."""

    def setup_method(self) -> None:
        self.agent = TrafficControllerAgent()
        self.agent.start()

    def test_backpressure_activates_on_high_lag(self) -> None:
        """Test backpressure activates when lag > 200ms."""
        event = {"type": "kafka.metrics", "consumer_lag_ms": 300.0, "messages_per_sec": 5000}
        result = self.agent.process_event(event)
        
        assert result["backpressure"] is True

    def test_no_backpressure_on_low_lag(self) -> None:
        """Test no backpressure when lag < 200ms."""
        event = {"type": "kafka.metrics", "consumer_lag_ms": 100.0, "messages_per_sec": 5000}
        result = self.agent.process_event(event)
        
        assert result["backpressure"] is False


class TestLayoutMorphologistAgent:
    """Tests for Agent 1.4: The Layout Morphologist."""

    def setup_method(self) -> None:
        self.agent = LayoutMorphologistAgent()
        self.agent.start()

    def test_volatility_triggers_layout_switch(self) -> None:
        """Test high volatility triggers Trader HUD switch."""
        event = {"type": "market.volatility", "volatility": 0.05}  # 5% move
        result = self.agent.process_event(event)
        
        assert result is not None
        assert result["to"] == "trader_hud"

    def test_low_volatility_no_switch(self) -> None:
        """Test low volatility does not trigger switch."""
        event = {"type": "market.volatility", "volatility": 0.01}  # 1% move
        result = self.agent.process_event(event)
        
        assert result is None


class TestRedTeamSentryAgent:
    """Tests for Agent 1.5: The Red-Team Sentry."""

    def setup_method(self) -> None:
        self.agent = RedTeamSentryAgent()
        self.agent.start()

    def test_blocks_os_system(self) -> None:
        """Test blocking of os.system calls."""
        event = {"type": "syscall.audit", "agent_id": "rogue.agent", "syscall": "os.system('rm -rf /')"}
        result = self.agent.process_event(event)
        
        assert result["status"] == "SIGKILL"
        assert result["violation"] == "os.system"

    def test_blocks_eval(self) -> None:
        """Test blocking of eval calls."""
        event = {"type": "syscall.audit", "agent_id": "bad.actor", "syscall": "eval(user_input)"}
        result = self.agent.process_event(event)
        
        assert result["status"] == "SIGKILL"
        assert result["violation"] == "eval("

    def test_allows_safe_code(self) -> None:
        """Test safe code is allowed."""
        event = {"type": "syscall.audit", "agent_id": "good.agent", "syscall": "print('hello')"}
        result = self.agent.process_event(event)
        
        assert result["status"] == "allowed"


class TestContextWeaverAgent:
    """Tests for Agent 1.6: The Context Weaver."""

    def setup_method(self) -> None:
        self.agent = ContextWeaverAgent()
        self.agent.start()

    def test_record_action(self) -> None:
        """Test action recording."""
        event = {"type": "action.completed", "agent_id": "trader.4.1", "action": "BUY AAPL", "result": "success"}
        result = self.agent.process_event(event)
        
        assert result["status"] == "recorded"
        assert result["buffer_size"] == 1

    def test_context_buffer_limited_to_5(self) -> None:
        """Test context buffer is limited to 5 items."""
        for i in range(10):
            self.agent.process_event({
                "type": "action.completed",
                "agent_id": f"agent.{i}",
                "action": f"action_{i}",
                "result": "ok"
            })
        
        result = self.agent.process_event({"type": "context.request"})
        assert result["item_count"] == 5

    def test_inject_context_on_role_switch(self) -> None:
        """Test context injection on department switch."""
        # Add some actions first
        self.agent.process_event({"type": "action.completed", "agent_id": "trader", "action": "trade", "result": "ok"})
        
        event = {"type": "role.switch", "target_department": "strategist"}
        result = self.agent.process_event(event)
        
        assert result["status"] == "context_injected"
        assert result["target_department"] == "strategist"
        assert result["context_items"] == 1


class TestOrchestratorRegistry:
    """Tests for the agent registry function."""

    def test_get_all_orchestrator_agents(self) -> None:
        """Test that all 6 agents are returned."""
        agents = get_orchestrator_agents()
        
        assert len(agents) == 6
        assert "orchestrator.synthesizer.1.1" in agents
        assert "orchestrator.interpreter.1.2" in agents
        assert "orchestrator.traffic.1.3" in agents
        assert "orchestrator.layout.1.4" in agents
        assert "orchestrator.sentry.1.5" in agents
        assert "orchestrator.weaver.1.6" in agents
