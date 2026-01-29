"""
Unit tests for Position Sizer Logic.
Verifies the standard 1% risk rule and JPY scaling.
"""
import pytest
from decimal import Decimal
from services.risk.position_sizer import PositionSizer

def test_standard_sizing():
    # $100k account, 20 pip SL
    # Risk = $1k
    # Lots = 1000 / (20 * 10) = 5.0 lots
    balance = Decimal("100000.00")
    result = PositionSizer.calculate_size(balance, 20.0, "EUR/USD")
    
    assert result['lots'] == 5.0
    assert result['risk_amount'] == 1000.0

def test_conservative_sizing():
    # $100k account, 20 pip SL, CONSERVATIVE (0.5%)
    # Risk = $500
    # Lots = 500 / (20 * 10) = 2.5 lots
    balance = Decimal("100000.00")
    result = PositionSizer.calculate_size(balance, 20.0, "EUR/USD", regime="CONSERVATIVE")
    
    assert result['lots'] == 2.5
    assert result['risk_pct'] == 0.005

def test_jpy_scaling():
    # $100k account, 50 pip SL, USD/JPY
    # Risk = $1k
    # Lots = 1000 / (50 * 7) = 2.857... -> 2.86 lots
    balance = Decimal("100000.00")
    result = PositionSizer.calculate_size(balance, 50.0, "USD/JPY")
    
    assert result['lots'] == 2.86

def test_minimum_stop_loss_enforcement():
    # Request 2 pip SL
    # System should force 10 pip SL
    balance = Decimal("10000.00")
    result = PositionSizer.calculate_size(balance, 2.0, "EUR/USD")
    
    assert result['stop_loss_pips'] == 10.0
    assert result['lots'] == 1.0 # 100 / (10 * 10)
