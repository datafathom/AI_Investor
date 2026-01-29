import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

class TargetReturnAdjuster:
    """Adjusts nominal target returns to maintain a constant real return goal."""
    
    def adjust_target(self, desired_real_return: float, current_inflation: float) -> float:
        """
        Nominal = (1 + Real) * (1 + Inflation) - 1
        Approx: Nominal = Real + Inflation
        """
        nominal_target = (1 + desired_real_return) * (1 + current_inflation) - 1
        
        logger.info(f"PLAN_LOG: Real Goal {desired_real_return:.2%} + Inflation {current_inflation:.2%} -> Nominal Target {nominal_target:.2%}")
        
        return round(float(nominal_target), 4)
