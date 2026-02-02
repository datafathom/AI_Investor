
import pytest
from services.system.cache_service import CacheService

from unittest.mock import MagicMock, patch

@pytest.fixture
def cache():
    # Force simulated mode for reliable tests without Redis server
    # Patch redis to prevent actual connection attempt in __init__
    with patch('services.system.cache_service.redis.Redis') as mock_redis:
        mock_client = MagicMock()
        mock_redis.return_value = mock_client
        # Ensure ping raises exception so it falls back to simulated, OR just force it.
        # Actually initializing with mock is fine, we just overwrite _is_simulated below.
        
        CacheService._instance = None
        c = CacheService()
        c._is_simulated = True
        c._memory_cache = {}
        return c

def test_cache_set_get(cache):
    cache.set("test_key", {"data": "info"})
    val = cache.get("test_key")
    assert val == {"data": "info"}

def test_cache_delete(cache):
    cache.set("to_delete", 123)
    assert cache.delete("to_delete") is True
    assert cache.get("to_delete") is None

def test_cache_clear_namespace(cache):
    cache.set("ns:1", "a")
    cache.set("ns:2", "b")
    cache.set("other", "c")
    
    count = cache.clear_namespace("ns:")
    assert count == 2
    assert cache.get("ns:1") is None
    assert cache.get("other") == "c"

def test_cache_missing_key(cache):
    assert cache.get("missing") is None
