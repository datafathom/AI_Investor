import logging
from decimal import Decimal
from typing import Dict, Any

logger = logging.getLogger(__name__)

class SynergyEstimator:
    """
    Phase 176.4: Add-On Acquisition Synergy Estimator.
    Estimates revenue and cost synergies from 'Buy and Build' strategy.
    """
    
    def estimate_synergies(
        self,
        platform_ebitda: Decimal,
        target_ebitda: Decimal,
        overlap_pct: Decimal
    ) -> Dict[str, Any]:
        """
        Policy: 
        - Cost Synergies: 20% of Target SG&A (assumed 15% of EBITDA for simplicity).
        - Revenue Synergies: 5% cross-sell uplift on combined.
        """
        cost_savings = target_ebitda * Decimal('0.20') # Aggressive cost cutting on target
        revenue_uplift = (platform_ebitda + target_ebitda) * Decimal('0.05')
        
        total_synergy = cost_savings + revenue_uplift
        pro_forma_ebitda = platform_ebitda + target_ebitda + total_synergy
        
        logger.info(f"PE_LOG: Estimated synergies: ${total_synergy:,.2f}. Pro-forma EBITDA: ${pro_forma_ebitda:,.2f}")
        
        return {
            "cost_synergies": round(float(cost_savings), 2),
            "revenue_synergies": round(float(revenue_uplift), 2),
            "total_synergy_value": round(float(total_synergy), 2),
            "pro_forma_ebitda": round(float(pro_forma_ebitda), 2)
        }
