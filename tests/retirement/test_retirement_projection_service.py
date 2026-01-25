"""
Tests for Retirement Projection Service
Comprehensive test coverage for Monte Carlo retirement projections
"""

import pytest
from datetime import datetime
from unittest.mock import Mock, AsyncMock, patch
from services.retirement.retirement_projection_service import RetirementProjectionService
from models.retirement import RetirementScenario, RetirementProjection


@pytest.fixture
def service():
    """Create service instance with mocked dependencies."""
    with patch('services.retirement.retirement_projection_service.MonteCarloEngine'), \
         patch('services.retirement.retirement_projection_service.get_cache_service'):
        return RetirementProjectionService()


@pytest.fixture
def mock_scenario():
    """Mock retirement scenario."""
    return RetirementScenario(
        current_age=35,
        retirement_age=65,
        current_savings=100000.0,
        annual_contribution=10000.0,
        expected_return=0.07,
        withdrawal_rate=0.04
    )


@pytest.mark.asyncio
async def test_project_retirement(service, mock_scenario):
    """Test retirement projection."""
    service.monte_carlo.simulate = AsyncMock(return_value=[[2000000.0] * 10000])
    service.cache_service.get = AsyncMock(return_value=None)
    service.cache_service.set = AsyncMock()
    
    result = await service.project_retirement(
        scenario=mock_scenario,
        n_simulations=10000
    )
    
    assert result is not None
    assert isinstance(result, RetirementProjection)
    assert result.scenario == mock_scenario


@pytest.mark.asyncio
async def test_project_retirement_cached(service, mock_scenario):
    """Test cached retirement projection."""
    cached_data = {
        'scenario': mock_scenario.dict(),
        'median_retirement_savings': 2000000.0,
        'success_probability': 0.85
    }
    service.cache_service.get = AsyncMock(return_value=cached_data)
    
    result = await service.project_retirement(mock_scenario)
    
    assert result is not None
    service.monte_carlo.simulate.assert_not_called()
