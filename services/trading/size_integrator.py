"""
Position Size Integrator.
Integrates stop loss logic with position sizing.
"""
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

class SizeIntegrator:
    """Integrates stop distance into sizing calculate."""
    
    def __init__(self, risk_pct: float = 0.01):
        self.risk_pct = risk_pct
        
    def calculate_size(self, entry_price: float, stop_price: float, account_equity: float) -> Dict[str, Any]:
        risk_per_share = abs(entry_price - stop_price)
        if risk_per_share == 0:
            return {"units": 0, "error": "Zero risk per share"}
            
        risk_amount = account_equity * self.risk_pct
        units = risk_amount / risk_per_share
        
        return {
            "units": round(units, 2),
            "risk_amount": round(risk_amount, 2),
            "risk_per_share": round(risk_per_share, 4)
        }
