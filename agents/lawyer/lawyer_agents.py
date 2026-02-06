"""
Lawyer Department Agents (8.1)
Phase 7 Implementation: The Compliance Shield

The Lawyer Department ensures regulatory compliance and structural integrity.
"""

import logging
from typing import Any, Dict, Optional
from agents.base_agent import BaseAgent, AgentState
from services.compliance.compliance_service import get_compliance_service

logger = logging.getLogger(__name__)

class WashSaleWatchdogAgent(BaseAgent):
    """
    AGENT 8.1: The Wash-Sale Watchdog
    Blocks trades that would trigger wash-sale tax violations.
    """
    def __init__(self):
        super().__init__("lawyer.watchdog.8.1")
        self.compliance = get_compliance_service()

    async def process_event(self, event: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        if event.get("type") != "trade.request":
            return None

        await self.transition_to(AgentState.SCANNING, "Checking wash-sale rules for ticker")
        
        ticker = event.get("ticker")
        trade_date = event.get("trade_date") # datetime instance
        
        await self.transition_to(AgentState.ANALYZING, f"Analyzing trade history for {ticker}")
        
        result = self.compliance.check_wash_sale(ticker, trade_date)
        
        if result["is_wash_sale"]:
            await self.transition_to(AgentState.ERROR, f"Wash-sale detected: {result['reason']}")
            return {
                "status": "blocked",
                "reason": "wash_sale_violation",
                "details": result["reason"]
            }

        await self.transition_to(AgentState.COMPLETED, "Trade compliant with wash-sale rules")
        return {
            "status": "approved",
            "compliance": "wash_sale_check_passed"
        }
