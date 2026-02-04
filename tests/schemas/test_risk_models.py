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
    RiskMetricMethod
)


class TestRiskMetrics:
    """Tests for RiskMetrics model."""
    
    def test_valid_risk_metrics(self):
        """Test valid risk metrics creation."""
        metrics = RiskMetrics(
            portfolio_id="portfolio_1",
            calculation_date=datetime.now(),
            var_95=0.05,
            var_99=0.08,  # Added
            cvar_95=0.07,
            cvar_99=0.10, # Added
            maximum_drawdown=0.12, # Renamed from max_drawdown
            maximum_drawdown_duration_days=10, # Added
            sharpe_ratio=1.5,
            sortino_ratio=1.8,
            calmar_ratio=1.2,
            volatility=0.15,
            beta=1.0,
            method=RiskMetricMethod.HISTORICAL # Added
        )
        assert metrics.portfolio_id == "portfolio_1"
        assert metrics.var_95 == 0.05
        assert metrics.sharpe_ratio == 1.5
        assert metrics.method == "historical"


class TestStressScenario:
    """Tests for StressScenario model."""
    
    def test_valid_stress_scenario(self):
        """Test valid stress scenario creation."""
        scenario = StressScenario(
            scenario_name="market_crash",
            description="Simulated market crash", # Added
            market_shock={"equity": -0.2}, # Changed to dict
            correlation_breakdown=True,
            duration_days=5 # Added default/explicit
        )
        assert scenario.scenario_name == "market_crash"
        assert scenario.market_shock["equity"] == -0.2
        assert scenario.correlation_breakdown is True


class TestStressTestResult:
    """Tests for StressTestResult model."""
    
    def test_valid_stress_test_result(self):
        """Test valid stress test result creation."""
        scenario = StressScenario(
            scenario_name="2008_financial_crisis",
            description="Crisis scenario",
            market_shock={"all": -0.3}
        )
        
        result = StressTestResult(
            portfolio_id="portfolio_1",
            scenario=scenario, # Changed to object
            initial_value=100000.0, # Renamed
            stressed_value=70000.0, # Renamed
            loss_amount=30000.0, # Added
            loss_percentage=30.0,
            calculation_date=datetime.now() # Added
        )
        assert result.portfolio_id == "portfolio_1"
        assert result.loss_percentage == 30.0
        assert result.stressed_value == 70000.0
