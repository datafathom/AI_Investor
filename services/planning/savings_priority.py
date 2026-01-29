import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

class SavingsPriorityEngine:
    """Prioritizes cash flows between emergency savings and investment accounts."""
    
    def prioritize_allocation(self, income: float, emergency_balance: float, emergency_target: float) -> Dict[str, float]:
        """
        Policy: 100% of excess goes to EF until it matches target.
        """
        gap = max(0, emergency_target - emergency_balance)
        
        if gap > 0:
            ef_alloc = min(income, gap)
            inv_alloc = income - ef_alloc
            logger.info(f"PLANNING_LOG: Replenishing EF (Gap: ${gap:,.2f}). EF Alloc: ${ef_alloc:,.2f}")
        else:
            ef_alloc = 0.0
            inv_alloc = income
            logger.info("PLANNING_LOG: EF is full. 100% to investments.")
            
        return {
            "emergency_fund_allocation": ef_alloc,
            "investment_allocation": inv_alloc
        }
