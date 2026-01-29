import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

class MoatScoreService:
    """
    Scores the competitive advantage ('Moat') of a company.
    Based on Gross Margin Stability, ROIC, and Market Share.
    """
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(MoatScoreService, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if hasattr(self, '_initialized') and self._initialized:
            return
        self._initialized = True
        logger.info("MoatScoreService initialized")

    def calculate_moat_score(self, financials: Dict[str, Any]) -> Dict[str, Any]:
        """
        Logic:
        - Gross Margin > 40% is good.
        - ROIC > 15% is good.
        - Stability (simulated) helps.
        """
        gross_margin = financials.get('gross_margin', 0.20)
        roic = financials.get('roic', 0.10)
        
        score = 0
        moat_rating = "NONE"
        
        if gross_margin > 0.40:
            score += 3
        elif gross_margin > 0.20:
            score += 1
            
        if roic > 0.15:
            score += 4
        elif roic > 0.08:
            score += 2
            
        if score >= 6:
            moat_rating = "WIDE"
        elif score >= 3:
            moat_rating = "NARROW"
            
        logger.info(f"Moat Scorer: Rating {moat_rating} (Score {score}) for asset.")
        
        return {
            "moat_rating": moat_rating,
            "moat_score": score,
            "rationale": f"GM: {gross_margin:.1%}, ROIC: {roic:.1%}"
        }
