import logging
from decimal import Decimal
from typing import Dict, Any, List

logger = logging.getLogger(__name__)

class DilutionTracker:
    """
    Tracks 'Inter-Generational Dilution'.
    Calculates the 'Concentration Decay' of wealth as heirs multiply.
    """
    
    def estimate_dilution(self, 
                          current_wealth: Decimal, 
                          growth_rate: Decimal,
                          generations: int = 3) -> List[Dict[str, Any]]:
        """
        Projects wealth per capita assuming average 3 children per generation.
        """
        results = []
        heirs = 1
        wealth = current_wealth
        
        for g in range(generations + 1):
            per_capita = wealth / Decimal(str(heirs))
            results.append({
                "generation": g,
                "total_wealth": round(wealth, 2),
                "num_heirs": heirs,
                "wealth_per_capita": round(per_capita, 2),
                "status": "DYNASTIC" if per_capita > 25000000 else "UHNW" if per_capita > 5000000 else "DEGRADED"
            })
            
            # Next gen
            wealth = wealth * ((1 + growth_rate) ** 30) # 30 years between generations
            heirs *= 3 # Average 3 kids
            
        logger.info(f"Dilution: Estimated wealth per capita after {generations} generations.")
        return results
