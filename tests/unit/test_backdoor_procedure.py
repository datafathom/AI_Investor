import pytest
from services.tax.backdoor_roth_procedure import BackdoorRothProcedure

def test_backdoor_clean_plan():
    svc = BackdoorRothProcedure()
    # No existing balance
    plan = svc.get_step_plan(0.0)
    assert len(plan) == 3
    assert plan[0]["action"] == "CONTRIBUTE_NON_DEDUCTIBLE"

def test_backdoor_rollover_first():
    svc = BackdoorRothProcedure()
    # Existing balance detected
    plan = svc.get_step_plan(50000.0)
    assert len(plan) == 4
    assert plan[0]["action"] == "CLEAR_TRAD_IRA"
