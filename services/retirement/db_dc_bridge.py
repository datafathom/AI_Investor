import logging
from typing import Dict, Any, List

logger = logging.getLogger(__name__)

class DBDCBridge:
    """Bridges Defined Benefit (Pension) and Defined Contribution (401k) data."""
    
    def normalize_to_income_stream(self, pension_data: Dict[str, Any], dc_balance: float, retirement_years: int) -> Dict[str, Any]:
        """Converts both to a monthly retirement income estimate."""
        # Pension is already an income stream
        pension_monthly = pension_data.get("monthly_benefit", 0.0)
        
        # DC requires a withdrawal rate (e.g., 4% rule)
        dc_monthly = (dc_balance * 0.04) / 12
        
        total_monthly = pension_monthly + dc_monthly
        
        return {
            "pension_contribution": pension_monthly,
            "dc_contribution": dc_monthly,
            "total_estimated_monthly": round(total_monthly, 2),
            "pension_portion_pct": round((pension_monthly / total_monthly * 100), 2) if total_monthly > 0 else 0
        }
