import unittest
from services.ingestion.sec_scraper import SECScraperService
from services.analysis.filing_analyzer import FilingAnalyzerService
from services.valuation.dcf_engine import DCFEngineService
from services.analysis.moat_score import MoatScoreService
from services.analysis.insider_signal import InsiderSignalService
from services.analysis.earnings_sentiment import EarningsSentimentService

class TestProfessionalDiligence(unittest.TestCase):

    def setUp(self):
        self.sec_svc = SECScraperService()
        self.filing_svc = FilingAnalyzerService()
        self.dcf_svc = DCFEngineService()
        self.moat_svc = MoatScoreService()
        self.insider_svc = InsiderSignalService()
        self.earnings_svc = EarningsSentimentService()

    def test_sec_ingestion_and_analysis(self):
        """Test mock scraping and simulated LLM analysis."""
        text = self.sec_svc.get_latest_filing_text("AAPL", "10-K")
        self.assertIn("Simulated 10-K", text)
        
        analysis = self.filing_svc.analyze_filing_text(text)
        self.assertIn("risk_factors_summary", analysis)

    def test_dcf_valuation(self):
        """Test Discounted Cash Flow math."""
        # Simple Case: $1M FCF, 0% growth, 10% WACC, 100 shares
        # Value = 1M/0.10 = $10M total. Share = $100,000.
        # Using the engine with defaults
        
        fcf = 100
        wacc = 0.10
        shares = 1
        
        # Test roughly
        val = self.dcf_svc.calculate_intrinsic_value(
            free_cash_flow=fcf,
            growth_rate=0.0,
            wacc=wacc,
            terminal_growth=0.0,
            projection_years=5,
            shares_outstanding=shares
        )
        # Should be close to 1000 (Perpetuity: 100/0.1 = 1000)
        # The 2-stage model sums discrete years + terminal, so it might vary slightly but should match logic.
        self.assertGreater(val, 900)
        self.assertLess(val, 1100)

    def test_moat_scoring(self):
        """Test Moat Logic."""
        strong_financials = {'gross_margin': 0.50, 'roic': 0.20} # High GM, High ROIC
        res = self.moat_svc.calculate_moat_score(strong_financials)
        self.assertEqual(res['moat_rating'], "WIDE")
        
        weak_financials = {'gross_margin': 0.10, 'roic': 0.05}
        res = self.moat_svc.calculate_moat_score(weak_financials)
        self.assertEqual(res['moat_rating'], "NONE")

    def test_insider_buying_signal(self):
        """Test Cluster Buying Detection."""
        filings = [
            {'transaction_type': 'BUY', 'is_open_market': True, 'value': 400000, 'reporting_person': 'CEO'},
            {'transaction_type': 'BUY', 'is_open_market': True, 'value': 400000, 'reporting_person': 'CFO'},
            {'transaction_type': 'BUY', 'is_open_market': True, 'value': 400000, 'reporting_person': 'Director'}
        ]
        # Total > 1M, 3 unique people -> High Conviction
        res = self.insider_svc.detect_high_conviction_buying(filings)
        self.assertEqual(res['signal'], "HIGH_CONVICTION_BUY")

    def test_earnings_sentiment(self):
        """Test Sentiment Analysis."""
        bullish_text = "We achieved record revenue this quarter."
        bearish_text = "We face significant headwinds and remain cautious."
        
        res_bull = self.earnings_svc.analyze_transcript(bullish_text)
        self.assertGreater(res_bull['sentiment_score'], 0)
        
        res_bear = self.earnings_svc.analyze_transcript(bearish_text)
        self.assertLess(res_bear['sentiment_score'], 0)
        self.assertTrue(res_bear['evasiveness_detected'])

if __name__ == '__main__':
    unittest.main()
