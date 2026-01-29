import pytest
from services.quantitative.excess_return import ExcessReturnCalculator

def test_positive_excess_return():
    svc = ExcessReturnCalculator()
    # 10% portfolio, 4% RFR -> 6% excess
    assert svc.calculate_excess_ret(0.10, 0.04) == 0.06

def test_negative_excess_return():
    svc = ExcessReturnCalculator()
    # 2% portfolio, 5% RFR -> -3% excess
    assert svc.calculate_excess_ret(0.02, 0.05) == -0.03

def test_rfr_selection_short():
    svc = ExcessReturnCalculator()
    curve = {"yield_3mo": 0.04, "yield_10yr": 0.035}
    assert svc.validate_rfr_selection("CASH_LIKE", curve) == 0.04

def test_rfr_selection_long():
    svc = ExcessReturnCalculator()
    curve = {"yield_3mo": 0.04, "yield_10yr": 0.035}
    assert svc.validate_rfr_selection("EQUITY", curve) == 0.035
