import sys
import os
import logging
from decimal import Decimal

# Add project root to path
sys.path.append(os.getcwd())

from services.lending.stock_lending_svc import StockLendingService
from services.lending.payment_sched import PaymentScheduleTracker
from services.kafka.collateral_monitor import CollateralMonitor
from services.neo4j.lending_graph import LendingGraphService

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("VERIFY_PHASE_167")

def verify_167():
    print("\n" + "="*60)
    print("       PHASE 167: STOCK-BASED LENDING VERIFICATION")
    print("="*60 + "\n")

    # 1. Stock Lending Service
    print("[*] Testing StockLendingService...")
    lending = StockLendingService()
    cap = lending.calculate_borrowing_power("TSLA", Decimal('10000000'), 45.0)
    print(f"    Capacity: ${cap['available_liquidity']:,.2f} (Expected: $2,000,000.00)")
    
    # 2. Spread Analysis
    print("\n[*] Testing Spread Analysis...")
    spread = lending.analyze_borrow_vs_sell(Decimal('10000000'), Decimal('1000000'), Decimal('0.20'), Decimal('0.06'))
    print(f"    Breakeven Years: {spread['breakeven_years']} (Expected: 6.0)")

    # 3. Collateral Monitor (Kafka)
    print("\n[*] Testing CollateralMonitor...")
    mon = CollateralMonitor()
    is_margin_call = mon.check_margin_status("LOAN-1", 5000000, 4000000, 0.75) # 80% LTV > 75%
    print(f"    Margin Call Triggered: {is_margin_call} (Expected: True)")

    # 4. Payment Schedule
    print("\n[*] Testing PaymentScheduleTracker...")
    tracker = PaymentScheduleTracker()
    sched = tracker.generate_io_schedule(Decimal('1000000'), 5.0, 3)
    print(f"    Monthly IO Payment: ${sched[0]['interest_payment']:,.2f} (Expected: $4,166.67)")

    print("\n" + "="*60)
    print("               PHASE 167 VERIFICATION COMPLETE")
    print("="*60 + "\n")

if __name__ == "__main__":
    verify_167()
