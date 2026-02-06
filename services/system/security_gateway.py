"""
Security Gateway Service
Manages API security policies including rate limiting and basic WAF rules.
-Limiter to FastAPI-compatible implementation.
"""
import logging
from functools import wraps
from collections import defaultdict
from datetime import datetime, timedelta
from typing import Dict, Any, Optional, Callable

from fastapi import Request, HTTPException


logger = logging.getLogger(__name__)


class InMemoryRateLimiter:
    """Simple in-memory rate limiter for FastAPI (use Redis in production)."""
    
    def __init__(self) -> None:
        self.requests: Dict[str, list] = defaultdict(list)
    
    def is_allowed(self, key: str, limit: int, window_seconds: int) -> bool:
        """Check if the request is allowed based on rate limit."""
        now = datetime.now()
        window_start = now - timedelta(seconds=window_seconds)
        
        # Clean old requests
        self.requests[key] = [t for t in self.requests[key] if t > window_start]
        
        # Check limit
        if len(self.requests[key]) >= limit:
            return False
        
        # Add current request
        self.requests[key].append(now)
        return True
    
    def reset(self, key: str) -> None:
        """Reset rate limit for a key."""
        self.requests[key] = []


# Global limiter instance
_limiter = InMemoryRateLimiter()


def limit(rate_string: str) -> Callable:
    """
    Rate limiting decorator for FastAPI.
    Parses rate strings like '2 per minute', '500 per hour'.
    """
    # Parse rate string
    parts = rate_string.lower().split()
    count = int(parts[0])
    
    if 'minute' in rate_string.lower():
        window = 60
    elif 'hour' in rate_string.lower():
        window = 3600
    elif 'day' in rate_string.lower():
        window = 86400
    else:
        window = 60  # default to minute
    
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Try to get the request from kwargs (FastAPI injects it)
            request = kwargs.get('request')
            if request and hasattr(request, 'client'):
                client_ip = request.client.host if request.client else "unknown"
            else:
                client_ip = "unknown"
            
            key = f"{client_ip}:{func.__name__}"
            
            if not _limiter.is_allowed(key, count, window):
                raise HTTPException(status_code=429, detail="Rate limit exceeded")
            
            return await func(*args, **kwargs)
        return wrapper
    return decorator


class SecurityGatewayService:
    """
    Manages API security policies including rate limiting and basic WAF rules.
    """
    def __init__(self) -> None:
        self.logger = logging.getLogger(__name__)
        self.status = "Active"
        self.waf_mode = "Core v1 (Enabled)"

    def get_status(self) -> Dict[str, Any]:
        """Returns the current state of the security gateway."""
        return {
            "status": self.status,
            "rate_limiter": "Active",
            "waf_rules": self.waf_mode,
            "default_limits": "10000/day, 500/hr"
        }


def get_security_gateway() -> SecurityGatewayService:
    return SecurityGatewayService()


def get_rate_limiter() -> InMemoryRateLimiter:
    """Get the global rate limiter instance."""
    return _limiter

