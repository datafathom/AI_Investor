import logging
import random
from decimal import Decimal
from typing import Dict, Any, List

logger = logging.getLogger(__name__)

class SensitivityEngine:
    """
    Phase 176.5: Sensitivity Analysis (Base, Bull, Bear).
    Runs Monte Carlo simulations on LBO business plans.
    """
    
    def run_sensitivity_scenarios(
        self,
        base_ebitda: Decimal,
        exit_multiple: float,
        iterations: int = 1000
    ) -> Dict[str, Any]:
        """
        Policy: Variable multiple (±2.0) and EBITDA growth (±10%).
        """
        results = []
        for _ in range(iterations):
            ebitda_var = random.uniform(0.9, 1.1) # ±10% growth
            multiple_var = exit_multiple + random.uniform(-2.0, 2.0)
            
            final_valuation = float(base_ebitda) * ebitda_var * multiple_var
            results.append(final_valuation)
            
        avg_val = sum(results) / len(results)
        bull_case = max(results)
        bear_case = min(results)
        
        logger.info(f"SIM_LOG: Sensitivity Analysis complete. Mean Val: ${avg_val:,.2f}")
        
        return {
            "mean_valuation": round(avg_val, 2),
            "bull_case_max": round(bull_case, 2),
            "bear_case_min": round(bear_case, 2),
            "confidence_interval_95": "SIMULATED"
        }
