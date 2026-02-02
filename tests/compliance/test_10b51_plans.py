import pytest
import datetime
from services.compliance.selling_plan_service import SellingPlanService
from services.compliance.fiduciary_execution_layer import FiduciaryExecutionLayer

@pytest.fixture
def plan_svc():
    return SellingPlanService()

@pytest.fixture
def fid_layer():
    return FiduciaryExecutionLayer()

def test_create_selling_plan(plan_svc):
    user_id = "u_99"
    ticker = "AMZN"
    today = datetime.date.today()
    dates = [today + datetime.timedelta(days=90), today + datetime.timedelta(days=180)]
    
    plan = plan_svc.create_selling_plan(user_id, ticker, 1000, dates, 500)
    assert plan["user_id"] == user_id
    assert plan["ticker"] == ticker
    assert len(plan["schedule"]) == 2
    assert plan["schedule"][0]["shares"] == 500

def test_validate_plan_revision(plan_svc):
    # Case: Allowed
    res = plan_svc.validate_plan_revision("PLAN_1", False, False)
    assert res["can_revise"] is True
    
    # Case: Blackout
    res2 = plan_svc.validate_plan_revision("PLAN_2", True, False)
    assert res2["can_revise"] is False
    assert "blackout" in res2["blocking_reason"].lower()
    
    # Case: MNPI
    res3 = plan_svc.validate_plan_revision("PLAN_3", False, True)
    assert res3["can_revise"] is False
    assert "insider" in res3["blocking_reason"].lower()

def test_fiduciary_execution(fid_layer):
    res = fid_layer.execute_scheduled_sale("PLAN_1", "TSLA", 1000)
    assert res["shares_executed"] == 1000
    assert "This trade was executed automatically" in res["fiduciary_attestation"]
    
    justified = fid_layer.log_non_timing_justification(res["execution_id"], "Scheduled quarterly exit.")
    assert justified is True
