"""
Verification script for Phase 19.
Simulates Sentinel triggers and illegal SL removal attempts.
"""
import sys
import os
from decimal import Decimal

# Ensure paths
sys.path.append(os.getcwd())

from services.risk.stop_loss_sentinel import StopLossSentinel
from services.risk.sl_removal_blocker import SLRemovalBlocker
from services.trading.order_validator import OrderValidator

def run_verification():
    print("=== Starting Phase 19 Verification ===")
    
    sentinel = StopLossSentinel()
    blocker = SLRemovalBlocker()
    validator = OrderValidator()

    # 1. Mandatory Stop Loss Check (Submission rejection)
    print("\n[1/4] Testing Mandatory SL Validation (Missing SL submission)...")
    bad_request = {"symbol": "EUR/USD", "side": "LONG", "lots": 1.0}
    ok, reason = validator.validate_submission(bad_request)
    if not ok and "Mandatory Stop Loss" in reason:
        print(f"✅ Submission Blocked: {reason}")
    else:
        print("❌ Order validator failed to block trade without SL!")
        return False

    # 2. Simulate Sentinel Breach (LONG)
    print("\n[2/4] Testing LONG Sentinel Breach...")
    pos_long = {"symbol": "EUR/USD", "side": "LONG", "stop_loss": 1.0800}
    price_long = 1.0790 # Breach
    triggered = sentinel.check_position(pos_long, price_long)
    if triggered:
        print("✅ Sentinel Triggered successfully.")
        sentinel.broadcast_kill("EUR/USD", "SL_BREACH")
    else:
        print("❌ Sentinel failed to trigger on breach!")
        return False

    # 2. Simulate Illegal SL Removal
    print("\n[2/3] Testing SL Removal Block (Compliance Gate)...")
    ok, reason = blocker.validate_modification(Decimal("1.0800"), None, "LONG", Decimal("1.0850"))
    if not ok and "FORBIDDEN" in reason:
        print(f"✅ Removal Blocked: {reason}")
    else:
        print("❌ Compliance gate failed to block SL removal!")
        return False

    # 3. Simulate Illegal SL Increase (Moving SL further away)
    print("\n[3/3] Testing SL Modification (Risk Increase Attempt)...")
    # Move SL from 1.0800 to 1.0700 (increasing loss potential)
    ok, reason = blocker.validate_modification(Decimal("1.0800"), Decimal("1.0700"), "LONG", Decimal("1.0850"))
    if not ok and "ILLEGAL_MOVE" in reason:
        print(f"✅ Risk Increase Blocked: {reason}")
    else:
        print("❌ Compliance gate failed to block SL risk increase!")
        return False

    print("\n=== Phase 19 Verification SUCCESS ===")
    return True

if __name__ == "__main__":
    if not run_verification():
        sys.exit(1)
