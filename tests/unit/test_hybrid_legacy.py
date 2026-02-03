import unittest
from datetime import datetime, timedelta
from services.real_estate.reit_data import REITDataService
from services.compliance.wash_sale import WashSaleGuardService
from services.ingestion.fred_stream import FREDStreamService

class TestPhases31_50Services(unittest.TestCase):

    def test_reit_yields(self):
        """Test REIT data service."""
        svc = REITDataService()
        yields = svc.get_reit_yields()
        self.assertGreater(len(yields), 0)
        self.assertIn("symbol", yields[0])
        self.assertIn("yield_pct", yields[0])

    def test_wash_sale_safe_after_30_days(self):
        """Test wash sale guard detects safe window."""
        svc = WashSaleGuardService()
        old_date = datetime.utcnow() - timedelta(days=35)
        self.assertTrue(svc.is_safe_to_harvest("AAPL", old_date))

    def test_wash_sale_blocks_recent(self):
        """Test wash sale guard blocks recent purchases."""
        svc = WashSaleGuardService()
        recent_date = datetime.utcnow() - timedelta(days=15)
        self.assertFalse(svc.is_safe_to_harvest("AAPL", recent_date))

    def test_fred_curve_inversion(self):
        """Test FRED stream yield curve check."""
        svc = FREDStreamService()
        yields = svc.fetch_treasury_yields()
        self.assertIn("US_10Y", yields)
        # Current mock shows inverted curve
        self.assertTrue(svc.is_curve_inverted())

if __name__ == '__main__':
    unittest.main()
