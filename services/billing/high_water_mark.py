import logging
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

class HWMTracker:
    """Ensures performance fees are only charged on new gains above previous highs."""
    
    def calculate_incentive_fee(self, current_nav: float, last_hwm: float, carry_pct: float) -> float:
        if current_nav <= last_hwm:
            logger.info(f"HWM_LOG: No incentive fee. NAV {current_nav} below HWM {last_hwm}")
            return 0.0
            
        new_gain = current_nav - last_hwm
        fee = new_gain * carry_pct
        
        logger.info(f"HWM_LOG: Performance fee triggered on ${new_gain:,.2f} gain. Fee: ${fee:,.2f}")
        return round(fee, 2)

    def update_hwm(self, current_nav: float, last_hwm: float) -> float:
        return max(current_nav, last_hwm)
