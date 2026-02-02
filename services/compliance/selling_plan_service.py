import logging
import datetime
from typing import Dict, List, Any, Optional
from decimal import Decimal

logger = logging.getLogger(__name__)

class SellingPlanService:
    """
    Phase 186.1: 10b5-1 Preset Selling Plan Framework.
    Models pre-scripted exit plans for executives to avoid insider trading.
    """
    
    def create_selling_plan(
        self, 
        user_id: str, 
        ticker: str, 
        total_shares: int, 
        sale_dates: List[datetime.date], 
        shares_per_date: int
    ) -> Dict[str, Any]:
        """
        Creates a fixed, non-discretionary selling plan.
        """
        if len(sale_dates) * shares_per_date > total_shares:
            raise ValueError("Total shares in schedule exceeds allocated shares.")

        plan_id = f"PLAN_{user_id}_{ticker}_{datetime.date.today().isoformat()}"
        
        logger.info(f"PLAN_LOG: Created 10b5-1 plan {plan_id} for {user_id} on {ticker}.")
        
        return {
            "plan_id": plan_id,
            "user_id": user_id,
            "ticker": ticker,
            "total_shares": total_shares,
            "schedule": [{"date": d.isoformat(), "shares": shares_per_date} for d in sale_dates],
            "status": "ACTIVE",
            "created_at": datetime.datetime.now().isoformat()
        }

    def validate_plan_revision(self, plan_id: str, is_blackout_period: bool, has_inside_info: bool) -> Dict[str, Any]:
        """
        Phase 186.3: Plan Revision Gate.
        Prevents plan changes once insider knowledge of future performance is likely.
        """
        can_revise = not (is_blackout_period or has_inside_info)
        
        reason = "NONE"
        if is_blackout_period:
            reason = "Currently in corporate blackout period (e.g., pre-earnings)."
        elif has_inside_info:
            reason = "Insider possesses Material Non-Public Information (MNPI)."
            
        logger.info(f"PLAN_LOG: Revision check for {plan_id}. Allowed: {can_revise}. Reason: {reason}")
        
        return {
            "plan_id": plan_id,
            "can_revise": can_revise,
            "blocking_reason": reason,
            "action": "ALLOW_REVISION" if can_revise else "BLOCK_REVISION"
        }

    def get_upcoming_executions(self, plan: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Identifies scheduled sales that are due to be executed.
        """
        today = datetime.date.today().isoformat()
        upcoming = [s for s in plan["schedule"] if s["date"] >= today]
        return upcoming
