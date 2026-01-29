import pytest
from services.trusts.crt_distribution import CRTDistributionCalculator

def test_crut_payout_math():
    svc = CRTDistributionCalculator()
    # 1M value, 6% rate -> 60k payout
    res = svc.calculate_payout("CRUT", 0.06, 1000000)
    assert res["required_distribution"] == 60000.0
    assert res["is_compliant"] == True

def test_crt_illegal_rate():
    svc = CRTDistributionCalculator()
    # 3% rate is < 5% minimum
    res = svc.calculate_payout("CRAT", 0.03, 1000000, fixed_annuity=30000)
    assert res["is_compliant"] == False
