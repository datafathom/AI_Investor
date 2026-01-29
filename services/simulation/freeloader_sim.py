import logging
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

class FreeloaderSimulator:
    """Simulates market price efficiency as passive indexing adoption grows."""
    
    def simulate_efficiency_degradation(self, passive_adoption_pct: float) -> float:
        """
        Efficiency Score: 1.0 (perfect) to 0.0 (chaos).
        Model: Efficiency stays high until 70% adoption, then drops exponentially.
        """
        if passive_adoption_pct < 0.70:
            efficiency = 1.0 - (passive_adoption_pct * 0.1)
        else:
            # 70%+ -> rapid degradation
            efficiency = 0.93 - (passive_adoption_pct - 0.7)**2 * 10
            
        logger.info(f"SIM_LOG: Efficiency at {passive_adoption_pct*100}% passive: {efficiency:.2f}")
        return round(max(0, efficiency), 4)

    def suggest_active_pivot(self, current_efficiency: float) -> bool:
        """Suggests moving to active management when price discovery fails."""
        return current_efficiency < 0.8
