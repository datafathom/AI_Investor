
import logging
from typing import Dict, Any, List

logger = logging.getLogger(__name__)

class PlanRecommender:
    """
    Recommends 529 plans based on state residency and tax benefits.
    """
    
    # Heuristic rules for 529 tax deductions (2024)
    STATE_RULES = {
        "NY": {"has_deduction": True, "limit": 10000.0, "parity": False},
        "PA": {"has_deduction": True, "limit": 18000.0, "parity": True},
        "FL": {"has_deduction": False, "limit": 0.0, "parity": True},
        "TX": {"has_deduction": False, "limit": 0.0, "parity": True},
        "UT": {"has_deduction": True, "limit": 4580.0, "parity": False}
    }
    
    def recommend_best_plan(self, residency_state: str) -> Dict[str, Any]:
        """
        Determines if an in-state or out-of-state plan is superior.
        """
        rules = self.STATE_RULES.get(residency_state, {"has_deduction": False, "parity": True})
        
        logger.info(f"529 Recommender: Residency={residency_state}, Deduction={rules['has_deduction']}")
        
        if rules["has_deduction"] and not rules["parity"]:
            return {
                "recommendation": f"In-State {residency_state} Plan",
                "benefit": f"Up to ${rules['limit']} state tax deduction.",
                "type": "TAX_OPTIMIZED_RESIDENT"
            }
            
        return {
            "recommendation": "Utah My529 or Vanguard NV 529",
            "benefit": "Lowest national fees and best investment selection.",
            "type": "NATIONAL_LOW_FEE"
        }
