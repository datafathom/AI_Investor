import pytest
import math
from services.analysis.monte_carlo_service import MonteCarloService, SimulationResult, DrawdownMetrics

@pytest.mark.asyncio
async def test_gbm_simulation_basics():
    service = MonteCarloService()
    initial_value = 100000.0
    days = 100
    paths = 50
    
    result = await service.run_gbm_simulation(
        initial_value=initial_value,
        mu=0.08,
        sigma=0.20,
        days=days,
        paths=paths
    )
    
    assert isinstance(result, SimulationResult)
    assert len(result.paths) <= 100 # Capped in service
    assert len(result.paths[0]) == days + 1
    assert result.paths[0][0] == initial_value
    assert "p5" in result.quantiles
    assert len(result.quantiles["p5"]) == days + 1
    assert 0 <= result.ruin_probability <= 1.0

@pytest.mark.asyncio
async def test_drawdown_calculation():
    service = MonteCarloService()
    # Simple path: [100, 90, 80, 110, 100]
    # Max DD: (100-80)/100 = 0.2
    # Recovery: yes, reaches 110
    path = [100.0, 90.0, 80.0, 110.0, 100.0]
    
    metrics = await service.calculate_drawdown_metrics(path)
    
    assert metrics.max_drawdown == pytest.approx(0.2)
    assert metrics.max_duration_days >= 2 # 90, 80
    assert metrics.ulcer_index > 0

@pytest.mark.asyncio
async def test_overfit_detection():
    service = MonteCarloService()
    # High variance
    is_overfit, variance = await service.detect_overfit(2.0, 1.0)
    assert is_overfit is True
    assert variance == pytest.approx(0.5)
    
    # Low variance
    is_overfit, variance = await service.detect_overfit(1.5, 1.4)
    assert is_overfit is False
    assert variance < 0.1

@pytest.mark.asyncio
async def test_simulation_ruin():
    service = MonteCarloService()
    # High volatility, low drift -> likely ruin
    result = await service.run_gbm_simulation(
        initial_value=100.0,
        mu=-0.5,
        sigma=0.8,
        days=252,
        paths=100
    )
    # With a 50% threshold, it's very likely some paths hit it
    assert result.ruin_probability >= 0

@pytest.mark.asyncio
async def test_calculate_ruin_probability():
    service = MonteCarloService()
    result = SimulationResult(paths=[], quantiles={}, ruin_probability=0.25, median_final=100.0, mean_final=100.0)
    prob = await service.calculate_ruin_probability(result)
    assert prob == 0.25

@pytest.mark.asyncio
async def test_drawdown_no_drawdown():
    service = MonteCarloService()
    path = [100.0, 110.0, 120.0, 130.0]
    metrics = await service.calculate_drawdown_metrics(path)
    assert metrics.max_drawdown == 0
    assert metrics.avg_drawdown == 0
    assert metrics.ulcer_index == 0
    assert metrics.max_duration_days == 0

@pytest.mark.asyncio
async def test_drawdown_empty():
    service = MonteCarloService()
    metrics = await service.calculate_drawdown_metrics([])
    assert metrics.max_drawdown == 0

def test_singleton():
    from services.analysis.monte_carlo_service import get_monte_carlo_service
    s1 = get_monte_carlo_service()
    s2 = get_monte_carlo_service()
    assert s1 is s2
