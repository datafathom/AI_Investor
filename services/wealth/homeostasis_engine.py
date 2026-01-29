"""
Total Wealth Homeostasis Engine.
Maintains balance between liquid, illiquid, and safe assets.
"""
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

class HomeostasisEngine:
    """Maintains portfolio homeostasis."""
    
    TARGET_RATIOS = {
        "liquid_growth": 0.50,
        "safe_moat": 0.30,
        "speculative": 0.20
    }
    
    def check_homeostasis(self, portfolio: Dict[str, float]) -> Dict[str, Any]:
        total = sum(portfolio.values())
        if total == 0:
            return {"status": "EMPTY"}
            
        current_ratios = {k: v / total for k, v in portfolio.items()}
        deviations = {}
        
        actions = []
        for cat, target in self.TARGET_RATIOS.items():
            current = current_ratios.get(cat, 0)
            dev = current - target
            deviations[cat] = dev
            
            if abs(dev) > 0.05: # 5% tolerance
                action = "REDUCE" if dev > 0 else "ADD"
                actions.append(f"{action} {cat} by {abs(dev)*100:.1f}%")
                
        return {
            "deviations": deviations,
            "actions_required": actions,
            "is_balanced": len(actions) == 0
        }
