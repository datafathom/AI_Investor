import pytest
from services.portfolio.contrarian_rebalancer import ContrarianRebalancer

def test_contrarian_opportunity_selection():
    svc = ContrarianRebalancer()
    perf = [
        {"ticker": "NVDA", "perf_1y": 1.50},  # Up big
        {"ticker": "GOLD", "perf_1y": -0.05}, # Down slight
        {"ticker": "BOND", "perf_1y": -0.15}, # Down big
        {"ticker": "SPY", "perf_1y": 0.20}
    ]
    opps = svc.identify_opportunities(perf)
    # Bottom 2 should be BOND and GOLD
    assert opps[0]["ticker"] == "BOND"
    assert opps[1]["ticker"] == "GOLD"
