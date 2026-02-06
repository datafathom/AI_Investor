"""
Auditor Department Agents (9.5, 9.6)
Phase 7 Implementation: The Compliance Shield

The Auditor Department manages forensic reconciliation and behavioral analysis.
"""

import logging
from typing import Any, Dict, Optional
from agents.base_agent import BaseAgent, AgentState
from services.compliance.record_vault import get_record_vault

logger = logging.getLogger(__name__)

class ReconciliationBotAgent(BaseAgent):
    """
    AGENT 9.5: The Reconciliation Bot
    Ensures 'Ground Truth' between internal ledger and external banks.
    """
    def __init__(self):
        super().__init__("auditor.reconciler.9.5")
        self.vault = get_record_vault()

    async def process_event(self, event: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        if event.get("type") != "audit.reconcile":
            return None

        await self.transition_to(AgentState.SCANNING, "Fetching ledger and bank balances")
        
        ledger_bal = event.get("ledger_balance", 0.0)
        bank_bal = event.get("bank_balance", 0.0)
        
        await self.transition_to(AgentState.ANALYZING, f"Comparing balances: L=${ledger_bal}, B=${bank_bal}")
        
        variance = abs(ledger_bal - bank_bal)
        is_matched = variance <= 0.05
        
        if not is_matched:
            await self.transition_to(AgentState.ERROR, f"Variance detected: ${variance}")
        else:
            await self.transition_to(AgentState.COMPLETED, "Balances reconciled successfully")

        # Record audit to vault
        self.vault.add_record("reconciliation_audit", {
            "ledger_balance": ledger_bal,
            "bank_balance": bank_bal,
            "variance": variance,
            "is_matched": is_matched
        })

        return {
            "status": "completed",
            "variance": variance,
            "is_matched": is_matched
        }

class MistakeClassifierAgent(BaseAgent):
    """
    AGENT 9.6: The Mistake Classifier
    Triages losses and identifies if they were systemic or emotional.
    """
    def __init__(self):
        super().__init__("auditor.classifier.9.6")

    async def process_event(self, event: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        if event.get("type") != "audit.classify_mistake":
            return None

        await self.transition_to(AgentState.SCANNING, "Reviewing trade logs and behavioral data")
        
        loss_amount = event.get("loss", 0.0)
        # Mock logic based on 'tilt_score' in event
        tilt_score = event.get("tilt_score", 0.0) # 0 to 1.0
        
        await self.transition_to(AgentState.ANALYZING, f"Classifying loss of ${loss_amount} (Tilt: {tilt_score})")
        
        classification = "Market Risk"
        if tilt_score > 0.7:
            classification = "Human Tilt"
            await self.emit_trace("BEHAVIOR_ALERT", "High emotional variance detected during trade.", "error")
        elif loss_amount > 1000 and tilt_score < 0.2:
            classification = "Systemic Error"

        await self.transition_to(AgentState.COMPLETED, f"Loss classified as {classification}")
        
        return {
            "status": "analyzed",
            "classification": classification,
            "loss": loss_amount
        }
