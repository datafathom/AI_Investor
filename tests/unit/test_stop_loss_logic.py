"""
Unit tests for Stop Loss Logic.
Verifies Sentinel triggers and SL removal blocking.
"""
import pytest
from decimal import Decimal
from services.risk.stop_loss_sentinel import StopLossSentinel
from services.risk.sl_removal_blocker import SLRemovalBlocker

def test_sentinel_trigger_long():
    sentinel = StopLossSentinel()
    pos = {"symbol": "EUR/USD", "side": "LONG", "stop_loss": 1.0800}
    # Price hit SL
    assert sentinel.check_position(pos, 1.0800) == True
    # Price below SL
    assert sentinel.check_position(pos, 1.0795) == True
    # Price above SL
    assert sentinel.check_position(pos, 1.0801) == False

def test_sentinel_trigger_short():
    sentinel = StopLossSentinel()
    pos = {"symbol": "EUR/USD", "side": "SHORT", "stop_loss": 1.0900}
    # Price hit SL
    assert sentinel.check_position(pos, 1.0900) == True
    # Price above SL
    assert sentinel.check_position(pos, 1.0905) == True
    # Price below SL
    assert sentinel.check_position(pos, 1.0899) == False

def test_sl_removal_blocking():
    blocker = SLRemovalBlocker()
    # Attempt to remove SL (None)
    ok, reason = blocker.validate_modification(Decimal("1.0800"), None, "LONG", Decimal("1.0850"))
    assert ok == False
    assert "FORBIDDEN" in reason

def test_sl_illegal_move_long():
    blocker = SLRemovalBlocker()
    # Move SL further away (1.0800 -> 1.0750)
    ok, reason = blocker.validate_modification(Decimal("1.0800"), Decimal("1.0750"), "LONG", Decimal("1.0850"))
    assert ok == False
    assert "ILLEGAL_MOVE" in reason

def test_sl_legal_tighten_long():
    blocker = SLRemovalBlocker()
    # Move SL closer (1.0800 -> 1.0820)
    ok, reason = blocker.validate_modification(Decimal("1.0800"), Decimal("1.0820"), "LONG", Decimal("1.0850"))
    assert ok == True
