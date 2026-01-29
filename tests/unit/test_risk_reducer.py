import pytest
from services.risk.risk_reducer import RiskReducerService

def test_risk_reduction_active():
    svc = RiskReducerService()
    # 6 months left -> Trigger
    res = svc.evaluate_deadline_risk(6)
    assert res["action"] == "FORCE_CASH_OFFSET"
    assert res["cash_buffer_suggested"] == 0.25

def test_risk_reduction_inactive():
    svc = RiskReducerService()
    # 24 months left -> No action
    res = svc.evaluate_deadline_risk(24)
    assert res["action"] == "NONE"
