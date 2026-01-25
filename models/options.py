"""
==============================================================================
FILE: models/options.py
ROLE: Options Data Models
PURPOSE: Pydantic models for options strategies, Greeks, and analytics.

INTEGRATION POINTS:
    - OptionsStrategyBuilderService: Strategy construction
    - OptionsAnalyticsService: Greeks and P&L analysis
    - OptionsAPI: API response models
    - FrontendOptions: Options dashboard widgets

AUTHOR: AI Investor Team
CREATED: 2026-01-21
LAST_MODIFIED: 2026-01-21
==============================================================================
"""

from pydantic import BaseModel, Field
from datetime import datetime
from typing import Dict, List, Optional
from enum import Enum


class OptionType(str, Enum):
    """Option type."""
    CALL = "call"
    PUT = "put"


class OptionAction(str, Enum):
    """Option action."""
    BUY = "buy"
    SELL = "sell"


class OptionLeg(BaseModel):
    """Single option leg in a strategy."""
    symbol: str
    option_type: OptionType
    action: OptionAction
    strike: float
    expiration: datetime
    quantity: int
    premium: Optional[float] = None


class OptionsStrategy(BaseModel):
    """Multi-leg options strategy."""
    strategy_id: str
    strategy_name: str
    underlying_symbol: str
    legs: List[OptionLeg]
    net_cost: float
    max_profit: Optional[float] = None
    max_loss: Optional[float] = None
    breakeven_points: List[float] = []
    created_date: datetime
    strategy_type: str  # e.g., "covered_call", "straddle", "custom"


class Greeks(BaseModel):
    """Option Greeks."""
    delta: float
    gamma: float
    theta: float
    vega: float
    rho: Optional[float] = None


class StrategyGreeks(BaseModel):
    """Greeks for entire strategy."""
    strategy_id: str
    total_delta: float
    total_gamma: float
    total_theta: float
    total_vega: float
    total_rho: Optional[float] = None
    leg_greeks: Dict[str, Greeks] = {}  # {leg_id: Greeks}


class StrategyPnL(BaseModel):
    """P&L analysis for strategy."""
    strategy_id: str
    underlying_price: float
    days_to_expiration: int
    profit_loss: float
    profit_loss_pct: float
    intrinsic_value: float
    time_value: float


class StrategyAnalysis(BaseModel):
    """Complete strategy analysis."""
    strategy: OptionsStrategy
    greeks: StrategyGreeks
    pnl: StrategyPnL
    probability_profit: Optional[float] = None
    implied_volatility: Optional[float] = None
