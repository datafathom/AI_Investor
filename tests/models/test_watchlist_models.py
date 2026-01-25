"""
Tests for Watchlist Pydantic Models
Phase 7: Model Validation Tests
"""

import pytest
from datetime import datetime
from pydantic import ValidationError
from models.watchlist import (
    AlertType,
    AlertStatus,
    Watchlist,
    PriceAlert,
    AlertHistory
)


class TestAlertEnums:
    """Tests for alert enums."""
    
    def test_alert_type_enum(self):
        """Test alert type enum values."""
        assert AlertType.PRICE_ABOVE == "price_above"
        assert AlertType.PRICE_BELOW == "price_below"
        assert AlertType.VOLUME_SPIKE == "volume_spike"
        assert AlertType.NEWS_ALERT == "news_alert"
    
    def test_alert_status_enum(self):
        """Test alert status enum values."""
        assert AlertStatus.ACTIVE == "active"
        assert AlertStatus.TRIGGERED == "triggered"
        assert AlertStatus.CANCELLED == "cancelled"


class TestWatchlist:
    """Tests for Watchlist model."""
    
    def test_valid_watchlist(self):
        """Test valid watchlist creation."""
        watchlist = Watchlist(
            watchlist_id='watchlist_1',
            user_id='user_1',
            watchlist_name='My Watchlist',
            symbols=['AAPL', 'MSFT', 'GOOGL'],
            created_date=datetime.now(),
            updated_date=datetime.now()
        )
        assert watchlist.watchlist_id == 'watchlist_1'
        assert watchlist.watchlist_name == 'My Watchlist'
        assert len(watchlist.symbols) == 3
    
    def test_watchlist_empty_symbols(self):
        """Test watchlist with empty symbols."""
        watchlist = Watchlist(
            watchlist_id='watchlist_1',
            user_id='user_1',
            watchlist_name='Empty Watchlist',
            symbols=[],
            created_date=datetime.now(),
            updated_date=datetime.now()
        )
        assert len(watchlist.symbols) == 0


class TestPriceAlert:
    """Tests for PriceAlert model."""
    
    def test_valid_price_alert(self):
        """Test valid price alert creation."""
        alert = PriceAlert(
            alert_id='alert_1',
            user_id='user_1',
            symbol='AAPL',
            alert_type=AlertType.PRICE_ABOVE,
            threshold=150.0,
            current_price=145.0,
            status=AlertStatus.ACTIVE,
            notification_methods=['email', 'push'],
            created_date=datetime.now(),
            triggered_date=None
        )
        assert alert.alert_id == 'alert_1'
        assert alert.threshold == 150.0
        assert alert.alert_type == AlertType.PRICE_ABOVE
        assert alert.status == AlertStatus.ACTIVE
    
    def test_price_alert_defaults(self):
        """Test price alert with default values."""
        alert = PriceAlert(
            alert_id='alert_1',
            user_id='user_1',
            symbol='AAPL',
            alert_type=AlertType.PRICE_ABOVE,
            threshold=150.0,
            created_date=datetime.now()
        )
        assert alert.current_price is None
        assert alert.status == AlertStatus.ACTIVE
        assert len(alert.notification_methods) == 0


class TestAlertHistory:
    """Tests for AlertHistory model."""
    
    def test_valid_alert_history(self):
        """Test valid alert history creation."""
        history = AlertHistory(
            history_id='history_1',
            alert_id='alert_1',
            triggered_date=datetime.now(),
            trigger_value=150.5,
            notification_sent=True
        )
        assert history.history_id == 'history_1'
        assert history.trigger_value == 150.5
        assert history.notification_sent is True
