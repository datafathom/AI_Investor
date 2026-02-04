
import pytest
from unittest.mock import AsyncMock, patch
from fastapi import FastAPI
from fastapi.testclient import TestClient
from datetime import datetime, timezone
from web.api.advanced_orders_api import router, get_advanced_order_service, get_smart_execution_service
from web.auth_utils import get_current_user

@pytest.fixture
def api_app(mock_advanced_order_service, mock_smart_execution_service):
    """Create FastAPI app for testing."""
    app = FastAPI()
    app.include_router(router)
    app.dependency_overrides[get_advanced_order_service] = lambda: mock_advanced_order_service
    app.dependency_overrides[get_smart_execution_service] = lambda: mock_smart_execution_service
    app.dependency_overrides[get_current_user] = lambda: {"id": "user_1", "role": "user"}
    return app


@pytest.fixture
def client(api_app):
    """Create test client."""
    return TestClient(api_app)


@pytest.fixture
def mock_advanced_order_service():
    """Mock AdvancedOrderService."""
    service = AsyncMock()
    return service


@pytest.fixture
def mock_smart_execution_service():
    """Mock SmartExecutionService."""
    service = AsyncMock()
    return service


def test_create_trailing_stop_success(client, mock_advanced_order_service):
    """Test successful trailing stop order creation."""
    from schemas.orders import TrailingStopOrder
    
    mock_order = TrailingStopOrder(
        order_id='order_1',
        symbol='AAPL',
        quantity=100,
        trailing_type='percentage',
        trailing_value=5.0,
        initial_stop_price=145.0,
        current_stop_price=145.0,
        highest_price=150.0,
        user_id='user_1',
        status='pending',
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc)
    )
    mock_advanced_order_service.create_trailing_stop.return_value = mock_order
    
    response = client.post('/api/v1/execution/trailing-stop',
                          json={
                              'user_id': 'user_1',
                              'symbol': 'AAPL',
                              'quantity': 100,
                              'trailing_type': 'percentage',
                              'trailing_value': 5.0
                          })
    
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert data['data']['trailing_type'] == 'percentage'


def test_create_trailing_stop_missing_params(client):
    """Test trailing stop creation with missing parameters."""
    response = client.post('/api/v1/execution/trailing-stop',
                          json={'user_id': 'user_1', 'symbol': 'AAPL'})
    
    # FastAPI returns 422 for validation errors, but 400 if we manually raise HTTPException
    # Assuming validation failure results in 422
    assert response.status_code in [400, 422]
    # data = response.json()
    # assert 'success' in data or 'detail' in data


def test_create_bracket_order_success(client, mock_advanced_order_service):
    """Test successful bracket order creation."""
    from schemas.orders import BracketOrder
    
    mock_order = BracketOrder(
        bracket_id='bracket_1',
        entry_order_id='order_1',
        profit_target_order_id='order_2',
        stop_loss_order_id='order_3',
        profit_target_price=160.0,
        stop_loss_price=145.0,
        user_id='user_1',
        symbol='AAPL',
        quantity=100,
        status='pending',
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc)
    )
    mock_advanced_order_service.create_bracket_order.return_value = mock_order
    
    response = client.post('/api/v1/execution/bracket',
                          json={
                              'user_id': 'user_1',
                              'symbol': 'AAPL',
                              'quantity': 100,
                              'entry_price': 150.0,
                              'profit_target_price': 160.0,
                              'stop_loss_price': 145.0
                          })
    
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True


def test_execute_twap_success(client, mock_smart_execution_service):
    """Test successful TWAP execution."""
    from schemas.orders import ExecutionResult
    
    mock_result = ExecutionResult(
        execution_id='exec_1',
        order_id='order_1',
        filled_quantity=100,
        average_price=150.0,
        execution_time=datetime.now(timezone.utc),
        execution_strategy='twap',
        symbol='AAPL',
        side='buy',
        status='filled'
    )
    mock_smart_execution_service.execute_twap.return_value = [mock_result]
    
    response = client.post('/api/v1/execution/twap',
                          json={
                              'symbol': 'AAPL',
                              'total_quantity': 100,
                              'time_window_minutes': 60
                          })
    
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
