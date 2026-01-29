import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

class ActiveShareGrader:
    """Grades managers based on Alpha delivery, with emphasis on down markets."""
    
    def grade_manager(self, avg_alpha: float, bear_market_alpha: float) -> str:
        """
        Grades: 
        - ALPHA_MASTER: Positive alpha > 2% and positive Bear Market Alpha.
        - GOOD: Positive alpha.
        - BENCHMARK_HUGGER: Alpha ~ 0.
        - LAGGARD: Negative alpha.
        """
        if avg_alpha > 0.02 and bear_market_alpha > 0:
            grade = "ALPHA_MASTER"
        elif abs(avg_alpha) < 0.005:
            grade = "BENCHMARK_HUGGER"
        elif avg_alpha > 0:
            grade = "GOOD"
        else:
            grade = "LAGGARD"
            
        logger.info(f"QUANT_LOG: Manager graded as {grade} (Alpha: {avg_alpha:.2%})")
        return grade
