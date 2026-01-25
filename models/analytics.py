"""
==============================================================================
FILE: models/analytics.py
ROLE: Analytics Data Models
PURPOSE: Pydantic models for portfolio analytics including performance
         attribution, risk decomposition, and analytics results.

INTEGRATION POINTS:
    - PerformanceAttributionService: Attribution result models
    - RiskDecompositionService: Risk analysis models
    - AnalyticsAPI: API response models
    - FrontendAnalytics: Frontend data consumption

AUTHOR: AI Investor Team
CREATED: 2026-01-21
LAST_MODIFIED: 2026-01-21
==============================================================================
"""

from pydantic import BaseModel, Field
from datetime import datetime
from typing import Dict, List, Optional
from enum import Enum


class AttributionType(str, Enum):
    """Type of attribution calculation."""
    MULTI_FACTOR = "multi_factor"
    HIERARCHICAL = "hierarchical"
    SIMPLE = "simple"


class AttributionBreakdown(BaseModel):
    """Breakdown of attribution for a category."""
    category: str
    allocation_effect: float = Field(..., description="Allocation effect in basis points")
    selection_effect: float = Field(..., description="Selection effect in basis points")
    interaction_effect: float = Field(..., description="Interaction effect in basis points")
    total_effect: float = Field(..., description="Total effect in basis points")
    weight: float = Field(..., description="Portfolio weight (0-1)")
    return_pct: float = Field(..., description="Return percentage")


class HoldingAttribution(BaseModel):
    """Attribution for a single holding."""
    symbol: str
    name: str
    weight: float
    return_pct: float
    contribution_absolute: float
    contribution_pct: float
    allocation_effect: float
    selection_effect: float


class BenchmarkComparison(BaseModel):
    """Benchmark comparison results."""
    benchmark_symbol: str
    portfolio_return: float
    benchmark_return: float
    active_return: float
    allocation_effect: float
    selection_effect: float
    interaction_effect: float
    tracking_error: float


class CalculationMetadata(BaseModel):
    """Metadata about the calculation."""
    calculation_method: str
    calculation_date: datetime
    data_quality: str
    missing_data_points: int
    cache_hit: bool = False


class AttributionResult(BaseModel):
    """Result of performance attribution calculation."""
    portfolio_id: str
    period_start: datetime
    period_end: datetime
    total_return: float
    total_return_pct: float
    attribution_by_asset_class: Dict[str, AttributionBreakdown]
    attribution_by_sector: Dict[str, AttributionBreakdown]
    attribution_by_geography: Dict[str, AttributionBreakdown]
    attribution_by_holding: List[HoldingAttribution]
    benchmark_comparison: Optional[BenchmarkComparison] = None
    calculation_metadata: CalculationMetadata


class HoldingContribution(BaseModel):
    """Contribution of a single holding."""
    symbol: str
    name: str
    weight: float
    return_pct: float
    contribution_absolute: float
    contribution_pct: float
    rank: int


# Risk Decomposition Models

class FactorExposure(BaseModel):
    """Factor exposure for a single factor."""
    factor_name: str
    exposure: float
    contribution: float
    risk_contribution: float


class FactorRiskDecomposition(BaseModel):
    """Factor risk decomposition results."""
    portfolio_id: str
    factor_model: str
    total_risk: float
    factor_exposures: List[FactorExposure]
    idiosyncratic_risk: float
    r_squared: float


class ConcentrationMetric(BaseModel):
    """Concentration metric for a dimension."""
    dimension: str
    herfindahl_hirschman_index: float
    top_5_concentration: float
    top_10_concentration: float
    max_weight: float
    max_weight_symbol: str


class ConcentrationRiskAnalysis(BaseModel):
    """Concentration risk analysis results."""
    portfolio_id: str
    by_holding: ConcentrationMetric
    by_sector: ConcentrationMetric
    by_geography: ConcentrationMetric
    by_asset_class: ConcentrationMetric


class CorrelationAnalysis(BaseModel):
    """Correlation analysis results."""
    portfolio_id: str
    correlation_matrix: Dict[str, Dict[str, float]]
    average_correlation: float
    diversification_ratio: float
    highly_correlated_pairs: List[Dict[str, str]]


class TailRiskContribution(BaseModel):
    """Tail risk contribution for a holding."""
    symbol: str
    var_contribution: float
    cvar_contribution: float
    marginal_var: float
    marginal_cvar: float


class TailRiskContributions(BaseModel):
    """Tail risk contributions results."""
    portfolio_id: str
    confidence_level: float
    portfolio_var: float
    portfolio_cvar: float
    contributions: List[TailRiskContribution]
    method: str
