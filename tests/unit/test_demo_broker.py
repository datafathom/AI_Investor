"""
Unit tests for Demo Broker.
"""
import pytest
from services.brokers.demo_broker import DemoBrokerService

class TestDemoBroker:
    @pytest.fixture
    def broker(self):
        broker = DemoBrokerService()
        broker.reset_account()
        return broker

    def test_initial_state(self, broker):
        summary = broker.get_account_summary()
        assert summary["balance"] == 100000.0
        assert len(summary["positions"]) == 0

    def test_buy_order(self, broker):
        trade = broker.execute_market_order("AAPL", "BUY", 10, 150.0)
        assert trade["status"] == "FILLED"
        summary = broker.get_account_summary()
        # Cost = 1500. Balance should be 100000 - 1500 = 98500
        assert summary["balance"] == 98500.0
        assert summary["positions"]["AAPL"]["quantity"] == 10.0

    def test_reset(self, broker):
        broker.execute_market_order("AAPL", "BUY", 10, 150.0)
        broker.reset_account()
        summary = broker.get_account_summary()
        assert summary["balance"] == 100000.0
        assert summary["positions"] == {}
