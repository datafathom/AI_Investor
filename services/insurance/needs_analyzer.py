import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

class NeedsAnalyzer:
    """Analyzes life insurance needs based on financial obligations."""
    
    def calculate_gap(self, annual_income: float, debt: float, current_benefit: float) -> Dict[str, Any]:
        """Simple 'Income Replacement' method: 10x income + debt."""
        target = (annual_income * 10) + debt
        gap = target - current_benefit
        
        logger.info(f"INSURANCE_LOG: Target: ${target:,.2f}, Gap: ${max(0, gap):,.2f}")
        
        return {
            "target_coverage": target,
            "current_coverage": current_benefit,
            "gap": round(max(0, gap), 2),
            "is_underinsured": gap > 0
        }
