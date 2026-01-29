import pytest
from services.compliance.cois_calculator import COISCalculator

def test_cois_calculation_clean():
    calc = COISCalculator()
    data = {
        "commission_revenue_pct": 0.0,
        "kickback_revenue_pct": 0.0,
        "trading_volume_excess": 0.0,
        "fee_transparency_score": 1.0
    }
    score = calc.calculate_score(data)
    assert score == 100.0

def test_cois_calculation_conflicted():
    calc = COISCalculator()
    data = {
        "commission_revenue_pct": 0.5, # 40% * 0.5 = 20 penalty
        "kickback_revenue_pct": 0.3,   # 30% * 0.3 = 9 penalty
        "trading_volume_excess": 0.2,  # 15% * 0.2 = 3 penalty
        "fee_transparency_score": 0.0  # 0 bonus
    }
    # 85 - (20 + 9 + 3) = 53
    score = calc.calculate_score(data)
    assert score == 53.0

def test_cois_calculation_bounds():
    calc = COISCalculator()
    data = {
        "commission_revenue_pct": 1.0,
        "kickback_revenue_pct": 1.0,
        "trading_volume_excess": 1.0,
        "fee_transparency_score": 0.0
    }
    score = calc.calculate_score(data)
    assert score == 0.0
