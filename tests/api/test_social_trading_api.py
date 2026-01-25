"""
Tests for Social Trading API Endpoints
Phase 19: Social Trading & Copy Trading
"""

import pytest
from unittest.mock import AsyncMock, patch
from flask import Flask
from web.api.social_trading_api import social_trading_bp


@pytest.fixture
def app():
    """Create Flask app for testing."""
    app = Flask(__name__)
    app.config['TESTING'] = True
    app.register_blueprint(social_trading_bp)
    return app


@pytest.fixture
def client(app):
    """Create test client."""
    return app.test_client()


@pytest.fixture
def mock_social_trading_service():
    """Mock SocialTradingService."""
    with patch('web.api.social_trading_api.get_social_trading_service') as mock:
        service = AsyncMock()
        mock.return_value = service
        yield service


@pytest.fixture
def mock_copy_trading_service():
    """Mock CopyTradingService."""
    with patch('web.api.social_trading_api.get_copy_trading_service') as mock:
        service = AsyncMock()
        mock.return_value = service
        yield service


@pytest.mark.asyncio
async def test_create_trader_profile_success(client, mock_social_trading_service):
    """Test successful trader profile creation."""
    from models.social_trading import TraderProfile
    
    mock_profile = TraderProfile(
        profile_id='profile_1',
        user_id='user_1',
        display_name='Test Trader',
        bio='Test bio',
        is_public=True
    )
    mock_social_trading_service.create_trader_profile.return_value = mock_profile
    
    response = client.post('/api/social-trading/profile/create',
                          json={
                              'user_id': 'user_1',
                              'display_name': 'Test Trader',
                              'bio': 'Test bio',
                              'is_public': True
                          })
    
    assert response.status_code == 200
    data = response.get_json()
    assert data['success'] is True
    assert data['data']['display_name'] == 'Test Trader'


@pytest.mark.asyncio
async def test_create_trader_profile_missing_params(client):
    """Test trader profile creation with missing parameters."""
    response = client.post('/api/social-trading/profile/create',
                          json={'user_id': 'user_1'})
    
    assert response.status_code == 400
    data = response.get_json()
    assert data['success'] is False


@pytest.mark.asyncio
async def test_get_top_traders_success(client, mock_social_trading_service):
    """Test successful top traders retrieval."""
    from models.social_trading import TraderProfile
    
    mock_traders = [
        TraderProfile(
            profile_id='profile_1',
            user_id='user_1',
            display_name='Top Trader',
            is_public=True
        )
    ]
    mock_social_trading_service.get_top_traders.return_value = mock_traders
    
    response = client.get('/api/social-trading/traders/top?limit=10')
    
    assert response.status_code == 200
    data = response.get_json()
    assert data['success'] is True
    assert len(data['data']) == 1


@pytest.mark.asyncio
async def test_follow_trader_success(client, mock_social_trading_service):
    """Test successful trader follow."""
    response = client.post('/api/social-trading/follow',
                          json={
                              'user_id': 'user_1',
                              'trader_id': 'trader_1'
                          })
    
    assert response.status_code == 200
    data = response.get_json()
    assert data['success'] is True


@pytest.mark.asyncio
async def test_create_copy_trading_config_success(client, mock_copy_trading_service):
    """Test successful copy trading configuration creation."""
    from models.social_trading import CopyTradingConfig
    
    mock_config = CopyTradingConfig(
        config_id='config_1',
        user_id='user_1',
        trader_id='trader_1',
        allocation_percent=10.0,
        risk_controls={}
    )
    mock_copy_trading_service.create_copy_config.return_value = mock_config
    
    response = client.post('/api/social-trading/copy/create',
                          json={
                              'user_id': 'user_1',
                              'trader_id': 'trader_1',
                              'allocation_percent': 10.0
                          })
    
    assert response.status_code == 200
    data = response.get_json()
    assert data['success'] is True
