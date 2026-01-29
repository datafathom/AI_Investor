import pytest
from services.portfolio.equal_weight_rebalancer import EqualWeightRebalancer

def test_equal_weighting_output():
    svc = EqualWeightRebalancer()
    tickers = ["AAPL", "MSFT", "GOOG", "AMZN"]
    res = svc.calculate_equal_weights(tickers)
    assert len(res) == 4
    assert res[0]["target_weight"] == 0.25

def test_drift_calculation():
    svc = EqualWeightRebalancer()
    # 2 assets. Equal should be 0.5. 
    # Current: 0.8 / 0.2. Drift = |0.8 - 0.5| + |0.2 - 0.5| = 0.3 + 0.3 = 0.6.
    holdings = [
        {"ticker": "A", "weight": 0.8},
        {"ticker": "B", "weight": 0.2}
    ]
    assert svc.estimate_drift(holdings) == 0.6
