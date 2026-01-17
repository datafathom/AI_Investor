"""
==============================================================================
FILE: tests/strategy/test_rebalancing.py
ROLE: Consistency Guard
PURPOSE:
    Ensure the RebalanceEngine correctly detects drift and generates 
    mathematically accurate orders.
==============================================================================
"""

import pytest
from services.strategy.rebalance_engine import RebalanceEngine

class TestRebalanceEngine:
    
    def test_drift_calculation(self):
        engine = RebalanceEngine()
        current = {"AAPL": 0.5, "GOOG": 0.3, "CASH": 0.2}
        target = {"AAPL": 0.4, "GOOG": 0.4, "CASH": 0.2}
        
        drift = engine.calculate_drift(current, target)
        assert drift["AAPL"] == pytest.approx(0.1)
        assert drift["GOOG"] == pytest.approx(-0.1)
        assert drift["CASH"] == 0.0
        
    def test_rebalance_threshold(self):
        engine = RebalanceEngine(drift_threshold=0.05)
        # 3% drift should NOT trigger
        drift_small = {"AAPL": 0.03}
        assert engine.check_rebalance_needed(drift_small) is False
        
        # 6% drift SHOULD trigger
        drift_large = {"AAPL": 0.06}
        assert engine.check_rebalance_needed(drift_large) is True

    def test_order_generation(self):
        engine = RebalanceEngine()
        drift = {"AAPL": 0.1} # Overweight 10%
        prices = {"AAPL": 150}
        portfolio_value = 15000 # 10% is $1500 -> 10 shares
        
        orders = engine.generate_rebalance_orders(drift, portfolio_value, prices)
        
        assert len(orders) == 1
        assert orders[0]["symbol"] == "AAPL"
        assert orders[0]["side"] == "SELL"
        assert orders[0]["quantity"] == 10
