import logging
from decimal import Decimal
from typing import Dict, Any, List

logger = logging.getLogger(__name__)

class BotMonitorService:
    """
    Analyzes social media (mocked data sources) to detect 'Inorganic' promo volume.
    Flags botnets and coordinated 'Pump' campaigns.
    """
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(BotMonitorService, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if hasattr(self, '_initialized') and self._initialized:
            return
        self._initialized = True
        logger.info("BotMonitorService initialized")

    def analyze_social_stream(
        self, 
        ticker: str, 
        mentions_count: int, 
        unique_authors_count: int,
        duplicate_msg_ratio: float
    ) -> Dict[str, Any]:
        """
        Policy: High volume + Low unique authors + High duplicates = BOTNET.
        """
        # Calculate 'Organic Ratio'
        if mentions_count == 0:
            return {"risk_score": 0, "status": "QUIET"}

        authors_per_mention = unique_authors_count / mentions_count
        
        # If 1000 mentions but only 10 authors -> 0.01 (Extremely suspicious)
        # If 1000 mentions and 900 authors -> 0.9 (Organic)
        
        suspicion_score = 0
        if authors_per_mention < 0.10:
            suspicion_score += 50
        elif authors_per_mention < 0.30:
            suspicion_score += 20
            
        if duplicate_msg_ratio > 0.80:
            suspicion_score += 40 # 80% of messages are identical copy-paste
            
        is_attack = suspicion_score > 60
        
        if is_attack:
            logger.warning(f"BOT_ALERT: {ticker} under PROMO ATTACK. Suspicion: {suspicion_score}")

        return {
            "ticker": ticker,
            "mentions": mentions_count,
            "organic_author_ratio": round(authors_per_mention, 2),
            "bot_suspicion_score": suspicion_score,
            "is_promo_attack": is_attack,
            "recommendation": "AVOID_TRADING" if is_attack else "MONITOR"
        }
