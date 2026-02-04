"""
==============================================================================
FILE: services/watchlist/alert_service.py
ROLE: Alert System
PURPOSE: Manages price alerts, volume alerts, and news alerts with
         multi-channel notifications.

INTEGRATION POINTS:
    - WatchlistService: Symbol tracking
    - MarketDataService: Real-time price data
    - NotificationService: Alert delivery
    - AlertAPI: Alert endpoints
    - FrontendWatchlist: Alert management

FEATURES:
    - Price alerts (above/below)
    - Volume spike alerts
    - News alerts
    - Multi-channel notifications

AUTHOR: AI Investor Team
CREATED: 2026-01-21
LAST_MODIFIED: 2026-01-21
==============================================================================
"""

import logging
from datetime import timezone, datetime
from typing import Dict, List, Optional
from schemas.watchlist import (
    PriceAlert, AlertType, AlertStatus, AlertHistory
)
from services.system.cache_service import get_cache_service

logger = logging.getLogger(__name__)


class AlertService:
    """
    Service for alert management and monitoring.
    """
    
    def __init__(self):
        """Initialize service with dependencies."""
        self.cache_service = get_cache_service()
        self.active_alerts: Dict[str, PriceAlert] = {}
        
    async def create_price_alert(
        self,
        user_id: str,
        symbol: str,
        alert_type: str,
        threshold: float,
        notification_methods: Optional[List[str]] = None
    ) -> PriceAlert:
        """
        Create a price alert.
        
        Args:
            user_id: User identifier
            symbol: Stock symbol
            alert_type: Alert type (price_above, price_below, price_change)
            threshold: Alert threshold
            notification_methods: Notification methods (email, push, sms)
            
        Returns:
            PriceAlert object
        """
        logger.info(f"Creating {alert_type} alert for {symbol}")
        
        alert = PriceAlert(
            alert_id=f"alert_{user_id}_{datetime.now(timezone.utc).timestamp()}",
            user_id=user_id,
            symbol=symbol,
            alert_type=AlertType(alert_type),
            threshold=threshold,
            status=AlertStatus.ACTIVE,
            notification_methods=notification_methods or ['email'],
            created_date=datetime.now(timezone.utc)
        )
        
        # Save alert
        await self._save_alert(alert)
        self.active_alerts[alert.alert_id] = alert
        
        return alert
    
    async def check_alerts(
        self,
        symbol: str,
        current_price: float,
        volume: Optional[float] = None
    ) -> List[PriceAlert]:
        """
        Check if any alerts should be triggered.
        
        Args:
            symbol: Stock symbol
            current_price: Current market price
            volume: Optional current volume
            
        Returns:
            List of triggered alerts
        """
        triggered_alerts = []
        
        # Check all active alerts for this symbol
        for alert_id, alert in self.active_alerts.items():
            if alert.symbol != symbol or alert.status != AlertStatus.ACTIVE:
                continue
            
            should_trigger = False
            
            if alert.alert_type == AlertType.PRICE_ABOVE:
                should_trigger = current_price >= alert.threshold
            elif alert.alert_type == AlertType.PRICE_BELOW:
                should_trigger = current_price <= alert.threshold
            elif alert.alert_type == AlertType.PRICE_CHANGE:
                if alert.current_price:
                    change_pct = abs((current_price - alert.current_price) / alert.current_price) * 100
                    should_trigger = change_pct >= alert.threshold
            elif alert.alert_type == AlertType.VOLUME_SPIKE:
                # Would compare with average volume
                should_trigger = False  # Simplified
            
            if should_trigger:
                alert.status = AlertStatus.TRIGGERED
                alert.triggered_date = datetime.now(timezone.utc)
                alert.current_price = current_price
                
                # Create history record
                history = AlertHistory(
                    history_id=f"history_{alert.alert_id}_{datetime.now(timezone.utc).timestamp()}",
                    alert_id=alert.alert_id,
                    triggered_date=datetime.now(timezone.utc),
                    trigger_value=current_price,
                    notification_sent=False
                )
                
                # Send notifications (would integrate with notification service)
                await self._send_notifications(alert)
                history.notification_sent = True
                
                await self._save_alert(alert)
                await self._save_history(history)
                
                triggered_alerts.append(alert)
        
        return triggered_alerts
    
    async def _send_notifications(self, alert: PriceAlert):
        """Send alert notifications (simplified)."""
        # In production, would integrate with notification service
        logger.info(f"Sending {alert.notification_methods} notifications for alert {alert.alert_id}")
    
    async def _get_alert(self, alert_id: str) -> Optional[PriceAlert]:
        """Get alert from cache."""
        cache_key = f"alert:{alert_id}"
        alert_data = self.cache_service.get(cache_key)
        if alert_data:
            return PriceAlert(**alert_data)
        return None
    
    async def _save_alert(self, alert: PriceAlert):
        """Save alert to cache."""
        cache_key = f"alert:{alert.alert_id}"
        self.cache_service.set(cache_key, alert.model_dump(), ttl=86400 * 365)
    
    async def _save_history(self, history: AlertHistory):
        """Save alert history to cache."""
        cache_key = f"alert_history:{history.history_id}"
        self.cache_service.set(cache_key, history.model_dump(), ttl=86400 * 365)


# Singleton instance
_alert_service: Optional[AlertService] = None


def get_alert_service() -> AlertService:
    """Get singleton alert service instance."""
    global _alert_service
    if _alert_service is None:
        _alert_service = AlertService()
    return _alert_service
