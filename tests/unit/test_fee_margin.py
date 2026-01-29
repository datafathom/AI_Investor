import pytest
from services.finance.fee_margin_calc import FeeMarginCalculator

def test_margin_profitability_high():
    svc = FeeMarginCalculator()
    # Gross 1%, Ops 0.5% -> Net 0.5% -> High vs 0.03% beta
    res = svc.calculate_margin(0.01, 0.005)
    assert res["profitability"] == "HIGH"
    assert res["margin_vs_beta_bps"] == 47.0

def test_margin_pressured():
    svc = FeeMarginCalculator()
    # Gross 0.2%, Ops 0.3% -> Negative Margin!
    res = svc.calculate_margin(0.002, 0.003)
    assert res["profitability"] == "PRESSURED"
