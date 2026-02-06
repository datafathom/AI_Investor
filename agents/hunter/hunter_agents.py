"""
Hunter Department Agents (10.2)
Phase 8 Implementation: The Global HQ

Focuses on Venture Growth, deal sourcing, and modeling.
"""

import logging
from typing import Any, Dict, Optional
from agents.base_agent import BaseAgent, AgentState
from services.growth.venture_service import get_venture_service, ShareClass

logger = logging.getLogger(__name__)

class CapTableModelerAgent(BaseAgent):
    """
    AGENT 10.2: The Cap-Table Modeler
    Analyzes venture deal terms and models potential exit scenarios.
    """
    def __init__(self):
        super().__init__("hunter.modeler.10.2")
        self.venture_service = get_venture_service()

    async def process_event(self, event: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Analyzes a deal or exit scenario.
        Event type: 'growth.analyze_exit' or 'growth.model_round'
        """
        if event.get("type") == "growth.analyze_exit":
            return await self._handle_exit_analysis(event)
        elif event.get("type") == "growth.model_round":
            return await self._handle_round_modeling(event)
        return None

    async def _handle_exit_analysis(self, event: Dict[str, Any]) -> Dict[str, Any]:
        await self.transition_to(AgentState.SCANNING, "Reviewing cap-table structure")
        
        exit_value = event.get("exit_value", 0.0)
        raw_cap_table = event.get("cap_table", [])
        common_shares = event.get("common_shares", 0)
        
        await self.transition_to(AgentState.ANALYZING, f"Running waterfall for ${exit_value} exit")
        
        # Convert raw entries to ShareClass objects
        cap_table = [ShareClass(**sc) for sc in raw_cap_table]
        
        result = self.venture_service.calculate_waterfall(exit_value, cap_table, common_shares)
        
        await self.transition_to(AgentState.COMPLETED, "Waterfall analysis complete")
        return {
            "status": "success",
            "analysis": result
        }

    async def _handle_round_modeling(self, event: Dict[str, Any]) -> Dict[str, Any]:
        await self.transition_to(AgentState.SCANNING, "Fetching current round terms")
        
        current_shares = event.get("current_shares", 0)
        new_investment = event.get("new_investment", 0.0)
        pre_money = event.get("pre_money_valuation", 0.0)
        
        await self.transition_to(AgentState.ANALYZING, f"Modeling ${new_investment} round at ${pre_money} pre-money")
        
        result = self.venture_service.simulate_dilution(current_shares, new_investment, pre_money)
        
        summary = (f"Price/Share: ${result['price_per_share']:.2f}. "
                   f"Dilution: {result['dilution_percentage']:.2f}%. "
                   f"Post-Money: ${result['post_money']:.2f}")
        
        await self.emit_trace("DILUTION_REPORT", summary)
        
        await self.transition_to(AgentState.COMPLETED, "Round modeling complete")
        return {
            "status": "success",
            "modeling": result
        }
