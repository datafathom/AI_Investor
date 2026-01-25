
import pytest
from services.system.cache_service import CacheService

@pytest.fixture
def cache():
    # Force simulated mode for reliable tests without Redis server
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
