"""
Idle Cash Sweeper.
Suggests deployment of sitting cash into yield-bearing assets.
"""
import logging
from typing import Dict, Any, List

logger = logging.getLogger(__name__)

class IdleSweeper:
    """Finds idle cash and suggests deployment."""
    
    SWEEP_THRESHOLD = 50000.0 # $50k
    
    def get_deployment_suggestions(self, balances: Dict[str, float]) -> List[Dict[str, Any]]:
        suggestions = []
        for curr, bal in balances.items():
            if bal > self.SWEEP_THRESHOLD:
                suggestions.append({
                    "currency": curr,
                    "amount": bal,
                    "action": "BUY_T_BILLS" if curr == "USD" else "CONVERT_TO_BASE_AND_INVEST",
                    "reason": f"Balance exceeds threshold of ${self.SWEEP_THRESHOLD}"
                })
        return suggestions
