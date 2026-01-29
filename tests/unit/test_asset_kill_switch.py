"""
Unit tests for Asset Kill Switch Logic.
Verifies 10% drawdown detection and liquidation triggers.
"""
import pytest
from decimal import Decimal
from services.risk.threshold_monitor import ThresholdMonitor
from services.risk.asset_kill_switch import AssetKillSwitch

def test_drawdown_calculation_long():
    monitor = ThresholdMonitor()
    # LONG: Entry 1.1000, Price 1.0450 (5% loss)
    entry = Decimal("1.1000")
    curr = Decimal("1.0450")
    loss_pct = monitor.calculate_drawdown_pct(entry, curr, "LONG")
    assert loss_pct == 0.05

    # LONG: Entry 1.1000, Price 0.9900 (10% loss)
    curr_kill = Decimal("0.9900")
    loss_kill = monitor.calculate_drawdown_pct(entry, curr_kill, "LONG")
    assert loss_kill == 0.10

def test_drawdown_calculation_short():
    monitor = ThresholdMonitor()
    # SHORT: Entry 1.0000, Price 1.0500 (5% loss)
    entry = Decimal("1.0000")
    curr = Decimal("1.0500")
    loss_pct = monitor.calculate_drawdown_pct(entry, curr, "SHORT")
    assert loss_pct == 0.05

    # SHORT: Entry 1.0000, Price 1.1000 (10% loss)
    curr_kill = Decimal("1.1000")
    loss_kill = monitor.calculate_drawdown_pct(entry, curr_kill, "SHORT")
    assert loss_kill == 0.10

def test_kill_switch_trigger():
    ks = AssetKillSwitch(kill_threshold=0.10)
    positions = [
        {"symbol": "EUR/USD", "entry_price": 1.1000, "side": "LONG"},
        {"symbol": "GBP/USD", "entry_price": 1.2000, "side": "SHORT"}
    ]
    
    # Prices: EUR/USD down 11% (KILL), GBP/USD up 5% (STAY)
    spot_prices = {
        "EUR/USD": 0.9790, # 1.1000 * 0.89 = 0.979
        "GBP/USD": 1.2600  # 5% loss (1.2000 * 1.05)
    }
    
    targets = ks.inspect_portfolio(positions, spot_prices)
    assert "EUR/USD" in targets
    assert "GBP/USD" not in targets
    assert ks.interventions == 1
