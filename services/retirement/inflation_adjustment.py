import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

class WithdrawalInflationModel:
    """Adjusts withdrawal amounts for realized inflation (CPI)."""
    
    def adjust_for_inflation(self, base_amount: float, cpi_rate: float) -> float:
        """
        Policy: Increase previous year's amount by the CPI rate.
        """
        adjusted = base_amount * (1 + cpi_rate)
        logger.info(f"RET_LOG: Adjusted withdrawal ${base_amount:,.2f} for {cpi_rate:.2%} inflation -> ${adjusted:,.2f}")
        return round(adjusted, 2)
