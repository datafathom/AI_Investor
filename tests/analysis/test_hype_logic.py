"""
==============================================================================
FILE: tests/analysis/test_hype_logic.py
ROLE: Signal Auditor
PURPOSE:
    Verify that the HypeTracker correctly calculates scores and detects
    viral trends based on engagement metrics.
==============================================================================
"""

import pytest
from services.analysis.hype_tracker import HypeTracker

class TestHypeTracker:
    
    def test_hype_score_calculation(self):
        tracker = HypeTracker()
        # High engagement
        score_high = tracker.calculate_hype_score(views=1000000, shares=50000, like_ratio=0.1, velocity=1.0)
        assert score_high == 1.0
        
        # Low engagement
        score_low = tracker.calculate_hype_score(views=10000, shares=100, like_ratio=0.01, velocity=0.1)
        assert score_low < 0.1
        
    def test_viral_detection(self):
        tracker = HypeTracker(hype_threshold=0.8)
        
        # Viral mention
        metrics_viral = {"views": 900000, "shares": 60000, "velocity": 0.9}
        result = tracker.process_social_mention("GME", "TikTok", metrics_viral)
        assert result["is_viral"] is True
        assert result["symbol"] == "GME"
        
        # Non-viral mention
        metrics_quiet = {"views": 1000, "shares": 5, "velocity": 0.05}
        result_quiet = tracker.process_social_mention("AAPL", "YouTube", metrics_quiet)
        assert result_quiet["is_viral"] is False
