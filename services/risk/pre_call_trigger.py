import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

class PreCallTrigger:
    """Predictive alert system to detect impending margin calls."""
    
    def evaluate_margin_safety(self, maintenance_excess: float, market_value: float) -> Dict[str, Any]:
        """
        Policy: Alert if maintenance excess is < 10% of market value.
        """
        if market_value <= 0: return {"is_safe": True}
        
        buffer_ratio = maintenance_excess / market_value
        is_safe = buffer_ratio > 0.10
        
        if not is_safe:
            logger.warning(f"RISK_ALERT: IMPENDING MARGIN CALL! Buffer {buffer_ratio:.2%} is below 10% threshold.")
            
        return {
            "is_safe": is_safe,
            "buffer_ratio": round(float(buffer_ratio), 4),
            "status": "SAFE" if is_safe else "DANGER_PRE_CALL"
        }
