import logging
from decimal import Decimal
from typing import Dict, Any
from services.retirement.match_calculator import MatchCalculator
from schemas.employer_match import EmployerMatchConfig

logger = logging.getLogger(__name__)

class MaxMatchCalculator:
    """Finds the optimal contribution to capture full match."""
    
    def __init__(self):
        self.match_calc = MatchCalculator()

    def find_optimal_contribution(self, salary: float, config: EmployerMatchConfig) -> Dict[str, Any]:
        # Simple iterative search for optimal %
        best_pct = 0.0
        max_match_found = 0.0
        
        # Test 1% to 20%
        for pct in [float(i) for i in range(1, 21)]:
            match = self.match_calc.calculate_match(salary, pct, config)
            if match > max_match_found:
                max_match_found = match
                best_pct = pct
            elif match == max_match_found and match > 0:
                # We reached the ceiling, don't need more
                break
                
        return {
            "optimal_contribution_pct": best_pct,
            "annual_match_received": max_match_found,
            "match_efficiency": round((max_match_found / (salary * best_pct / 100)) * 100, 2) if best_pct > 0 else 0
        }
