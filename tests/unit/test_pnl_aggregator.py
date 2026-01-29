"""
Unit tests for PnL Aggregator.
Verifies profit/loss calculations for LONG and SHORT positions with pips.
"""
import pytest
from decimal import Decimal
from services.portfolio.pnl_aggregator import PnLAggregator

def test_single_long_profit():
    agg = PnLAggregator()
    # EUR/USD LONG, 1 lot, 1.0800 to 1.0810 (10 pips)
    # Expected: 10 pips * $10 * 1 lot = $100.00
    pos = {"symbol": "EUR/USD", "entry_price": 1.0800, "side": "LONG", "lots": 1.0}
    pnl = agg.calculate_position_pnl(pos, 1.0810)
    assert pnl == Decimal("100.00")

def test_single_short_loss():
    agg = PnLAggregator()
    # EUR/USD SHORT, 1 lot, 1.0800 to 1.0810 (10 pips loss)
    # Expected: -$100.00
    pos = {"symbol": "EUR/USD", "entry_price": 1.0800, "side": "SHORT", "lots": 1.0}
    pnl = agg.calculate_position_pnl(pos, 1.0810)
    assert pnl == Decimal("-100.00")

def test_jpy_long_profit():
    agg = PnLAggregator()
    # USD/JPY LONG, 1 lot, 150.00 to 150.10 (10 pips)
    # Expected: 10 pips * $7 (approx) * 1 lot = $70.00
    pos = {"symbol": "USD/JPY", "entry_price": 150.00, "side": "LONG", "lots": 1.0}
    pnl = agg.calculate_position_pnl(pos, 150.10)
    assert pnl == Decimal("70.00")

def test_total_portfolio_pnl():
    agg = PnLAggregator()
    positions = [
        {"symbol": "EUR/USD", "entry_price": 1.0800, "side": "LONG", "lots": 1.0},
        {"symbol": "GBP/USD", "entry_price": 1.2700, "side": "SHORT", "lots": 0.5}
    ]
    prices = {
        "EUR/USD": 1.0820, # +20 pips -> +$200
        "GBP/USD": 1.2710  # -10 pips -> -$50
    }
    total = agg.aggregate_total_pnl(positions, prices)
    assert total == Decimal("150.00")
