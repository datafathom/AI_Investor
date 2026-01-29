"""
Unit tests for Neo4j Liquidity Logic.
Verifies Order Block detection, zone mitigation, and strategy filtering.
"""
import pytest
from services.analysis.order_blocks import OrderBlockDetector
from services.analysis.zone_mitigation import ZoneMitigation
from services.strategies.zone_filter import ZoneFilter

def test_order_block_detection():
    # Sequence with impulsive bullish move
    # 5 neutral candles, 1 impulsive (Close-Open = 50 pips, ATR ~10)
    candles = [
        {"open": 1.0800, "high": 1.0810, "low": 1.0790, "close": 1.0805},
        {"open": 1.0805, "high": 1.0815, "low": 1.0800, "close": 1.0810},
        {"open": 1.0810, "high": 1.0820, "low": 1.0805, "close": 1.0815},
        {"open": 1.0815, "high": 1.0825, "low": 1.0810, "close": 1.0820},
        {"open": 1.0820, "high": 1.0870, "low": 1.0815, "close": 1.0870} # Impulsive
    ]
    
    zones = OrderBlockDetector.detect_zones(candles, atr_multiplier=2.0)
    assert len(zones) >= 1
    assert zones[0]["type"] == "DEMAND"
    # Preceding candle high/low was [1.0810, 1.0825]
    assert zones[0]["price_high"] == 1.0825

def test_zone_mitigation():
    demand_zone = {"type": "DEMAND", "price_low": 1.0800, "price_high": 1.0820}
    # Price breaks below demand
    assert ZoneMitigation.check_mitigation(demand_zone, 1.0799) == True
    # Price stays above demand
    assert ZoneMitigation.check_mitigation(demand_zone, 1.0810) == False

def test_zone_filter_buy_blocked():
    supply_zone = {"type": "SUPPLY", "price_low": 1.1000, "price_high": 1.1020}
    # Try to buy at 1.0998 (2 pips from supply)
    ok, reason = ZoneFilter.validate_signal("BUY", 1.0998, nearest_supply=supply_zone)
    assert ok == False
    assert "LIMIT_BLOCKED" in reason

def test_zone_filter_sell_blocked():
    demand_zone = {"type": "DEMAND", "price_low": 1.0700, "price_high": 1.0720}
    # Try to sell at 1.0722 (2 pips from demand)
    ok, reason = ZoneFilter.validate_signal("SELL", 1.0722, nearest_demand=demand_zone)
    assert ok == False
    assert "LIMIT_BLOCKED" in reason
