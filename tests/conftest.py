"""
Root pytest configuration for AI Investor test suite.

Provides shared fixtures and pytest configuration for all test categories.
"""
import pytest
import asyncio
import sys
import warnings
from pathlib import Path
from unittest.mock import MagicMock, AsyncMock

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

# Filter deprecation warnings that are in our control
warnings.filterwarnings("ignore", message=".*datetime.utcnow.*", category=DeprecationWarning)
warnings.filterwarnings("ignore", message=".*Pydantic V1.*", category=DeprecationWarning)


@pytest.fixture(scope="session")
def event_loop():
    """Create an event loop for the test session."""
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
def mock_db():
    """Provide a mock database connection."""
    db = MagicMock()
    db.execute = MagicMock(return_value=MagicMock(fetchall=lambda: []))
    db.commit = MagicMock()
    db.close = MagicMock()
    return db


@pytest.fixture
def mock_async_db():
    """Provide an async mock database connection."""
    db = AsyncMock()
    db.execute = AsyncMock(return_value=MagicMock(fetchall=lambda: []))
    db.commit = AsyncMock()
    db.close = AsyncMock()
    return db


@pytest.fixture
def mock_redis():
    """Provide a mock Redis client."""
    redis_client = MagicMock()
    redis_client.get = MagicMock(return_value=None)
    redis_client.set = MagicMock(return_value=True)
    redis_client.delete = MagicMock(return_value=True)
    redis_client.exists = MagicMock(return_value=False)
    return redis_client


@pytest.fixture
def mock_http_client():
    """Provide a mock HTTP client for external API testing."""
    client = AsyncMock()
    client.get = AsyncMock(return_value=MagicMock(status_code=200, json=lambda: {}))
    client.post = AsyncMock(return_value=MagicMock(status_code=200, json=lambda: {}))
    return client


@pytest.fixture
def sample_user_data() -> dict:
    """Provide sample user data for testing."""
    return {
        "user_id": "test_user_123",
        "email": "test@example.com",
        "username": "testuser",
        "first_name": "Test",
        "last_name": "User"
    }


@pytest.fixture
def sample_portfolio_data() -> dict:
    """Provide sample portfolio data for testing."""
    return {
        "portfolio_id": "port_123",
        "user_id": "test_user_123",
        "name": "Test Portfolio",
        "holdings": [
            {"symbol": "AAPL", "quantity": 10, "avg_cost": 150.00},
            {"symbol": "GOOGL", "quantity": 5, "avg_cost": 2800.00}
        ],
        "total_value": 15500.00
    }
