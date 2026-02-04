"""
Tests for Rebalancing Service
Comprehensive test coverage for rebalancing checks, recommendations, and execution
"""

import pytest
from datetime import datetime, timedelta, timezone
from unittest.mock import Mock, AsyncMock, patch
from services.optimization.rebalancing_service import RebalancingService
from schemas.optimization import RebalancingRecommendation, RebalancingHistory


@pytest.fixture
def service():
    """Create service instance with mocked dependencies."""
    with patch('services.optimization.rebalancing_service.get_portfolio_aggregator'), \
         patch('services.optimization.rebalancing_service.get_optimizer_service'), \
         patch('services.optimization.rebalancing_service.get_cache_service'):
        return RebalancingService()


@pytest.fixture
def mock_current_weights():
    """Mock current portfolio weights."""
    return {'AAPL': 0.45, 'MSFT': 0.35, 'JPM': 0.20}


@pytest.fixture
def mock_target_weights():
    """Mock target portfolio weights."""
    return {'AAPL': 0.40, 'MSFT': 0.30, 'JPM': 0.30}


@pytest.mark.asyncio
async def test_check_rebalancing_needed_true(service, mock_current_weights, mock_target_weights):
    """Test rebalancing check when drift exceeds threshold."""
    service._get_current_weights = AsyncMock(return_value=mock_current_weights)
    service._get_target_weights = AsyncMock(return_value=mock_target_weights)
    
    # JPM has 10% drift (0.20 current vs 0.30 target), exceeds 5% threshold
    result = await service.check_rebalancing_needed(
        portfolio_id="test_portfolio",
        threshold=0.05
    )
    
    assert result is True


@pytest.mark.asyncio
async def test_check_rebalancing_needed_false(service):
    """Test rebalancing check when drift is within threshold."""
    current_weights = {'AAPL': 0.41, 'MSFT': 0.31, 'JPM': 0.28}
    target_weights = {'AAPL': 0.40, 'MSFT': 0.30, 'JPM': 0.30}
    
    service._get_current_weights = AsyncMock(return_value=current_weights)
    service._get_target_weights = AsyncMock(return_value=target_weights)
    
    # Max drift is 2% (JPM: 0.28 vs 0.30), within 5% threshold
    result = await service.check_rebalancing_needed(
        portfolio_id="test_portfolio",
        threshold=0.05
    )
    
    assert result is False


@pytest.mark.asyncio
async def test_check_rebalancing_needed_custom_threshold(service, mock_current_weights, mock_target_weights):
    """Test rebalancing check with custom threshold."""
    service._get_current_weights = AsyncMock(return_value=mock_current_weights)
    service._get_target_weights = AsyncMock(return_value=mock_target_weights)
    
    # With 10% threshold, should return False (max drift is 10%)
    result = await service.check_rebalancing_needed(
        portfolio_id="test_portfolio",
        threshold=0.10
    )
    
    assert result is False


@pytest.mark.asyncio
async def test_generate_rebalancing_recommendation(service, mock_current_weights, mock_target_weights):
    """Test rebalancing recommendation generation."""
    service._get_current_weights = AsyncMock(return_value=mock_current_weights)
    service._get_target_weights = AsyncMock(return_value=mock_target_weights)
    service._calculate_drift = AsyncMock(return_value=0.10)
    service._generate_trades = AsyncMock(return_value=[
        {'symbol': 'AAPL', 'action': 'sell', 'quantity': 10},
        {'symbol': 'JPM', 'action': 'buy', 'quantity': 20},
    ])
    service._estimate_trading_cost = AsyncMock(return_value=50.0)
    service._estimate_tax_impact = AsyncMock(return_value=200.0)
    
    result = await service.generate_rebalancing_recommendation(
        portfolio_id="test_portfolio",
        strategy="threshold"
    )
    
    assert result is not None
    assert isinstance(result, RebalancingRecommendation)
    assert result.portfolio_id == "test_portfolio"
    assert result.drift_percentage == 0.10
    assert len(result.recommended_trades) == 2
    assert result.estimated_cost == 50.0
    assert result.estimated_tax_impact == 200.0


