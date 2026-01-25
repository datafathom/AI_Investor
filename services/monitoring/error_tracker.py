"""
Production Error Tracking Service
Integrates with Sentry for production error tracking and monitoring
"""

import os
import logging
from typing import Optional, Dict, Any
import traceback
from datetime import datetime

logger = logging.getLogger(__name__)

# Try to import Sentry
try:
    import sentry_sdk
    from sentry_sdk.integrations.flask import FlaskIntegration
    from sentry_sdk.integrations.sqlalchemy import SqlalchemyIntegration
    from sentry_sdk.integrations.redis import RedisIntegration
    SENTRY_AVAILABLE = True
except ImportError:
    SENTRY_AVAILABLE = False
    logger.warning("Sentry SDK not installed. Install with: pip install sentry-sdk")


class ErrorTracker:
    """Production error tracking service."""
    
    _instance = None
    _initialized = False
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ErrorTracker, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not self._initialized:
            self._initialized = True
            self._sentry_enabled = False
            self._init_sentry()
    
    def _init_sentry(self):
        """Initialize Sentry SDK."""
        if not SENTRY_AVAILABLE:
            logger.warning("Sentry not available - error tracking disabled")
            return
        
        dsn = os.getenv('SENTRY_DSN')
        if not dsn:
            logger.warning("SENTRY_DSN not set - error tracking disabled")
            return
        
        try:
            sentry_sdk.init(
                dsn=dsn,
                environment=os.getenv('APP_ENV', 'production'),
                traces_sample_rate=float(os.getenv('SENTRY_TRACES_SAMPLE_RATE', '0.1')),
                profiles_sample_rate=float(os.getenv('SENTRY_PROFILES_SAMPLE_RATE', '0.1')),
                send_default_pii=False,  # Don't send PII by default
                integrations=[
                    FlaskIntegration(transaction_style='endpoint'),
                    SqlalchemyIntegration(),
                    RedisIntegration(),
                ],
                before_send=self._before_send,
                release=os.getenv('APP_VERSION', 'unknown'),
            )
            self._sentry_enabled = True
            logger.info("Sentry error tracking initialized")
        except Exception as e:
            logger.error(f"Failed to initialize Sentry: {e}")
            self._sentry_enabled = False
    
    def _before_send(self, event, hint):
        """Filter events before sending to Sentry."""
        # Don't send events in development
        if os.getenv('APP_ENV', 'production') == 'development':
            return None
        
        # Filter out certain error types if needed
        if 'exc_info' in hint:
            exc_type, exc_value, tb = hint['exc_info']
            # Example: Don't send 404 errors
            if isinstance(exc_value, Exception) and '404' in str(exc_value):
                return None
        
        return event
    
    def capture_exception(self, exception: Exception, **kwargs):
        """Capture an exception."""
        if self._sentry_enabled:
            sentry_sdk.capture_exception(exception, **kwargs)
        else:
            logger.error(f"Exception: {exception}", exc_info=True)
    
    def capture_message(self, message: str, level: str = 'error', **kwargs):
        """Capture a message."""
        if self._sentry_enabled:
            sentry_sdk.capture_message(message, level=level, **kwargs)
        else:
            logger.log(getattr(logging, level.upper(), logging.ERROR), message)
    
    def set_user(self, user_id: Optional[str] = None, email: Optional[str] = None, 
                 username: Optional[str] = None, **kwargs):
        """Set user context for error tracking."""
        if self._sentry_enabled:
            sentry_sdk.set_user({
                'id': user_id,
                'email': email,
                'username': username,
                **kwargs
            })
    
    def set_context(self, key: str, value: Dict[str, Any]):
        """Set additional context."""
        if self._sentry_enabled:
            sentry_sdk.set_context(key, value)
    
    def add_breadcrumb(self, message: str, category: str = 'default', 
                      level: str = 'info', **kwargs):
        """Add breadcrumb for debugging."""
        if self._sentry_enabled:
            sentry_sdk.add_breadcrumb(
                message=message,
                category=category,
                level=level,
                **kwargs
            )
    
    def set_tag(self, key: str, value: str):
        """Set a tag for filtering."""
        if self._sentry_enabled:
            sentry_sdk.set_tag(key, value)
    
    def start_transaction(self, op: str, name: str, **kwargs):
        """Start a performance transaction."""
        if self._sentry_enabled:
            return sentry_sdk.start_transaction(op=op, name=name, **kwargs)
        return None
    
    def is_enabled(self) -> bool:
        """Check if error tracking is enabled."""
        return self._sentry_enabled


def get_error_tracker() -> ErrorTracker:
    """Get the error tracker instance."""
    return ErrorTracker()
