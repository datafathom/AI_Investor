import logging
from typing import Dict, Any
from schemas.financial_plan import FinancialPlan

logger = logging.getLogger(__name__)

class ComplexityAnalyzer:
    """Analyzes planning complexity to determine AI vs. Human routing."""
    
    def analyze_complexity(self, user_data: Dict[str, Any]) -> float:
        """
        Score: 0.0 (Simple) to 1.0 (Hyper-Complex).
        Factors: Net Worth, Multi-Jurisdiction, Trust complexity, business ownership.
        """
        score = 0.1
        
        if user_data.get("net_worth", 0) > 10000000: score += 0.4
        if user_data.get("has_business", False): score += 0.2
        if user_data.get("international_assets", False): score += 0.3
        
        logger.info(f"PLANNING_LOG: Complexity score calculated: {score:.2f}")
        return round(min(1.0, score), 2)

    def requires_human(self, score: float) -> bool:
        """Threshold for AI-only planning is 0.6."""
        return score > 0.6
