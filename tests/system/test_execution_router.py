
import pytest
import os
from unittest.mock import MagicMock, patch
from services.brokerage.execution_service import ExecutionService

@pytest.fixture
def service():
    # Ensure a fresh instance for each test
    ExecutionService._instance = None
    return ExecutionService()

def test_place_order_simulated(service):
    order_data = {"symbol": "AAPL", "qty": 10, "side": "buy"}
    result = service.place_order(order_data)
    assert result['status'] == 'FILLED'
    assert 'sim_ord_' in result['order_id']
    assert result['simulated'] is True

def test_kill_switch_blocking(service):
    # Mock environment variable for kill switch
    with patch.dict(os.environ, {"SYSTEM_HALTED": "TRUE"}):
        order_data = {"symbol": "TSLA", "qty": 1, "side": "buy"}
        result = service.place_order(order_data)
        assert result['status'] == 'REJECTED'
        assert "Kill Switch" in result['reason']

def test_risk_limit_rejection(service):
    order_data = {"symbol": "BTC", "qty": 5000, "side": "buy"} # > 1000
    result = service.place_order(order_data)
    assert result['status'] == 'REJECTED'
    assert "Risk Management" in result['reason']

def test_order_routing_error_handling(service):
    # Force simulated=False and mock a failure
    service._brokerage._is_simulated = False
    service._brokerage._client = MagicMock()
    service._brokerage._client.submit_order.side_effect = Exception("API Down")
    
    order_data = {"symbol": "AAPL", "qty": 1, "side": "buy"}
    result = service.place_order(order_data)
    assert result['status'] == 'ERROR'
    assert "API Down" in result['reason']
