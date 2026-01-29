import pytest
from services.insurance.needs_analyzer import NeedsAnalyzer

def test_insurance_gap():
    analyzer = NeedsAnalyzer()
    # Income 100k (needs 1M), Debt 200k -> Total 1.2M
    # Current benefit 500k -> Gap 700k
    res = analyzer.calculate_gap(100000, 200000, 500000)
    assert res["gap"] == 700000.0
    assert res["is_underinsured"] == True

def test_fully_insured():
    analyzer = NeedsAnalyzer()
    # Need 1.2M, have 1.5M
    res = analyzer.calculate_gap(100000, 200000, 1500000)
    assert res["gap"] == 0
    assert res["is_underinsured"] == False
