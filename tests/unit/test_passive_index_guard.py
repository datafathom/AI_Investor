import pytest
from services.compliance.passive_index_guard import PassiveIndexGuard

def test_passive_guard_allow_etf():
    guard = PassiveIndexGuard()
    # Account is passive, ticker is an index fund/ETF
    result = guard.validate_trade("PASSIVE_INDEX", "VOO", True)
    assert result["allowed"] == True

def test_passive_guard_block_stock():
    guard = PassiveIndexGuard()
    # Account is passive, ticker is an individual stock
    result = guard.validate_trade("PASSIVE_INDEX", "AAPL", False)
    assert result["allowed"] == False
    assert result["code"] == "STOCK_PICK_BLOCKED"

def test_passive_guard_active_account():
    guard = PassiveIndexGuard()
    # Active account, can buy anything
    result = guard.validate_trade("TACTICAL_ALGO", "TSLA", False)
    assert result["allowed"] == True
