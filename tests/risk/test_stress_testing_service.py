"""
Tests for Stress Testing Service
Comprehensive test coverage for historical scenarios and Monte Carlo simulation
"""

import pytest
from datetime import datetime
from unittest.mock import Mock, AsyncMock, patch
import numpy as np
from services.risk.stress_testing_service import StressTestingService
from schemas.risk import StressTestResult, StressScenario, MonteCarloResult


@pytest.fixture
def service():
    """Create service instance with mocked dependencies."""
    with patch('services.risk.stress_testing_service.get_portfolio_aggregator'), \
         patch('services.risk.stress_testing_service.get_cache_service'), \
         patch('services.risk.stress_testing_service.MonteCarloEngine'):
        return StressTestingService()


@pytest.mark.asyncio
async def test_run_historical_scenario_2008_crisis(service):
    """Test running 2008 financial crisis scenario."""
    service._get_portfolio_value = AsyncMock(return_value=100000.0)
    service._apply_stress = AsyncMock(return_value=50000.0)  # 50% loss
    
    result = await service.run_historical_scenario(
        portfolio_id="test_portfolio",
        scenario_name="2008_financial_crisis"
    )
    
    assert result is not None
    assert isinstance(result, StressTestResult)
    assert result.scenario.scenario_name == "2008_financial_crisis"
    assert result.initial_value == 100000.0
    assert result.stressed_value == 50000.0
    assert result.loss_amount == 50000.0
    assert result.loss_percentage == 50.0


@pytest.mark.asyncio
async def test_run_historical_scenario_2020_covid(service):
    """Test running 2020 COVID crash scenario."""
    service._get_portfolio_value = AsyncMock(return_value=100000.0)
    service._apply_stress = AsyncMock(return_value=65000.0)  # 35% loss
    
    result = await service.run_historical_scenario(
        portfolio_id="test_portfolio",
        scenario_name="2020_covid_crash"
    )
    
    assert result is not None
    assert result.scenario.scenario_name == "2020_covid_crash"
    assert result.loss_percentage == 35.0


@pytest.mark.asyncio
async def test_run_historical_scenario_2022_inflation(service):
    """Test running 2022 inflation shock scenario."""
    service._get_portfolio_value = AsyncMock(return_value=100000.0)
    service._apply_stress = AsyncMock(return_value=80000.0)  # 20% loss
    
    result = await service.run_historical_scenario(
        portfolio_id="test_portfolio",
        scenario_name="2022_inflation_shock"
    )
    
    assert result is not None
    assert result.scenario.scenario_name == "2022_inflation_shock"
    assert result.loss_percentage == 20.0


@pytest.mark.asyncio
async def test_run_historical_scenario_invalid(service):
    """Test running invalid scenario name."""
    with pytest.raises(ValueError, match="Unknown scenario"):
        await service.run_historical_scenario(
            portfolio_id="test_portfolio",
            scenario_name="invalid_scenario"
        )


@pytest.mark.asyncio
async def test_run_monte_carlo_simulation(service):
    """Test Monte Carlo simulation."""
    service._get_portfolio_value = AsyncMock(return_value=100000.0)
    service.monte_carlo.simulate = AsyncMock(return_value=[
        [120000.0, 110000.0, 90000.0, 105000.0, 115000.0] * 2000  # 10000 simulations
    ])
    
    result = await service.run_monte_carlo_simulation(
        portfolio_id="test_portfolio",
        n_simulations=10000,
        time_horizon_days=252
    )
    
    assert result is not None
    assert isinstance(result, MonteCarloResult)
    assert result.portfolio_id == "test_portfolio"
    assert result.n_simulations == 10000
    assert result.time_horizon_days == 252
    assert result.time_horizon_days == 252
    assert result.expected_value is not None


