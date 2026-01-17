"""
==============================================================================
FILE: tests/analysis/test_congress_tracker.py
ROLE: Political Auditor
PURPOSE:
    Verify that the CongressTracker correctly ingests disclosures and
    calculates political alpha scores.
==============================================================================
"""

import pytest
from services.analysis.congress_tracker import CongressTracker

class TestCongressTracker:
    
    def test_fetch_disclosures(self):
        tracker = CongressTracker()
        disclosures = tracker.fetch_latest_disclosures()
        
        assert len(disclosures) > 0
        assert disclosures[0]["member"] == "Nancy Pelosi"
        assert disclosures[0]["ticker"] == "NVDA"
        
    def test_lobbying_correlation(self):
        tracker = CongressTracker()
        correlation = tracker.correlate_with_lobbying("NVDA")
        
        assert correlation["lobbying_intensity"] > 0.8
        assert correlation["confidence"] == "HIGH"
        
        quiet_ticker = tracker.correlate_with_lobbying("MSFT")
        assert quiet_ticker["lobbying_intensity"] < 0.5

    def test_alpha_signal_calculation(self):
        tracker = CongressTracker()
        tracker.fetch_latest_disclosures() # Load mocks
        
        # NVDA has 1 BUY mention in mock and high lobbying
        # Score = (0.85 * 0.6) + (0.2 * 0.4) = 0.51 + 0.08 = 0.59
        score = tracker.get_political_alpha_signal("NVDA")
        assert score >= 0.5
        
        # Non-mocked ticker
        score_low = tracker.get_political_alpha_signal("AAPL")
        assert score_low < 0.3
