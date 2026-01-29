"""
Verification script for Phase 9.
Mocks price events and verifies correlation recalculation flow.
"""
import sys
import unittest
from unittest.mock import MagicMock, patch
from services.rolling_window import rolling_window_service
from services.kafka.graph_bridge import GraphBridge

class TestPhase9Verification(unittest.TestCase):
    def setUp(self):
        rolling_window_service.clear()
        self.bridge = GraphBridge()
        # Mock Neo4j updater
        self.patcher = patch('services.kafka.graph_bridge.edge_weight_updater')
        self.mock_updater = self.patcher.start()

    def tearDown(self):
        self.patcher.stop()

    def test_correlation_recalc_flow(self):
        print("\n[1/2] Simulating price events...")
        
        # We need at least 10 points for GraphBridge to trigger update
        # Simulating EUR/USD and GBP/USD trending together
        for i in range(15):
            eur_msg = {'symbol': 'EUR/USD', 'price': 1.1000 + (i * 0.0001)}
            gbp_msg = {'symbol': 'GBP/USD', 'price': 1.2500 + (i * 0.0001)}
            
            self.bridge.process_message(eur_msg)
            self.bridge.process_message(gbp_msg)

        print("[2/2] Verifying Neo4j update calls...")
        
        # Check if update_correlation was called
        # It should be called after the 10th iteration for each message
        self.assertTrue(self.mock_updater.update_correlation.called)
        
        # Verify specific arguments for the last call
        # It should show positive correlation
        call_args = self.mock_updater.update_correlation.call_args[0]
        coefficient = call_args[2]
        
        print(f"Detected Correlation Coefficient: {coefficient:.4f}")
        self.assertGreater(coefficient, 0.9)
        print("✅ Flow verified: Prices -> Rolling Window -> Correlation -> Neo4j")

if __name__ == '__main__':
    print("=== Starting Phase 9 Verification ===")
    suite = unittest.TestLoader().loadTestsFromTestCase(TestPhase9Verification)
    result = unittest.TextTestRunner(verbosity=1).run(suite)
    if not result.wasSuccessful():
        sys.exit(1)
