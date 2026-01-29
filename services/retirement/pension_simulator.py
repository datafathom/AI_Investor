import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

class PensionSimulator:
    """Simulates pension sustainability and payment reliability."""
    
    def simulate_payout_risk(self, funding_ratio: float, credit_rating: str) -> Dict[str, Any]:
        """
        Calculates the probability of benefit reduction.
        """
        # Base risk from funding status (Ideal is > 0.8)
        funding_risk = 1.0 - funding_ratio if funding_ratio < 0.8 else 0.0
        
        # Credit rating penalty (Simplified)
        rating_penalty = 0.0
        if credit_rating in ["B", "C", "D"]: rating_penalty = 0.4
        elif credit_rating == "BBB": rating_penalty = 0.1
        
        failure_prob = min(1.0, funding_risk + rating_penalty)
        
        logger.info(f"PENSION_LOG: Simulation for ratio {funding_ratio:.2f} ({credit_rating}) -> Failure Risk: {failure_prob:.2%}")
        
        return {
            "is_sustainable": failure_prob < 0.2,
            "failure_probability": round(failure_prob, 4),
            "recommendation": "PLAN_FOR_REDUCTION" if failure_prob > 0.3 else "CORE_FIXED_INCOME"
        }