@pytest.mark.asyncio
async def test_run_monte_carlo_simulation_different_horizons(service):
    """Test Monte Carlo simulation with different time horizons."""
    service._get_portfolio_value = AsyncMock(return_value=100000.0)
    service.monte_carlo.simulate = AsyncMock(return_value=[[100000.0] * 1000])
    
    horizons = [30, 90, 180, 252, 365]
    for horizon in horizons:
        result = await service.run_monte_carlo_simulation(
            portfolio_id="test_portfolio",
            n_simulations=1000,
            time_horizon_days=horizon
        )
        assert result.time_horizon_days == horizon


@pytest.mark.asyncio
async def test_run_custom_stress_scenario(service):
    """Test running custom stress scenario."""
    custom_scenario = StressScenario(
        scenario_name="custom_test",
        description="Custom stress test",
        market_shock={"Equity": -0.30, "Fixed Income": -0.10},
        duration_days=60
    )
    
    service._get_portfolio_value = AsyncMock(return_value=100000.0)
    service._apply_stress = AsyncMock(return_value=70000.0)
    
    result = await service.run_custom_stress_scenario(
        portfolio_id="test_portfolio",
        scenario=custom_scenario
    )
    
    assert result is not None
    assert result.scenario.scenario_name == "custom_test"
    assert result.loss_percentage == 30.0


@pytest.mark.asyncio
async def test_run_historical_scenario_zero_portfolio_value(service):
    """Test historical scenario with zero portfolio value."""
    service._get_portfolio_value = AsyncMock(return_value=0.0)
    service._apply_stress = AsyncMock(return_value=0.0)
    
    result = await service.run_historical_scenario(
        portfolio_id="empty_portfolio",
        scenario_name="2008_financial_crisis"
    )
    
    assert result is not None
    assert result.initial_value == 0.0
    assert result.loss_percentage == 0.0


@pytest.mark.asyncio
async def test_run_monte_carlo_simulation_small_sample(service):
    """Test Monte Carlo simulation with small sample size."""
    service._get_portfolio_value = AsyncMock(return_value=100000.0)
    service.monte_carlo.simulate = AsyncMock(return_value=[[100000.0] * 100])
    
    result = await service.run_monte_carlo_simulation(
        portfolio_id="test_portfolio",
        n_simulations=100,
        time_horizon_days=252
    )
    
    assert result is not None
    assert result.n_simulations == 100


@pytest.mark.asyncio
async def test_run_historical_scenario_error_handling(service):
    """Test error handling in historical scenario."""
    service._get_portfolio_value = AsyncMock(side_effect=Exception("Portfolio not found"))
    
    with pytest.raises(Exception):
        await service.run_historical_scenario(
            portfolio_id="nonexistent",
            scenario_name="2008_financial_crisis"
        )


@pytest.mark.asyncio
async def test_run_monte_carlo_simulation_error_handling(service):
    """Test error handling in Monte Carlo simulation."""
    service._get_portfolio_value = AsyncMock(side_effect=Exception("Database error"))
    
    with pytest.raises(Exception):
        await service.run_monte_carlo_simulation(
            portfolio_id="error_portfolio",
            n_simulations=1000
        )


@pytest.mark.asyncio
async def test_list_historical_scenarios(service):
    """Test listing available historical scenarios."""
    scenarios = service.list_historical_scenarios()
    
    assert scenarios is not None
    assert len(scenarios) > 0
    assert "2008_financial_crisis" in scenarios
    assert "2020_covid_crash" in scenarios
    assert "2022_inflation_shock" in scenarios


@pytest.mark.asyncio
async def test_run_historical_scenario_all_scenarios(service):
    """Test running all available historical scenarios."""
    service._get_portfolio_value = AsyncMock(return_value=100000.0)
    service._apply_stress = AsyncMock(return_value=50000.0)
    
    scenarios = service.list_historical_scenarios()
    for scenario_name in scenarios:
        result = await service.run_historical_scenario(
            portfolio_id="test_portfolio",
            scenario_name=scenario_name
        )
        assert result is not None
        assert result.scenario.scenario_name == scenario_name
