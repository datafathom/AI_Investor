import logging
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

class AUMCalculator:
    """Calculates Assets Under Management (AUM) for advisors."""
    
    def calculate_advisor_aum(self, clients: List[Dict[str, Any]]) -> float:
        total_aum = sum(c.get("net_worth", 0) for c in clients)
        logger.info(f"AUM_LOG: Calculated total AUM: ${total_aum:,.2f}")
        return total_aum

    def calculate_billable_fee(self, aum: float, fee_pct: float) -> float:
        """Calculates quarterly fee based on annual percentage."""
        annual_fee = aum * (fee_pct / 100)
        return annual_fee / 4
