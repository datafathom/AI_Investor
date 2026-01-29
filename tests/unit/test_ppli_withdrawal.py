import pytest
from services.insurance.ppli_withdrawal import PPLIWithdrawalEngine

def test_ppli_loan_calculation():
    svc = PPLIWithdrawalEngine()
    # 1M cash value, 50k annual COI. 
    # Buffer = 100k. 
    # Max Loan = (1M - 100k) * 0.90 = 810k.
    res = svc.calculate_max_loan(1000000, 50000)
    assert res["max_safe_loan"] == 810000.0
    assert res["lapse_buffer_retained"] == 100000.0

def test_ppli_loan_no_value():
    svc = PPLIWithdrawalEngine()
    res = svc.calculate_max_loan(0, 50000)
    assert res["max_safe_loan"] == 0.0
