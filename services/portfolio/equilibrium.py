"""
Portfolio Equilibrium Monitor.
Monitors asset class balance.
"""
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

class EquilibriumMonitor:
    """Monitors portfolio balance."""
    
    TARGET_ALLOCATION = {
        "equities": 0.60,
        "fixed_income": 0.30,
        "cash": 0.10
    }
    
    def check_balance(self, current_holdings: Dict[str, float]) -> Dict[str, Any]:
        total = sum(current_holdings.values())
        if total == 0:
            return {"status": "EMPTY"}
            
        deviations = {}
        for asset, value in current_holdings.items():
            current_pct = value / total
            target = self.TARGET_ALLOCATION.get(asset, 0)
            deviations[asset] = current_pct - target
            
        max_dev = max(abs(v) for v in deviations.values())
        is_balanced = max_dev < 0.05 # 5% drift tolerance
        
        return {
            "balanced": is_balanced,
            "deviations": deviations,
            "max_drift_pct": max_dev * 100
        }
