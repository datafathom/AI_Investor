"""
Diversification Myth Buster - Phase 37.
Analyzes correlation to expose false diversification.
"""
import logging
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

class DiversificationAnalyzer:
    """Exposes false diversification through correlation analysis."""
    
    @staticmethod
    def calculate_correlation(asset_a: List[float], asset_b: List[float]) -> float:
        # Simple correlation calculation
        if len(asset_a) != len(asset_b) or len(asset_a) < 2:
            return 0.0
        n = len(asset_a)
        mean_a = sum(asset_a) / n
        mean_b = sum(asset_b) / n
        cov = sum((a - mean_a) * (b - mean_b) for a, b in zip(asset_a, asset_b)) / n
        std_a = (sum((a - mean_a)**2 for a in asset_a) / n) ** 0.5
        std_b = (sum((b - mean_b)**2 for b in asset_b) / n) ** 0.5
        if std_a == 0 or std_b == 0:
            return 0.0
        return cov / (std_a * std_b)
    
    @staticmethod
    def is_false_diversification(correlation: float) -> bool:
        return correlation > 0.7
