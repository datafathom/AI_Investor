"""
Zen Mode: Disable Tactical Noise - Phase 95.
Filters out tactical noise for strategic clarity.
"""
import logging
from typing import Dict, Any, List

logger = logging.getLogger(__name__)

class TacticalNoiseFilter:
    """Filters tactical noise."""
    
    NOISE_SOURCES = ["DAILY_NEWS", "SOCIAL_MEDIA", "SHORT_TERM_ANALYSIS", "FOMO_SIGNALS"]
    
    def __init__(self):
        self.blocked_sources: List[str] = []
    
    def enable_zen(self):
        self.blocked_sources = self.NOISE_SOURCES.copy()
    
    def disable_zen(self):
        self.blocked_sources = []
    
    def should_filter(self, source: str) -> bool:
        return source in self.blocked_sources
