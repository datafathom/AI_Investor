import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

class GlidePathRecommender529:
    """Recommends 529 plan allocations based on time to enrollment."""
    
    def recommend_allocation(self, years_to_enrollment: int) -> Dict[str, float]:
        """
        Conservative Glide Path Profile.
        """
        if years_to_enrollment >= 15:
            res = {"equity": 0.90, "fixed_income": 0.10, "cash": 0.00}
        elif years_to_enrollment >= 10:
            res = {"equity": 0.70, "fixed_income": 0.25, "cash": 0.05}
        elif years_to_enrollment >= 5:
            res = {"equity": 0.50, "fixed_income": 0.40, "cash": 0.10}
        elif years_to_enrollment >= 2:
            res = {"equity": 0.25, "fixed_income": 0.50, "cash": 0.25}
        else:
            res = {"equity": 0.10, "fixed_income": 0.40, "cash": 0.50}
            
        logger.info(f"529_LOG: Recommended {res['equity']*100}% equity for {years_to_enrollment} years out.")
        return res
