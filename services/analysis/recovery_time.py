"""
Time-to-Breakeven Estimator.
Forecasts recovery duration from drawdowns.
"""
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

class RecoveryEstimator:
    """Estimates recovery time after shocks."""
    
    def estimate_recovery(self, loss_pct: float, monthly_yield_exp: float) -> Dict[str, Any]:
        """
        loss_pct: e.g. 0.10 for 10%
        """
        # Linear recovery for simplicity
        if monthly_yield_exp <= 0:
             return {"months": 999, "status": "NO_RECOVERY"}
             
        months = (loss_pct / monthly_yield_exp)
        
        return {
            "months_to_breakeven": round(months, 1),
            "trajectory": "STABLE" if months < 12 else "PROLONGED"
        }
