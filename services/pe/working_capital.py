import logging
from decimal import Decimal
from typing import Dict, Any

logger = logging.getLogger(__name__)

class WorkingCapitalCalc:
    """
    Phase 176.2: Supply Chain Optimization Calculator.
    Models cash flow improvements via DPO (Payables), DSO (Receivables), and DIO (Inventory).
    """
    
    def calculate_cash_unlock(
        self,
        annual_revenue: Decimal,
        days_improvement: int,
        metric_type: str # DSO, DPO, DIO
    ) -> Dict[str, Any]:
        """
        Policy: Cash Unlock = (Revenue / 365) * Days Improvement.
        """
        # Daily revenue/cost equivalent
        daily_impact = annual_revenue / Decimal('365')
        cash_unlocked = daily_impact * Decimal(str(days_improvement))
        
        logger.info(f"PE_LOG: Working Capital {metric_type} improvement of {days_improvement} days unlocked ${cash_unlocked:,.2f}")
        
        return {
            "metric": metric_type.upper(),
            "days_improved": days_improvement,
            "cash_unlocked_usd": round(float(cash_unlocked), 2),
            "status": "CASH_POSITIVE" if cash_unlocked > 0 else "NEUTRAL"
        }
