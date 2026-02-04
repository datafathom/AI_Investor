"""
Tests for Social Trading API Endpoints
"""

import pytest
from unittest.mock import MagicMock, AsyncMock
from fastapi import FastAPI
from fastapi.testclient import TestClient
from web.api.social_trading_api import router, get_social_trading_provider, get_copy_trading_provider


@pytest.fixture
def api_app():
    """Create FastAPI app merchant testing."""
    app = FastAPI()
    app.include_router(router)
    return app


@pytest.fixture
def client(api_app):
    """Create test client."""
    return TestClient(api_app)


@pytest.fixture
def mock_social_service(api_app):
    """Mock Social Trading Service."""
    service = AsyncMock()
    
    profile = MagicMock()
    profile.model_dump.return_value = {"user_id": "u1", "display_name": "Trader 1"}
    
    service.create_trader_profile.return_value = profile
    service.get_top_traders.return_value = [profile]
    service.follow_trader.return_value = {"status": "followed"}
    
    api_app.dependency_overrides[get_social_trading_provider] = lambda: service
    return service


@pytest.fixture
def mock_copy_service(api_app):
    """Mock Copy Trading Service."""
    service = AsyncMock()
    
    config = MagicMock()
    config.model_dump.return_value = {"trader_id": "t1", "allocation": 0.5}
    
    trade = MagicMock()
    trade.model_dump.return_value = {"id": "ct1", "symbol": "AAPL"}
    
    service.create_copy_config.return_value = config
    service.execute_copy_trade.return_value = [trade]
    
    api_app.dependency_overrides[get_copy_trading_provider] = lambda: service
    return service


def test_create_trader_profile_success(client, mock_social_service):
    """Test creating trader profile."""
    # Mock current_user dependency
    from web.auth_utils import get_current_user
    client.app.dependency_overrides[get_current_user] = lambda: {"user_id": "test_user"}
    
    payload = {"user_id": "u1", "display_name": "Trader 1"}
    response = client.post('/api/v1/social_trading/profile/create', json=payload)
    
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert data['data']['user_id'] == "u1"


def test_get_top_traders_success(client, mock_social_service):
    """Test getting top traders."""
    from web.auth_utils import get_current_user
    client.app.dependency_overrides[get_current_user] = lambda: {"user_id": "test_user"}
    
    response = client.get('/api/v1/social_trading/traders/top')
    
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert len(data['data']) == 1


def test_follow_trader_success(client, mock_social_service):
    """Test following trader."""
    from web.auth_utils import get_current_user
    client.app.dependency_overrides[get_current_user] = lambda: {"user_id": "test_user"}
    
    payload = {"follower_id": "f1", "trader_id": "t1"}
    response = client.post('/api/v1/social_trading/follow', json=payload)
    
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True


def test_create_copy_config_success(client, mock_copy_service):
    """Test creating copy config."""
    from web.auth_utils import get_current_user
    client.app.dependency_overrides[get_current_user] = lambda: {"user_id": "test_user"}
    
    payload = {"follower_id": "f1", "trader_id": "t1", "allocation_percentage": 0.5}
    response = client.post('/api/v1/social_trading/copy/create', json=payload)
    
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True


def test_execute_copy_trade_success(client, mock_copy_service):
    """Test executing copy trade."""
    from web.auth_utils import get_current_user
    client.app.dependency_overrides[get_current_user] = lambda: {"user_id": "test_user"}
    
    payload = {"trader_id": "t1", "original_trade": {"symbol": "AAPL", "side": "buy"}}
    response = client.post('/api/v1/social_trading/copy/execute', json=payload)
    
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert len(data['data']) == 1
