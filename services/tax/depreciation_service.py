import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

class DepreciationService:
    """Calculates IRS-compliant depreciation deductions for properties."""
    
    PERIODS = {
        "RESIDENTIAL": 27.5,
        "COMMERCIAL": 39.0
    }

    def calculate_annual_deduction(self, building_value: float, prop_type: str) -> float:
        years = self.PERIODS.get(prop_type.upper(), 27.5)
        deduction = building_value / years
        
        logger.info(f"TAX_LOG: Annual depreciation for {prop_type} (${building_value:,.2f}): ${deduction:,.2f}")
        return round(float(deduction), 2)

    def calculate_tax_shield(self, deduction: float, tax_bracket: float) -> float:
        """Immediate cash benefit of the deduction."""
        benefit = deduction * tax_bracket
        return round(float(benefit), 2)
