"""
Tests for Optimization Pydantic Models
Phase 7: Model Validation Tests
"""

import pytest
from datetime import datetime
from pydantic import ValidationError
from schemas.optimization import (
    OptimizationObjective,
    OptimizationMethod,
    PositionConstraint,
    SectorConstraint,
    OptimizationConstraints,
    OptimizationResult,
    RebalancingStrategy,
    RebalancingSchedule,
    RebalancingRecommendation,
    RebalancingHistory
)


class TestOptimizationEnums:
    """Tests for optimization enums."""
    
    def test_optimization_objective_enum(self):
        """Test optimization objective enum values."""
        assert OptimizationObjective.MAXIMIZE_SHARPE == "maximize_sharpe"
        assert OptimizationObjective.MINIMIZE_RISK == "minimize_risk"
        assert OptimizationObjective.MAXIMIZE_RETURN == "maximize_return"
    
    def test_optimization_method_enum(self):
        """Test optimization method enum values."""
        assert OptimizationMethod.MEAN_VARIANCE == "mean_variance"
        assert OptimizationMethod.RISK_PARITY == "risk_parity"
        assert OptimizationMethod.MINIMUM_VARIANCE == "minimum_variance"


class TestPositionConstraint:
    """Tests for PositionConstraint model."""
    
    def test_valid_position_constraint(self):
        """Test valid position constraint creation."""
        constraint = PositionConstraint(
            symbol="AAPL",
            min_weight=0.1,
            max_weight=0.3
        )
        assert constraint.symbol == "AAPL"
        assert constraint.min_weight == 0.1
        assert constraint.max_weight == 0.3
    
    def test_position_constraint_defaults(self):
        """Test position constraint with default values."""
        constraint = PositionConstraint(symbol="AAPL")
        assert constraint.min_weight == 0.0
        assert constraint.max_weight == 1.0


class TestSectorConstraint:
    """Tests for SectorConstraint model."""
    
    def test_valid_sector_constraint(self):
        """Test valid sector constraint creation."""
        constraint = SectorConstraint(
            sector="Technology",
            min_weight=0.2,
            max_weight=0.4
        )
        assert constraint.sector == "Technology"
        assert constraint.min_weight == 0.2


class TestOptimizationConstraints:
    """Tests for OptimizationConstraints model."""
    
    def test_valid_optimization_constraints(self):
        """Test valid optimization constraints creation."""
        constraints = OptimizationConstraints(
            position_limits=[
                PositionConstraint(symbol="AAPL", min_weight=0.1, max_weight=0.3)
            ],
            sector_limits=[
                SectorConstraint(sector="Technology", min_weight=0.2, max_weight=0.4)
            ],
            long_only=True,
            transaction_cost_rate=0.001
        )
        assert len(constraints.position_limits) == 1
        assert constraints.long_only is True
        assert constraints.transaction_cost_rate == 0.001


class TestOptimizationResult:
    """Tests for OptimizationResult model."""
    
    def test_valid_optimization_result(self):
        """Test valid optimization result creation."""
        result = OptimizationResult(
            portfolio_id="portfolio_1",
            optimization_method="mean_variance",
            objective="maximize_sharpe",
            optimal_weights={"AAPL": 0.4, "MSFT": 0.6},
            expected_return=0.12,
            expected_risk=0.15,
            sharpe_ratio=1.5,
            constraint_satisfaction={"position_limits": True},
            optimization_time_seconds=2.5,
            optimization_date=datetime.now()
        )
        assert result.portfolio_id == "portfolio_1"
        assert result.sharpe_ratio == 1.5
        assert result.optimal_weights["AAPL"] == 0.4


class TestRebalancingRecommendation:
    """Tests for RebalancingRecommendation model."""
    
    def test_valid_rebalancing_recommendation(self):
        """Test valid rebalancing recommendation creation."""
        recommendation = RebalancingRecommendation(
            portfolio_id="portfolio_1",
            trades=[],
            estimated_cost=0.0,
            requires_approval=False
        )
        assert recommendation.portfolio_id == "portfolio_1"
        assert recommendation.requires_approval is False


class TestRebalancingHistory:
    """Tests for RebalancingHistory model."""
    
    def test_valid_rebalancing_history(self):
        """Test valid rebalancing history creation."""
        history = RebalancingHistory(
            portfolio_id="portfolio_1",
            executed_at=datetime.now(),
            trades=[],
            total_cost=0.0
        )
        assert history.portfolio_id == "portfolio_1"
        assert history.total_cost == 0.0
