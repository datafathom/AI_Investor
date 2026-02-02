"""
Tests for Tax Optimization Service
Comprehensive test coverage for lot selection, tax projections, and tax-aware rebalancing
"""

import pytest
from datetime import datetime, timedelta
from unittest.mock import Mock, AsyncMock, patch
from services.tax.tax_optimization_service import TaxOptimizationService, LotSelectionMethod


@pytest.fixture
def service():
    """Create service instance with mocked dependencies."""
    with patch('services.tax.tax_optimization_service.get_portfolio_aggregator'), \
         patch('services.tax.tax_optimization_service.get_cache_service'):
        return TaxOptimizationService()


@pytest.fixture
def mock_lots():
    """Mock lot data."""
    return [
        {'lot_id': '1', 'purchase_date': datetime(2023, 1, 1), 'quantity': 50, 'cost_basis': 150.0, 'price': 150.0},
        {'lot_id': '2', 'purchase_date': datetime(2023, 6, 1), 'quantity': 50, 'cost_basis': 160.0, 'price': 160.0},
        {'lot_id': '3', 'purchase_date': datetime(2024, 1, 1), 'quantity': 50, 'cost_basis': 170.0, 'price': 170.0},
    ]


@pytest.mark.asyncio
async def test_optimize_lot_selection_highest_cost(service, mock_lots):
    """Test lot selection with highest cost method."""
    service._get_lots = AsyncMock(return_value=mock_lots)
    service._select_lots = AsyncMock(return_value=[mock_lots[2]])  # Highest cost
    service._get_current_price = AsyncMock(return_value=180.0)
    service._calculate_tax_impact = AsyncMock(return_value={'short_term_gain': 500.0, 'tax_rate': 0.37})
    
    result = await service.optimize_lot_selection(
        portfolio_id="test_portfolio",
        symbol="AAPL",
        quantity=50,
        method="highest_cost"
    )
    
    assert result is not None
    assert result['symbol'] == "AAPL"
    assert result['quantity'] == 50
    assert result['method'] == "highest_cost"
    assert len(result['selected_lots']) == 1
    assert result['total_cost_basis'] == 170.0
    service._select_lots.assert_called_once()


@pytest.mark.asyncio
async def test_optimize_lot_selection_lowest_cost(service, mock_lots):
    """Test lot selection with lowest cost method."""
    service._get_lots = AsyncMock(return_value=mock_lots)
    service._select_lots = AsyncMock(return_value=[mock_lots[0]])  # Lowest cost
    service._get_current_price = AsyncMock(return_value=180.0)
    service._calculate_tax_impact = AsyncMock(return_value={'long_term_gain': 1500.0, 'tax_rate': 0.20})
    
    result = await service.optimize_lot_selection(
        portfolio_id="test_portfolio",
        symbol="AAPL",
        quantity=50,
        method="lowest_cost"
    )
    
    assert result is not None
    assert result['method'] == "lowest_cost"
    assert result['total_cost_basis'] == 150.0


@pytest.mark.asyncio
async def test_optimize_lot_selection_fifo(service, mock_lots):
    """Test lot selection with FIFO method."""
    service._get_lots = AsyncMock(return_value=mock_lots)
    service._select_lots = AsyncMock(return_value=[mock_lots[0]])  # First in
    service._get_current_price = AsyncMock(return_value=180.0)
    service._calculate_tax_impact = AsyncMock(return_value={'long_term_gain': 1500.0, 'tax_rate': 0.20})
    
    result = await service.optimize_lot_selection(
        portfolio_id="test_portfolio",
        symbol="AAPL",
        quantity=50,
        method="fifo"
    )
    
    assert result is not None
    assert result['method'] == "fifo"


@pytest.mark.asyncio
async def test_optimize_lot_selection_lifo(service, mock_lots):
    """Test lot selection with LIFO method."""
    service._get_lots = AsyncMock(return_value=mock_lots)
    service._select_lots = AsyncMock(return_value=[mock_lots[2]])  # Last in
    service._get_current_price = AsyncMock(return_value=180.0)
    service._calculate_tax_impact = AsyncMock(return_value={'short_term_gain': 500.0, 'tax_rate': 0.37})
    
    result = await service.optimize_lot_selection(
        portfolio_id="test_portfolio",
        symbol="AAPL",
        quantity=50,
        method="lifo"
    )
    
    assert result is not None
    assert result['method'] == "lifo"


@pytest.mark.asyncio
async def test_optimize_lot_selection_no_lots(service):
    """Test lot selection with no lots available."""
    service._get_lots = AsyncMock(return_value=[])
    
    with pytest.raises(ValueError, match="No lots found"):
        await service.optimize_lot_selection(
            portfolio_id="test_portfolio",
            symbol="AAPL",
            quantity=50
        )


