"""
==============================================================================
FILE: models/social_trading.py
ROLE: Social Trading Data Models
PURPOSE: Pydantic models for social trading, copy trading, and trader
         following.

INTEGRATION POINTS:
    - SocialTradingService: Trader discovery
    - CopyTradingService: Copy trading execution
    - SocialTradingAPI: Social trading endpoints
    - FrontendSocial: Social trading dashboard

AUTHOR: AI Investor Team
CREATED: 2026-01-21
LAST_MODIFIED: 2026-01-21
==============================================================================
"""

from pydantic import BaseModel, Field
from datetime import datetime
from typing import Dict, List, Optional
from enum import Enum


class TraderRanking(str, Enum):
    """Trader ranking levels."""
    BRONZE = "bronze"
    SILVER = "silver"
    GOLD = "gold"
    PLATINUM = "platinum"
    DIAMOND = "diamond"


class TraderProfile(BaseModel):
    """Trader profile for social trading."""
    trader_id: str
    user_id: str
    display_name: str
    bio: Optional[str] = None
    ranking: TraderRanking = TraderRanking.BRONZE
    total_return: float = 0.0
    sharpe_ratio: float = 0.0
    win_rate: float = 0.0
    followers_count: int = 0
    is_public: bool = True
    created_date: datetime


class CopyTradingConfig(BaseModel):
    """Copy trading configuration."""
    config_id: str
    follower_id: str
    trader_id: str
    allocation_percentage: float = Field(..., ge=0, le=100)  # % of capital to copy
    risk_multiplier: float = 1.0  # Risk adjustment factor
    max_position_size: Optional[float] = None
    is_active: bool = True
    created_date: datetime
    updated_date: datetime


class CopyTrade(BaseModel):
    """Copy trade execution record."""
    copy_trade_id: str
    config_id: str
    original_trade_id: str
    symbol: str
    quantity: int
    price: float
    executed_date: datetime
    status: str  # "pending", "executed", "failed"
