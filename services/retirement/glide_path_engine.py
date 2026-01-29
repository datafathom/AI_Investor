import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

class GlidePathEngine:
    """Calculates asset allocation targets based on the timeline to a goal."""
    
    def calculate_target_allocation(self, years_to_target: float, strategy: str = "MODERATE") -> Dict[str, Any]:
        """
        Policy (Moderate): 
        - 20+ Yrs: 90% Equity
        - 10 Yrs: 75% Equity
        - 5 Yrs: 60% Equity
        - 0 Yrs: 40% Equity
        """
        if years_to_target >= 20: 
            equity = 0.90
        elif years_to_target <= 0:
            equity = 0.40
        else:
            # Linear interpolation between values if needed, or stepped logic
            if years_to_target > 10:
                equity = 0.75 + (years_to_target - 10) * 0.015 # Approx 90 at 20
            elif years_to_target > 5:
                equity = 0.60 + (years_to_target - 5) * 0.03 # Approx 75 at 10
            else:
                equity = 0.40 + (years_to_target) * 0.04 # Approx 60 at 5
                
        bond = 1.0 - equity
        
        logger.info(f"RET_LOG: Glide path calculation: {years_to_target:.1f} years left -> {equity:.0%} Equity / {bond:.0%} Bond")
        
        return {
            "years_remaining": round(years_to_target, 2),
            "target_equity_pct": round(float(equity), 4),
            "target_bond_pct": round(float(bond), 4),
            "rebalance_action": "TRIM_EQUITY" if years_to_target < 10 else "HOLD"
        }
