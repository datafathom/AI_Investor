"""
==============================================================================
FILE: models/watchlist.py
ROLE: Watchlist & Alerts Data Models
PURPOSE: Pydantic models for watchlists, price alerts, and notification
         management.

INTEGRATION POINTS:
    - WatchlistService: Watchlist management
    - AlertService: Alert system
    - WatchlistAPI: Watchlist endpoints
    - FrontendWatchlist: Watchlist widgets

AUTHOR: AI Investor Team
CREATED: 2026-01-21
LAST_MODIFIED: 2026-01-21
==============================================================================
"""

from pydantic import BaseModel, Field
from datetime import datetime
from typing import Dict, List, Optional
from enum import Enum


class AlertType(str, Enum):
    """Alert types."""
    PRICE_ABOVE = "price_above"
    PRICE_BELOW = "price_below"
    PRICE_CHANGE = "price_change"
    VOLUME_SPIKE = "volume_spike"
    NEWS_ALERT = "news_alert"
    EARNINGS = "earnings"


class AlertStatus(str, Enum):
    """Alert status."""
    ACTIVE = "active"
    TRIGGERED = "triggered"
    CANCELLED = "cancelled"
    EXPIRED = "expired"


class Watchlist(BaseModel):
    """Watchlist definition."""
    watchlist_id: str
    user_id: str
    watchlist_name: str
    symbols: List[str] = []
    created_date: datetime
    updated_date: datetime


class PriceAlert(BaseModel):
    """Price alert definition."""
    alert_id: str
    user_id: str
    symbol: str
    alert_type: AlertType
    threshold: float
    current_price: Optional[float] = None
    status: AlertStatus = AlertStatus.ACTIVE
    notification_methods: List[str] = []  # email, push, sms
    created_date: datetime
    triggered_date: Optional[datetime] = None


class AlertHistory(BaseModel):
    """Alert trigger history."""
    history_id: str
    alert_id: str
    triggered_date: datetime
    trigger_value: float
    notification_sent: bool
