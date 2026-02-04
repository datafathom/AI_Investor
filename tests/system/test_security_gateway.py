"""
Security Gateway Tests
Tests rate limiting and security gateway functionality with FastAPI.
"""
import pytest
from fastapi import FastAPI, Request
from fastapi.testclient import TestClient
from services.system.security_gateway import (
    limit,
    get_security_gateway,
    get_rate_limiter,
    InMemoryRateLimiter
)


def test_rate_limiting_enforcement() -> None:
    """
    Tests rate limiting on a FastAPI app.
    Uses a limit of 2 per minute for quick testing.
    """
    app = FastAPI()
    limiter = get_rate_limiter()
    
    # Reset the limiter for clean test
    limiter.requests.clear()
    
    @app.get("/test-limit")
    @limit("2 per minute")
    async def test_limit_endpoint(request: Request):
        return {"status": "OK"}
    
    client = TestClient(app)
    
    # Hit 1
    response1 = client.get("/test-limit")
    assert response1.status_code == 200
    
    # Hit 2
    response2 = client.get("/test-limit")
    assert response2.status_code == 200
    
    # Hit 3 (Should be rate limited)
    response3 = client.get("/test-limit")
    assert response3.status_code == 429


def test_gateway_status() -> None:
    """Test the security gateway status endpoint."""
    gw = get_security_gateway()
    status = gw.get_status()
    assert status["status"] == "Active"
    assert "rate_limiter" in status
    assert "waf_rules" in status


def test_in_memory_limiter() -> None:
    """Test the InMemoryRateLimiter directly."""
    limiter = InMemoryRateLimiter()
    key = "test_key"
    
    # First 3 requests should pass with limit of 3
    assert limiter.is_allowed(key, limit=3, window_seconds=60) is True
    assert limiter.is_allowed(key, limit=3, window_seconds=60) is True
    assert limiter.is_allowed(key, limit=3, window_seconds=60) is True
    
    # Fourth should fail
    assert limiter.is_allowed(key, limit=3, window_seconds=60) is False
    
    # Reset and try again
    limiter.reset(key)
    assert limiter.is_allowed(key, limit=3, window_seconds=60) is True
