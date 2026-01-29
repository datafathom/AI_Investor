"""
Jurisdiction Tax Efficiency Scorer.
Compares tax rates across states/countries.
"""
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

class JurisdictionScorer:
    """Scores tax efficiency of locations."""
    
    DATA = {
        "CA": {"income_tax": 0.13, "cap_gains": 0.13, "protection": 3},
        "NV": {"income_tax": 0.00, "cap_gains": 0.00, "protection": 9},
        "WY": {"income_tax": 0.00, "cap_gains": 0.00, "protection": 10},
        "TX": {"income_tax": 0.00, "cap_gains": 0.00, "protection": 7}
    }
    
    def compare(self, current: str, target: str, capital_gains: float) -> Dict[str, Any]:
        curr_stats = self.DATA.get(current, {"income_tax": 0.10, "cap_gains": 0.10, "protection": 5})
        targ_stats = self.DATA.get(target, {"income_tax": 0.10, "cap_gains": 0.10, "protection": 5})
        
        savings = capital_gains * (curr_stats["cap_gains"] - targ_stats["cap_gains"])
        
        return {
            "estimated_savings": round(savings, 2),
            "protection_uplift": targ_stats["protection"] - curr_stats["protection"],
            "recommendation": "MOVE" if savings > 10000 else "STAY"
        }
