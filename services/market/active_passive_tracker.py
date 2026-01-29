import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

class ActivePassiveTracker:
    """Tracks ratio of active vs passive trading volume."""
    
    def calculate_passive_dominance(self, ticker: str, active_vol: float, flows: float) -> Dict[str, Any]:
        passive_vol = abs(flows) # Simplified
        total_vol = active_vol + passive_vol
        
        passive_pct = (passive_vol / total_vol) if total_vol > 0 else 0
        
        # High dominance threshold (e.g. 80%)
        threshold_breach = passive_pct > 0.80
        
        if threshold_breach:
            logger.warning(f"MARKET_ALERT: Passive dominance for {ticker} at {passive_pct*100:.1f}%")
            
        return {
            "ticker": ticker,
            "passive_pct": round(passive_pct, 4),
            "active_pct": round(1 - passive_pct, 4),
            "threshold_breach": threshold_breach
        }
