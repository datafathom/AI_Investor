import sys
import os
import unittest

# Add project root to path
sys.path.append(os.getcwd())

from services.risk.risk_monitor import get_risk_monitor
from services.risk.circuit_breaker import get_circuit_breaker

class TestRiskEngine(unittest.TestCase):
    def setUp(self):
        self.monitor = get_risk_monitor()
        self.breaker = get_circuit_breaker()
        self.breaker.reset()

    def test_position_limit(self):
        # Case: Trade within limits
        analysis = self.monitor.analyze_trade_risk("AAPL", "BUY", 10, 150.0) # $1,500
        self.assertEqual(analysis['rating'], "SAFE")
        
        # Case: Trade exceeds limit
        analysis = self.monitor.analyze_trade_risk("TSLA", "BUY", 100, 200.0) # $20,000
        self.assertEqual(analysis['rating'], "DANGER")
        self.assertIn("exceeds max position size", analysis['reasons'][0])

    def test_kill_switch(self):
        self.assertFalse(self.breaker.is_halted())
        
        # Trigger manual halt
        self.breaker.trigger_global_kill_switch("Manual Test Halt")
        self.assertTrue(self.breaker.is_halted())
        self.assertEqual(self.breaker.freeze_reason, "Manual Test Halt")
        
        # Reset
        self.breaker.reset()
        self.assertFalse(self.breaker.is_halted())

    def test_drawdown_halt(self):
        # Trigger via drawdown (-4% > -3% limit)
        is_halted = self.breaker.check_portfolio_freeze(-0.04)
        self.assertTrue(is_halted)
        self.assertTrue(self.breaker.is_halted())
        self.assertIn("Daily Drawdown", self.breaker.freeze_reason)

if __name__ == '__main__':
    unittest.main()
