import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

class DBDCMigrationCalculator:
    """Calculates the break-even for migrating from a Pension (DB) to a Matching 401k (DC)."""
    
    def calculate_equivalence(self, db_monthly_benefit: float, dc_employer_match: float, salary: float, years_to_ret: int) -> Dict[str, Any]:
        """
        Calculates if the lump sum equivalent of a pension exceeds expected 401k match growth.
        """
        # Estimated lump sum equivalent (25x annual)
        pension_value = db_monthly_benefit * 12 * 25
        
        # 401k growth (6% return)
        dc_annual_match = salary * dc_employer_match
        dc_projected = dc_annual_match * ((1.06**years_to_ret - 1) / 0.06)
        
        logger.info(f"RET_LOG: DB Value: ${pension_value:,.2f} vs DC Match Proj: ${dc_projected:,.2f}")
        
        return {
            "pension_equity_value": round(pension_value, 2),
            "projected_match_value": round(dc_projected, 2),
            "preference": "PENSION" if pension_value > dc_projected else "MATCHING_401K"
        }
