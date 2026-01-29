import pytest
from services.tax.penalty_calculator_529 import PenaltyCalculator529

def test_penalty_calculation():
    svc = PenaltyCalculator529()
    # 10k withdrawal, 2k of which is earnings. 24% bracket.
    # Penalty: 2k * 0.10 = 200
    # Tax: 2k * 0.24 = 480
    # Total hit: 680. Net: 9320.
    res = svc.calculate_liability(10000, 2000, 0.24)
    assert res["irs_penalty"] == 200.0
    assert res["income_tax"] == 480.0
    assert res["total_tax_hit"] == 680.0
    assert res["net_to_client"] == 9320.0

def test_zero_earnings_withdrawal():
    svc = PenaltyCalculator529()
    # If all is principal (earnings=0), no hit.
    res = svc.calculate_liability(5000, 0, 0.37)
    assert res["total_tax_hit"] == 0.0
    assert res["net_to_client"] == 5000.0
