"""
==============================================================================
FILE: services/calendar/earnings_sync.py
ROLE: Earnings Calendar Sync Service
PURPOSE: Syncs upcoming earnings dates from market data to user's Google Calendar.
         Runs daily after market close to create/update earnings events.

INTEGRATION POINTS:
    - GoogleCalendarService: Creates calendar events
    - AlphaVantageService: Fetches earnings calendar
    - PortfolioService: Gets user's holdings

AUTHOR: AI Investor Team
CREATED: 2026-01-21
==============================================================================
"""

import logging
import asyncio
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


class EarningsSyncService:
    """
    Service for syncing earnings calendar events to Google Calendar.
    """
    
    def __init__(self, mock: bool = False):
        """
        Initialize earnings sync service.
        
        Args:
            mock: Use mock mode if True
        """
        self.mock = mock
        self._synced_events = {}  # Track synced events (event_id -> symbol)
    
    async def sync_earnings_for_user(
        self,
        user_id: str,
        access_token: str,
        holdings: List[str],
        days_ahead: int = 90
    ) -> Dict[str, Any]:
        """
        Sync earnings events for user's holdings.
        
        Args:
            user_id: User ID
            access_token: Google OAuth access token
            holdings: List of stock symbols user owns
            days_ahead: Number of days ahead to sync
            
        Returns:
            Dict with sync statistics
        """
        if self.mock:
            await asyncio.sleep(0.5)
            logger.info(f"[MOCK] Synced earnings for {len(holdings)} holdings")
            return {
                "events_created": len(holdings),
                "events_skipped": 0,
                "holdings_processed": len(holdings)
            }
        
        try:
            from services.calendar.google_calendar_service import get_calendar_service
            from services.data.alpha_vantage import get_alpha_vantage_client
            
            calendar_service = get_calendar_service()
            alpha_vantage = get_alpha_vantage_client()
            
            events_created = 0
            events_skipped = 0
            
            # Get earnings calendar
            end_date = datetime.now() + timedelta(days=days_ahead)
            earnings_data = await alpha_vantage.get_earnings_calendar(
                start_date=datetime.now().strftime("%Y-%m-%d"),
                end_date=end_date.strftime("%Y-%m-%d")
            )
            
            # Filter for user's holdings
            user_earnings = [
                e for e in earnings_data
                if e.get('symbol') in holdings
            ]
            
            # Create events for each earnings date
            for earnings in user_earnings:
                symbol = earnings.get('symbol')
                earnings_date = earnings.get('reportDate')
                
                if not symbol or not earnings_date:
                    continue
                
                # Check if event already exists
                event_key = f"{user_id}_{symbol}_{earnings_date}"
                if event_key in self._synced_events:
                    events_skipped += 1
                    continue
                
                # Parse earnings date
                try:
                    event_date = datetime.strptime(earnings_date, "%Y-%m-%d")
                    # Set time to market open (9:30 AM ET)
                    event_date = event_date.replace(hour=9, minute=30)
                except:
                    logger.warning(f"Invalid earnings date format: {earnings_date}")
                    continue
                
                # Create calendar event
                event_result = await calendar_service.create_event(
                    access_token=access_token,
                    title=f"{symbol} Earnings Call",
                    description=f"{symbol} is reporting earnings. Expected EPS: ${earnings.get('estimatedEPS', 'N/A')}",
                    start_time=event_date,
                    end_time=event_date + timedelta(hours=1),
                    event_type="earnings",
                    location="Virtual/Conference Call"
                )
                
                # Track synced event
                self._synced_events[event_key] = symbol
                events_created += 1
                
                logger.info(f"Created earnings event for {symbol} on {earnings_date}")
            
            return {
                "events_created": events_created,
                "events_skipped": events_skipped,
                "holdings_processed": len(holdings),
                "earnings_found": len(user_earnings)
            }
            
        except Exception as e:
            logger.error(f"Earnings sync failed: {e}", exc_info=True)
            raise RuntimeError(f"Failed to sync earnings: {str(e)}")
    
    async def sync_dividend_dates(
        self,
        user_id: str,
        access_token: str,
        holdings: List[Dict[str, Any]],
        days_ahead: int = 365
    ) -> Dict[str, Any]:
        """
        Sync dividend payment dates to calendar.
        
        Args:
            user_id: User ID
            access_token: Google OAuth access token
            holdings: List of holdings with symbol and dividend info
            days_ahead: Number of days ahead to sync
            
        Returns:
            Dict with sync statistics
        """
        if self.mock:
            await asyncio.sleep(0.3)
            return {
                "events_created": len(holdings),
                "events_skipped": 0
            }
        
        try:
            from services.calendar.google_calendar_service import get_calendar_service
            
            calendar_service = get_calendar_service()
            events_created = 0
            
            for holding in holdings:
                symbol = holding.get('symbol')
                dividend_date = holding.get('dividend_date')
                
                if not symbol or not dividend_date:
                    continue
                
                # Parse dividend date
                try:
                    event_date = datetime.strptime(dividend_date, "%Y-%m-%d")
                except:
                    continue
                
                # Create event
                await calendar_service.create_event(
                    access_token=access_token,
                    title=f"{symbol} Dividend Payment",
                    description=f"Dividend payment of ${holding.get('dividend_per_share', 'N/A')} per share",
                    start_time=event_date,
                    end_time=event_date + timedelta(hours=1),
                    event_type="dividend"
                )
                
                events_created += 1
            
            return {
                "events_created": events_created,
                "events_skipped": 0
            }
            
        except Exception as e:
            logger.error(f"Dividend sync failed: {e}")
            raise


# Singleton instance
_earnings_sync_service: Optional[EarningsSyncService] = None


def get_earnings_sync_service(mock: bool = True) -> EarningsSyncService:
    """
    Get singleton earnings sync service instance.
    
    Args:
        mock: Use mock mode if True
        
    Returns:
        EarningsSyncService instance
    """
    global _earnings_sync_service
    
    if _earnings_sync_service is None:
        _earnings_sync_service = EarningsSyncService(mock=mock)
        logger.info(f"Earnings sync service initialized (mock={mock})")
    
    return _earnings_sync_service
