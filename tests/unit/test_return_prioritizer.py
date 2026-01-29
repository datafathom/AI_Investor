import pytest
from services.quantitative.return_prioritizer import ReturnPrioritizer

def test_prioritize_assets():
    svc = ReturnPrioritizer()
    assets = [
        {"ticker": "NVDA", "expected_return": 0.20, "volatility": 0.30}, # Efficiency 0.66
        {"ticker": "SPY", "expected_return": 0.10, "volatility": 0.12},  # Efficiency 0.83
        {"ticker": "BILL", "expected_return": 0.05, "volatility": 0.01}  # Efficiency 5.0
    ]
    ranked = svc.rank_assets(assets)
    # Treasury bills should be #1 for risk-adjusted return here
    assert ranked[0]["ticker"] == "BILL"
    assert ranked[2]["ticker"] == "NVDA"
