import pytest
from services.retirement.inflation_adjustment import WithdrawalInflationModel

def test_inflation_increase():
    svc = WithdrawalInflationModel()
    # 40k base, 5% inflation -> 42k
    assert svc.adjust_for_inflation(40000, 0.05) == 42000.0

def test_no_inflation():
    svc = WithdrawalInflationModel()
    assert svc.adjust_for_inflation(40000, 0.0) == 40000.0
