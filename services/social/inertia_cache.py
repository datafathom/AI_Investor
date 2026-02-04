"""
Social Inertia Cache - Singleton for tracking sentiment momentum.
"""
from typing import Dict, Optional, List
from datetime import timezone, datetime, timedelta
import threading
import logging

logger = logging.getLogger(__name__)

class SocialInertiaCache:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super(SocialInertiaCache, cls).__new__(cls)
                cls._instance._initialized = False
            return cls._instance

    def __init__(self):
        if self._initialized:
            return
        self.inertia_data: Dict[str, Dict] = {}
        self.default_inertia = 0.1
        self._initialized = True
        logger.info("SocialInertiaCache initialized")

    def update_inertia(self, ticker: str, sentiment: float, velocity: float):
        """
        Update the inertia for a ticker.
        Inertia is a weighted move towards the current sentiment sentiment.
        """
        now = datetime.now(timezone.utc).isoformat()
        current = self.inertia_data.get(ticker, {
            "inertia": 0.0,
            "velocity": 0.0,
            "last_updated": now
        })

        # Simple exponential smoothing for inertia
        alpha = 0.2
        new_inertia = (alpha * sentiment) + ((1 - alpha) * current["inertia"])
        
        self.inertia_data[ticker] = {
            "inertia": round(new_inertia, 4),
            "velocity": velocity,
            "last_updated": now
        }

    def get_inertia(self, ticker: str) -> float:
        """Get current inertia (drift factor) for a ticker."""
        return self.inertia_data.get(ticker, {}).get("inertia", 0.0)

    def get_trending_tickers(self, limit: int = 10) -> List[str]:
        """Get tickers with the highest sentiment velocity."""
        sorted_tickers = sorted(
            self.inertia_data.keys(),
            key=lambda t: self.inertia_data[t]["velocity"],
            reverse=True
        )
        return sorted_tickers[:limit]

_inertia_cache = SocialInertiaCache()
def get_inertia_cache() -> SocialInertiaCache:
    return _inertia_cache
