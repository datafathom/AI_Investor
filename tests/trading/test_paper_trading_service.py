"""
Tests for Paper Trading Service
Comprehensive test coverage for virtual portfolios and order execution
"""

import pytest
from datetime import datetime, timezone
from unittest.mock import Mock, AsyncMock, patch
from services.trading.paper_trading_service import PaperTradingService
from schemas.paper_trading import VirtualPortfolio, PaperOrder


@pytest.fixture
def service():
    """Create service instance with mocked dependencies."""
    with patch('services.trading.paper_trading_service.get_cache_service'):
        return PaperTradingService()


@pytest.mark.asyncio
async def test_create_virtual_portfolio(service):
    """Test virtual portfolio creation."""
    service._save_portfolio = AsyncMock()
    
    result = await service.create_virtual_portfolio(
        user_id="user_123",
        portfolio_name="Test Portfolio",
        initial_cash=100000.0
    )
    
    assert result is not None
    assert isinstance(result, VirtualPortfolio)
    assert result.user_id == "user_123"
    assert result.portfolio_name == "Test Portfolio"
    assert result.initial_cash == 100000.0
    assert result.current_cash == 100000.0


@pytest.mark.asyncio
async def test_execute_paper_order_market(service):
    """Test market order execution."""
    portfolio = VirtualPortfolio(
        portfolio_id="portfolio_123",
        user_id="user_123",
        portfolio_name="Test",
        initial_cash=100000.0,
        current_cash=100000.0,
        total_value=100000.0,
        positions={},
        created_date=datetime.now(timezone.utc),
        updated_date=datetime.now(timezone.utc)
    )
    
    service._get_portfolio = AsyncMock(return_value=portfolio)
    service._get_market_price = AsyncMock(return_value=150.0)
    service._calculate_commission = Mock(return_value=1.0)
    service._update_portfolio_positions = AsyncMock()
    
    result = await service.execute_paper_order(
        portfolio_id="portfolio_123",
        symbol="AAPL",
        quantity=100,
        order_type="market"
    )
    
    assert result is not None
    assert isinstance(result, PaperOrder)
    assert result.symbol == "AAPL"
    assert result.quantity == 100


@pytest.mark.asyncio
async def test_execute_paper_order_limit(service):
    """Test limit order execution."""
    portfolio = VirtualPortfolio(
        portfolio_id="portfolio_123",
        user_id="user_123",
        portfolio_name="Test",
        initial_cash=100000.0,
        current_cash=100000.0,
        total_value=100000.0,
        positions={},
        created_date=datetime.now(timezone.utc),
        updated_date=datetime.now(timezone.utc)
    )
    
    service._get_portfolio = AsyncMock(return_value=portfolio)
    service._get_market_price = AsyncMock(return_value=145.0)  # Below limit
    service._calculate_commission = Mock(return_value=1.0)
    service._update_portfolio_positions = AsyncMock()
    
    result = await service.execute_paper_order(
        portfolio_id="portfolio_123",
        symbol="AAPL",
        quantity=100,
        order_type="limit",
        price=150.0
    )
    
    assert result is not None
    assert result.order_type == "limit"
    assert result.price == 150.0


@pytest.mark.asyncio
async def test_execute_paper_order_insufficient_cash(service):
    """Test order execution with insufficient cash."""
    portfolio = VirtualPortfolio(
        portfolio_id="portfolio_123",
        user_id="user_123",
        portfolio_name="Test",
        initial_cash=1000.0,  # Not enough for 100 shares at $150
        current_cash=1000.0,
        total_value=1000.0,
        positions={},
        created_date=datetime.now(timezone.utc),
        updated_date=datetime.now(timezone.utc)
    )
    
    service._get_portfolio = AsyncMock(return_value=portfolio)
    service._get_market_price = AsyncMock(return_value=150.0)
    
    with pytest.raises(ValueError, match="Insufficient"):
        await service.execute_paper_order(
            portfolio_id="portfolio_123",
            symbol="AAPL",
            quantity=100,
            order_type="market"
        )


@pytest.mark.asyncio
async def test_get_portfolio_performance(service):
    """Test portfolio performance retrieval."""
    portfolio = VirtualPortfolio(
        portfolio_id="portfolio_123",
        user_id="user_123",
        portfolio_name="Test",
        initial_cash=100000.0,
        current_cash=50000.0,
        total_value=120000.0,
        positions={'AAPL': {'quantity': 100, 'avg_price': 150.0, 'current_price': 160.0}},
        created_date=datetime.now(timezone.utc),
        updated_date=datetime.now(timezone.utc)
    )
    
    service._get_portfolio = AsyncMock(return_value=portfolio)
    
    result = await service.get_portfolio_performance("portfolio_123")
    
    assert result is not None
    assert 'total_return' in result
    assert 'total_value' in result
    assert result['num_positions'] == 1


@pytest.mark.asyncio
async def test_get_portfolio_positions(service):
    """Test portfolio positions retrieval."""
    portfolio = VirtualPortfolio(
        portfolio_id="portfolio_123",
        user_id="user_123",
        portfolio_name="Test",
        initial_cash=100000.0,
        current_cash=50000.0,
        total_value=120000.0,
        positions={
            'AAPL': {'quantity': 100, 'avg_price': 150.0},
            'MSFT': {'quantity': 50, 'avg_price': 300.0}
        },
        created_date=datetime.now(timezone.utc),
        updated_date=datetime.now(timezone.utc)
    )
    
    service._get_portfolio = AsyncMock(return_value=portfolio)
    
    result = await service.get_portfolio_positions("portfolio_123")
    
    assert result is not None
    assert len(result) == 2
    assert 'AAPL' in result
    assert 'MSFT' in result


@pytest.mark.asyncio
async def test_execute_paper_order_error_handling(service):
    """Test error handling in order execution."""
    service._get_portfolio = AsyncMock(side_effect=Exception("Portfolio not found"))
    
    with pytest.raises(Exception):
        await service.execute_paper_order(
            portfolio_id="nonexistent",
            symbol="AAPL",
            quantity=100,
            order_type="market"
        )
