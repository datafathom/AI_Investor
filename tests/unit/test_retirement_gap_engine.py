import pytest
from services.retirement.gap_engine import RetirementGapEngine

def test_gap_calculation():
    engine = RetirementGapEngine()
    # 500k balance, 10k target monthly income, 20 years to ret
    # Required: 10k * 12 * 25 = 3M
    # Projected: 500k * (1.06)^20 = 500k * 3.2 = 1.6M
    # Gap approx 1.4M
    res = engine.calculate_gap(500000, 10000, 20)
    assert res["target_met"] == False
    assert res["gap"] > 1000000

def test_surplus_calculation():
    engine = RetirementGapEngine()
    # 2M balance, 5k target income, 10 years to ret
    # Required: 5k * 12 * 25 = 1.5M
    # Target Met
    res = engine.calculate_gap(2000000, 5000, 10)
    assert res["target_met"] == True
    assert res["surplus"] > 0
