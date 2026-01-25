"""
Tests for Retirement Pydantic Models
Phase 7: Model Validation Tests
"""

import pytest
from datetime import datetime
from pydantic import ValidationError
from models.retirement import (
    WithdrawalStrategy,
    RetirementScenario,
    RetirementProjection,
    WithdrawalPlan,
    RMDCalculation
)


class TestWithdrawalStrategyEnum:
    """Tests for WithdrawalStrategy enum."""
    
    def test_withdrawal_strategy_enum(self):
        """Test withdrawal strategy enum values."""
        assert WithdrawalStrategy.FIXED_AMOUNT == "fixed_amount"
        assert WithdrawalStrategy.PERCENTAGE == "percentage"
        assert WithdrawalStrategy.INFLATION_ADJUSTED == "inflation_adjusted"
        assert WithdrawalStrategy.GUYTON_KINGSTON == "guyton_kingston"


class TestRetirementScenario:
    """Tests for RetirementScenario model."""
    
    def test_valid_retirement_scenario(self):
        """Test valid retirement scenario creation."""
        scenario = RetirementScenario(
            scenario_name='Standard Retirement',
            current_age=35,
            retirement_age=65,
            life_expectancy=85,
            current_savings=100000.0,
            annual_contribution=10000.0,
            expected_return=0.07,
            inflation_rate=0.03,
            withdrawal_rate=0.04,
            social_security_benefit=2000.0
        )
        assert scenario.scenario_name == 'Standard Retirement'
        assert scenario.current_age == 35
        assert scenario.retirement_age == 65
        assert scenario.expected_return == 0.07
    
    def test_retirement_scenario_defaults(self):
        """Test retirement scenario with default values."""
        scenario = RetirementScenario(
            scenario_name='Test',
            current_age=35,
            retirement_age=65,
            life_expectancy=85,
            current_savings=100000.0,
            annual_contribution=10000.0,
            expected_return=0.07
        )
        assert scenario.inflation_rate == 0.03
        assert scenario.withdrawal_rate == 0.04
        assert scenario.social_security_benefit is None


class TestRetirementProjection:
    """Tests for RetirementProjection model."""
    
    def test_valid_retirement_projection(self):
        """Test valid retirement projection creation."""
        projection = RetirementProjection(
            scenario_id='scenario_1',
            projected_retirement_savings=1000000.0,
            projected_annual_income=40000.0,
            years_in_retirement=20,
            probability_of_success=0.85,
            monte_carlo_results={'10th': 800000.0, '50th': 1000000.0, '90th': 1200000.0},
            projected_timeline=[]
        )
        assert projection.scenario_id == 'scenario_1'
        assert projection.probability_of_success == 0.85
        assert projection.projected_retirement_savings == 1000000.0


class TestWithdrawalPlan:
    """Tests for WithdrawalPlan model."""
    
    def test_valid_withdrawal_plan(self):
        """Test valid withdrawal plan creation."""
        plan = WithdrawalPlan(
            plan_id='plan_1',
            strategy=WithdrawalStrategy.PERCENTAGE,
            initial_withdrawal_amount=40000.0,
            withdrawal_rate=0.04,
            inflation_adjustment=True,
            account_sequence=['401k', 'IRA', 'taxable']
        )
        assert plan.plan_id == 'plan_1'
        assert plan.strategy == WithdrawalStrategy.PERCENTAGE
        assert plan.inflation_adjustment is True


class TestRMDCalculation:
    """Tests for RMDCalculation model."""
    
    def test_valid_rmd_calculation(self):
        """Test valid RMD calculation creation."""
        rmd = RMDCalculation(
            account_type='IRA',
            account_balance=500000.0,
            age=72,
            rmd_amount=19531.25,
            distribution_date=datetime(2024, 12, 31)
        )
        assert rmd.account_type == 'IRA'
        assert rmd.age == 72
        assert rmd.rmd_amount == 19531.25
