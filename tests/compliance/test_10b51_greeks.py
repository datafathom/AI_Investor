import pytest
from datetime import date, timedelta
from decimal import Decimal
from uuid import uuid4
from services.compliance.plan_execution_svc import PlanExecutionService
from services.options.greeks_engine import GreeksEngine

@pytest.fixture
def plan_svc():
    return PlanExecutionService()

@pytest.fixture
def greeks():
    return GreeksEngine()

def test_10b51_cooling_off_validation(plan_svc):
    # Created 10 days ago -> Restricted
    short_date = date.today() - timedelta(days=10)
    result = plan_svc.validate_plan_window(short_date, cooling_off_days=90)
    assert result['is_plan_eligible_for_execution'] is False

def test_greeks_delta_call(greeks):
    # S=100, K=100, T=1, r=0.05, sigma=0.2
    # ATM call delta ~ 0.6
    res = greeks.calculate_bs_greeks(100, 100, 1.0, 0.05, 0.2, is_call=True)
    assert res['delta'] > 0.5
    assert res['delta'] < 0.7

def test_greeks_gamma_put(greeks):
    res = greeks.calculate_bs_greeks(100, 100, 1.0, 0.05, 0.2, is_call=False)
    assert res['gamma'] > 0
    # Delta for put should be negative
    assert res['delta'] < 0
