"""
==============================================================================
FILE: models/strategy.py
ROLE: Strategy Data Models
PURPOSE: Pydantic models for algorithmic trading strategies, rules, and
         execution.

INTEGRATION POINTS:
    - StrategyBuilderService: Strategy creation
    - StrategyExecutionService: Live strategy execution
    - StrategyAPI: Strategy endpoints
    - FrontendStrategy: Strategy builder widgets

AUTHOR: AI Investor Team
CREATED: 2026-01-21
LAST_MODIFIED: 2026-01-21
==============================================================================
"""

from pydantic import BaseModel, Field
from datetime import datetime
from typing import Dict, List, Optional, Any
from enum import Enum


class StrategyStatus(str, Enum):
    """Strategy execution status."""
    DRAFT = "draft"
    ACTIVE = "active"
    PAUSED = "paused"
    STOPPED = "stopped"
    ERROR = "error"


class ConditionType(str, Enum):
    """Condition types for strategy rules."""
    PRICE = "price"
    VOLUME = "volume"
    INDICATOR = "indicator"
    TIME = "time"
    CUSTOM = "custom"


class StrategyRule(BaseModel):
    """Strategy rule definition."""
    rule_id: str
    condition_type: ConditionType
    condition: Dict[str, Any]  # Condition parameters
    action: Dict[str, Any]  # Action to take when condition is met
    priority: int = 0


class TradingStrategy(BaseModel):
    """Trading strategy definition."""
    strategy_id: str
    user_id: str
    strategy_name: str
    description: Optional[str] = None
    rules: List[StrategyRule] = []
    status: StrategyStatus = StrategyStatus.DRAFT
    portfolio_id: Optional[str] = None
    risk_limits: Dict[str, float] = {}  # {limit_type: value}
    created_date: datetime
    updated_date: datetime
    last_executed: Optional[datetime] = None


class StrategyExecution(BaseModel):
    """Strategy execution record."""
    execution_id: str
    strategy_id: str
    rule_id: str
    action_taken: str
    order_id: Optional[str] = None
    execution_time: datetime
    result: str  # "success", "failed", "skipped"


class StrategyPerformance(BaseModel):
    """Strategy performance metrics."""
    strategy_id: str
    total_trades: int
    winning_trades: int
    losing_trades: int
    win_rate: float
    total_pnl: float
    sharpe_ratio: float
    max_drawdown: float
    current_status: StrategyStatus
