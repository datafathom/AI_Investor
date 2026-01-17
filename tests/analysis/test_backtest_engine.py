"""
==============================================================================
FILE: tests/analysis/test_backtest_engine.py
ROLE: Simulation Auditor
PURPOSE:
    Verify that the EventBacktester accurately tracks cash and positions
    across simulated time steps.
==============================================================================
"""

import pytest
from services.analysis.backtest_engine import EventBacktester

class TestBacktestEngine:
    
    def test_basic_buy_hold(self):
        tester = EventBacktester(initial_cash=10000)
        
        # Test Data: Price goes from 100 to 120
        data = [
            {"timestamp": "2023-01-01", "SPY": 100},
            {"timestamp": "2023-01-02", "SPY": 110},
            {"timestamp": "2023-01-03", "SPY": 120},
        ]
        
        # Simple Strategy: Buy 50 shares on day 1
        def buy_on_day_1(ts, pos, cash, prices):
            if ts == "2023-01-01":
                return [{"symbol": "SPY", "side": "BUY", "quantity": 50}]
            return []
            
        result = tester.run(data, buy_on_day_1)
        
        # Final Value: $5000 (cash left) + 50 * 120 (positions) = $11000
        assert result.final_value == 11000
        assert result.total_return == 0.1
        assert result.trades_executed == 1
        
    def test_insufficient_cash(self):
        tester = EventBacktester(initial_cash=1000)
        data = [{"timestamp": "T1", "SPY": 2000}]
        
        def buy_expensive(ts, pos, cash, prices):
            return [{"symbol": "SPY", "side": "BUY", "quantity": 1}]
            
        result = tester.run(data, buy_expensive)
        assert result.trades_executed == 0
        assert result.final_value == 1000
