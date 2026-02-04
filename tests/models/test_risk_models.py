"""
Tests for Risk Pydantic Models
Phase 7: Model Validation Tests
"""

import pytest
from datetime import datetime
from pydantic import ValidationError
from schemas.risk import (
    RiskMetrics,
    StressScenario,
    StressTestResult,
    VaRMethod,
    StressScenarioType
)


class TestRiskMetrics:
    """Tests for RiskMetrics model."""
    
    def test_valid_risk_metrics(self):
        """Test valid risk metrics creation."""
        metrics = RiskMetrics(
            portfolio_id="portfolio_1",
            var_95=0.05,
            cvar_95=0.07,
            max_drawdown=0.12,
            sharpe_ratio=1.5,
            sortino_ratio=1.8,
            calmar_ratio=1.2,
            volatility=0.15,
            beta=1.0
        )
        assert metrics.portfolio_id == "portfolio_1"
        assert metrics.var_95 == 0.05
        assert metrics.sharpe_ratio == 1.5


class TestStressScenario:
    """Tests for StressScenario model."""
    
    def test_valid_stress_scenario(self):
        """Test valid stress scenario creation."""
        scenario = StressScenario(
            scenario_name="market_crash",
            scenario_type=StressScenarioType.CUSTOM,
            market_shock=-0.2,
            correlation_breakdown=True
        )
        assert scenario.scenario_name == "market_crash"
        assert scenario.market_shock == -0.2
        assert scenario.correlation_breakdown is True


class TestStressTestResult:
    """Tests for StressTestResult model."""
    
    def test_valid_stress_test_result(self):
        """Test valid stress test result creation."""
        result = StressTestResult(
            portfolio_id="portfolio_1",
            scenario_name="2008_financial_crisis",
            portfolio_value_before=100000.0,
            portfolio_value_after=70000.0,
            loss_percent=30.0
        )
        assert result.portfolio_id == "portfolio_1"
        assert result.loss_percent == 30.0
        assert result.portfolio_value_after == 70000.0
