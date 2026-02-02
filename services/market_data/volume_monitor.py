import logging
import json
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional

logger = logging.getLogger(__name__)

class VolumeMonitor:
    """
    Phase 185.3: Volume Monitor & Promo Detector.
    Tracks Average Weekly Trading Volume and flags social media activity spikes.
    """
    
    def __init__(self):
        self.topic = "market_volume_v1"
        logger.info(f"VolumeMonitor initialized for topic: {self.topic}")

    def calculate_avg_weekly_volume(self, daily_volumes: List[int]) -> int:
        """
        Calculates the average weekly trading volume for the previous 4 weeks.
        Expects a list of 20 daily volume integers (approx 4 weeks).
        """
        if not daily_volumes:
            return 0
            
        avg_daily = sum(daily_volumes) / len(daily_volumes)
        avg_weekly = int(avg_daily * 5) # 5 trading days in a week
        
        logger.info(f"MARKET_LOG: Avg Weekly Volume calculated: {avg_weekly:,}")
        return avg_weekly

    def detect_promo_spike(self, ticker: str, current_vol: int, avg_vol: int, social_sentiment_score: float) -> Dict[str, Any]:
        """
        Phase 185.3: Volume Promo Detector.
        Identifies aggressive social media promotion intended to increase sellable volume.
        """
        # A spike is defined as current volume > 2x average AND high sentiment
        volume_ratio = current_vol / avg_vol if avg_vol > 0 else 1.0
        is_spike = volume_ratio > 2.0 and social_sentiment_score > 0.8
        
        logger.info(f"PROMO_LOG: {ticker} Spike detected: {is_spike} (Ratio: {volume_ratio:.2f}x, Sentiment: {social_sentiment_score})")
        
        return {
            "ticker": ticker,
            "is_promo_spike": is_spike,
            "volume_ratio": round(volume_ratio, 2),
            "social_sentiment": social_sentiment_score,
            "action": "FLAG_FOR_144_AUDIT" if is_spike else "NONE"
        }

    def process_volume_message(self, raw_message: str) -> Optional[Dict[str, Any]]:
        try:
            data = json.loads(raw_message)
            return self.detect_promo_spike(
                data["ticker"], 
                data["current_volume"], 
                data["avg_volume"], 
                data["sentiment"]
            )
        except Exception as e:
            logger.error(f"Failed to process volume message: {e}")
            return None
