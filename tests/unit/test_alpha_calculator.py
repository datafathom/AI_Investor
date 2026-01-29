import pytest
from services.quantitative.alpha_calculator import AlphaCalculator

def test_simple_alpha():
    svc = AlphaCalculator()
    # 10% vs 8% -> 2% Alpha
    assert svc.calculate_simple_alpha(0.10, 0.08) == 0.02

def test_jensens_alpha():
    svc = AlphaCalculator()
    # Rp 12%, Rm 10%, Rf 4%, Beta 1.2
    # Expected = 4 + 1.2*(10 - 4) = 4 + 7.2 = 11.2%
    # Alpha = 12 - 11.2 = 0.8%
    res = svc.calculate_jensens_alpha(0.12, 0.10, 0.04, 1.2)
    assert res == 0.008
