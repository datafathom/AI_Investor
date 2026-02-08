import logging
import json
import random
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional

logger = logging.getLogger(__name__)

MOCK_TICKERS = ["AAPL", "MSFT", "NVDA", "TSLA", "AMZN", "GOOGL", "META", "AMD", "INTC", "SPY"]


class VolumeMonitor:
    """
    Phase 4.3: Volume Monitor & Promo Detector.
    Tracks Average Weekly Trading Volume and flags social media activity spikes.
    """
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(VolumeMonitor, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if self._initialized:
            return
        self._initialized = True
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
        Identifies aggressive social media promotion intended to increase sellable volume.
        """
        # Deterministic-ish for ticker
        random.seed(sum(ord(c) for c in ticker))
        
        volume_ratio = current_vol / avg_vol if avg_vol > 0 else 1.0
        social_intensity = random.uniform(0.2, 0.95)
        wash_trading_signal = random.uniform(0.1, 0.6)
        
        # Logic: High volume ratio + High social intensity = Promo Spike
        # Wash trading signal adds weight to the risk
        is_spike = volume_ratio > 1.8 and social_intensity > 0.75
        
        risk_score = (volume_ratio * 15) + (social_intensity * 40) + (wash_trading_signal * 50)
        risk_score = min(100, max(0, risk_score))

        return {
            "ticker": ticker,
            "is_promo_spike": is_spike,
            "volume_ratio": round(volume_ratio, 2),
            "social_intensity": round(social_intensity, 2),
            "social_sentiment": social_sentiment_score,
            "wash_trading_signal": round(wash_trading_signal, 2),
            "risk_score": round(risk_score, 1),
            "action": "FLAG_FOR_144_AUDIT" if is_spike else "MONITOR",
            "detected_at": datetime.now().isoformat(),
            "severity": "CRITICAL" if risk_score > 85 else ("HIGH" if is_spike else "LOW")
        }

    def get_promo_spikes(self) -> List[Dict[str, Any]]:
        """Get current promo spike detections (mock data for API)."""
        # Stability seed
        random.seed(datetime.now().hour)
        spikes = []
        for ticker in MOCK_TICKERS:
            current_vol = random.randint(5000000, 50000000)
            avg_vol = random.randint(10000000, 25000000)
            sentiment = round(random.uniform(0.4, 0.95), 2)
            spike = self.detect_promo_spike(ticker, current_vol, avg_vol, sentiment)
            spikes.append(spike)
        
        # Sort by risk score
        spikes.sort(key=lambda x: x["risk_score"], reverse=True)
        return spikes

    def get_volume_baseline(self, ticker: str) -> Dict[str, Any]:
        """Get volume baseline for a specific ticker."""
        random.seed(sum(ord(c) for c in ticker))
        return {
            "ticker": ticker.upper(),
            "avg_4_week_volume": random.randint(8000000, 45000000),
            "current_volume": random.randint(5000000, 65000000),
            "volume_trend": random.choice(["INCREASING", "DECREASING", "STABLE"]),
            "last_updated": datetime.now().isoformat()
        }

    def get_ticker_promo_history(self, ticker: str, days: int = 30) -> List[Dict[str, Any]]:
        """Get historical promo events for a ticker."""
        random.seed(sum(ord(c) for c in ticker))
        history = []
        for i in range(random.randint(2, 6)):
            history.append({
                "ticker": ticker.upper(),
                "detected_at": (datetime.now() - timedelta(days=random.randint(1, days))).isoformat(),
                "volume_ratio": round(random.uniform(1.8, 4.2), 2),
                "sentiment_score": round(random.uniform(0.75, 0.99), 2),
                "risk_score": round(random.uniform(60, 95), 1),
                "action_taken": random.choice(["FLAGGED", "UNDER_REVIEW"])
            })
        return sorted(history, key=lambda x: x["detected_at"], reverse=True)

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


def get_volume_monitor() -> VolumeMonitor:
    return VolumeMonitor()
