"""
==============================================================================
FILE: models/orders.py
ROLE: Advanced Order Data Models
PURPOSE: Pydantic models for advanced order types, execution strategies, and
         order management.

INTEGRATION POINTS:
    - AdvancedOrderService: Order type management
    - SmartExecutionService: Execution algorithms
    - OrderAPI: Order endpoints
    - FrontendTrading: Order entry widgets

AUTHOR: AI Investor Team
CREATED: 2026-01-21
LAST_MODIFIED: 2026-01-21
==============================================================================
"""

from pydantic import BaseModel, Field
from datetime import datetime
from typing import Dict, List, Optional
from enum import Enum


class OrderType(str, Enum):
    """Advanced order types."""
    MARKET = "market"
    LIMIT = "limit"
    STOP = "stop"
    STOP_LIMIT = "stop_limit"
    TRAILING_STOP = "trailing_stop"
    BRACKET = "bracket"
    OCO = "oco"  # One-Cancels-Other
    OTO = "oto"  # One-Triggers-Other
    CONDITIONAL = "conditional"


class OrderStatus(str, Enum):
    """Order status."""
    PENDING = "pending"
    SUBMITTED = "submitted"
    PARTIALLY_FILLED = "partially_filled"
    FILLED = "filled"
    CANCELLED = "cancelled"
    REJECTED = "rejected"
    EXPIRED = "expired"


class TrailingStopOrder(BaseModel):
    """Trailing stop order definition."""
    order_id: str
    symbol: str
    quantity: int
    trailing_type: str  # "amount" or "percentage"
    trailing_value: float
    initial_stop_price: Optional[float] = None
    current_stop_price: Optional[float] = None
    highest_price: Optional[float] = None


class BracketOrder(BaseModel):
    """Bracket order with entry, profit target, and stop loss."""
    bracket_id: str
    entry_order_id: str
    profit_target_order_id: Optional[str] = None
    stop_loss_order_id: Optional[str] = None
    profit_target_price: Optional[float] = None
    stop_loss_price: Optional[float] = None


class ConditionalOrder(BaseModel):
    """Conditional order with trigger conditions."""
    order_id: str
    symbol: str
    quantity: int
    order_type: str  # Market, Limit, etc.
    condition_type: str  # "price", "time", "volume"
    condition_value: float
    triggered: bool = False


class ExecutionStrategy(str, Enum):
    """Execution strategy types."""
    MARKET = "market"
    TWAP = "twap"  # Time-Weighted Average Price
    VWAP = "vwap"  # Volume-Weighted Average Price
    IS = "implementation_shortfall"  # Implementation Shortfall
    ICEBERG = "iceberg"


class ExecutionResult(BaseModel):
    """Order execution result."""
    execution_id: str
    order_id: str
    filled_quantity: int
    average_price: float
    execution_time: datetime
    execution_strategy: str
    market_impact: Optional[float] = None
