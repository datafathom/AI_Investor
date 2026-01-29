import pytest
from services.tax.liquidation_pain import LiquidationPainCalculator

def test_liquidation_pain_high():
    calc = LiquidationPainCalculator()
    # Sell 100k, Basis 50k (50k gain) @ 20% tax
    # Tax: 10k. Spread: 500 (50bps)
    # Total hit 10,500
    res = calc.calculate_pain(100000, 50000, 0.20, 50)
    assert res["tax_hit"] == 10000.0
    assert res["net_proceeds"] == 89500.0
    assert res["pain_index"] == 0.105

def test_liquidation_loss_pain():
    calc = LiquidationPainCalculator()
    # Loss sale -> No tax. Just spread.
    res = calc.calculate_pain(100000, 120000, 0.20, 50)
    assert res["tax_hit"] == 0.0
    assert res["net_proceeds"] == 99500.0
