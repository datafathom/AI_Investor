"""
==============================================================================
FILE: models/paper_trading.py
ROLE: Paper Trading Data Models
PURPOSE: Pydantic models for paper trading, simulation, and virtual portfolios.

INTEGRATION POINTS:
    - PaperTradingService: Virtual portfolio management
    - SimulationService: Historical replay
    - PaperTradingAPI: Paper trading endpoints
    - FrontendPaperTrading: Paper trading dashboard

AUTHOR: AI Investor Team
CREATED: 2026-01-21
LAST_MODIFIED: 2026-01-21
==============================================================================
"""

from pydantic import BaseModel, Field
from datetime import datetime
from typing import Dict, List, Optional
from enum import Enum


class PaperOrder(BaseModel):
    """Paper trading order."""
    order_id: str
    user_id: str
    symbol: str
    quantity: int
    order_type: str  # market, limit, stop
    price: Optional[float] = None
    status: str = "pending"  # pending, filled, cancelled
    filled_price: Optional[float] = None
    filled_quantity: int = 0
    commission: float = 0.0
    slippage: float = 0.0
    created_date: datetime


class VirtualPortfolio(BaseModel):
    """Virtual portfolio for paper trading."""
    portfolio_id: str
    user_id: str
    portfolio_name: str
    initial_cash: float
    current_cash: float
    total_value: float
    positions: Dict[str, Dict] = {}  # {symbol: {quantity, avg_price, current_price}}
    created_date: datetime
    updated_date: datetime


class SimulationResult(BaseModel):
    """Simulation/backtest result."""
    simulation_id: str
    strategy_name: str
    start_date: datetime
    end_date: datetime
    initial_capital: float
    final_capital: float
    total_return: float
    sharpe_ratio: float
    max_drawdown: float
    win_rate: float
    trades: List[Dict] = []
