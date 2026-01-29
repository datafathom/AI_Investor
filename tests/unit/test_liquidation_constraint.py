import pytest
from services.risk.liquidation_constraint import LiquidationConstraint

def test_trade_blocking():
    constraint = LiquidationConstraint()
    # Block buy if < 3 mo
    res = constraint.check_trade_allowed(2.5, "BUY")
    assert res["allowed"] == False
    
    # Allow sell even if critical
    res = constraint.check_trade_allowed(2.5, "SELL")
    assert res["allowed"] == True

def test_trade_allowing():
    constraint = LiquidationConstraint()
    res = constraint.check_trade_allowed(6.0, "BUY")
    assert res["allowed"] == True
