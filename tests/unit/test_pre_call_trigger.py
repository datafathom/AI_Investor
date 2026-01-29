import pytest
from services.risk.pre_call_trigger import PreCallTrigger

def test_pre_call_danger():
    svc = PreCallTrigger()
    # 1M value, 50k excess (5%) -> Danger
    res = svc.evaluate_margin_safety(50000, 1000000)
    assert res["is_safe"] == False
    assert res["status"] == "DANGER_PRE_CALL"

def test_pre_call_safe():
    svc = PreCallTrigger()
    # 1M value, 150k excess (15%) -> Safe
    res = svc.evaluate_margin_safety(150000, 1000000)
    assert res["is_safe"] == True
    assert res["status"] == "SAFE"
