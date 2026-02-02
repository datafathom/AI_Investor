import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

class EmotionalUtilityOptimizer:
    """
    Phase 174.4: 'Passion Asset' Emotional Value Weighting.
    Allows for over-allocation to assets with high emotional utility (e.g. Vintage Cars).
    """
    
    def calculate_weighted_utility(self, financial_return: float, emotional_score: float) -> Dict[str, Any]:
        """
        Total Utility = (Financial Return * 0.7) + (Emotional Score * 0.3).
        Emotional Score is normalized 0.0 to 1.0.
        """
        weighted_utility = (financial_return * 0.7) + (emotional_score * 0.3)
        
        logger.info(f"PORTFOLIO_LOG: Emotional Utility Optimization (Fin: {financial_return:.2%}, Emo: {emotional_score:.2f}) -> Total: {weighted_utility:,.4f}")
        
        return {
            "financial_return_contribution": round(financial_return * 0.7, 4),
            "emotional_value_contribution": round(emotional_score * 0.3, 4),
            "total_utility_index": round(weighted_utility, 4)
        }
