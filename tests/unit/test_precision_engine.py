"""
Unit tests for PrecisionEngine.
"""
import pytest
from decimal import Decimal
from services.pricing.precision_engine import PrecisionEngine

def test_eurusd_normalization():
    # EUR/USD should have 5 decimals
    price = 1.0850567
    normalized = PrecisionEngine.normalize_price("EUR/USD", price)
    assert str(normalized) == "1.08506"

def test_usdjpy_normalization():
    # USD/JPY should have 3 decimals
    price = 149.50567
    normalized = PrecisionEngine.normalize_price("USD/JPY", price)
    assert str(normalized) == "149.506"

def test_pip_calculation_eurusd():
    # 1.0850 -> 1.0851 = 1 pip
    diff = 0.0001
    pips = PrecisionEngine.get_pip_value("EUR/USD", diff)
    assert pips == Decimal("1")

def test_pip_calculation_usdjpy():
    # 149.00 -> 149.01 = 1 pip
    diff = 0.01
    pips = PrecisionEngine.get_pip_value("USD/JPY", diff)
    assert pips == Decimal("1")

def test_display_formatting():
    # Ensure trailing zeros are kept
    price = 1.08
    formatted = PrecisionEngine.format_for_display("EUR/USD", price)
    assert formatted == "1.08000"
    
    jpy_price = 149.5
    formatted_jpy = PrecisionEngine.format_for_display("USD/JPY", jpy_price)
    assert formatted_jpy == "149.500"

def test_lot_size_rounding():
    lots = 0.1234
    rounded = PrecisionEngine.check_lot_size("EUR/USD", lots)
    assert str(rounded) == "0.12"
