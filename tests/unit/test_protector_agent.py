"""
Unit tests for Protector Agent.
"""
import pytest
from agents.protector_agent import ProtectorAgent

class TestProtectorAgent:
    @pytest.fixture
    def agent(self):
        return ProtectorAgent()

    def test_approve_valid_order(self, agent):
        # 0.5% risk (allowed)
        event = {
            "type": "VALIDATE_ORDER",
            "amount": 500.0,
            "balance": 100000.0,
            "daily_loss": 0.0
        }
        result = agent.process_event(event)
        assert result["action"] == "APPROVE"

    def test_reject_high_risk_order(self, agent):
        # 2% risk (rejected)
        event = {
            "type": "VALIDATE_ORDER",
            "amount": 2000.0,
            "balance": 100000.0,
            "daily_loss": 0.0
        }
        result = agent.process_event(event)
        assert result["action"] == "REJECT"
        assert result["reason"] == "RISK_EXCEEDS_1_PERCENT"

    def test_circuit_breaker_reject(self, agent):
        # Daily loss already 4% (circuit tripped)
        event = {
            "type": "VALIDATE_ORDER",
            "amount": 100.0,
            "balance": 100000.0,
            "daily_loss": 4000.0
        }
        result = agent.process_event(event)
        assert result["action"] == "REJECT"
        assert result["reason"] == "CIRCUIT_BREAKER_TRIPPED"
