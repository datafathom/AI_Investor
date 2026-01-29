import logging
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

class AntiMadoffGuard:
    """Blocks advisor operations that mimic high-risk fraud patterns."""
    
    def validate_statement_source(self, provider_name: str, custodian_name: str) -> bool:
        """Mandates that statements must originate from a qualified custodian, not the advisor."""
        is_valid = provider_name == custodian_name
        if not is_valid:
            logger.error(f"FRAUD_ALERT: Statement provider ({provider_name}) does not match custodian ({custodian_name})!")
        return is_valid

    def detect_return_striation(self, returns: List[float]) -> bool:
        """Detects suspiciously consistent positive returns with near-zero volatility."""
        import numpy as np
        if len(returns) < 12: return False
        
        std = np.std(returns)
        # If monthly volatility < 0.1% over a year, something is likely fake
        if std < 0.001:
            logger.warning("FRAUD_ALERT: Suspiciously consistent returns detected. Madoff pattern flagged.")
            return True
        return False
