"""
Currency Exposure Risk Guard.
Prevents excessive concentration in single currencies.
"""
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

class FXGuard:
    """Enforces currency exposure limits."""
    
    MAX_EXPOSURE_PCT = 0.15 # 15% limit
    
    def check_exposure(self, currency: str, balance_usd: float, total_portfolio_usd: float) -> Dict[str, Any]:
        if total_portfolio_usd == 0:
            return {"valid": False, "reason": "Empty portfolio"}
            
        exposure_pct = balance_usd / total_portfolio_usd
        
        if exposure_pct > self.MAX_EXPOSURE_PCT and currency != "USD":
            logger.warning(f"FX_RISK: {currency} exposure at {exposure_pct*100:.1f}%. Limit is {self.MAX_EXPOSURE_PCT*100}%")
            return {
                "valid": False,
                "reason": f"Exposure to {currency} exceeds {self.MAX_EXPOSURE_PCT*100}%",
                "current_pct": exposure_pct
            }
            
        return {"valid": True, "exposure_pct": exposure_pct}
