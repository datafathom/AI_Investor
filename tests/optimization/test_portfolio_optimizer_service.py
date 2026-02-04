"""
Tests for Portfolio Optimizer Service
Comprehensive test coverage for all optimization methods and edge cases
"""

import pytest
from datetime import datetime, timezone
from unittest.mock import Mock, AsyncMock, patch
import numpy as np
from services.optimization.portfolio_optimizer_service import PortfolioOptimizerService
from schemas.optimization import OptimizationResult, OptimizationConstraints, OptimizationObjective


@pytest.fixture
def service():
    """Create service instance with mocked dependencies."""
    with patch('services.optimization.portfolio_optimizer_service.get_portfolio_aggregator'), \
         patch('services.optimization.portfolio_optimizer_service.get_cache_service'):
        return PortfolioOptimizerService()


@pytest.fixture
def mock_portfolio_data():
    """Mock portfolio holdings data."""
    return {
        'holdings': [
            {'symbol': 'AAPL', 'quantity': 100, 'weight': 0.4},
            {'symbol': 'MSFT', 'quantity': 50, 'weight': 0.3},
            {'symbol': 'JPM', 'quantity': 200, 'weight': 0.2},
            {'symbol': 'TSLA', 'quantity': 50, 'weight': 0.1},
        ],
        'total_value': 100000.0
    }


@pytest.fixture
def mock_expected_returns():
    """Mock expected returns."""
    return np.array([0.12, 0.10, 0.08, 0.15])


@pytest.fixture
def mock_covariance_matrix():
    """Mock covariance matrix."""
    return np.array([
        [0.04, 0.02, 0.01, 0.03],
        [0.02, 0.03, 0.01, 0.02],
        [0.01, 0.01, 0.02, 0.01],
        [0.03, 0.02, 0.01, 0.05]
    ])


@pytest.mark.asyncio
async def test_optimize_mean_variance(service, mock_portfolio_data, mock_expected_returns, mock_covariance_matrix):
    """Test mean-variance optimization."""
    service._get_portfolio_data = AsyncMock(return_value=mock_portfolio_data)
    service.cache_service.get = Mock(return_value=None)  # Sync method
    service.cache_service.set = Mock()  # Sync method
    service._get_expected_returns = AsyncMock(return_value=mock_expected_returns)
    service._get_covariance_matrix = AsyncMock(return_value=mock_covariance_matrix)
    service._mean_variance_optimize = AsyncMock(return_value=np.array([0.3, 0.3, 0.2, 0.2]))
    service._check_constraints = AsyncMock(return_value={'weights_sum_to_one': True, 'long_only': True})
    
    result = await service.optimize(
        portfolio_id="test_portfolio",
        objective="maximize_sharpe",
        method="mean_variance"
    )
    
    assert result is not None
    assert isinstance(result, OptimizationResult)
    assert result.optimization_method == "mean_variance"
    assert result.objective == "maximize_sharpe"
    assert len(result.optimal_weights) == 4
    service.cache_service.set.assert_called_once()


@pytest.mark.asyncio
async def test_optimize_risk_parity(service, mock_portfolio_data, mock_covariance_matrix):
    """Test risk parity optimization."""
    service._get_portfolio_data = AsyncMock(return_value=mock_portfolio_data)
    service.cache_service.get = Mock(return_value=None)
    service.cache_service.set = Mock()
    service._get_expected_returns = AsyncMock(return_value=np.array([0.1, 0.1, 0.1, 0.1]))
    service._get_covariance_matrix = AsyncMock(return_value=mock_covariance_matrix)
    service._risk_parity_optimize = AsyncMock(return_value=np.array([0.25, 0.25, 0.25, 0.25]))
    service._check_constraints = AsyncMock(return_value={'weights_sum_to_one': True, 'long_only': True})
    
    result = await service.optimize(
        portfolio_id="test_portfolio",
        objective="risk_parity",
        method="risk_parity"
    )
    
    assert result is not None
    assert result.optimization_method == "risk_parity"


@pytest.mark.asyncio
async def test_optimize_minimum_variance(service, mock_portfolio_data, mock_covariance_matrix):
    """Test minimum variance optimization."""
    service._get_portfolio_data = AsyncMock(return_value=mock_portfolio_data)
    service.cache_service.get = Mock(return_value=None)
    service.cache_service.set = Mock()
    service._get_expected_returns = AsyncMock(return_value=np.array([0.1, 0.1, 0.1, 0.1]))
    service._get_covariance_matrix = AsyncMock(return_value=mock_covariance_matrix)
    service._minimum_variance_optimize = AsyncMock(return_value=np.array([0.2, 0.3, 0.3, 0.2]))
    service._check_constraints = AsyncMock(return_value={'weights_sum_to_one': True, 'long_only': True})
    
    result = await service.optimize(
        portfolio_id="test_portfolio",
        objective="minimize_risk",
        method="minimum_variance"
    )
    
    assert result is not None
    assert result.optimization_method == "minimum_variance"


