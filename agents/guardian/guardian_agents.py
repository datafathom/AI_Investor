"""
Guardian Department Agents (6.1 - 6.6)
Phase 6 Implementation: The Financial Fortress

The Guardian Department is the Automated Treasury, managing cash flows,
bills, budgets, and bank reconciliations.

ACCEPTANCE CRITERIA:
- Agent 6.1: Bill OCR processing with 0 errors in amount.
- Agent 6.2: ACH sweep triggering for checking > $5,000.
"""

import logging
import time
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
from dataclasses import dataclass, field

from agents.base_agent import BaseAgent
from services.system.model_manager import ModelProvider
from services.banking.treasury_service import get_treasury_service

logger = logging.getLogger(__name__)

class BillAutomatorAgent(BaseAgent):
    """
    Agent 6.1: The Bill Automator
    
    Processes utility bills and stages them for payment.
    
    Acceptance Criteria:
    - 100% accuracy on Amount and Due Date from PDF OCR.
    """

    def __init__(self) -> None:
        super().__init__(name="guardian.bill.6.1", provider=ModelProvider.GEMINI)
        self.treasury = get_treasury_service()

    def process_event(self, event: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        if event.get("type") == "bill.ingest":
            return self._ingest_bill(event)
        return None

    def _ingest_bill(self, event: Dict[str, Any]) -> Dict[str, Any]:
        """Ingest and parse a bill PDF."""
        start_time = time.perf_counter()
        
        pdf_text = event.get("content", "")
        # Call treasury OCR service
        results = self.treasury.process_bill_ocr(pdf_text)
        
        elapsed_ms = (time.perf_counter() - start_time) * 1000
        
        if results["status"] == "SUCCESS":
            return {
                "status": "STAGED",
                "bill_details": results,
                "latency_ms": elapsed_ms,
            }
        else:
            return {
                "status": "ERROR",
                "reason": results.get("reason"),
                "latency_ms": elapsed_ms,
            }

class FlowMasterAgent(BaseAgent):
    """
    Agent 6.2: The Flow Master
    
    Manages ACH cash flow sweeps and liquidity thresholds.
    
    Acceptance Criteria:
    - Triggers ACH sweep when checking > $5,000.
    """

    def __init__(self) -> None:
        super().__init__(name="guardian.flow.6.2", provider=ModelProvider.GEMINI)
        self.treasury = get_treasury_service()

    def process_event(self, event: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        if event.get("type") == "flow.check_sweeps":
            return self._check_sweeps(event)
        return None

    def _check_sweeps(self, event: Dict[str, Any]) -> Dict[str, Any]:
        """Check all accounts for sweep opportunities."""
        self.treasury.sync_accounts()
        sweeps = self.treasury.execute_cash_sweep(threshold=event.get("threshold", 5000.0))
        
        return {
            "status": "ANALYZED",
            "sweeps_executed": len(sweeps),
            "details": sweeps
        }

class NetWorthAuditorAgent(BaseAgent):
    """
    Agent 6.5: The Net Worth Auditor
    
    Reconciles internal ledger with external bank balances.
    
    Acceptance Criteria:
    - Flags discrepancies > $0.05 within 60s.
    """

    def __init__(self) -> None:
        super().__init__(name="guardian.auditor.6.5", provider=ModelProvider.GEMINI)
        self.treasury = get_treasury_service()

    def process_event(self, event: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        if event.get("type") == "audit.reconcile":
            return self._reconcile(event)
        return None

    def _reconcile(self, event: Dict[str, Any]) -> Dict[str, Any]:
        # Mock reconciliation logic
        self.treasury.sync_accounts()
        ledger_balance = event.get("ledger_balance", 0.0)
        bank_total = sum(a.balance for a in self.treasury.accounts.values())
        
        discrepancy = abs(ledger_balance - bank_total)
        flag = discrepancy > 0.05
        
        return {
            "status": "AUDITED",
            "discrepancy": discrepancy,
            "bank_total": bank_total,
            "ledger_total": ledger_balance,
            "alert": flag
        }

# Agent Registry for Dept 6
def get_guardian_agents() -> Dict[str, BaseAgent]:
    return {
        "guardian.bill.6.1": BillAutomatorAgent(),
        "guardian.flow.6.2": FlowMasterAgent(),
        "guardian.auditor.6.5": NetWorthAuditorAgent(),
    }
