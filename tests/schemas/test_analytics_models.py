"""
Tests for Analytics Pydantic Models
Phase 7: Model Validation Tests
"""

import pytest
from datetime import datetime
from pydantic import ValidationError
from schemas.analytics import (
    AttributionBreakdown,
    HoldingAttribution,
    AttributionResult, # Replaced PerformanceAttribution
    HoldingContribution,
    FactorRiskDecomposition,
    ConcentrationRiskAnalysis, # Replaced ConcentrationRisk
    CorrelationAnalysis,
    TailRiskContributions,
    CalculationMetadata,
    BenchmarkComparison
)


class TestAttributionBreakdown:
    """Tests for AttributionBreakdown model."""
    
    def test_valid_attribution_breakdown(self):
        """Test valid attribution breakdown creation."""
        breakdown = AttributionBreakdown(
            category="Technology",
            allocation_effect=50.0,
            selection_effect=30.0,
            interaction_effect=10.0,
            total_effect=90.0,
            weight=0.3,
            return_pct=15.0
        )
        assert breakdown.category == "Technology"
        assert breakdown.total_effect == 90.0
        assert breakdown.weight == 0.3
    
    def test_attribution_breakdown_missing_field(self):
        """Test attribution breakdown with missing required field."""
        with pytest.raises(ValidationError):
            AttributionBreakdown(
                category="Technology",
                allocation_effect=50.0
                # Missing other required fields
            )


class TestHoldingAttribution:
    """Tests for HoldingAttribution model."""
    
    def test_valid_holding_attribution(self):
        """Test valid holding attribution creation."""
        attribution = HoldingAttribution(
            symbol="AAPL",
            name="Apple Inc.",
            weight=0.2,
            return_pct=12.5,
            contribution_absolute=2500.0,
            contribution_pct=2.5,
            allocation_effect=10.0,
            selection_effect=5.0
        )
        assert attribution.symbol == "AAPL"
        assert attribution.weight == 0.2
        assert attribution.contribution_pct == 2.5


class TestAttributionResult: # Replaced TestPerformanceAttribution
    """Tests for AttributionResult model."""
    
    def test_valid_attribution_result(self):
        """Test valid attribution result creation."""
        metadata = CalculationMetadata(
            calculation_method="multi_factor",
            calculation_date=datetime.now(),
            data_quality="high",
            missing_data_points=0
        )
        
        result = AttributionResult(
            portfolio_id="portfolio_1",
            period_start=datetime.now(),
            period_end=datetime.now(),
            total_return=15.5,
            total_return_pct=0.155,
            attribution_by_asset_class={},
            attribution_by_sector={},
            attribution_by_geography={},
            attribution_by_holding=[],
            benchmark_comparison=BenchmarkComparison(
                benchmark_symbol="SPY",
                portfolio_return=15.5,
                benchmark_return=12.0,
                active_return=3.5,
                allocation_effect=1.0,
                selection_effect=2.0,
                interaction_effect=0.5,
                tracking_error=0.05
            ),
            calculation_metadata=metadata
        )
        assert result.portfolio_id == "portfolio_1"
        assert result.total_return == 15.5
        assert result.benchmark_comparison.active_return == 3.5


class TestHoldingContribution:
    """Tests for HoldingContribution model."""
    
    def test_valid_holding_contribution(self):
        """Test valid holding contribution creation."""
        contribution = HoldingContribution(
            symbol="AAPL",
            name="Apple Inc.",
            weight=0.2,
            return_pct=12.5,
            contribution_absolute=2500.0,
            contribution_pct=2.5,
            rank=1
        )
        assert contribution.symbol == "AAPL"
        assert contribution.rank == 1


class TestFactorRiskDecomposition:
    """Tests for FactorRiskDecomposition model."""
    
    def test_valid_factor_risk_decomposition(self):
        """Test valid factor risk decomposition creation."""
        decomposition = FactorRiskDecomposition(
            portfolio_id="portfolio_1",
            factor_model="fama_french",
            total_risk=0.18,
            factor_exposures=[], # Renamed from factor_risks
            idiosyncratic_risk=0.05,
            r_squared=0.85
        )
        assert decomposition.portfolio_id == "portfolio_1"
        assert decomposition.total_risk == 0.18


class TestConcentrationRiskAnalysis: # Replaced TestConcentrationRisk
    """Tests for ConcentrationRiskAnalysis model."""
    
    def test_valid_concentration_risk(self):
        """Test valid concentration risk analysis creation."""
        valid_metric = {
            "dimension": "holding",
            "herfindahl_hirschman_index": 0.25,
            "top_5_concentration": 0.4,
            "top_10_concentration": 0.6,
            "max_weight": 0.1,
            "max_weight_symbol": "AAPL"
        }
        concentration = ConcentrationRiskAnalysis(
            portfolio_id="portfolio_1",
            by_holding=valid_metric,
            by_sector={**valid_metric, "dimension": "sector"},
            by_geography={**valid_metric, "dimension": "geography"},
            by_asset_class={**valid_metric, "dimension": "asset_class"}
        )
        assert concentration.portfolio_id == "portfolio_1"
        assert concentration.by_holding.herfindahl_hirschman_index == 0.25


class TestCorrelationAnalysis:
    """Tests for CorrelationAnalysis model."""
    
    def test_valid_correlation_analysis(self):
        """Test valid correlation analysis creation."""
        correlation = CorrelationAnalysis(
            portfolio_id="portfolio_1",
            average_correlation=0.6, # Renamed from avg_correlation
            correlation_matrix={"AAPL": {"MSFT": 0.6}},
            diversification_ratio=1.2,
            highly_correlated_pairs=[]
        )
        assert correlation.portfolio_id == "portfolio_1"
        assert correlation.average_correlation == 0.6


class TestTailRiskContributions:
    """Tests for TailRiskContributions model."""
    
    def test_valid_tail_risk_contributions(self):
        """Test valid tail risk contributions creation."""
        tail_risk = TailRiskContributions(
            portfolio_id="portfolio_1",
            confidence_level=0.95,
            portfolio_var=0.05, # Renamed from var_95
            portfolio_cvar=0.07, # Renamed from cvar_95
            contributions=[],
            method="historical"
        )
        assert tail_risk.portfolio_id == "portfolio_1"
        assert tail_risk.portfolio_var == 0.05
