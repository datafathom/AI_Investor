import logging
from datetime import date, timedelta
from typing import Dict, Any, List
from uuid import UUID

logger = logging.getLogger(__name__)

class PlanExecutionService:
    """
    Automates execution of SEC 10b5-1 safe-harbor selling plans.
    Ensures non-discretionary compliance: once a plan is active, the insider
    cannot modify or stop individual trades based on MNPI.
    """
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(PlanExecutionService, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if hasattr(self, '_initialized') and self._initialized:
            return
        self._initialized = True
        logger.info("PlanExecutionService initialized")

    def validate_plan_window(self, creation_date: date, cooling_off_days: int = 90) -> Dict[str, Any]:
        """
        Policy: Plans must have a cooling-off period (usually 90 days for directors/officers).
        """
        today = date.today()
        days_passed = (today - creation_date).days
        is_active = days_passed >= cooling_off_days
        
        return {
            "creation_date": creation_date.isoformat(),
            "cooling_off_period": cooling_off_days,
            "days_elapsed": days_passed,
            "is_plan_eligible_for_execution": is_active,
            "next_available_trade_date": (creation_date + timedelta(days=cooling_off_days)).isoformat() if not is_active else "NOW"
        }

    def execute_non_discretionary_trade(self, plan_id: UUID, ticker: str, quantity: int) -> Dict[str, Any]:
        """
        Policy: Execute trade without user confirmation to maintain 10b5-1 safe harbor.
        """
        logger.warning(f"10B51_LOG: AUTO-EXECUTING trade for Plan {plan_id}: SELL {quantity} {ticker}.")
        
        return {
            "plan_id": str(plan_id),
            "ticker": ticker,
            "executed_qty": quantity,
            "execution_type": "VWAP_ALGO",
            "status": "COMPLETED",
            "safe_harbor_audit_log": "NON_DISCRETIONARY_TRIGGER_FIRED"
        }
