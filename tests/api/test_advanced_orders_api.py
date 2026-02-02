"""
Tests for Advanced Orders API Endpoints
Phase 13: Advanced Order Types & Smart Execution
"""

import pytest
from unittest.mock import AsyncMock, patch
from flask import Flask
from datetime import datetime, timezone
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


def test_create_trailing_stop_success(client, mock_advanced_order_service):
    """Test successful trailing stop order creation."""
    from models.orders import TrailingStopOrder
    
    mock_order = TrailingStopOrder(
        order_id='order_1',
        symbol='AAPL',
        quantity=100,
        trailing_type='percentage',
        trailing_value=5.0,
        initial_stop_price=145.0,
        current_stop_price=145.0,
        highest_price=150.0
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
    assert data['data']['trailing_type'] == 'percentage'


def test_create_trailing_stop_missing_params(client):
    """Test trailing stop creation with missing parameters."""
    response = client.post('/api/orders/trailing-stop',
                          json={'user_id': 'user_1', 'symbol': 'AAPL'})
    
    assert response.status_code == 400
    data = response.get_json()
    assert data['success'] is False


def test_create_bracket_order_success(client, mock_advanced_order_service):
    """Test successful bracket order creation."""
    from models.orders import BracketOrder
    
    mock_order = BracketOrder(
        bracket_id='bracket_1',
        entry_order_id='order_1',
        profit_target_order_id='order_2',
        stop_loss_order_id='order_3',
        profit_target_price=160.0,
        stop_loss_price=145.0
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


def test_execute_twap_success(client, mock_smart_execution_service):
    """Test successful TWAP execution."""
    from models.orders import ExecutionResult
    
    mock_result = ExecutionResult(
        execution_id='exec_1',
        order_id='order_1',
        filled_quantity=100,
        average_price=150.0,
        execution_time=datetime.now(timezone.utc),
        execution_strategy='twap'
    )
    mock_smart_execution_service.execute_twap.return_value = [mock_result]
    
    response = client.post('/api/execution/twap',
                          json={
                              'symbol': 'AAPL',
                              'total_quantity': 100,
                              'time_window_minutes': 60
                          })
    
    assert response.status_code == 200
    data = response.get_json()
    assert data['success'] is True
