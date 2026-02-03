"""
Verification script for Phase 17.
Simulates portfolio fluctuations to verify real-time equity tracking and reconciliation.
"""
import sys
import os
from decimal import Decimal
from datetime import datetime

# Ensure paths
sys.path.append(os.getcwd())

from services.portfolio.pnl_aggregator import PnLAggregator
from services.portfolio.equity_curve_logger import EquityCurveLogger
from services.reconciliation.consistency_checker import ConsistencyChecker
from services.portfolio.fast_balance import get_balance_service

def run_verification():
    print("=== Starting Phase 17 Verification ===")
    
    balance_svc = get_balance_service()
    pnl_agg = PnLAggregator()
    logger_svc = EquityCurveLogger()
    checker = ConsistencyChecker()

    # 1. Setup Initial State
    initial_balance = Decimal("100000.00")
    balance_svc.update_balance(initial_balance)
    print(f"Initial Balance Set: ${initial_balance:,.2f}")

    # 2. Simulate Open Positions
    positions = [
        {"symbol": "EUR/USD", "entry_price": 1.0800, "side": "LONG", "lots": 2.0},
        {"symbol": "GBP/USD", "entry_price": 1.2700, "side": "SHORT", "lots": 1.0}
    ]
    
    # 3. Simulate Price Movement
    # EUR/USD: 1.0800 -> 1.0820 (+20 pips -> +$400)
    # GBP/USD: 1.2700 -> 1.2710 (-10 pips -> -$100)
    # Total PnL: +$300
    spot_prices = {
        "EUR/USD": 1.0820,
        "GBP/USD": 1.2710
    }
    
    print("\n[1/3] Calculating Real-time PnL & Equity...")
    unrealized_pnl = pnl_agg.aggregate_total_pnl(positions, spot_prices)
    equity = initial_balance + unrealized_pnl
    print(f"Calculated PnL: ${unrealized_pnl:,.2f} | Current Equity: ${equity:,.2f}")

    if unrealized_pnl != Decimal("300.00"):
        print(f"❌ PnL mismatch! Expected $300.00, got ${unrealized_pnl}")
        return False
    print("✅ PnL calculation accurate.")

    # 4. Log Snapshot
    print("\n[2/3] Testing Equity Curve Logging...")
    snapshot = logger_svc.log_snapshot(positions, spot_prices)
    if snapshot["equity"] == equity:
        print(f"✅ Snapshot Validated: Equity matches ${snapshot['equity']:,.2f}")
    else:
        print("❌ Snapshot equity mismatch!")
        return False

    # 5. Reconciliation Check
    print("\n[3/3] Running Consistency Check vs. Broker...")
    broker_balance = Decimal("100000.00")
    is_ok, drift = checker.verify_ledger(initial_balance, broker_balance)
    checker.log_reconciliation(is_ok, drift)
    
    if not is_ok:
        print("❌ Reconciliation failed!")
        return False

    print("\n=== Phase 17 Verification SUCCESS ===")
    return True

if __name__ == "__main__":
    if not run_verification():
        sys.exit(1)
