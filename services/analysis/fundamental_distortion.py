import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

class FundamentalDistortionLogger:
    """Tracks divergence between market-cap weights and fundamental (revenue) weights."""
    
    def calculate_distortion(self, cap_weight: float, fundamental_weight: float) -> float:
        """
        Distortion score: Ratio of price-weight to fundamental-weight.
        Score > 1.0 indicates 'Growth' or 'Overvalued' tilt compared to fundamentals.
        """
        if fundamental_weight <= 0: return 99.9
        
        distortion = cap_weight / fundamental_weight
        logger.info(f"ANALYSIS_LOG: Fundamental Distortion: {distortion:.2f}")
        return round(float(distortion), 4)

    def classify_distortion(self, distortion: float) -> str:
        if distortion > 2.0: return "SEVERE"
        if distortion > 1.5: return "MODERATE"
        return "MINOR"
