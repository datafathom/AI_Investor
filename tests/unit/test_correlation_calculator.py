import pytest
from services.quantitative.correlation_calculator import CorrelationCalculator

def test_pearson_perfect():
    calc = CorrelationCalculator()
    a = [10, 11, 12, 13, 14]
    b = [20, 22, 24, 26, 28] # b = 2a (perfect positive)
    assert calc.calculate_pearson(a, b) == 1.0

def test_pearson_inverse():
    calc = CorrelationCalculator()
    a = [1, 2, 3, 4, 5]
    b = [5, 4, 3, 2, 1] # inverse
    assert calc.calculate_pearson(a, b) == -1.0

def test_rolling_correlation():
    calc = CorrelationCalculator()
    a = [1, 2, 3, 4, 5, 6, 7]
    b = [1, 2, 3, 4, 5, 2, 1] # breaks after 5
    res = calc.calculate_rolling_correlation(a, b, window=3)
    assert len(res) == 5
