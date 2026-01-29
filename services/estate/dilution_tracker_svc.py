import logging
from decimal import Decimal
from typing import Dict, Any

logger = logging.getLogger(__name__)

class DilutionTrackerService:
    """
    Models inter-generational wealth dilution.
    'Shirt Sleeves to Shirt Sleeves' calculator: Wealth / Heirs = Per Capita Wealth.
    Ensures each subsequent generation can maintain the same Social Class.
    """
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(DilutionTrackerService, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if hasattr(self, '_initialized') and self._initialized:
            return
        self._initialized = True
        logger.info("DilutionTrackerService initialized")

    def calculate_generational_dilution(
        self, 
        current_wealth: Decimal, 
        heir_count: int, 
        generations: int
    ) -> Dict[str, Any]:
        """
        Policy: Wealth splits per generation.
        Gen 1: 1 person ($100M).
        Gen 2: 3 heirs ($33M each).
        Gen 3: 9 heirs ($11M each).
        """
        # Avoid division by zero or negative heirs
        if heir_count < 1:
            heir_count = 1
            
        # Calculate total descendants at the Nth generation
        # Formula: Heirs^(Generations - 1)
        # Gen 1 (Founder) -> Gen 2 (Heirs^1) -> Gen 3 (Heirs^2)
        total_descendants = heir_count ** (generations - 1)
        
        if total_descendants == 0:
            wealth_per_capita = current_wealth
        else:
            wealth_per_capita = current_wealth / Decimal(total_descendants)
        
        social_class_threshold = Decimal('10000000') # Minimum $10M to be 'UHNW' class
        
        status = "MAINTAINING_CLASS"
        if wealth_per_capita < social_class_threshold:
            status = "CLASS_DROP_RISK"
            
        logger.info(f"SCM_LOG: Gen {generations} Dilution. Heirs: {total_descendants}. Per Capita: ${wealth_per_capita:,.2f}")

        return {
            "generations_forward": generations,
            "total_heirs_estimated": total_descendants,
            "wealth_per_capita_future": round(wealth_per_capita, 2),
            "social_standing_status": status
        }
