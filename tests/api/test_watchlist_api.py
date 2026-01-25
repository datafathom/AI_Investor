"""
Tests for Watchlist & Alerts API Endpoints
Phase 17: Watchlists & Price Alerts
"""

import pytest
from unittest.mock import AsyncMock, patch
from flask import Flask
from web.api.watchlist_api import watchlist_bp, alert_bp


@pytest.fixture
def app():
    """Create Flask app for testing."""
    app = Flask(__name__)
    app.config['TESTING'] = True
    app.register_blueprint(watchlist_bp)
    app.register_blueprint(alert_bp)
    return app


@pytest.fixture
def client(app):
    """Create test client."""
    return app.test_client()


@pytest.fixture
def mock_watchlist_service():
    """Mock WatchlistService."""
    with patch('web.api.watchlist_api.get_watchlist_service') as mock:
        service = AsyncMock()
        mock.return_value = service
        yield service


@pytest.fixture
def mock_alert_service():
    """Mock AlertService."""
    with patch('web.api.watchlist_api.get_alert_service') as mock:
        service = AsyncMock()
        mock.return_value = service
        yield service


@pytest.mark.asyncio
async def test_create_watchlist_success(client, mock_watchlist_service):
    """Test successful watchlist creation."""
    from models.watchlist import Watchlist
    
    mock_watchlist = Watchlist(
        watchlist_id='watchlist_1',
        user_id='user_1',
        watchlist_name='My Watchlist',
        symbols=['AAPL', 'MSFT']
    )
    mock_watchlist_service.create_watchlist.return_value = mock_watchlist
    
    response = client.post('/api/watchlist/create',
                          json={
                              'user_id': 'user_1',
                              'watchlist_name': 'My Watchlist',
                              'symbols': ['AAPL', 'MSFT']
                          })
    
    assert response.status_code == 200
    data = response.get_json()
    assert data['success'] is True
    assert data['data']['watchlist_name'] == 'My Watchlist'


@pytest.mark.asyncio
async def test_create_watchlist_missing_params(client):
    """Test watchlist creation with missing parameters."""
    response = client.post('/api/watchlist/create', json={'user_id': 'user_1'})
    
    assert response.status_code == 400
    data = response.get_json()
    assert data['success'] is False


@pytest.mark.asyncio
async def test_get_user_watchlists_success(client, mock_watchlist_service):
    """Test successful user watchlists retrieval."""
    from models.watchlist import Watchlist
    
    mock_watchlists = [
        Watchlist(
            watchlist_id='watchlist_1',
            user_id='user_1',
            watchlist_name='My Watchlist',
            symbols=[]
        )
    ]
    mock_watchlist_service.get_user_watchlists.return_value = mock_watchlists
    
    response = client.get('/api/watchlist/user/user_1')
    
    assert response.status_code == 200
    data = response.get_json()
    assert data['success'] is True
    assert len(data['data']) == 1


@pytest.mark.asyncio
async def test_add_symbol_to_watchlist_success(client, mock_watchlist_service):
    """Test successful symbol addition to watchlist."""
    from models.watchlist import Watchlist
    
    mock_watchlist = Watchlist(
        watchlist_id='watchlist_1',
        user_id='user_1',
        watchlist_name='My Watchlist',
        symbols=['AAPL']
    )
    mock_watchlist_service.add_symbol.return_value = mock_watchlist
    
    response = client.post('/api/watchlist/watchlist_1/add',
                          json={'symbol': 'AAPL'})
    
    assert response.status_code == 200
    data = response.get_json()
    assert data['success'] is True


@pytest.mark.asyncio
async def test_create_alert_success(client, mock_alert_service):
    """Test successful alert creation."""
    from models.watchlist import Alert
    
    mock_alert = Alert(
        alert_id='alert_1',
        user_id='user_1',
        symbol='AAPL',
        alert_type='price',
        threshold=150.0,
        condition='above'
    )
    mock_alert_service.create_alert.return_value = mock_alert
    
    response = client.post('/api/alert/create',
                          json={
                              'user_id': 'user_1',
                              'symbol': 'AAPL',
                              'alert_type': 'price',
                              'threshold': 150.0,
                              'condition': 'above'
                          })
    
    assert response.status_code == 200
    data = response.get_json()
    assert data['success'] is True
    assert data['data']['symbol'] == 'AAPL'


@pytest.mark.asyncio
async def test_get_user_alerts_success(client, mock_alert_service):
    """Test successful user alerts retrieval."""
    from models.watchlist import Alert
    
    mock_alerts = [
        Alert(
            alert_id='alert_1',
            user_id='user_1',
            symbol='AAPL',
            alert_type='price',
            threshold=150.0,
            condition='above'
        )
    ]
    mock_alert_service.get_user_alerts.return_value = mock_alerts
    
    response = client.get('/api/alert/user/user_1')
    
    assert response.status_code == 200
    data = response.get_json()
    assert data['success'] is True
    assert len(data['data']) == 1