@pytest.mark.asyncio
async def test_optimize_lot_selection_partial_quantity(service, mock_lots):
    """Test lot selection with partial quantity."""
    service._get_lots = AsyncMock(return_value=mock_lots)
    service._select_lots = AsyncMock(return_value=[{**mock_lots[0], 'quantity': 30}])  # Partial
    service._get_current_price = AsyncMock(return_value=180.0)
    service._calculate_tax_impact = AsyncMock(return_value={'long_term_gain': 900.0, 'tax_rate': 0.20})
    
    result = await service.optimize_lot_selection(
        portfolio_id="test_portfolio",
        symbol="AAPL",
        quantity=30,
        method="highest_cost"
    )
    
    assert result is not None
    assert result['quantity'] == 30


@pytest.mark.asyncio
async def test_project_year_end_tax(service):
    """Test year-end tax projection."""
    service._get_realized_gains = AsyncMock(return_value=[
        {'symbol': 'AAPL', 'gain': 5000.0, 'long_term': True},
        {'symbol': 'MSFT', 'gain': -2000.0, 'long_term': False},
    ])
    service._get_unrealized_gains = AsyncMock(return_value=[
        {'symbol': 'TSLA', 'gain': 10000.0, 'long_term': True},
    ])
    service._estimate_transaction_tax_impact = AsyncMock(return_value=1000.0)
    service._calculate_tax_liability = AsyncMock(return_value=1200.0)
    
    result = await service.project_year_end_tax(
        portfolio_id="test_portfolio",
        planned_transactions=[{'symbol': 'JPM', 'quantity': 100, 'action': 'sell'}]
    )
    
    assert result is not None
    assert result['portfolio_id'] == "test_portfolio"
    assert result['realized_gains_losses'] == 3000.0  # 5000 - 2000
    assert result['estimated_tax_liability'] == 1200.0
    assert 'breakdown' in result


@pytest.mark.asyncio
async def test_project_year_end_tax_no_transactions(service):
    """Test year-end tax projection with no planned transactions."""
    service._get_realized_gains = AsyncMock(return_value=[])
    service._get_unrealized_gains = AsyncMock(return_value=[])
    service._calculate_tax_liability = AsyncMock(return_value=0.0)
    
    result = await service.project_year_end_tax(
        portfolio_id="test_portfolio"
    )
    
    assert result is not None
    assert result['planned_transaction_impact'] == 0.0


@pytest.mark.asyncio
async def test_optimize_tax_aware_rebalancing(service):
    """Test tax-aware rebalancing optimization."""
    current_weights = {'AAPL': 0.4, 'MSFT': 0.3, 'JPM': 0.3}
    target_weights = {'AAPL': 0.3, 'MSFT': 0.4, 'JPM': 0.3}
    
    service._get_portfolio_data = AsyncMock(return_value={
        'holdings': [
            {'symbol': 'AAPL', 'weight': 0.4, 'unrealized_gain': 5000.0},
            {'symbol': 'MSFT', 'weight': 0.3, 'unrealized_gain': -2000.0},
            {'symbol': 'JPM', 'weight': 0.3, 'unrealized_gain': 1000.0},
        ]
    })
    service._calculate_rebalancing_trades = AsyncMock(return_value=[
        {'symbol': 'AAPL', 'action': 'sell', 'quantity': 10, 'tax_impact': 1850.0},
        {'symbol': 'MSFT', 'action': 'buy', 'quantity': 20, 'tax_impact': 0.0},
    ])
    
    result = await service.optimize_tax_aware_rebalancing(
        portfolio_id="test_portfolio",
        target_weights=target_weights
    )
    
    assert result is not None
    assert 'trades' in result
    assert 'total_tax_impact' in result


@pytest.mark.asyncio
async def test_optimize_lot_selection_error_handling(service):
    """Test error handling in lot selection."""
    service._get_lots = AsyncMock(side_effect=Exception("Database error"))
    
    with pytest.raises(Exception):
        await service.optimize_lot_selection(
            portfolio_id="error_portfolio",
            symbol="AAPL",
            quantity=50
        )


@pytest.mark.asyncio
async def test_project_year_end_tax_error_handling(service):
    """Test error handling in tax projection."""
    service._get_realized_gains = AsyncMock(side_effect=Exception("Database error"))
    
    with pytest.raises(Exception):
        await service.project_year_end_tax(
            portfolio_id="error_portfolio"
        )


@pytest.mark.asyncio
async def test_optimize_lot_selection_all_methods(service, mock_lots):
    """Test lot selection with all available methods."""
    methods = ["fifo", "lifo", "highest_cost", "lowest_cost", "specific_lot"]
    
    service._get_lots = AsyncMock(return_value=mock_lots)
    service._select_lots = AsyncMock(return_value=[mock_lots[0]])
    service._get_current_price = AsyncMock(return_value=180.0)
    service._calculate_tax_impact = AsyncMock(return_value={'gain': 1500.0, 'tax_rate': 0.20})
    
    for method in methods:
        result = await service.optimize_lot_selection(
            portfolio_id="test_portfolio",
            symbol="AAPL",
            quantity=50,
            method=method
        )
        assert result['method'] == method
