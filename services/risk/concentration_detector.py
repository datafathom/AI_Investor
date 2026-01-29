import logging
import numpy as np
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

class ConcentrationDetector:
    """Detects dangerous concentration levels in index funds (e.g. Top 10 > 40%)."""
    
    def calculate_hhi(self, weights: List[float]) -> float:
        """Herfindahl-Hirschman Index: sum of squared weights."""
        hhi = sum(w**2 for w in weights)
        return round(float(hhi), 6)

    def analyze_concentration(self, weights: List[float]) -> Dict[str, Any]:
        """
        Policy: 
        - CRITICAL: Top 10 > 40%
        - HIGH: Top 10 > 35%
        - NORMAL: Else
        """
        sorted_weights = sorted(weights, reverse=True)
        top_10_sum = sum(sorted_weights[:10])
        hhi = self.calculate_hhi(weights)
        
        if top_10_sum > 0.40:
            level = "CRITICAL"
        elif top_10_sum > 0.35:
            level = "HIGH"
        else:
            level = "NORMAL"
            
        logger.info(f"RISK_LOG: Index Concentration: {top_10_sum:.2%} (Level: {level}, HHI: {hhi})")
        
        return {
            "top_10_weight": round(top_10_sum, 4),
            "hhi": hhi,
            "concentration_level": level,
            "effective_holdings": int(1/hhi) if hhi > 0 else 0
        }
