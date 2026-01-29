import pytest
from services.retirement.pension_simulator import PensionSimulator

def test_pension_bankrupt_risk():
    sim = PensionSimulator()
    # 50% funding ratio, Junk rating (D)
    res = sim.simulate_payout_risk(0.5, "D")
    assert res["is_sustainable"] == False
    assert res["failure_probability"] > 0.8

def test_pension_healthy():
    sim = PensionSimulator()
    # 95% funding, AA rating
    res = sim.simulate_payout_risk(0.95, "AA")
    assert res["is_sustainable"] == True
    assert res["failure_probability"] == 0.0
