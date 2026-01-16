
import pytest
from services.execution.broker_service import get_broker, MockBroker

class TestBrokerService:
    
    def test_mock_broker_flow(self):
        broker = get_broker("MOCK")
        assert isinstance(broker, MockBroker)
        
        # Auth
        assert broker.authenticate() is True
        
        # Initial State
        assert broker.get_cash_balance() == 100000.0
        assert len(broker.get_positions()) == 0
        
        # Buy Order
        order = broker.place_order("AAPL", 10, "BUY")
        assert order['status'] == "FILLED"
        assert broker.get_cash_balance() == 99000.0 # 10 * $100 mock price
        
        positions = broker.get_positions()
        assert len(positions) == 1
        assert positions[0]['symbol'] == "AAPL"
        assert positions[0]['quantity'] == 10

    def test_not_authenticated_error(self):
        broker = MockBroker()
        # Skip broker.authenticate()
        
        with pytest.raises(ConnectionError):
            broker.get_cash_balance()
