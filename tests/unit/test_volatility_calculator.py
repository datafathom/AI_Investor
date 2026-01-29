import pytest
from services.quantitative.volatility_calculator import VolatilityCalculator

def test_std_dev_calculation():
    calc = VolatilityCalculator()
    # Returns of 1% every day for 252 days
    returns = [0.01 for _ in range(252)]
    # Std dev of zero variance should be 0
    assert calc.calculate_annualized_vol(returns) == 0.0

def test_max_drawdown():
    calc = VolatilityCalculator()
    equity = [100, 110, 90, 100, 80, 110]
    # Peak was 110, low after was 80. (110 - 80) / 110 = 0.2727
    res = calc.calculate_max_drawdown(equity)
    assert round(res, 2) == 0.27
