"""
API Governance Service - Rate Limiting & Cost Control
Enforces quotas for external API providers to stay within Free Tier limits.
"""

import logging
import time
from typing import Dict, Any, Optional
from datetime import datetime
import asyncio

logger = logging.getLogger(__name__)

class APIGovernor:
    """
    Singleton service to track and throttle external API usage.
    """
    LIMITS = {
        "ALPHA_VANTAGE": {
            "per_minute": 5,
            "per_day": 25, # Strict Free Tier limit
        },
        "FRED": {
            "per_minute": 120,
            "per_day": 10000,
        },
        "GIVINGBLOCK": {
            "per_minute": 10,
            "per_day": 100,
        },
        "OPENAI": {
            "per_minute": 3,
            "per_day": 200,
        },
        "ANTHROPIC": {
            "per_minute": 3,
            "per_day": 200,
        },
        "GEMINI": {
            "per_minute": 15,
            "per_day": 1500,
        },
        "PERPLEXITY": {
            "per_minute": 5,
            "per_day": 500,
        },
        "REDDIT": {
            "per_minute": 100,
            "per_day": 10000,
        },
        "GOOGLE_TRENDS": {
            "per_minute": 5,
            "per_day": 200,
        },
        "SEC_EDGAR": {
            "per_minute": 600, # 10 per second
            "per_day": 10000,
        },
        "SOLANA": {
            "per_minute": 600, # 100 per 10 seconds
            "per_day": 10000,
        },
        # New vendors added
        "FACEBOOK": {
            "per_minute": 200,
            "per_day": 5000,
        },
        "STOCKTWITS": {
            "per_minute": 16, # 1000/hour
            "per_day": 16000, # 500k/month
        },
        "DISCORD": {
            "per_minute": 50,
            "per_day": 10000,
        },
        "YOUTUBE": {
            "per_minute": 100,
            "per_day": 10000, # 10k units/day
        },
        "QUANDL": {
            "per_minute": 30, # 300/10sec
            "per_day": 50000,
        },
        "NEWSAPI": {
            "per_minute": 1, # 100/day free tier
            "per_day": 100,
        },
        "TWILIO": {
            "per_minute": 100,
            "per_day": 1000,
        },
        "SENDGRID": {
            "per_minute": 10,
            "per_day": 100, # Free tier
        },
        "PLAID": {
            "per_minute": 10,
            "per_day": 200, # Free tier
        },
        "FINNHUB": {
            "per_minute": 30, # 30 calls/sec
            "per_day": 10000,
        },
        "GMAIL": {
            "per_minute": 250,
            "per_day": 25000,
        },
        "GOOGLE_CALENDAR": {
            "per_minute": 100,
            "per_day": 10000,
        },
    }


    def __init__(self):
        # State: {Provider: { "minute": [timestamps], "day_count": N, "last_reset_day": YYYY-MM-DD }}
        self._usage_stats: Dict[str, Dict] = {}
        logger.info("APIGovernor initialized")

    def _get_stats(self, provider: str) -> Dict:
        if provider not in self._usage_stats:
            self._usage_stats[provider] = {
                "minute": [],
                "day_count": 0,
                "last_reset_day": datetime.now().strftime("%Y-%m-%d")
            }
        
        # Reset daily count if day changed
        current_day = datetime.now().strftime("%Y-%m-%d")
        if self._usage_stats[provider]["last_reset_day"] != current_day:
            self._usage_stats[provider]["day_count"] = 0
            self._usage_stats[provider]["last_reset_day"] = current_day
            
        return self._usage_stats[provider]

    async def wait_for_slot(self, provider: str):
        """
        Async wait if we are hitting rate limits.
        """
        if provider not in self.LIMITS:
            return

        limit = self.LIMITS[provider]
        stats = self._get_stats(provider)

        # 1. Daily Limit Check
        if stats["day_count"] >= limit["per_day"]:
            logger.error(f"FATAL: DAILY API LIMIT REACHED FOR {provider}. Blocking all requests.")
            raise RuntimeError(f"Daily limit exceeded for {provider} ({limit['per_day']})")

        # 2. Minute Limit Check (Sliding Window)
        while True:
            now = time.time()
            # Clean old timestamps
            stats["minute"] = [t for t in stats["minute"] if now - t < 60]
            
            if len(stats["minute"]) < limit["per_minute"]:
                break
                
            # Wait a bit and check again
            logger.warning(f"RATE LIMIT: Throttling {provider} (Minute limit {limit['per_minute']} hit)")
            await asyncio.sleep(2)

    def report_usage(self, provider: str):
        """
        Call after a successful API request.
        """
        if provider not in self.LIMITS:
            return

        stats = self._get_stats(provider)
        stats["minute"].append(time.time())
        stats["day_count"] += 1
        
        logger.info(f"API USAGE [{provider}]: Minute: {len(stats['minute'])}/{self.LIMITS[provider]['per_minute']}, Day: {stats['day_count']}/{self.LIMITS[provider]['per_day']}")

# Singleton Instance
_governor: Optional[APIGovernor] = None

def get_governor() -> APIGovernor:
    global _governor
    if _governor is None:
        _governor = APIGovernor()
    return _governor
