"""
Unit Tests for Phase 7: The Compliance Shield
Tests for Hash-Chaining, State-Machine Agents, and Compliance Logic.
"""

import pytest
import asyncio
from datetime import datetime, timezone, timedelta
from unittest.mock import MagicMock, patch

from services.compliance.record_vault import get_record_vault
from services.compliance.compliance_service import get_compliance_service
from agents.lawyer.lawyer_agents import WashSaleWatchdogAgent
from agents.auditor.auditor_agents import ReconciliationBotAgent, MistakeClassifierAgent
from agents.base_agent import AgentState

class TestComplianceShield:
    def setup_method(self):
        self.vault = get_record_vault()
        # Reset vault chain for tests
        self.vault.chain = []
        self.compliance = get_compliance_service()

    def test_record_vault_integrity(self):
        """Verify hash-chaining and tamper detection."""
        self.vault.add_record("test_type", {"foo": "bar"})
        self.vault.add_record("test_type", {"secret": "data"}, sensitive_keys=["secret"])
        
        assert len(self.vault.chain) == 2
        assert self.vault.verify_chain() is True
        
        # Test Decryption
        secret_record = self.vault.chain[1]
        decrypted = self.vault.decrypt_value(secret_record.data["secret"])
        assert decrypted == "data"
        
        # Test Tampering
        self.vault.chain[0].data["foo"] = "TAMPERED"
        assert self.vault.verify_chain() is False

    @pytest.mark.asyncio
    async def test_wash_sale_watchdog(self):
        """Verify Agent 8.1 state transitions and blocking."""
        agent = WashSaleWatchdogAgent()
        
        # 1. Setup a loss 10 days ago
        now = datetime.now(timezone.utc)
        loss_date = now - timedelta(days=10)
        self.vault.add_record("trade_execution", {
            "ticker": "AAPL",
            "pnl": -500.0,
            "executed_at": loss_date.isoformat()
        })
        
        # 2. Request a trade for AAPL
        event = {
            "type": "trade.request",
            "ticker": "AAPL",
            "trade_date": now
        }
        
        # Mock SocketManager to avoid network calls
        with patch("services.system.socket_manager.get_socket_manager") as mock_socket:
            mock_sm = MagicMock()
            mock_socket.return_value = mock_sm
            
            result = await agent.process_event(event)
            
            assert result["status"] == "blocked"
            assert agent.state == AgentState.ERROR
            assert mock_sm.emit_event.called

    @pytest.mark.asyncio
    async def test_reconciliation_bot(self):
        """Verify Agent 9.5 reconciliation logic."""
        agent = ReconciliationBotAgent()
        
        event = {
            "type": "audit.reconcile",
            "ledger_balance": 1000.0,
            "bank_balance": 1000.0
        }
        
        with patch("services.system.socket_manager.get_socket_manager") as mock_socket:
            result = await agent.process_event(event)
            assert result["is_matched"] is True
            assert agent.state == AgentState.COMPLETED
            
            # Check vault record
            reco_records = self.vault.get_records_by_type("reconciliation_audit")
            assert len(reco_records) == 1
            assert reco_records[0]["data"]["is_matched"] is True

    @pytest.mark.asyncio
    async def test_mistake_classifier(self):
        """Verify Agent 9.6 behavioral analysis."""
        agent = MistakeClassifierAgent()
        
        # Test Tilt
        event = {
            "type": "audit.classify_mistake",
            "loss": 1500.0,
            "tilt_score": 0.9
        }
        
        with patch("services.system.socket_manager.get_socket_manager"):
            result = await agent.process_event(event)
            assert result["classification"] == "Human Tilt"
            assert agent.state == AgentState.COMPLETED # Transitions back to completed after analysis
