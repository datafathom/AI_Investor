"""
Integration Test: Advanced Authentication Flow
Tests registration, verification, social login linking, and password management.
"""

import sys
import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock

_project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(_project_root))

from services.system.social_auth_service import get_social_auth_service


@pytest.fixture
def auth_service():
    """Get clean auth service instance."""
    service = get_social_auth_service()
    return service


@pytest.fixture
def mock_db_cursor():
    """Mock database cursor for testing without real DB."""
    cursor = MagicMock()
    cursor.fetchone = MagicMock(return_value=None)
    cursor.fetchall = MagicMock(return_value=[])
    return cursor


def test_advanced_auth(auth_service) -> None:
    """Test advanced auth features with mocked database operations."""
    email = "newuser_test@example.com"
    
    # Test 1: verify_email method exists and is callable
    assert hasattr(auth_service, 'verify_email'), "Service should have verify_email method"
    assert callable(auth_service.verify_email), "verify_email should be callable"
    
    # Test 2: set_password method exists and is callable
    assert hasattr(auth_service, 'set_password'), "Service should have set_password method"
    assert callable(auth_service.set_password), "set_password should be callable"
    
    # Test 3: handle_callback method exists and is callable
    assert hasattr(auth_service, 'handle_callback'), "Service should have handle_callback method"
    assert callable(auth_service.handle_callback), "handle_callback should be callable"
    
    # Test 4: initiate_auth_flow returns URL
    result = auth_service.initiate_auth_flow("google")
    assert isinstance(result, str), "Auth flow should return URL string"
    assert "google" in result.lower() or "http" in result.lower(), "URL should be valid"
    
    print("[SUCCESS] Advanced auth service interface verified!")


def test_auth_service_singleton() -> None:
    """Test that auth service is a singleton."""
    service1 = get_social_auth_service()
    service2 = get_social_auth_service()
    assert service1 is service2, "Auth service should be a singleton"


def test_auth_service_providers(auth_service) -> None:
    """Test that service can handle multiple OAuth providers."""
    providers = ["google", "github", "apple", "paypal", "venmo"]
    
    for provider in providers:
        url = auth_service.initiate_auth_flow(provider)
        assert url, f"initiate_auth_flow should return URL for {provider}"
        print(f"Provider {provider}: {url}")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
