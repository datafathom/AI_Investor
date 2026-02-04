"""
Tests for Alert Service
Comprehensive test coverage for price alerts, volume alerts, and notifications
"""

import pytest
from datetime import timezone, datetime
from unittest.mock import Mock, AsyncMock, patch
from services.watchlist.alert_service import AlertService
from schemas.watchlist import PriceAlert, AlertType, AlertStatus


@pytest.fixture
def service():
    """Create service instance with mocked dependencies."""
    with patch('services.watchlist.alert_service.get_cache_service'):
        return AlertService()


@pytest.mark.asyncio
async def test_create_price_alert_above(service):
    """Test creating price above alert."""
    service._save_alert = AsyncMock()
    
    result = await service.create_price_alert(
        user_id="user_123",
        symbol="AAPL",
        alert_type="price_above",
        threshold=150.0,
        notification_methods=['email', 'push']
    )
    
    assert result is not None
    assert isinstance(result, PriceAlert)
    assert result.symbol == "AAPL"
    assert result.alert_type == AlertType.PRICE_ABOVE
    assert result.threshold == 150.0
    assert result.status == AlertStatus.ACTIVE


@pytest.mark.asyncio
async def test_create_price_alert_below(service):
    """Test creating price below alert."""
    service._save_alert = AsyncMock()
    
    result = await service.create_price_alert(
        user_id="user_123",
        symbol="AAPL",
        alert_type="price_below",
        threshold=140.0
    )
    
    assert result is not None
    assert result.alert_type == AlertType.PRICE_BELOW
    assert result.threshold == 140.0


@pytest.mark.asyncio
async def test_check_alerts(service):
    """Test checking alerts against current prices."""
    alert = PriceAlert(
        alert_id="alert_123",
        user_id="user_123",
        symbol="AAPL",
        alert_type=AlertType.PRICE_ABOVE,
        threshold=150.0,
        status=AlertStatus.ACTIVE,
        notification_methods=['email'],
        created_date=datetime.now(timezone.utc)
    )
    
    service.active_alerts["alert_123"] = alert
    service._get_current_price = AsyncMock(return_value=155.0)  # Above threshold
    service._trigger_alert = AsyncMock()
    service._update_alert = AsyncMock()
    
    result = await service.check_alerts("AAPL", 155.0)
    
    assert result is not None
    assert len(result) > 0  # Should have triggered alerts


@pytest.mark.asyncio
async def test_get_user_alerts(service):
    """Test getting user alerts."""
    service._get_alerts_from_db = AsyncMock(return_value=[
        PriceAlert(
            alert_id="alert_1",
            user_id="user_123",
            symbol="AAPL",
            alert_type=AlertType.PRICE_ABOVE,
            threshold=150.0,
            status=AlertStatus.ACTIVE,
            notification_methods=['email'],
            created_date=datetime.now(timezone.utc)
        )
    ])
    
    result = await service.get_user_alerts("user_123")
    
    assert result is not None
    assert len(result) == 1


@pytest.mark.asyncio
async def test_deactivate_alert(service):
    """Test deactivating an alert."""
    alert = PriceAlert(
        alert_id="alert_123",
        user_id="user_123",
        symbol="AAPL",
        alert_type=AlertType.PRICE_ABOVE,
        threshold=150.0,
        status=AlertStatus.ACTIVE,
        notification_methods=['email'],
        created_date=datetime.now(timezone.utc)
    )
    
    service._get_alert = AsyncMock(return_value=alert)
    service._save_alert = AsyncMock()
    
    result = await service.deactivate_alert("alert_123")
    
    assert result is not None
    assert result.status == AlertStatus.INACTIVE


@pytest.mark.asyncio
async def test_create_alert_error_handling(service):
    """Test error handling in alert creation."""
    service._save_alert = AsyncMock(side_effect=Exception("Database error"))
    
    with pytest.raises(Exception):
        await service.create_price_alert(
            user_id="user_123",
            symbol="AAPL",
            alert_type="price_above",
            threshold=150.0
        )
