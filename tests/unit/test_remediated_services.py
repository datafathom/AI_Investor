import unittest
from services.demo_reset_service import DemoResetService
from services.analysis.market_structure import MarketStructureService
from services.analysis.mean_reversion import MeanReversionService

class TestRemediatedServices(unittest.TestCase):

    def test_demo_reset(self):
        """Test demo reset service."""
        svc = DemoResetService()
        result = svc.reset_demo_account("user-123")
        self.assertEqual(result["new_balance"], 100000.00)
        self.assertEqual(result["user_id"], "user-123")

    def test_market_structure_swing_points(self):
        """Test swing point detection."""
        svc = MarketStructureService()
        prices = [1.0, 1.1, 1.2, 1.15, 1.1, 1.05, 1.0, 1.05, 1.1, 1.15, 1.2, 1.25]
        result = svc.detect_swing_points(prices, lookback=2)
        self.assertIn("swing_highs", result)
        self.assertIn("swing_lows", result)

    def test_market_structure_trend(self):
        """Test trend identification."""
        svc = MarketStructureService()
        # Uptrend: HH + HL
        trend = svc.identify_trend([1.0, 1.2], [0.9, 1.0])
        self.assertEqual(trend, "UPTREND")
        # Downtrend: LH + LL
        trend = svc.identify_trend([1.2, 1.0], [1.0, 0.9])
        self.assertEqual(trend, "DOWNTREND")

    def test_mean_reversion_z_score(self):
        """Test Z-score calculation."""
        svc = MeanReversionService()
        z = svc.calculate_z_score(110, 100, 5)
        self.assertEqual(z, 2.0)

    def test_mean_reversion_extreme(self):
        """Test extreme extension detection."""
        svc = MeanReversionService()
        # Create data with variance and extreme at end
        prices = [99.0, 101.0, 100.0, 102.0, 98.0, 100.0, 101.0, 99.0, 100.0, 101.0,
                  99.0, 101.0, 100.0, 102.0, 98.0, 100.0, 101.0, 99.0, 100.0, 115.0]
        result = svc.detect_extreme_extension(prices, threshold=2.0)
        self.assertEqual(result, "OVERBOUGHT")


if __name__ == '__main__':
    unittest.main()
