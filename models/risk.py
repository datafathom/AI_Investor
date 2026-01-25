"""
==============================================================================
FILE: models/risk.py
ROLE: Risk Management Data Models
PURPOSE: Pydantic models for risk metrics, stress testing, and scenario analysis.

INTEGRATION POINTS:
    - AdvancedRiskMetricsService: Risk metrics results
    - StressTestingService: Stress test results
    - RiskAPI: API response models
    - FrontendRisk: Risk dashboard widgets

AUTHOR: AI Investor Team
CREATED: 2026-01-21
LAST_MODIFIED: 2026-01-21
==============================================================================
"""

from pydantic import BaseModel, Field
from datetime import datetime
from typing import Dict, List, Optional
from enum import Enum


class RiskMetricMethod(str, Enum):
    """Risk metric calculation methods."""
    HISTORICAL = "historical"
    PARAMETRIC = "parametric"
    MONTE_CARLO = "monte_carlo"


class RiskMetrics(BaseModel):
    """Comprehensive risk metrics."""
    portfolio_id: str
    calculation_date: datetime
    var_95: float = Field(..., description="Value-at-Risk at 95% confidence")
    var_99: float = Field(..., description="Value-at-Risk at 99% confidence")
    cvar_95: float = Field(..., description="Conditional VaR at 95% confidence")
    cvar_99: float = Field(..., description="Conditional VaR at 99% confidence")
    maximum_drawdown: float
    maximum_drawdown_duration_days: int
    sharpe_ratio: float
    sortino_ratio: float
    calmar_ratio: float
    volatility: float
    beta: Optional[float] = None
    method: str


class StressScenario(BaseModel):
    """Stress test scenario."""
    scenario_name: str
    description: str
    market_shock: Dict[str, float]  # {asset_class: shock_percentage}
    correlation_breakdown: bool = False
    duration_days: int = 1


class StressTestResult(BaseModel):
    """Result of stress test."""
    portfolio_id: str
    scenario: StressScenario
    initial_value: float
    stressed_value: float
    loss_amount: float
    loss_percentage: float
    recovery_time_days: Optional[int] = None
    calculation_date: datetime


class MonteCarloResult(BaseModel):
    """Monte Carlo simulation result."""
    portfolio_id: str
    n_simulations: int
    time_horizon_days: int
    expected_value: float
    value_at_5th_percentile: float
    value_at_95th_percentile: float
    probability_of_loss: float
    probability_of_positive_return: float
    calculation_date: datetime
