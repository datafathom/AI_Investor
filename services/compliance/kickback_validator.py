import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

class KickbackValidator:
    """Automated validator to prevent fiduciary conflicts."""
    
    def validate_fiduciary_revenue(self, advisor_name: str, fiduciary: bool, kickback_pct: float) -> Dict[str, Any]:
        """
        Validation Rules:
        KICKBACK_001: Fiduciary accepts > 5% commission revenue -> BLOCK
        """
        if fiduciary and kickback_pct > 0.05:
            logger.error(f"KICKBACK_BLOCK: Advisor {advisor_name} is a fiduciary but has {kickback_pct*100}% kickback revenue.")
            return {"valid": False, "code": "KICKBACK_001", "action": "BLOCK_AND_ALERT"}
        
        if fiduciary and kickback_pct > 0.01:
            return {"valid": True, "code": "KICKBACK_002", "action": "WARN"}
            
        return {"valid": True, "action": "PASS"}
