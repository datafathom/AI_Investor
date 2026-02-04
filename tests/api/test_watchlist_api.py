"""
Tests for Watchlist & Alerts API Endpoints
"""

import pytest
from unittest.mock import MagicMock, AsyncMock
from fastapi import FastAPI
from fastapi.testclient import TestClient
from web.api.watchlist_api import (
    watchlist_router,
    alert_router,
    get_watchlist_provider,
    get_alert_provider
)


@pytest.fixture
def api_app():
    """Create FastAPI app merchant testing."""
    app = FastAPI()
    app.include_router(watchlist_router)
    app.include_router(alert_router)
    return app


@pytest.fixture
def client(api_app):
    """Create test client."""
    return TestClient(api_app)


@pytest.fixture
def mock_watchlist_service(api_app):
    """Mock WatchlistService."""
    service = AsyncMock()
    
    watchlist = MagicMock()
    watchlist.model_dump.return_value = {"id": "w1", "name": "Tech"}
    
    service.create_watchlist.return_value = watchlist
    service.get_user_watchlists.return_value = [watchlist]
    service.add_symbol.return_value = watchlist
    service.remove_symbol.return_value = watchlist
    
    api_app.dependency_overrides[get_watchlist_provider] = lambda: service
    return service


@pytest.fixture
def mock_alert_service(api_app):
    """Mock AlertService."""
    service = AsyncMock()
    
    alert = MagicMock()
    alert.model_dump.return_value = {"id": "a1", "symbol": "AAPL"}
    alert.user_id = "test_user"
    
    service.create_price_alert.return_value = alert
    service.active_alerts = {"a1": alert}
    service._get_alert.return_value = alert
    service._save_alert = AsyncMock()
    
    api_app.dependency_overrides[get_alert_provider] = lambda: service
    return service


# --- Watchlist Tests ---

def test_create_watchlist_success(client, mock_watchlist_service):
    """Test creating watchlist."""
    from web.auth_utils import get_current_user
    client.app.dependency_overrides[get_current_user] = lambda: {"user_id": "test_user"}
    
    payload = {"user_id": "test_user", "watchlist_name": "Tech"}
    response = client.post('/api/v1/watchlist/create', json=payload)
    
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert data['data']['name'] == "Tech"


def test_get_user_watchlists_success(client, mock_watchlist_service):
    """Test getting user watchlists."""
    from web.auth_utils import get_current_user
    client.app.dependency_overrides[get_current_user] = lambda: {"user_id": "test_user"}
    
    response = client.get('/api/v1/watchlist/user/test_user')
    
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert len(data['data']) == 1


def test_add_symbol_success(client, mock_watchlist_service):
    """Test adding symbol to watchlist."""
    from web.auth_utils import get_current_user
    client.app.dependency_overrides[get_current_user] = lambda: {"user_id": "test_user"}
    
    payload = {"symbol": "AAPL"}
    response = client.post('/api/v1/watchlist/w1/add', json=payload)
    
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True


def test_remove_symbol_success(client, mock_watchlist_service):
    """Test removing symbol from watchlist."""
    from web.auth_utils import get_current_user
    client.app.dependency_overrides[get_current_user] = lambda: {"user_id": "test_user"}
    
    payload = {"symbol": "AAPL"}
    response = client.post('/api/v1/watchlist/w1/remove', json=payload)
    
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True


# --- Alert Tests ---

def test_create_alert_success(client, mock_alert_service):
    """Test creating alert."""
    from web.auth_utils import get_current_user
    client.app.dependency_overrides[get_current_user] = lambda: {"user_id": "test_user"}
    
    payload = {
        "user_id": "test_user",
        "symbol": "AAPL",
        "alert_type": "price_above",
        "threshold": 150.0
    }
    response = client.post('/api/v1/alert/create', json=payload)
    
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert data['data']['symbol'] == "AAPL"


def test_get_user_alerts_success(client, mock_alert_service):
    """Test getting user alerts."""
    from web.auth_utils import get_current_user
    client.app.dependency_overrides[get_current_user] = lambda: {"user_id": "test_user"}
    
    response = client.get('/api/v1/alert/user/test_user')
    
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert len(data['data']) == 1


def test_cancel_alert_success(client, mock_alert_service):
    """Test cancelling alert."""
    from web.auth_utils import get_current_user
    client.app.dependency_overrides[get_current_user] = lambda: {"user_id": "test_user"}
    
    response = client.post('/api/v1/alert/a1/cancel')
    
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
