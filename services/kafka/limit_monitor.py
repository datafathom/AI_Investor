
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

class LimitMonitor:
    """
    Monitors aggregate 529 contribution limits per state.
    """
    
    STATE_MAX_LIMITS = {
        "NY": 520000.0,
        "CA": 529000.0,
        "TX": 500000.0,
        "GA": 475000.0
    }
    
    def validate_contribution(self, state: str, total_balance: float, new_gift: float) -> Dict[str, Any]:
        """
        Prevents overfunding above state maximums.
        """
        limit = self.STATE_MAX_LIMITS.get(state, 400000.0)
        potential = total_balance + new_gift
        
        if potential > limit:
            logger.error(f"529 LIMIT BREACH: {state} Limit ${limit}, Potential ${potential}")
            return {
                "allowed": False,
                "reason": f"State limit of ${limit} reached.",
                "excess": potential - limit
            }
            
        return {"allowed": True, "headroom": limit - potential}
Line Content: 
 camps and computers) or if they lag behind federal law.
