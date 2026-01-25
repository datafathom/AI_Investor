"""
Tests for Watchlist Service
Comprehensive test coverage for watchlist management and symbol tracking
"""

import pytest
from datetime import datetime
from unittest.mock import Mock, AsyncMock, patch
from services.watchlist.watchlist_service import WatchlistService
from models.watchlist import Watchlist


@pytest.fixture
def service():
    """Create service instance with mocked dependencies."""
    with patch('services.watchlist.watchlist_service.get_cache_service'):
        return WatchlistService()


@pytest.mark.asyncio
async def test_create_watchlist(service):
    """Test watchlist creation."""
    service._save_watchlist = AsyncMock()
    
    result = await service.create_watchlist(
        user_id="user_123",
        watchlist_name="My Watchlist",
        symbols=['AAPL', 'MSFT']
    )
    
    assert result is not None
    assert isinstance(result, Watchlist)
    assert result.user_id == "user_123"
    assert result.watchlist_name == "My Watchlist"
    assert len(result.symbols) == 2


@pytest.mark.asyncio
async def test_create_watchlist_empty(service):
    """Test creating watchlist without initial symbols."""
    service._save_watchlist = AsyncMock()
    
    result = await service.create_watchlist(
        user_id="user_123",
        watchlist_name="Empty Watchlist"
    )
    
    assert result is not None
    assert len(result.symbols) == 0


@pytest.mark.asyncio
async def test_add_symbol(service):
    """Test adding symbol to watchlist."""
    watchlist = Watchlist(
        watchlist_id="watchlist_123",
        user_id="user_123",
        watchlist_name="Test Watchlist",
        symbols=['AAPL'],
        created_date=datetime.utcnow(),
        updated_date=datetime.utcnow()
    )
    
    service._get_watchlist = AsyncMock(return_value=watchlist)
    service._save_watchlist = AsyncMock()
    
    result = await service.add_symbol(
        watchlist_id="watchlist_123",
        symbol="MSFT"
    )
    
    assert result is not None
    assert "MSFT" in result.symbols
    assert len(result.symbols) == 2


@pytest.mark.asyncio
async def test_remove_symbol(service):
    """Test removing symbol from watchlist."""
    watchlist = Watchlist(
        watchlist_id="watchlist_123",
        user_id="user_123",
        watchlist_name="Test Watchlist",
        symbols=['AAPL', 'MSFT'],
        created_date=datetime.utcnow(),
        updated_date=datetime.utcnow()
    )
    
    service._get_watchlist = AsyncMock(return_value=watchlist)
    service._save_watchlist = AsyncMock()
    
    result = await service.remove_symbol(
        watchlist_id="watchlist_123",
        symbol="MSFT"
    )
    
    assert result is not None
    assert "MSFT" not in result.symbols
    assert len(result.symbols) == 1


@pytest.mark.asyncio
async def test_get_watchlists(service):
    """Test getting user watchlists."""
    service._get_watchlists_from_db = AsyncMock(return_value=[
        Watchlist(
            watchlist_id="watchlist_1",
            user_id="user_123",
            watchlist_name="Watchlist 1",
            symbols=['AAPL'],
            created_date=datetime.utcnow(),
            updated_date=datetime.utcnow()
        ),
        Watchlist(
            watchlist_id="watchlist_2",
            user_id="user_123",
            watchlist_name="Watchlist 2",
            symbols=['MSFT'],
            created_date=datetime.utcnow(),
            updated_date=datetime.utcnow()
        ),
    ])
    
    result = await service.get_watchlists("user_123")
    
    assert result is not None
    assert len(result) == 2


@pytest.mark.asyncio
async def test_add_symbol_duplicate(service):
    """Test adding duplicate symbol."""
    watchlist = Watchlist(
        watchlist_id="watchlist_123",
        user_id="user_123",
        watchlist_name="Test Watchlist",
        symbols=['AAPL'],
        created_date=datetime.utcnow(),
        updated_date=datetime.utcnow()
    )
    
    service._get_watchlist = AsyncMock(return_value=watchlist)
    
    # Should handle duplicate gracefully
    result = await service.add_symbol(
        watchlist_id="watchlist_123",
        symbol="AAPL"  # Already exists
    )
    
    assert result is not None
    assert result.symbols.count('AAPL') == 1  # Should not duplicate


@pytest.mark.asyncio
async def test_add_symbol_error_handling(service):
    """Test error handling when adding symbol."""
    service._get_watchlist = AsyncMock(return_value=None)
    
    with pytest.raises(ValueError, match="not found"):
        await service.add_symbol(
            watchlist_id="nonexistent",
            symbol="AAPL"
        )
