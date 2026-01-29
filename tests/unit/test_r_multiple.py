"""
Unit tests for R-Multiple Calculator.
"""
import pytest
from services.r_multiple_calculator import RMultipleCalculator

def test_long_profit():
    # Risk = 1.1000 - 1.0950 = 0.0050
    # Reward = 1.1100 - 1.1000 = 0.0100
    # R = 0.0100 / 0.0050 = 2.0
    r = RMultipleCalculator.calculate(1.1000, 1.1100, 1.0950, "LONG")
    assert pytest.approx(r) == 2.0

def test_long_loss():
    # Risk = 1.1000 - 1.0900 = 0.0100
    # Reward = 1.0950 - 1.1000 = -0.0050
    # R = -0.0050 / 0.0100 = -0.5
    r = RMultipleCalculator.calculate(1.1000, 1.0950, 1.0900, "LONG")
    assert pytest.approx(r) == -0.5

def test_short_profit():
    # Entry: 1.2500, StopLoss: 1.2550
    # Risk = 1.2550 - 1.2500 = 0.0050
    # Reward = 1.2500 - 1.2400 = 0.0100
    # R = 0.0100 / 0.0050 = 2.0
    r = RMultipleCalculator.calculate(1.2500, 1.2400, 1.2550, "SHORT")
    assert pytest.approx(r) == 2.0

def test_short_loss():
    # Entry: 1.2500, StopLoss: 1.2600
    # Risk = 0.0100
    # Reward = 1.2500 - 1.2550 = -0.0050
    # R = -0.5
    r = RMultipleCalculator.calculate(1.2500, 1.2550, 1.2600, "SHORT")
    assert pytest.approx(r) == -0.5

def test_zero_risk():
    r = RMultipleCalculator.calculate(1.1000, 1.1100, 1.1000, "LONG")
    assert r == 0.0

def test_invalid_long_setup():
    # StopLoss > Entry (Not a valid long risk)
    r = RMultipleCalculator.calculate(1.1000, 1.1100, 1.1050, "LONG")
    assert r == -1.0
