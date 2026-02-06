"""
Unit Tests for Phase 6: The Financial Fortress
Tests for Guardian, Architect agents, and Treasury/Life-Cycle services.
"""

import pytest
import time

from services.banking.treasury_service import get_treasury_service
from services.architect.life_cycle_service import get_lifecycle_service
from agents.guardian import get_guardian_agents
from agents.architect import get_architect_agents

class TestFinancialFortress:
    """Tests for Phase 6 components."""

    def setup_method(self) -> None:
        self.treasury = get_treasury_service()
        self.treasury.reset()
        self.lifecycle = get_lifecycle_service()
        self.guardian_agents = get_guardian_agents()
        self.architect_agents = get_architect_agents()

    def test_cash_sweep_logic(self) -> None:
        """Test that cash sweep triggers correctly above threshold."""
        self.treasury.sync_accounts()
        # Initial checking balance in mock is 7500.0
        # Threshold 5000.0 -> expect 2500.0 sweep
        sweeps = self.treasury.execute_cash_sweep(threshold=5000.0)
        
        assert len(sweeps) > 0
        assert sweeps[0]["amount"] == 2500.0
        assert self.treasury.accounts["acc_001"].balance == 5000.0

    def test_bill_ocr_agent(self) -> None:
        """Test bill automator agent processing."""
        agent = self.guardian_agents["guardian.bill.6.1"]
        agent.start()

        event = {
            "type": "bill.ingest",
            "content": "Invoice for Electric Co, Amount Due: $125.50, Due Date: 2026-03-15"
        }
        
        result = agent.process_event(event)
        assert result["status"] == "STAGED"
        assert result["bill_details"]["amount_due"] == 125.50

    def test_life_cycle_projection(self) -> None:
        """Test architect projection speed and logic."""
        agent = self.architect_agents["architect.modeler.7.1"]
        agent.start()

        event = {
            "type": "model.run_projection",
            "params": {
                "current_nw": 500000.0,
                "monthly_savings": 10000.0,
                "monthly_burn": 2000.0,
                "expected_return": 0.10,
                "inflation": 0.02,
                "horizon_years": 50,
                "current_age": 30
            }
        }
        
        result = agent.process_event(event)
        assert result["status"] == "COMPLETED"
        assert result["under_1s_sla"] is True
        assert result["fi_year"] is not None
        assert result["fi_age"] >= 30

    def test_net_worth_audit(self) -> None:
        """Test guardian reconciliation logic."""
        agent = self.guardian_agents["guardian.auditor.6.5"]
        agent.start()

        # Populate accounts
        self.treasury.sync_accounts()
        bank_total = sum(a.balance for a in self.treasury.accounts.values())
        
        # Test perfect match
        result = agent.process_event({"type": "audit.reconcile", "ledger_balance": bank_total})
        assert result["alert"] is False
        
        # Test discrepancy
        result = agent.process_event({"type": "audit.reconcile", "ledger_balance": bank_total + 10.0})
        assert result["alert"] is True
        assert result["discrepancy"] == 10.0
