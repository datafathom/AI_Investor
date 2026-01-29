import pytest
from services.market.discovery_delay_analyzer import DiscoveryDelayAnalyzer

def test_high_delay_score():
    analyzer = DiscoveryDelayAnalyzer()
    # 300s delay at 80% passive
    score = analyzer.calculate_delay_score("EARNINGS", 300, 0.8)
    assert score > 3.0

def test_low_delay_score():
    analyzer = DiscoveryDelayAnalyzer()
    # 5s delay at 20% passive
    score = analyzer.calculate_delay_score("NEWS", 5, 0.2)
    assert score < 1.0
