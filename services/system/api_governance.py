"""
API Governance Service - Rate Limiting & Cost Control
Enforces quotas for external API providers to stay within Free Tier limits.
"""

import logging
import time
from typing import Dict, Any, Optional
from datetime import datetime
import asyncio
from utils.database_manager import db_manager

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
        self._load_from_db()
        logger.info("APIGovernor initialized with DB persistence")

    def _load_from_db(self):
        """Loads daily usage counts from the database."""
        try:
            with db_manager.pg_cursor() as cur:
                cur.execute("SELECT provider, day_used, last_reset_day FROM api_quotas")
                rows = cur.fetchall()
                current_day = datetime.now().strftime("%Y-%m-%d")
                
                for provider, day_used, last_reset in rows:
                    reset_str = last_reset.strftime("%Y-%m-%d") if last_reset else current_day
                    self._usage_stats[provider] = {
                        "minute": [],
                        "day_count": day_used if reset_str == current_day else 0,
                        "last_reset_day": current_day
                    }
                    
                    # Update DB if we reset the day
                    if reset_str != current_day:
                        cur.execute("""
                            UPDATE api_quotas 
                            SET day_used = 0, last_reset_day = %s 
                            WHERE provider = %s
                        """, (current_day, provider))
                        
        except Exception as e:
            logger.error(f"Failed to load API quotas from DB: {e}")

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
        Call after a successful API request. Persists to DB.
        """
        if provider not in self.LIMITS:
            return

        stats = self._get_stats(provider)
        stats["minute"].append(time.time())
        stats["day_count"] += 1
        
        # Persist to DB
        try:
             with db_manager.pg_cursor() as cur:
                 cur.execute("""
                    UPDATE api_quotas 
                    SET day_used = %s, total_calls_lifetime = total_calls_lifetime + 1, updated_at = NOW()
                    WHERE provider = %s
                 """, (stats["day_count"], provider))
        except Exception as e:
            logger.error(f"Failed to persist API usage for {provider}: {e}")

        logger.info(f"API USAGE [{provider}]: Minute: {len(stats['minute'])}/{self.LIMITS[provider]['per_minute']}, Day: {stats['day_count']}/{self.LIMITS[provider]['per_day']}")

    def get_all_stats(self) -> Dict[str, Any]:
        """
        Retrieves current usage statistics for all tracked API providers.
        """
        results = {}
        now = time.time()
        for provider, limit in self.LIMITS.items():
            stats = self._get_stats(provider)
            # Clean minute window for reporting
            current_minute_usage = len([t for t in stats["minute"] if now - t < 60])
            
            results[provider] = {
                "minute_used": current_minute_usage,
                "minute_limit": limit["per_minute"],
                "day_used": stats["day_count"],
                "day_limit": limit["per_day"],
                "percent_day": round((stats["day_count"] / limit["per_day"]) * 100, 2) if limit["per_day"] > 0 else 0,
                "status": "nominal"
            }
            
            if results[provider]["percent_day"] > 80:
                results[provider]["status"] = "critical"
            elif results[provider]["percent_day"] > 50:
                results[provider]["status"] = "warning"
                
        return results

# Singleton Instance
_governor: Optional[APIGovernor] = None

def get_governor() -> APIGovernor:
    global _governor
    if _governor is None:
        _governor = APIGovernor()
    return _governor
