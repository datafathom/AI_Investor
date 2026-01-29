import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

class TradabilityClassifier:
    """Classifies international indices by liquidity and capital controls."""
    
    def calculate_tradability_score(self, ticker: str, avg_volume: float, aum: float, country_risk: float) -> Dict[str, Any]:
        """
        Calculates a score from 0 to 100.
        Factors: Volume/AUM ratio, Country Repatriation Risk.
        """
        liq_ratio = (avg_volume / aum) if aum > 0 else 0
        
        # Simplified scoring logic
        score = 80 # Baseline
        if liq_ratio < 0.01: score -= 30
        if country_risk > 5: score -= 20
        
        tier = "HIGHLY_LIQUID" if score >= 80 else "LIQUID" if score >= 60 else "MODERATE" if score >= 40 else "ILLIQUID"
        
        logger.info(f"TRADABILITY_LOG: {ticker} classified as {tier} (Score: {score})")
        return {
            "ticker": ticker,
            "score": score,
            "tier": tier,
            "is_restricted": score < 20
        }
