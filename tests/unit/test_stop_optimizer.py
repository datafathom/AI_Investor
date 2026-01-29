"""
Unit tests for Stop Loss Optimization.
"""
import pytest
from services.analysis.structure_scanner import StructureScanner
from services.indicators.atr_calc import ATRCalculator

def test_swing_low_detection():
    candles = [
        {"open": 1.10, "high": 1.11, "low": 1.09, "close": 1.105},
        {"open": 1.105, "high": 1.115, "low": 1.08, "close": 1.11}, # Swing Low
        {"open": 1.11, "high": 1.12, "low": 1.105, "close": 1.115},
    ]
    sl = StructureScanner.find_swing_low(candles)
    assert sl == 1.08

def test_atr_calculation():
    candles = [{"open": 1.10, "high": 1.11, "low": 1.09, "close": 1.10}] * 16
    atr = ATRCalculator.calculate_atr(candles, period=14)
    assert atr == pytest.approx(0.02, abs=0.001)

def test_padded_stop():
    atr = ATRCalculator.get_padded_stop(1.0800, 0.0020, "LONG", 1.5)
    assert atr == pytest.approx(1.0770, abs=0.0001)
