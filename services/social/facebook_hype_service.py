"""
==============================================================================
FILE: services/social/facebook_hype_service.py
ROLE: Facebook Hype Ingestion Service
PURPOSE: Monitors Facebook pages and groups for stock ticker mentions,
         aggregates mention counts hourly, and triggers alerts on spikes.

INTEGRATION POINTS:
    - FacebookAuthService: Access token management
    - HypeTrackerService: Spike alert delivery
    - Graph API: Page post monitoring

AUTHOR: AI Investor Team
CREATED: 2026-01-21
==============================================================================
"""

import logging
import asyncio
import re
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
from collections import defaultdict

logger = logging.getLogger(__name__)

try:
    import httpx
    HTTPX_AVAILABLE = True
except ImportError:
    HTTPX_AVAILABLE = False
    logger.warning("httpx not installed. Install with: pip install httpx")


class FacebookHypeService:
    """
    Service for monitoring Facebook pages/groups for stock ticker mentions.
    """
    
    # Graph API endpoint
    GRAPH_API_BASE = "https://graph.facebook.com/v18.0"
    
    # Ticker pattern (matches $AAPL, AAPL, etc.)
    TICKER_PATTERN = re.compile(r'\$?([A-Z]{1,5})\b')
    
    def __init__(self, mock: bool = False):
        """
        Initialize Facebook hype service.
        
        Args:
            mock: Use mock mode if True
        """
        self.mock = mock
        self._mention_counts = defaultdict(lambda: defaultdict(int))  # page_id -> ticker -> count
        self._last_check = {}
    
    async def monitor_page(
        self,
        page_id: str,
        access_token: str,
        tickers: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Monitor a Facebook page for stock ticker mentions.
        
        Args:
            page_id: Facebook page ID
            access_token: Facebook access token with pages_read_engagement
            tickers: Optional list of specific tickers to monitor
            
        Returns:
            Dict with mention counts per ticker
        """
        if self.mock:
            await asyncio.sleep(0.3)
            # Generate mock mentions
            mock_tickers = tickers or ["AAPL", "MSFT", "GOOGL", "TSLA", "NVDA"]
            mentions = {}
            for ticker in mock_tickers:
                mentions[ticker] = asyncio.get_event_loop().time() % 10  # Random count
            
            logger.info(f"[MOCK] Monitored page {page_id}, found {sum(mentions.values())} mentions")
            return {
                "page_id": page_id,
                "mentions": mentions,
                "checked_at": datetime.now().isoformat()
            }
        
        if not HTTPX_AVAILABLE:
            raise RuntimeError("httpx not available")
        
        try:
            async with httpx.AsyncClient() as client:
                # Get recent posts from page
                response = await client.get(
                    f"{self.GRAPH_API_BASE}/{page_id}/posts",
                    params={
                        "access_token": access_token,
                        "fields": "message,created_time",
                        "limit": 100
                    }
                )
                response.raise_for_status()
                data = response.json()
                
                posts = data.get("data", [])
                mentions = defaultdict(int)
                
                # Scan posts for ticker mentions
                for post in posts:
                    message = post.get("message", "")
                    found_tickers = self._extract_tickers(message)
                    
                    for ticker in found_tickers:
                        if not tickers or ticker in tickers:
                            mentions[ticker] += 1
                
                # Update aggregated counts
                for ticker, count in mentions.items():
                    self._mention_counts[page_id][ticker] += count
                
                self._last_check[page_id] = datetime.now()
                
                logger.info(f"Monitored page {page_id}, found {sum(mentions.values())} mentions")
                
                return {
                    "page_id": page_id,
                    "mentions": dict(mentions),
                    "total_posts_scanned": len(posts),
                    "checked_at": datetime.now().isoformat()
                }
                
        except Exception as e:
            logger.error(f"Failed to monitor page {page_id}: {e}")
            raise RuntimeError(f"Failed to monitor Facebook page: {str(e)}")
    
    def _extract_tickers(self, text: str) -> List[str]:
        """
        Extract stock ticker symbols from text.
        
        Args:
            text: Text to scan
            
        Returns:
            List of ticker symbols found
        """
        matches = self.TICKER_PATTERN.findall(text.upper())
        # Filter out common false positives
        false_positives = {"THE", "AND", "FOR", "ARE", "BUT", "NOT", "YOU", "ALL", "CAN", "HER", "WAS", "ONE", "OUR", "OUT", "DAY", "GET", "HAS", "HIM", "HIS", "HOW", "ITS", "MAY", "NEW", "NOW", "OLD", "SEE", "TWO", "WAY", "WHO", "BOY", "DID", "ITS", "LET", "PUT", "SAY", "SHE", "TOO", "USE"}
        return [ticker for ticker in matches if ticker not in false_positives]
    
    async def get_hourly_aggregates(
        self,
        page_id: Optional[str] = None,
        ticker: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Get hourly aggregated mention counts.
        
        Args:
            page_id: Optional page ID filter
            ticker: Optional ticker filter
            
        Returns:
            Dict with aggregated counts
        """
        if self.mock:
            await asyncio.sleep(0.1)
            return {
                "hourly_aggregates": {
                    "AAPL": 45,
                    "MSFT": 32,
                    "GOOGL": 28
                },
                "period": "last_hour",
                "aggregated_at": datetime.now().isoformat()
            }
        
        # Aggregate counts from last hour
        aggregates = defaultdict(int)
        
        for pid, ticker_counts in self._mention_counts.items():
            if page_id and pid != page_id:
                continue
            
            for t, count in ticker_counts.items():
                if ticker and t != ticker:
                    continue
                aggregates[t] += count
        
        return {
            "hourly_aggregates": dict(aggregates),
            "period": "last_hour",
            "aggregated_at": datetime.now().isoformat()
        }
    
    async def check_for_spikes(
        self,
        page_id: str,
        ticker: str,
        threshold_multiplier: float = 2.0
    ) -> Optional[Dict[str, Any]]:
        """
        Check if mention count has spiked above threshold.
        
        Args:
            page_id: Page ID to check
            ticker: Ticker symbol
            threshold_multiplier: Multiplier for spike detection (default 2x)
            
        Returns:
            Alert dict if spike detected, None otherwise
        """
        if self.mock:
            await asyncio.sleep(0.1)
            # Randomly generate spike
            if asyncio.get_event_loop().time() % 3 == 0:
                return {
                    "alert": "spike_detected",
                    "page_id": page_id,
                    "ticker": ticker,
                    "current_count": 50,
                    "baseline": 20,
                    "spike_multiplier": 2.5,
                    "detected_at": datetime.now().isoformat()
                }
            return None
        
        current_count = self._mention_counts[page_id].get(ticker, 0)
        
        # Calculate baseline (average of last 24 hours)
        # In production, this would use historical data
        baseline = current_count / 2  # Mock baseline
        
        if current_count >= baseline * threshold_multiplier:
            return {
                "alert": "spike_detected",
                "page_id": page_id,
                "ticker": ticker,
                "current_count": current_count,
                "baseline": baseline,
                "spike_multiplier": current_count / baseline if baseline > 0 else 0,
                "detected_at": datetime.now().isoformat()
            }
        
        return None


# Singleton instance
_facebook_hype_service: Optional[FacebookHypeService] = None


def get_facebook_hype_service(mock: bool = True) -> FacebookHypeService:
    """
    Get singleton Facebook hype service instance.
    
    Args:
        mock: Use mock mode if True
        
    Returns:
        FacebookHypeService instance
    """
    global _facebook_hype_service
    
    if _facebook_hype_service is None:
        _facebook_hype_service = FacebookHypeService(mock=mock)
        logger.info(f"Facebook hype service initialized (mock={mock})")
    
    return _facebook_hype_service
