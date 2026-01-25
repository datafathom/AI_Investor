"""
Tests for Advanced Orders API Endpoints
Phase 13: Advanced Order Types & Smart Execution
"""

import pytest
from unittest.mock import AsyncMock, patch
from flask import Flask
from web.api.advanced_orders_api import advanced_orders_bp, execution_bp


@pytest.fixture
def app():
    """Create Flask app for testing."""
    app = Flask(__name__)
    app.config['TESTING'] = True
    app.register_blueprint(advanced_orders_bp)
    app.register_blueprint(execution_bp)
    return app


@pytest.fixture
def client(app):
    """Create test client."""
    return app.test_client()


@pytest.fixture
def mock_advanced_order_service():
    """Mock AdvancedOrderService."""
    with patch('web.api.advanced_orders_api.get_advanced_order_service') as mock:
        service = AsyncMock()
        mock.return_value = service
        yield service


@pytest.fixture
def mock_smart_execution_service():
    """Mock SmartExecutionService."""
    with patch('web.api.advanced_orders_api.get_smart_execution_service') as mock:
        service = AsyncMock()
        mock.return_value = service
        yield service


@pytest.mark.asyncio
async def test_create_trailing_stop_success(client, mock_advanced_order_service):
    """Test successful trailing stop order creation."""
    from models.orders import Order
    
    mock_order = Order(
        order_id='order_1',
        user_id='user_1',
        symbol='AAPL',
        quantity=100,
        order_type='trailing_stop',
        status='pending'
    )
    mock_advanced_order_service.create_trailing_stop.return_value = mock_order
    
    response = client.post('/api/orders/trailing-stop',
                          json={
                              'user_id': 'user_1',
                              'symbol': 'AAPL',
                              'quantity': 100,
                              'trailing_type': 'percentage',
                              'trailing_value': 5.0
                          })
    
    assert response.status_code == 200
    data = response.get_json()
    assert data['success'] is True
    assert data['data']['order_type'] == 'trailing_stop'


@pytest.mark.asyncio
async def test_create_trailing_stop_missing_params(client):
    """Test trailing stop creation with missing parameters."""
    response = client.post('/api/orders/trailing-stop',
                          json={'user_id': 'user_1', 'symbol': 'AAPL'})
    
    assert response.status_code == 400
    data = response.get_json()
    assert data['success'] is False


@pytest.mark.asyncio
async def test_create_bracket_order_success(client, mock_advanced_order_service):
    """Test successful bracket order creation."""
    from models.orders import Order
    
    mock_order = Order(
        order_id='order_1',
        user_id='user_1',
        symbol='AAPL',
        quantity=100,
        order_type='bracket',
        status='pending'
    )
    mock_advanced_order_service.create_bracket_order.return_value = mock_order
    
    response = client.post('/api/orders/bracket',
                          json={
                              'user_id': 'user_1',
                              'symbol': 'AAPL',
                              'quantity': 100,
                              'entry_price': 150.0,
                              'profit_target': 160.0,
                              'stop_loss': 145.0
                          })
    
    assert response.status_code == 200
    data = response.get_json()
    assert data['success'] is True


@pytest.mark.asyncio
async def test_execute_twap_success(client, mock_smart_execution_service):
    """Test successful TWAP execution."""
    from models.orders import ExecutionResult
    
    mock_result = ExecutionResult(
        execution_id='exec_1',
        order_id='order_1',
        total_filled=100,
        avg_price=150.0
    )
    mock_smart_execution_service.execute_twap.return_value = mock_result
    
    response = client.post('/api/execution/twap',
                          json={
                              'order_id': 'order_1',
                              'duration_minutes': 60,
                              'interval_minutes': 5
                          })
    
    assert response.status_code == 200
    data = response.get_json()
    assert data['success'] is True
