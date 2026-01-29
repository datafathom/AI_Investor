"""
Correlation Calculator Service.
Computes Pearson correlation between asset price histories.
"""
from typing import List, Tuple, Optional
import numpy as np

class CorrelationCalculator:
    @staticmethod
    def calculate_pearson(prices1: List[float], prices2: List[float]) -> Tuple[float, float]:
        """
        Calculate Pearson correlation coefficient and confidence (mocked confidence for now).
        
        Returns:
            Tuple[float, float]: (correlation_coefficient, confidence)
        """
        if len(prices1) < 2 or len(prices2) < 2:
            return 0.0, 0.0
            
        # Synchronize lengths by taking the shortest common tail
        min_len = min(len(prices1), len(prices2))
        data1 = np.array(prices1[-min_len:])
        data2 = np.array(prices2[-min_len:])
        
        # Check for zero variance
        if np.std(data1) == 0 or np.std(data2) == 0:
            return 0.0, 0.0
            
        try:
            correlation_matrix = np.corrcoef(data1, data2)
            coefficient = float(correlation_matrix[0, 1])
            
            # Simple confidence calculation based on sample size
            # In a real system, this would be based on p-value or similar
            confidence = min(1.0, min_len / 100.0) 
            
            return coefficient, confidence
        except Exception:
            return 0.0, 0.0

    @staticmethod
    def get_correlation_direction(coefficient: float) -> str:
        """Categorize correlation direction."""
        if coefficient > 0.7:
            return "STRONG_POSITIVE"
        if coefficient > 0.3:
            return "POSITIVE"
        if coefficient < -0.7:
            return "STRONG_NEGATIVE"
        if coefficient < -0.3:
            return "NEGATIVE"
        return "NEUTRAL"
