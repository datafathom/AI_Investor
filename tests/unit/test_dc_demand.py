import pytest
from services.analysis.tech_demand_correlator import TechDemandCorrelator

def test_bullish_dc_demand():
    svc = TechDemandCorrelator()
    # 20% Tech CapEx growth, 5% DC rent growth -> 0.25 leverage, Bullish
    res = svc.analyze_dc_leverage(0.20, 0.05)
    assert res["demand_outlook"] == "BULLISH"
    assert res["tech_dc_leverage"] == 0.25

def test_stable_leverage():
    svc = TechDemandCorrelator()
    # 5% Tech CapEx, 2% DC rent
    res = svc.analyze_dc_leverage(0.05, 0.02)
    assert res["demand_outlook"] == "STABLE"
