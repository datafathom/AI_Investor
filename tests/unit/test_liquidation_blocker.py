import pytest
from services.risk.liquidation_blocker import LiquidationBlocker

def test_liquidation_blocked_empty():
    blocker = LiquidationBlocker()
    # No EF -> Block
    assert blocker.can_liquidate(0, 30000) == False

def test_liquidation_allowed_above_min():
    blocker = LiquidationBlocker()
    # $5k min, have $6k
    assert blocker.hard_block_check(6000, 5000) == True
    # $5k min, have $4k
    assert blocker.hard_block_check(4000, 5000) == False
