
import redis
import json
import logging
from typing import Any, Optional, Union
from services.system.secret_manager import get_secret_manager

logger = logging.getLogger(__name__)

class CacheService:
    """
    Singleton service for Redis-backed caching with in-memory fallback.
    """
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(CacheService, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if hasattr(self, '_initialized'):
            return
            
        sm = get_secret_manager()
        self._redis_host = sm.get_secret('REDIS_HOST', 'localhost')
        self._redis_port = int(sm.get_secret('REDIS_PORT', 6379))
        self._redis_db = int(sm.get_secret('REDIS_DB', 0))
        self._redis_password = sm.get_secret('REDIS_PASSWORD', None)
        
        self._client = None
        self._is_simulated = True
        self._memory_cache = {} # Fallback for local dev without Redis
        
        try:
            self._client = redis.Redis(
                host=self._redis_host,
                port=self._redis_port,
                db=self._redis_db,
                password=self._redis_password,
                decode_responses=True,
                socket_connect_timeout=2
            )
            # Ping to verify connectivity
            self._client.ping()
            self._is_simulated = False
            logger.info(f"CacheService connected to Redis at {self._redis_host}:{self._redis_port}")
        except Exception as e:
            logger.warning(f"Redis unavailable ({e}). Falling back to In-Memory simulation.")
            self._is_simulated = True

        self._initialized = True

    def get(self, key: str) -> Optional[Any]:
        """Retrieves a value from cache."""
        try:
            if not self._is_simulated:
                val = self._client.get(key)
                return json.loads(val) if val else None
            return self._memory_cache.get(key)
        except Exception as e:
            logger.error(f"Cache GET error for {key}: {e}")
            return None

    def set(self, key: str, value: Any, ttl: int = 3600) -> bool:
        """Sets a value in cache with optional TTL (seconds)."""
        try:
            if not self._is_simulated:
                serialized = json.dumps(value)
                return self._client.set(key, serialized, ex=ttl)
            self._memory_cache[key] = value
            # Note: Memory fallback doesn't strictly enforce TTL in this simple impl
            return True
        except Exception as e:
            logger.error(f"Cache SET error for {key}: {e}")
            return False

    def delete(self, key: str) -> bool:
        """Removes a key from cache."""
        try:
            if not self._is_simulated:
                return bool(self._client.delete(key))
            if key in self._memory_cache:
                del self._memory_cache[key]
                return True
            return False
        except Exception as e:
            logger.error(f"Cache DELETE error for {key}: {e}")
            return False

    def clear_namespace(self, prefix: str) -> int:
        """Deletes all keys starting with prefix."""
        count = 0
        try:
            if not self._is_simulated:
                keys = self._client.keys(f"{prefix}*")
                if keys:
                    count = self._client.delete(*keys)
            else:
                to_del = [k for k in self._memory_cache if k.startswith(prefix)]
                for k in to_del:
                    del self._memory_cache[k]
                count = len(to_del)
            return count
        except Exception as e:
            logger.error(f"Cache clear error for {prefix}: {e}")
            return 0

def get_cache_service() -> CacheService:
    return CacheService()
