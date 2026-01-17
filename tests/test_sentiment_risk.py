import sys
import os
import unittest
from unittest.mock import patch, MagicMock

# Mock dependencies that trigger praw
sys.modules['praw'] = MagicMock()
sys.modules['services.data.reddit_service'] = MagicMock()

# Add project root to path
sys.path.append(os.getcwd())

from services.risk.risk_monitor import get_risk_monitor

class TestSentimentRisk(unittest.TestCase):
    def setUp(self):
        self.monitor = get_risk_monitor()

    @patch('services.risk.risk_monitor.get_fear_greed_service')
    def test_sentiment_scaling(self, mock_get_service):
        # Mock the service instance and its method
        mock_service = MagicMock()
        mock_get_service.return_value = mock_service
        
        # Case 1: Extreme Greed (Score 90) -> 0.5x Multiplier
        mock_service.get_fear_greed_index.return_value = {'score': 90, 'label': 'EXTREME_GREED'}
        analysis = self.monitor.analyze_trade_risk("AAPL", "BUY", 20, 300.0) # $6,000
        # Normal limit is $10k. Scaled limit is $5k.
        self.assertEqual(analysis['rating'], "DANGER")
        self.assertEqual(analysis['sentiment']['multiplier'], 0.5)
        self.assertIn("Sentiment: 0.5x", analysis['reasons'][0])

        # Case 2: Neutral (Score 50) -> 1.0x Multiplier
        mock_service.get_fear_greed_index.return_value = {'score': 50, 'label': 'NEUTRAL'}
        analysis = self.monitor.analyze_trade_risk("AAPL", "BUY", 20, 300.0) # $6,000
        # Normal limit is $10k. Scaled limit is $10k.
        self.assertEqual(analysis['rating'], "SAFE")
        self.assertEqual(analysis['sentiment']['multiplier'], 1.0)

        # Case 3: Extreme Fear (Score 10) -> 1.1x Multiplier (conviction bonus)
        mock_service.get_fear_greed_index.return_value = {'score': 10, 'label': 'EXTREME_FEAR'}
        # Try a $10,500 trade (over standard $10k but under 1.1x scaled $11k)
        analysis = self.monitor.analyze_trade_risk("AAPL", "BUY", 21, 500.0) # $10,500
        self.assertEqual(analysis['rating'], "SAFE")
        self.assertEqual(analysis['sentiment']['multiplier'], 1.1)

if __name__ == '__main__':
    unittest.main()
