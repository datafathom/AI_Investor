import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

class CoverageAnalyzer:
    """Analyzes cash reserves against expense coverage requirements."""
    
    def determine_tier(self, months_coverage: float) -> str:
        if months_coverage < 3:
            return "CRITICAL"
        elif months_coverage < 6:
            return "LOW"
        elif months_coverage < 12:
            return "ADEQUATE"
        elif months_coverage < 24:
            return "STRONG"
        else:
            return "FORTRESS"

    def calculate_survival_probability(self, months: float, market_volatility: float) -> float:
        """Estimates probability of avoiding liquidation for X months."""
        # Simplified probability model
        prob = min(0.99, (months / 12) * (1 - market_volatility))
        return round(max(0.1, prob), 2)
