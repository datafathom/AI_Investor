import pytest
from services.retirement.safe_withdrawal import SafeWithdrawalService

def test_fair_valuation_withdrawal():
    svc = SafeWithdrawalService()
    # CAPE 20 (Normal) -> 4%
    res = svc.calculate_withdrawal(1000000, 20)
    assert res["withdrawal_rate"] == 0.04
    assert res["annual_amount"] == 40000.0

def test_high_valuation_reduction():
    svc = SafeWithdrawalService()
    # CAPE 35 (High) -> 3%
    res = svc.calculate_withdrawal(1000000, 35)
    assert res["withdrawal_rate"] == 0.03

def test_low_valuation_bonus():
    svc = SafeWithdrawalService()
    # CAPE 12 (Low) -> 5%
    res = svc.calculate_withdrawal(1000000, 12)
    assert res["withdrawal_rate"] == 0.05
