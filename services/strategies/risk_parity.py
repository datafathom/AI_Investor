"""
Volatility-Weighted Risk Parity.
Equalizes risk contribution across asset classes.
"""
import logging
from typing import Dict, List, Any

logger = logging.getLogger(__name__)

class RiskParityAllocator:
    """Calculates risk parity weights."""
    
    def calculate_weights(self, volatilties: Dict[str, float]) -> Dict[str, float]:
        """Weight = (1/Vol) / Sum(1/Vol)"""
        inv_vols = {k: 1.0 / v for k, v in volatilties.items() if v > 0}
        total_inv = sum(inv_vols.values())
        
        weights = {k: v / total_inv for k, v in inv_vols.items()}
        return weights
