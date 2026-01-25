"""
==============================================================================
FILE: models/optimization.py
ROLE: Optimization Data Models
PURPOSE: Pydantic models for portfolio optimization and rebalancing.

INTEGRATION POINTS:
    - PortfolioOptimizerService: Optimization results
    - RebalancingService: Rebalancing recommendations
    - OptimizationAPI: API response models
    - FrontendOptimization: Dashboard widgets

AUTHOR: AI Investor Team
CREATED: 2026-01-21
LAST_MODIFIED: 2026-01-21
==============================================================================
"""

from pydantic import BaseModel, Field
from datetime import datetime
from typing import Dict, List, Optional, Any
from enum import Enum


class OptimizationObjective(str, Enum):
    """Portfolio optimization objectives."""
    MAXIMIZE_RETURN = "maximize_return"
    MINIMIZE_RISK = "minimize_risk"
    MAXIMIZE_SHARPE = "maximize_sharpe"
    MAXIMIZE_SORTINO = "maximize_sortino"
    MAXIMIZE_INFORMATION_RATIO = "maximize_information_ratio"
    RISK_PARITY = "risk_parity"
    MINIMUM_VARIANCE = "minimum_variance"


class OptimizationMethod(str, Enum):
    """Optimization methods."""
    MEAN_VARIANCE = "mean_variance"
    BLACK_LITTERMAN = "black_litterman"
    RISK_PARITY = "risk_parity"
    MINIMUM_VARIANCE = "minimum_variance"


class PositionConstraint(BaseModel):
    """Position constraint for optimization."""
    symbol: str
    min_weight: Optional[float] = 0.0
    max_weight: Optional[float] = 1.0


class SectorConstraint(BaseModel):
    """Sector constraint for optimization."""
    sector: str
    min_weight: Optional[float] = 0.0
    max_weight: Optional[float] = 1.0


class OptimizationConstraints(BaseModel):
    """Optimization constraints."""
    position_limits: List[PositionConstraint] = []
    sector_limits: List[SectorConstraint] = []
    asset_class_limits: Dict[str, Dict[str, float]] = {}  # {asset_class: {min, max}}
    max_turnover: Optional[float] = None  # Maximum turnover percentage
    transaction_cost_rate: float = 0.001  # Transaction cost as percentage
    long_only: bool = True
    leverage_limit: Optional[float] = None


class OptimizationResult(BaseModel):
    """Result of portfolio optimization."""
    portfolio_id: str
    optimization_method: str
    objective: str
    optimal_weights: Dict[str, float]  # {symbol: weight}
    expected_return: float
    expected_risk: float
    sharpe_ratio: float
    sortino_ratio: Optional[float] = None
    information_ratio: Optional[float] = None
    constraint_satisfaction: Dict[str, bool]  # {constraint_name: satisfied}
    optimization_time_seconds: float
    optimization_date: datetime


class RebalancingStrategy(str, Enum):
    """Rebalancing strategies."""
    FULL = "full"  # Full rebalancing to target
    THRESHOLD = "threshold"  # Rebalance only when drift exceeds threshold
    CASH_FLOW = "cash_flow"  # Rebalance using cash flows only


class RebalancingSchedule(str, Enum):
    """Rebalancing schedules."""
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"
    QUARTERLY = "quarterly"
    MANUAL = "manual"


class RebalancingRecommendation(BaseModel):
    """Rebalancing recommendation."""
    portfolio_id: str
    current_weights: Dict[str, float]
    target_weights: Dict[str, float]
    recommended_trades: List[Dict[str, Any]]  # [{symbol, action, quantity, price}]
    drift_percentage: float
    estimated_cost: float
    estimated_tax_impact: float
    requires_approval: bool
    recommendation_date: datetime


class RebalancingHistory(BaseModel):
    """Historical rebalancing event."""
    rebalancing_id: str
    portfolio_id: str
    rebalancing_date: datetime
    strategy: str
    before_weights: Dict[str, float]
    after_weights: Dict[str, float]
    trades_executed: List[Dict[str, Any]]
    total_cost: float
    tax_impact: float
    status: str  # pending, approved, executed, cancelled