@pytest.mark.asyncio
async def test_generate_rebalancing_recommendation_requires_approval(service, mock_current_weights, mock_target_weights):
    """Test rebalancing recommendation that requires approval."""
    service._get_current_weights = AsyncMock(return_value=mock_current_weights)
    service._get_target_weights = AsyncMock(return_value=mock_target_weights)
    service._calculate_drift = AsyncMock(return_value=0.10)
    service._generate_trades = AsyncMock(return_value=[
        {'symbol': 'AAPL', 'action': 'sell', 'quantity': 1000},
    ])
    service._estimate_trading_cost = AsyncMock(return_value=15000.0)  # Exceeds $10k threshold
    service._estimate_tax_impact = AsyncMock(return_value=5000.0)
    
    result = await service.generate_rebalancing_recommendation(
        portfolio_id="test_portfolio"
    )
    
    assert result is not None
    assert result.requires_approval is True


@pytest.mark.asyncio
async def test_generate_rebalancing_recommendation_no_approval_needed(service, mock_current_weights, mock_target_weights):
    """Test rebalancing recommendation that doesn't require approval."""
    service._get_current_weights = AsyncMock(return_value=mock_current_weights)
    service._get_target_weights = AsyncMock(return_value=mock_target_weights)
    service._calculate_drift = AsyncMock(return_value=0.10)
    service._generate_trades = AsyncMock(return_value=[
        {'symbol': 'AAPL', 'action': 'sell', 'quantity': 10},
    ])
    service._estimate_trading_cost = AsyncMock(return_value=500.0)  # Below $10k threshold
    service._estimate_tax_impact = AsyncMock(return_value=100.0)
    
    result = await service.generate_rebalancing_recommendation(
        portfolio_id="test_portfolio"
    )
    
    assert result is not None
    assert result.requires_approval is False


@pytest.mark.asyncio
async def test_generate_rebalancing_recommendation_different_strategies(service, mock_current_weights, mock_target_weights):
    """Test rebalancing recommendation with different strategies."""
    service._get_current_weights = AsyncMock(return_value=mock_current_weights)
    service._get_target_weights = AsyncMock(return_value=mock_target_weights)
    service._calculate_drift = AsyncMock(return_value=0.10)
    service._generate_trades = AsyncMock(return_value=[])
    service._estimate_trading_cost = AsyncMock(return_value=50.0)
    service._estimate_tax_impact = AsyncMock(return_value=200.0)
    
    strategies = ["threshold", "full", "cash_flow"]
    for strategy in strategies:
        result = await service.generate_rebalancing_recommendation(
            portfolio_id="test_portfolio",
            strategy=strategy
        )
        assert result is not None


@pytest.mark.asyncio
async def test_execute_rebalancing(service):
    """Test rebalancing execution."""
    recommendation = RebalancingRecommendation(
        portfolio_id="test_portfolio",
        current_weights={'AAPL': 0.45, 'MSFT': 0.35, 'JPM': 0.20},
        target_weights={'AAPL': 0.40, 'MSFT': 0.30, 'JPM': 0.30},
        recommended_trades=[
            {'symbol': 'AAPL', 'action': 'sell', 'quantity': 10},
            {'symbol': 'JPM', 'action': 'buy', 'quantity': 20},
        ],
        drift_percentage=0.10,
        estimated_cost=50.0,
        estimated_tax_impact=200.0,
        requires_approval=False,
        recommendation_date=datetime.now(timezone.utc)
    )
    
    service._execute_trades = AsyncMock(return_value=[
        {'symbol': 'AAPL', 'action': 'sell', 'quantity': 10, 'status': 'filled', 'price': 100.0, 'value': 1000.0, 'execution_price': 100.0, 'execution_time': datetime.now(timezone.utc)},
        {'symbol': 'JPM', 'action': 'buy', 'quantity': 20, 'status': 'filled', 'price': 100.0, 'value': 2000.0, 'execution_price': 100.0, 'execution_time': datetime.now(timezone.utc)},
    ])
    service._record_rebalancing_history = AsyncMock(return_value=True)
    
    result = await service.execute_rebalancing(
        portfolio_id="test_portfolio",
        recommendation=recommendation,
        approved=True
    )
    
    assert result is not None
    assert isinstance(result, RebalancingHistory)
    service._execute_trades.assert_called_once()


@pytest.mark.asyncio
async def test_execute_rebalancing_requires_approval_not_given(service):
    """Test rebalancing execution when approval is required but not given."""
    recommendation = RebalancingRecommendation(
        portfolio_id="test_portfolio",
        current_weights={},
        target_weights={},
        recommended_trades=[],
        drift_percentage=0.10,
        estimated_cost=15000.0,  # Exceeds threshold
        estimated_tax_impact=5000.0,
        requires_approval=True,
        recommendation_date=datetime.now(timezone.utc)
    )
    
    with pytest.raises(ValueError, match="requires approval but was not approved"):
        await service.execute_rebalancing(
            portfolio_id="test_portfolio",
            recommendation=recommendation,
            approved=False
        )


