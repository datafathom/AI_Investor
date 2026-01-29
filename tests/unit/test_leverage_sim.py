import pytest
from services.simulation.leverage_sim import LeverageSimulator

def test_leverage_simulation_gain():
    svc = LeverageSimulator()
    # 100k principal, 2x leverage, 10% gross gain -> 20% net gain -> 120k
    res = svc.simulate_outcome(100000, 2.0, 0.10)
    assert res["net_return_pct"] == 0.20
    assert res["ending_equity"] == 120000.0

def test_leverage_wipeout():
    svc = LeverageSimulator()
    # 2x leverage, 50% drop -> 100% loss -> Wiped out
    res = svc.simulate_outcome(100000, 2.0, -0.50)
    assert res["net_return_pct"] == -1.0
    assert res["ending_equity"] == 0.0
    assert res["is_wiped_out"] == True
