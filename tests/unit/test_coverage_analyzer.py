import pytest
from services.planning.coverage_analyzer import CoverageAnalyzer

def test_coverage_tiers():
    analyzer = CoverageAnalyzer()
    assert analyzer.determine_tier(2.5) == "CRITICAL"
    assert analyzer.determine_tier(4.0) == "LOW"
    assert analyzer.determine_tier(8.0) == "ADEQUATE"
    assert analyzer.determine_tier(25.0) == "FORTRESS"

def test_survival_prob():
    analyzer = CoverageAnalyzer()
    # 12 months, 0 volatility -> 1.0 prob (capped at 0.99)
    prob = analyzer.calculate_survival_probability(12, 0.0)
    assert prob == 0.99
