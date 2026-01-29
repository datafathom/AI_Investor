import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

class CareerRiskScorer:
    """
    Calculates a career risk score to adjust target emergency fund size.
    Weights: Industry(25%), Income Stability(30%), Job Market(20%), Company(15%), Personal(10%)
    """
    
    def calculate_risk_factor(self, data: Dict[str, Any]) -> float:
        """Calculates factor from 0.5 (low risk) to 2.0 (high risk)."""
        industry_vol = data.get("industry_volatility", 0.5) # 0 to 1
        income_stability = data.get("income_stability", 0.5) # 0 to 1 (1 is stable)
        job_market_health = data.get("job_market_health", 0.5) # 0 to 1
        
        # Risk additions
        score = (industry_vol * 0.25) + ((1 - income_stability) * 0.30) + ((1 - job_market_health) * 0.20)
        
        # Map to multiplier (6 months base * factor)
        multiplier = 1.0 + (score * 2.0) # range roughly 1.0 to 2.5
        
        logger.info(f"CAREER_RISK: Calculated risk multiplier: {multiplier:.2f}")
        return round(multiplier, 2)
