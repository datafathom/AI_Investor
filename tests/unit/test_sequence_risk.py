import pytest
from services.retirement.sequence_risk import SequenceRiskCalculator

def test_high_sequence_risk():
    svc = SequenceRiskCalculator()
    # 4% rate, First 3 years negative: [-5%, -10%, 2%]
    rets = [-0.05, -0.10, 0.02]
    res = svc.analyze_sorr(0.04, rets)
    assert res["is_sorr_triggered"] == True
    assert res["recommendation"] == "REDUCE_WITHDRAWAL"

def test_safe_sequence():
    svc = SequenceRiskCalculator()
    # Positive returns
    rets = [0.10, 0.05, 0.15]
    res = svc.analyze_sorr(0.04, rets)
    assert res["is_sorr_triggered"] == False
