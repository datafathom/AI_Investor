import logging
from decimal import Decimal
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

class CLEWIndexService:
    """
    Calculates the 'Cost of Living Extremely Well' (CLEW) Index.
    This is the personal inflation rate for UHNW individuals, often 2-3x CPI.
    Tracks tuition, concierge medicine, private aviation, luxury travel etc.
    """
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(CLEWIndexService, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if hasattr(self, '_initialized') and self._initialized:
            return
        self._initialized = True
        # Demo basket
        self.basket = [
            {"name": "Tuition", "weight_pct": 0.25, "annual_inflation_rate": 0.07},
            {"name": "Staff/Concierge", "weight_pct": 0.20, "annual_inflation_rate": 0.05},
            {"name": "Private Aviation", "weight_pct": 0.30, "annual_inflation_rate": 0.12},
            {"name": "Luxury R/E", "weight_pct": 0.25, "annual_inflation_rate": 0.08}
        ]
        logger.info("CLEWIndexService initialized")

    def calculate_current_index(self) -> float:
        """Sum of weights * inflation as a baseline 100-indexed value (simplified)"""
        return 142.5 # Mocking current index level

    def get_uhnwi_inflation_rate(self) -> float:
        """Returns the weighted average inflation rate of the basket."""
        res = self.calculate_personal_inflation(self.basket)
        return float(res["clew_index_rate"])

    def calculate_personal_inflation(self, basket: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Policy: CLEW = Sum(Weight_i * Inflation_i).
        Basket items: Tuition (7%), Health (6%), Aviation (4%), General (3%).
        """
        personal_inflation = Decimal('0')
        total_weight = Decimal('0')
        
        for item in basket:
            weight = Decimal(str(item.get('weight_pct', 0)))
            inflation = Decimal(str(item.get('annual_inflation_rate', 0)))
            
            personal_inflation += weight * inflation
            total_weight += weight
            
        # Normalize if weights don't sum to 1.0 (though UI should enforce)
        if total_weight > 0 and total_weight != 1:
            personal_inflation = personal_inflation / total_weight
            
        logger.info(f"SCM_LOG: Calculated UHNW Inflation (CLEW): {personal_inflation:.2%}")
        
        return {
            "clew_index_rate": round(personal_inflation, 4),
            "basket_items_count": len(basket),
            "is_above_cpi": personal_inflation > Decimal('0.035') # Assuming 3.5% baseline CPI
        }

def get_clew_index_service() -> CLEWIndexService:
    """
    Singleton getter for CLEWIndexService.
    """
    return CLEWIndexService()
