import pytest
from services.tax.crt_deduction import CRTDeductionCalculator

def test_crt_deduction_pass():
    svc = CRTDeductionCalculator()
    # 1M initial, 5% payout, 20 years, 5% IRS rate
    # This should definitely pass 10% test
    res = svc.calculate_pv_remainder(1000000, 0.05, 20, 0.05)
    assert res["passes_10_percent_test"] == True
    assert res["remainder_pct"] > 0.10

def test_crt_deduction_fail():
    svc = CRTDeductionCalculator()
    # 1M initial, 20% payout, 40 years, 1% IRS rate
    # Payout is too high/long, PV of annuity will exceed corpus, fail 10%
    res = svc.calculate_pv_remainder(1000000, 0.20, 40, 0.01)
    assert res["passes_10_percent_test"] == False
