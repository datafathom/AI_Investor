"""
Performance Caching Service
Advanced caching strategies for improved performance
"""

import os
import json
import hashlib
import logging
from typing import Any, Optional, Callable
from datetime import timezone, datetime, timedelta
from functools import wraps

logger = logging.getLogger(__name__)

# Try to import Redis
try:
    import redis
    REDIS_AVAILABLE = True
except ImportError:
    REDIS_AVAILABLE = False
    logger.warning("Redis not available. Install with: pip install redis")


class PerformanceCache:
    """High-performance caching service with Redis backend."""
    
    _instance = None
    _initialized = False
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(PerformanceCache, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not self._initialized:
            self._initialized = True
            self._redis_client = None
            self._local_cache = {}  # Fallback in-memory cache
            self._init_redis()
    
    def _init_redis(self):
        """Initialize Redis connection."""
        if not REDIS_AVAILABLE:
            logger.warning("Using in-memory cache (Redis not available)")
            return
        
        try:
            redis_url = os.getenv('REDIS_URL', 'redis://localhost:6379/0')
            self._redis_client = redis.from_url(
                redis_url,
                decode_responses=True,
                socket_connect_timeout=5,
                socket_timeout=5,
                retry_on_timeout=True
            )
            # Test connection
            self._redis_client.ping()
            logger.info("Redis cache initialized")
        except Exception as e:
            logger.warning(f"Redis connection failed, using in-memory cache: {e}")
            self._redis_client = None
    
    def get(self, key: str, default: Any = None) -> Optional[Any]:
        """Get value from cache."""
        try:
            if self._redis_client:
                value = self._redis_client.get(key)
                if value:
                    return json.loads(value)
            else:
                # Fallback to local cache
                if key in self._local_cache:
                    entry = self._local_cache[key]
                    if entry['expires_at'] > datetime.now(timezone.utc):
                        return entry['value']
                    else:
                        del self._local_cache[key]
        except Exception as e:
            logger.error(f"Cache get error: {e}")
        
        return default
    
    def set(self, key: str, value: Any, ttl: int = 3600):
        """Set value in cache with TTL."""
        try:
            if self._redis_client:
                self._redis_client.setex(
                    key,
                    ttl,
                    json.dumps(value, default=str)
                )
            else:
                # Fallback to local cache
                self._local_cache[key] = {
                    'value': value,
                    'expires_at': datetime.now(timezone.utc) + timedelta(seconds=ttl)
                }
                # Cleanup old entries
                if len(self._local_cache) > 1000:
                    self._cleanup_local_cache()
        except Exception as e:
            logger.error(f"Cache set error: {e}")
    
    def delete(self, key: str):
        """Delete key from cache."""
        try:
            if self._redis_client:
                self._redis_client.delete(key)
            else:
                self._local_cache.pop(key, None)
        except Exception as e:
            logger.error(f"Cache delete error: {e}")
    
    def clear(self, pattern: Optional[str] = None):
        """Clear cache entries."""
        try:
            if self._redis_client:
                if pattern:
                    keys = self._redis_client.keys(pattern)
                    if keys:
                        self._redis_client.delete(*keys)
                else:
                    self._redis_client.flushdb()
            else:
                if pattern:
                    # Simple pattern matching for local cache
                    keys_to_delete = [k for k in self._local_cache.keys() if pattern in k]
                    for k in keys_to_delete:
                        del self._local_cache[k]
                else:
                    self._local_cache.clear()
        except Exception as e:
            logger.error(f"Cache clear error: {e}")
    
    def _cleanup_local_cache(self):
        """Remove expired entries from local cache."""
        now = datetime.now(timezone.utc)
        expired_keys = [
            k for k, v in self._local_cache.items()
            if v['expires_at'] <= now
        ]
        for k in expired_keys:
            del self._local_cache[k]
    
    def get_or_set(self, key: str, func: Callable, ttl: int = 3600, *args, **kwargs) -> Any:
        """Get from cache or compute and cache result."""
        value = self.get(key)
        if value is not None:
            return value
        
        # Compute value
        value = func(*args, **kwargs)
        self.set(key, value, ttl)
        return value
    
    def invalidate_pattern(self, pattern: str):
        """Invalidate all keys matching pattern."""
        self.clear(pattern)


def cache_key(*args, **kwargs) -> str:
    """Generate cache key from arguments."""
    key_parts = []
    for arg in args:
        if isinstance(arg, (str, int, float, bool)):
            key_parts.append(str(arg))
        else:
            key_parts.append(hashlib.md5(str(arg).encode()).hexdigest())
    
    for k, v in sorted(kwargs.items()):
        key_parts.append(f"{k}:{v}")
    
    return ":".join(key_parts)


def cached(ttl: int = 3600, key_func: Optional[Callable] = None):
    """Decorator for caching function results."""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            cache = PerformanceCache()
            
            # Generate cache key
            if key_func:
                cache_key_str = key_func(*args, **kwargs)
            else:
                cache_key_str = f"{func.__module__}:{func.__name__}:{cache_key(*args, **kwargs)}"
            
            # Try to get from cache
            result = cache.get(cache_key_str)
            if result is not None:
                return result
            
            # Compute result
            result = func(*args, **kwargs)
            
            # Cache result
            cache.set(cache_key_str, result, ttl)
            
            return result
        return wrapper
    return decorator


def get_cache() -> PerformanceCache:
    """Get cache instance."""
    return PerformanceCache()
