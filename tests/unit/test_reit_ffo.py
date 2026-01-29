import pytest
from services.reits.ffo_calculator import FFOCalculator

def test_ffo_calculation():
    svc = FFOCalculator()
    # Net 10M, Depr 5M, Gains 2M
    # FFO = 10 + 5 - 2 = 13M
    assert svc.calculate_ffo(10000000, 5000000, 2000000) == 13000000.0

def test_affo_calculation():
    svc = FFOCalculator()
    # FFO 13M, CapEx 3M
    assert svc.calculate_affo(13000000, 3000000) == 10000000.0
