"""
Toxic Liquidity Detection Service.
Monitors the ecosystem for high-risk liquidity conditions.
"""
import logging
from typing import Dict, Any, List
from services.risk.liquidity_validator import LiquidityValidator

logger = logging.getLogger(__name__)

class ToxicLiquidityDetector:
    """
    Identifies hazardous market conditions like flash crashes or liquidity voids.
    """

    @staticmethod
    def is_environment_toxic(books: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Evaluate a collection of books for systemic risk.
        If multiple majors fail liquidity thresholds simultaneously, it's toxic.
        """
        fails = 0
        total_majors = 0
        fail_reasons = []

        for book in books:
            # Only check majors for systemic toxic environment
            if book['symbol'] in ['EUR/USD', 'GBP/USD', 'USD/JPY']:
                total_majors += 1
                check = LiquidityValidator.is_safe_to_execute(book)
                if not check['safe']:
                    fails += 1
                    fail_reasons.append(f"{book['symbol']}: {check['reason']}")

        is_toxic = (fails / total_majors) > 0.5 if total_majors > 0 else False
        
        if is_toxic:
            logger.critical("SYSTEMIC TOXIC LIQUIDITY DETECTED: %s", " | ".join(fail_reasons))

        return {
            'is_toxic': is_toxic,
            'failed_count': fails,
            'total_checked': total_majors,
            'details': fail_reasons
        }
