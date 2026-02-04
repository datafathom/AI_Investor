"""
Tests for Analytics Pydantic Models
Phase 7: Model Validation Tests
"""

import pytest
from datetime import datetime
from pydantic import ValidationError
from schemas.analytics import (
    AttributionType,
    AttributionBreakdown,
    HoldingAttribution,
    PerformanceAttribution,
    HoldingContribution,
    FactorRiskDecomposition,
    ConcentrationRisk,
    CorrelationAnalysis,
    TailRiskContributions
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


class TestPerformanceAttribution:
    """Tests for PerformanceAttribution model."""
    
    def test_valid_performance_attribution(self):
        """Test valid performance attribution creation."""
        from schemas.analytics import CalculationMetadata
        
        attribution = PerformanceAttribution(
            portfolio_id="portfolio_1",
            total_return=15.5,
            benchmark_return=12.0,
            active_return=3.5,
            breakdown=[],
            calculation_metadata=CalculationMetadata(
                calculation_method="multi_factor",
                calculation_date=datetime.now(),
                data_quality="high",
                missing_data_points=0
            )
        )
        assert attribution.portfolio_id == "portfolio_1"
        assert attribution.total_return == 15.5
        assert attribution.active_return == 3.5


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
            total_risk=0.18,
            factor_risks=[]
        )
        assert decomposition.portfolio_id == "portfolio_1"
        assert decomposition.total_risk == 0.18


class TestConcentrationRisk:
    """Tests for ConcentrationRisk model."""
    
    def test_valid_concentration_risk(self):
        """Test valid concentration risk creation."""
        concentration = ConcentrationRisk(
            portfolio_id="portfolio_1",
            herfindahl_index=0.25,
            dimension_risks={}
        )
        assert concentration.portfolio_id == "portfolio_1"
        assert concentration.herfindahl_index == 0.25


class TestCorrelationAnalysis:
    """Tests for CorrelationAnalysis model."""
    
    def test_valid_correlation_analysis(self):
        """Test valid correlation analysis creation."""
        correlation = CorrelationAnalysis(
            portfolio_id="portfolio_1",
            avg_correlation=0.6,
            correlation_matrix={}
        )
        assert correlation.portfolio_id == "portfolio_1"
        assert correlation.avg_correlation == 0.6


class TestTailRiskContributions:
    """Tests for TailRiskContributions model."""
    
    def test_valid_tail_risk_contributions(self):
        """Test valid tail risk contributions creation."""
        tail_risk = TailRiskContributions(
            portfolio_id="portfolio_1",
            var_95=0.05,
            cvar_95=0.07,
            contributions={}
        )
        assert tail_risk.portfolio_id == "portfolio_1"
        assert tail_risk.var_95 == 0.05
        assert tail_risk.cvar_95 == 0.07
