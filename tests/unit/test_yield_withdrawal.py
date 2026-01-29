import pytest
from services.retirement.yield_withdrawal import YieldWithdrawalCalculator

def test_yield_sub_inflation():
    svc = YieldWithdrawalCalculator()
    # Yield 2%, Inflation 3% -> Safe withdrawal 0
    res = svc.calculate_yield_safe_amount(1000000, 0.02, 0.03)
    assert res["safe_withdrawal_rate"] == 0.0
    assert res["annual_amount"] == 0.0

def test_yield_high_real_return():
    svc = YieldWithdrawalCalculator()
    # Yield 7%, Inflation 2% -> Safe 5%
    res = svc.calculate_yield_safe_amount(1000000, 0.07, 0.02)
    assert res["safe_withdrawal_rate"] == 0.05
    assert res["annual_amount"] == 50000.0