@pytest.mark.asyncio
async def test_get_rebalancing_history(service):
    """Test retrieving rebalancing history."""
    service._get_history_from_db = AsyncMock(return_value=[
        {
            'rebalancing_id': 'rebal_1',
            'portfolio_id': 'test_portfolio',
            'rebalancing_date': datetime(2024, 1, 1, tzinfo=timezone.utc),
            'strategy': 'threshold',
            'before_weights': {},
            'after_weights': {},
            'trades_executed': [],
            'total_cost': 50.0,
            'tax_impact': 0.0,
            'status': 'executed'
        },
        {
            'rebalancing_id': 'rebal_2',
            'portfolio_id': 'test_portfolio',
            'rebalancing_date': datetime(2024, 2, 1, tzinfo=timezone.utc),
            'strategy': 'threshold',
            'before_weights': {},
            'after_weights': {},
            'trades_executed': [],
            'total_cost': 75.0,
            'tax_impact': 0.0,
            'status': 'executed'
        },
    ])
    
    result = await service.get_rebalancing_history(
        portfolio_id="test_portfolio",
        limit=10
    )
    
    assert result is not None
    assert len(result) == 2


@pytest.mark.asyncio
async def test_get_rebalancing_history_empty(service):
    """Test retrieving rebalancing history when empty."""
    service._get_history_from_db = AsyncMock(return_value=[])
    
    result = await service.get_rebalancing_history(
        portfolio_id="test_portfolio"
    )
    
    assert result is not None
    assert len(result) == 0


@pytest.mark.asyncio
async def test_check_rebalancing_needed_error_handling(service):
    """Test error handling in rebalancing check."""
    service._get_current_weights = AsyncMock(side_effect=Exception("Database error"))
    
    with pytest.raises(Exception):
        await service.check_rebalancing_needed(
            portfolio_id="error_portfolio"
        )


@pytest.mark.asyncio
async def test_generate_rebalancing_recommendation_error_handling(service):
    """Test error handling in recommendation generation."""
    service._get_current_weights = AsyncMock(side_effect=Exception("Database error"))
    
    with pytest.raises(Exception):
        await service.generate_rebalancing_recommendation(
            portfolio_id="error_portfolio"
        )


@pytest.mark.asyncio
async def test_execute_rebalancing_error_handling(service):
    """Test error handling in rebalancing execution."""
    recommendation = RebalancingRecommendation(
        portfolio_id="test_portfolio",
        current_weights={},
        target_weights={},
        recommended_trades=[],
        drift_percentage=0.10,
        estimated_cost=50.0,
        estimated_tax_impact=200.0,
        requires_approval=False,
        recommendation_date=datetime.now(timezone.utc)
    )
    
    service._execute_trades = AsyncMock(side_effect=Exception("Execution error"))
    
    with pytest.raises(Exception):
        await service.execute_rebalancing(
            portfolio_id="test_portfolio",
            recommendation=recommendation,
            approved=True
        )


@pytest.mark.asyncio
async def test_check_rebalancing_needed_no_drift(service):
    """Test rebalancing check when weights match exactly."""
    weights = {'AAPL': 0.40, 'MSFT': 0.30, 'JPM': 0.30}
    
    service._get_current_weights = AsyncMock(return_value=weights)
    service._get_target_weights = AsyncMock(return_value=weights)
    
    result = await service.check_rebalancing_needed(
        portfolio_id="test_portfolio",
        threshold=0.05
    )
    
    assert result is False


@pytest.mark.asyncio
async def test_generate_rebalancing_recommendation_no_trades_needed(service):
    """Test rebalancing recommendation when no trades are needed."""
    weights = {'AAPL': 0.40, 'MSFT': 0.30, 'JPM': 0.30}
    
    service._get_current_weights = AsyncMock(return_value=weights)
    service._get_target_weights = AsyncMock(return_value=weights)
    service._calculate_drift = AsyncMock(return_value=0.02)  # Below threshold
    service._generate_trades = AsyncMock(return_value=[])
    service._estimate_trading_cost = AsyncMock(return_value=0.0)
    service._estimate_tax_impact = AsyncMock(return_value=0.0)
    
    result = await service.generate_rebalancing_recommendation(
        portfolio_id="test_portfolio"
    )
    
    assert result is not None
    assert len(result.recommended_trades) == 0
