"""
==============================================================================
FILE: services/social/discord_bot.py
ROLE: Community Alpha Scout
PURPOSE: Monitors Discord channels for ticker mentions and sentiment signals.
         Mocks functionality for Phase 28.

AUTHOR: AI Investor Team
CREATED: 2026-01-22
==============================================================================
"""

import logging
import asyncio
import random
from typing import Dict, Any, List, Optional
from datetime import timezone, datetime
from services.system.secret_manager import get_secret_manager
from services.social.inertia_cache import get_inertia_cache

logger = logging.getLogger(__name__)

class DiscordBot:
    """
    Discord Bot Service for monitoring trading communities.
    Defaults to MOCK MODE for Phase 28.
    """
    
    def __init__(self, bot_token: Optional[str] = None, mock: bool = True):
        self.mock = mock
        sm = get_secret_manager()
        self.bot_token = bot_token or sm.get_secret('DISCORD_BOT_TOKEN')
        # Channels can be configured via env (comma-separated)
        channels_env = sm.get_secret('DISCORD_MONITORED_CHANNELS', '#general,#trading-floor,#alpha-sigs')
        self.connected_channels = [ch.strip() for ch in channels_env.split(',')]

    async def connect(self) -> bool:
        """Establish connection to Discord Gateway."""
        if self.mock:
            await asyncio.sleep(0.5)
            logger.info("Discord Bot connected to Gateway (Mock)")
            return True
        return False

    async def get_recent_mentions(self, ticker: str, limit: int = 50) -> List[Dict[str, Any]]:
        """Scout channels for ticker mentions."""
        if self.mock:
            await asyncio.sleep(0.3)
            messages = [
                f"Anyone seeing the breakout on ${ticker}?",
                f"Loading more ${ticker} here, order flow looks massive.",
                f"${ticker} is a total trap, watch out for the dump.",
                f"Wait for the retest on ${ticker} before going long.",
                f"The community sentiment is shift bullish on ${ticker}."
            ]
            
            mentions = []
            for i in range(5):
                mentions.append({
                    "id": f"msg_{random.randint(1000, 9999)}",
                    "channel": random.choice(self.connected_channels),
                    "author": f"trader_alpha_{random.randint(1,10)}",
                    "content": random.choice(messages),
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                    "sentiment": random.choice(["Bullish", "Bearish", "Neutral"])
                })
            return mentions
        return []

    async def get_hype_score(self, ticker: str) -> Dict[str, Any]:
        """Calculate hype metrics based on Discord activity."""
        if self.mock:
            score = random.uniform(-0.2, 0.8)
            velocity = random.randint(10, 500)
            
            # Update shared inertia cache
            cache = get_inertia_cache()
            cache.update_inertia(ticker.upper(), score, velocity)
            
            return {
                "ticker": ticker.upper(),
                "velocity": velocity, # Mentions per hour
                "growth_pct": round(random.uniform(5, 50), 2),
                "hot_channels": ["#trading-floor", "#alpha-sigs"],
                "last_updated": datetime.now(timezone.utc).isoformat()
            }
        return {}

_instance = None

def get_discord_bot(mock: bool = True) -> DiscordBot:
    global _instance
    if _instance is None:
        _instance = DiscordBot(mock=mock)
    return _instance
