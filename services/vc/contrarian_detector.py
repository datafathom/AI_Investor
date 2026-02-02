import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

class ContrarianDetector:
    """
    Phase 165.4: Unconventional 'Diamond in the Rough' Engine.
    Detects deals that deviate from current herd bias.
    """
    
    def analyze_deal_sentiment(self, sector: str, current_hype_level: float) -> Dict[str, Any]:
        """
        Logic: Low hype + high tech maturity = Contrarian Opportunity.
        """
        # Hype level: 0.0 (None) to 1.0 (Peak AI Bubble)
        is_contrarian = current_hype_level < 0.3
        
        logger.info(f"VC_LOG: Analyzing {sector} (Hype: {current_hype_level}). Contrarian: {is_contrarian}")
        
        return {
            "sector": sector,
            "hype_level": current_hype_level,
            "is_contrarian_bet": is_contrarian,
            "recommendation": "INVEST_NOW" if is_contrarian else "WATCH_AND_WAIT"
        }
