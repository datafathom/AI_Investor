import pytest
from services.quantitative.hedge_scorer import InflationHedgeScorer

def test_inflation_beta_positive():
    svc = InflationHedgeScorer()
    # Asset returns moves exactly with inflation
    inf = [0.01, 0.02, 0.03]
    rets = [0.01, 0.02, 0.03]
    assert svc.calculate_inflation_beta(rets, inf) == 1.0

def test_effectiveness_scoring():
    svc = InflationHedgeScorer()
    assert svc.score_effectiveness(1.2) == "SUPER_HEDGER"
    assert svc.score_effectiveness(-0.5) == "VULNERABLE"
