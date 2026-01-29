import unittest
from services.strategies.regime_detector import RegimeDetectorService, MarketRegime
from services.strategies.quality_tilt import QualityTiltService
from services.trading.beta_reducer import BetaReducerService
from services.trading.trailing_stop import TrailingStopService
from services.portfolio.dividend_safety import DividendSafetyService

class TestBearMarketDefense(unittest.TestCase):

    def setUp(self):
        self.regime_svc = RegimeDetectorService()
        self.quality_svc = QualityTiltService()
        self.beta_svc = BetaReducerService()
        self.stop_loss_svc = TrailingStopService()
        self.div_svc = DividendSafetyService()

    def test_regime_detection(self):
        """Test detection of Risk Off when Price < 200 SMA."""
        # Risk Off Scenario
        res = self.regime_svc.detect_regime('SPY', current_price=400, sma_200=420)
        self.assertEqual(res, MarketRegime.RISK_OFF)
        
        # Risk On Scenario
        res = self.regime_svc.detect_regime('SPY', current_price=450, sma_200=420)
        self.assertEqual(res, MarketRegime.RISK_ON)

    def test_quality_tilt_filtering(self):
        """Test filtering for High ROE / Low Debt."""
        assets = [
            {'ticker': 'JUNK', 'roe': 0.05, 'debt_to_equity': 2.0},
            {'ticker': 'GOLD', 'roe': 0.20, 'debt_to_equity': 0.3}
        ]
        
        filtered = self.quality_svc.filter_for_quality(assets)
        self.assertEqual(len(filtered), 1)
        self.assertEqual(filtered[0]['ticker'], 'GOLD')
        self.assertEqual(filtered[0]['quality_score'], 'HIGH')

    def test_beta_reduction(self):
        """Test logic to reduce high beta exposure in Risk Off."""
        holdings = [
            {'ticker': 'TSLA', 'beta': 2.0},
            {'ticker': 'KO', 'beta': 0.6}
        ]
        
        # In Risk On, should do nothing
        recs_on = self.beta_svc.recommend_rotation(holdings, MarketRegime.RISK_ON)
        self.assertEqual(len(recs_on), 0)
        
        # In Risk Off, should cut TSLA
        recs_off = self.beta_svc.recommend_rotation(holdings, MarketRegime.RISK_OFF)
        self.assertTrue(len(recs_off) > 0)
        self.assertEqual(recs_off[0]['ticker'], 'TSLA')
        self.assertEqual(recs_off[0]['action'], 'REDUCE')

    def test_trailing_stop(self):
        """Test 10% trailing stop logic."""
        position = {'ticker': 'NVDA', 'high_water_mark': 100.0}
        
        # Drop to 95 (5% drop) -> HOLD
        signal = self.stop_loss_svc.check_stop_loss(position, 95.0)
        self.assertEqual(signal, 'HOLD')
        
        # Drop to 89 (11% drop) -> SELL
        signal = self.stop_loss_svc.check_stop_loss(position, 89.0)
        self.assertEqual(signal, 'SELL_SIGNAL')

    def test_dividend_safety(self):
        """Test identification of Dividend Aristocrats."""
        assets = [
            {'ticker': 'T', 'dividend_growth_years': 35, 'dividend_yield': 0.06},
            {'ticker': 'GROW', 'dividend_growth_years': 5, 'dividend_yield': 0.01}
        ]
        
        aristocrats = self.div_svc.filter_aristocrats(assets)
        self.assertEqual(len(aristocrats), 1)
        self.assertEqual(aristocrats[0]['ticker'], 'T')

if __name__ == '__main__':
    unittest.main()
