"""
==============================================================================
FILE: services/ai/briefing_generator.py
ROLE: Service Layer
PURPOSE: Orchestrates the generation of daily market briefings.
         Fetches data from various sources (Market, Social, News) and 
         feeds it to Gemini for synthesis.
         
INTEGRATION POINTS:
    - GeminiClient: Generates text.
    - BriefingStore: Frontend state.

AUTHOR: AI Investor Team
CREATED: 2026-01-22
==============================================================================
"""

import logging
import datetime
from services.ai.gemini_client import get_gemini_client

logger = logging.getLogger(__name__)

class BriefingGenerator:
    """
    Generates the daily briefing.
    """
    def __init__(self, mock: bool = True):
        self.mock = mock
        self.client = get_gemini_client(mock=mock)

    async def get_daily_briefing(self) -> dict:
        """
        Gets the briefing for today.
        """
        today = datetime.date.today()
        logger.info("Generating briefing for %s", today)

        return await self.client.generate_briefing(today)

class BriefingGeneratorSingleton:
    """Singleton wrapper for BriefingGenerator."""
    _instance = None

    @classmethod
    def get_instance(cls, mock: bool = True) -> BriefingGenerator:
        """Returns the singleton instance of BriefingGenerator."""
        if cls._instance is None:
            cls._instance = BriefingGenerator(mock=mock)
        return cls._instance

def get_briefing_generator(mock: bool = True) -> BriefingGenerator:
    """Legacy helper to get the briefing generator instance."""
    return BriefingGeneratorSingleton.get_instance(mock=mock)
