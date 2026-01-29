import pytest
from services.risk.concentration_detector import ConcentrationDetector

def test_critical_concentration():
    svc = ConcentrationDetector()
    # Top 10 weights summing to 45%
    weights = [0.08, 0.07, 0.06, 0.05, 0.05, 0.04, 0.04, 0.02, 0.02, 0.02] + [0.001] * 100
    res = svc.analyze_concentration(weights)
    assert res["concentration_level"] == "CRITICAL"
    assert res["top_10_weight"] == 0.45

def test_hhi_calculation():
    svc = ConcentrationDetector()
    # 4 holdings @ 25% each. HHI = 4 * 0.25^2 = 0.25. Effective = 4.
    weights = [0.25, 0.25, 0.25, 0.25]
    assert svc.calculate_hhi(weights) == 0.25
    res = svc.analyze_concentration(weights)
    assert res["effective_holdings"] == 4
