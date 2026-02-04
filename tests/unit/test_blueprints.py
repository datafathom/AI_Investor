"""
Router Registration Tests
Verifies that all FastAPI routers are properly registered.
"""
import pytest


def test_fastapi_gateway_imports() -> None:
    """Test that FastAPI gateway can be imported without errors."""
    from web.fastapi_gateway import app
    assert app is not None
    assert app.title == "AI Investor API Gateway"


def test_gateway_routes_registered() -> None:
    """Test that routes are registered in the gateway."""
    from web.fastapi_gateway import app
    
    routes = [route.path for route in app.routes]
    
    # Verify core routes exist
    assert "/health" in routes
    assert "/api/health" in routes
    
    # Check that we have many routes registered (all the routers)
    assert len(routes) > 50, f"Expected many routes, got {len(routes)}"


def test_legal_router_registered() -> None:
    """Test that the legal router is registered."""
    from web.fastapi_gateway import app
    
    routes = [route.path for route in app.routes]
    legal_routes = [r for r in routes if '/legal' in r]
    
    assert len(legal_routes) > 0, "Legal routes should be registered"


def test_auth_router_registered() -> None:
    """Test that the auth router is registered."""
    from web.fastapi_gateway import app
    
    routes = [route.path for route in app.routes]
    auth_routes = [r for r in routes if '/auth' in r]
    
    assert len(auth_routes) > 0, "Auth routes should be registered"


def test_billing_router_registered() -> None:
    """Test that the billing router is registered."""
    from web.fastapi_gateway import app
    
    routes = [route.path for route in app.routes]
    billing_routes = [r for r in routes if '/billing' in r]
    
    assert len(billing_routes) > 0, "Billing routes should be registered"