@pytest.mark.asyncio
async def test_optimize_cached(service):
    """Test that cached optimization is returned when available."""
    cached_data = {
        'portfolio_id': 'test_portfolio',
        'optimization_method': 'mean_variance',
        'objective': 'maximize_sharpe',
        'optimal_weights': {'AAPL': 0.3, 'MSFT': 0.3, 'JPM': 0.2, 'TSLA': 0.2},
        'expected_return': 0.11,
        'expected_risk': 0.15,
        'sharpe_ratio': 0.6,
        'constraint_satisfaction': {'diversity': True, 'max_weight': True},
        'optimization_time_seconds': 0.5,
        'optimization_date': datetime.now(timezone.utc)
    }
    
    service.cache_service.get = Mock(return_value=cached_data)
    service._get_portfolio_data = AsyncMock()  # Should not be called
    
    result = await service.optimize(
        portfolio_id="test_portfolio",
        objective="maximize_sharpe",
        method="mean_variance"
    )
    
    assert result is not None
    assert result.sharpe_ratio == 0.6
    service._get_portfolio_data.assert_not_called()


@pytest.mark.asyncio
async def test_optimize_with_constraints(service, mock_portfolio_data, mock_expected_returns, mock_covariance_matrix):
    """Test optimization with constraints."""
    constraints = OptimizationConstraints(
        long_only=True,
        transaction_cost_rate=0.001
    )
    
    service._get_portfolio_data = AsyncMock(return_value=mock_portfolio_data)
    service.cache_service.get = Mock(return_value=None)
    service.cache_service.set = Mock()
    service._get_expected_returns = AsyncMock(return_value=mock_expected_returns)
    service._get_covariance_matrix = AsyncMock(return_value=mock_covariance_matrix)
    service._mean_variance_optimize = AsyncMock(return_value=np.array([0.3, 0.3, 0.2, 0.2]))
    service._check_constraints = AsyncMock(return_value={'long_only': True, 'weights_sum_to_one': True})
    
    result = await service.optimize(
        portfolio_id="test_portfolio",
        objective="maximize_sharpe",
        method="mean_variance",
        constraints=constraints
    )
    
    assert result is not None
    assert isinstance(result.constraint_satisfaction, dict)
    assert result.constraint_satisfaction['long_only'] is True


@pytest.mark.asyncio
async def test_optimize_empty_portfolio(service):
    """Test optimization with empty portfolio."""
    service._get_portfolio_data = AsyncMock(return_value={'holdings': []})
    service.cache_service.get = Mock(return_value=None)
    
    with pytest.raises(ValueError, match="Portfolio has no holdings"):
        await service.optimize(
            portfolio_id="empty_portfolio",
            objective="maximize_sharpe"
        )


@pytest.mark.asyncio
async def test_optimize_invalid_method(service, mock_portfolio_data):
    """Test optimization with invalid method."""
    service._get_portfolio_data = AsyncMock(return_value=mock_portfolio_data)
    service.cache_service.get = Mock(return_value=None)
    service._get_expected_returns = AsyncMock(return_value=np.array([0.1, 0.1, 0.1, 0.1]))
    service._get_covariance_matrix = AsyncMock(return_value=np.eye(4))
    
    with pytest.raises(ValueError, match="Unknown optimization method"):
        await service.optimize(
            portfolio_id="test_portfolio",
            method="invalid_method"
        )


@pytest.mark.asyncio
async def test_optimize_different_objectives(service, mock_portfolio_data, mock_expected_returns, mock_covariance_matrix):
    """Test optimization with different objectives."""
    service._get_portfolio_data = AsyncMock(return_value=mock_portfolio_data)
    service.cache_service.get = Mock(return_value=None)
    service.cache_service.set = Mock()
    service._get_expected_returns = AsyncMock(return_value=mock_expected_returns)
    service._get_covariance_matrix = AsyncMock(return_value=mock_covariance_matrix)
    service._mean_variance_optimize = AsyncMock(return_value=np.array([0.3, 0.3, 0.2, 0.2]))
    service._check_constraints = AsyncMock(return_value={'weights_sum_to_one': True, 'long_only': True})
    
    objectives = ["maximize_sharpe", "maximize_return", "minimize_risk"]
    for objective in objectives:
        result = await service.optimize(
            portfolio_id="test_portfolio",
            objective=objective,
            method="mean_variance"
        )
        assert result.objective == objective


@pytest.mark.asyncio
async def test_optimize_error_handling(service):
    """Test error handling in optimization."""
    service._get_portfolio_data = AsyncMock(side_effect=Exception("Database error"))
    service.cache_service.get = Mock(return_value=None)
    
    with pytest.raises(Exception):
        await service.optimize(
            portfolio_id="error_portfolio",
            objective="maximize_sharpe"
        )


@pytest.mark.asyncio
async def test_optimize_constraint_violation(service, mock_portfolio_data, mock_expected_returns, mock_covariance_matrix):
    """Test optimization when constraints are violated."""
    service._get_portfolio_data = AsyncMock(return_value=mock_portfolio_data)
    service.cache_service.get = Mock(return_value=None)
    service.cache_service.set = Mock()
    service._get_expected_returns = AsyncMock(return_value=mock_expected_returns)
    service._get_covariance_matrix = AsyncMock(return_value=mock_covariance_matrix)
    service._mean_variance_optimize = AsyncMock(return_value=np.array([0.6, 0.2, 0.1, 0.1]))  # Violates max_weight
    service._check_constraints = AsyncMock(return_value={'diversity': False, 'long_only': True})
    
    result = await service.optimize(
        portfolio_id="test_portfolio",
        objective="maximize_sharpe",
        method="mean_variance",
        constraints=OptimizationConstraints()
    )
    
    assert result is not None
    assert isinstance(result.constraint_satisfaction, dict)
    assert result.constraint_satisfaction['diversity'] is False
