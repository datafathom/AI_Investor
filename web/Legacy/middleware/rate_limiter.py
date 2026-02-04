"""
Advanced Rate Limiting Middleware
Production-ready rate limiting with Redis backend
"""

import os
import logging
import time
from functools import wraps
from flask import request, jsonify, g
from typing import Optional, Dict, Callable

logger = logging.getLogger(__name__)

# Try to import Redis
try:
    import redis
    REDIS_AVAILABLE = True
except ImportError:
    REDIS_AVAILABLE = False
    logger.warning("Redis not available. Install with: pip install redis")


class RateLimiter:
    """Advanced rate limiter with Redis backend."""
    
    _instance = None
    _initialized = False
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(RateLimiter, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not self._initialized:
            self._initialized = True
            self._redis_client = None
            self._in_memory_store = {}  # Fallback for when Redis unavailable
            self._init_redis()
    
    def _init_redis(self):
        """Initialize Redis connection."""
        if not REDIS_AVAILABLE:
            logger.warning("Using in-memory rate limiting (Redis not available)")
            return
        
        try:
            redis_url = os.getenv('REDIS_URL', 'redis://localhost:6379/0')
            self._redis_client = redis.from_url(redis_url, decode_responses=True)
            # Test connection
            self._redis_client.ping()
            logger.info("Redis rate limiter initialized")
        except Exception as e:
            logger.warning(f"Redis not available, using in-memory rate limiting: {e}")
            self._redis_client = None
    
    def check_rate_limit(self, key: str, max_requests: int, window: int):
        """
        Check if rate limit is exceeded.
        
        Args:
            key: Unique identifier for rate limiting (e.g., user_id, ip_address)
            max_requests: Maximum requests allowed
            window: Time window in seconds
        
        Returns:
            (is_allowed, rate_limit_info)
        """
        if self._redis_client:
            return self._check_redis(key, max_requests, window)
        else:
            return self._check_memory(key, max_requests, window)
    
    def _check_redis(self, key: str, max_requests: int, window: int):
        """Check rate limit using Redis."""
        try:
            rate_key = f"rate_limit:{key}"
            current = self._redis_client.incr(rate_key)
            
            if current == 1:
                # First request in window, set expiration
                self._redis_client.expire(rate_key, window)
            
            remaining = max(0, max_requests - current)
            reset_time = int(time.time()) + window
            
            is_allowed = current <= max_requests
            
            return is_allowed, {
                'limit': max_requests,
                'remaining': remaining,
                'reset': reset_time,
                'retry_after': window if not is_allowed else 0
            }
        except Exception as e:
            logger.error(f"Redis rate limit check failed: {e}")
            # Fail open - allow request if Redis fails
            return True, {'limit': max_requests, 'remaining': max_requests, 'reset': 0, 'retry_after': 0}
    
    def _check_memory(self, key: str, max_requests: int, window: int):
        """Check rate limit using in-memory store."""
        now = time.time()
        rate_key = f"rate_limit:{key}"
        
        if rate_key not in self._in_memory_store:
            self._in_memory_store[rate_key] = {
                'count': 0,
                'window_start': now
            }
        
        store = self._in_memory_store[rate_key]
        
        # Reset if window expired
        if now - store['window_start'] >= window:
            store['count'] = 0
            store['window_start'] = now
        
        store['count'] += 1
        remaining = max(0, max_requests - store['count'])
        reset_time = int(store['window_start'] + window)
        
        is_allowed = store['count'] <= max_requests
        
        return is_allowed, {
            'limit': max_requests,
            'remaining': remaining,
            'reset': reset_time,
            'retry_after': window if not is_allowed else 0
        }
    
    def get_rate_limit_info(self, key: str, max_requests: int, window: int) -> Dict:
        """Get rate limit information without incrementing."""
        if self._redis_client:
            try:
                rate_key = f"rate_limit:{key}"
                current = int(self._redis_client.get(rate_key) or 0)
                remaining = max(0, max_requests - current)
                reset_time = int(time.time()) + window
                
                return {
                    'limit': max_requests,
                    'remaining': remaining,
                    'reset': reset_time
                }
            except Exception:
                return {'limit': max_requests, 'remaining': max_requests, 'reset': 0}
        else:
            # In-memory fallback
            return {'limit': max_requests, 'remaining': max_requests, 'reset': 0}


def rate_limit(max_requests: int = 100, window: int = 60, 
               key_func: Optional[Callable] = None, per_user: bool = False):
    """
    Rate limiting decorator.
    
    Args:
        max_requests: Maximum requests allowed
        window: Time window in seconds
        key_func: Custom function to generate rate limit key
        per_user: If True, rate limit per user (requires authentication)
    """
    limiter = RateLimiter()
    
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Determine rate limit key
            if key_func:
                key = key_func()
            elif per_user:
                user_id = getattr(g, 'user_id', None)
                if not user_id:
                    return jsonify({'error': 'Authentication required'}), 401
                key = f"user:{user_id}"
            else:
                # Default: rate limit by IP
                key = f"ip:{request.remote_addr}"
            
            # Check rate limit
            is_allowed, rate_info = limiter.check_rate_limit(key, max_requests, window)
            
            # Add rate limit headers
            response_headers = {
                'X-RateLimit-Limit': str(rate_info['limit']),
                'X-RateLimit-Remaining': str(rate_info['remaining']),
                'X-RateLimit-Reset': str(rate_info['reset'])
            }
            
            if not is_allowed:
                response_headers['Retry-After'] = str(rate_info['retry_after'])
                return jsonify({
                    'error': 'Rate limit exceeded',
                    'message': f'Too many requests. Please try again in {rate_info["retry_after"]} seconds.',
                    'retry_after': rate_info['retry_after']
                }), 429, response_headers
            
            # Execute function
            response = func(*args, **kwargs)
            
            # Add rate limit headers to response
            if isinstance(response, tuple):
                response_obj, status_code, headers = response[0], response[1], response[2] if len(response) > 2 else {}
                headers.update(response_headers)
                return response_obj, status_code, headers
            else:
                # Flask response object
                for header, value in response_headers.items():
                    response.headers[header] = value
                return response
        
        return wrapper
    return decorator


def rate_limit_by_ip(max_requests: int = 100, window: int = 60):
    """Rate limit by IP address."""
    return rate_limit(max_requests=max_requests, window=window, per_user=False)


def rate_limit_by_user(max_requests: int = 1000, window: int = 60):
    """Rate limit by user ID (requires authentication)."""
    return rate_limit(max_requests=max_requests, window=window, per_user=True)


def rate_limit_by_endpoint(max_requests: int = 100, window: int = 60):
    """Rate limit by endpoint path."""
    def key_func():
        return f"endpoint:{request.path}"
    return rate_limit(max_requests=max_requests, window=window, key_func=key_func)
