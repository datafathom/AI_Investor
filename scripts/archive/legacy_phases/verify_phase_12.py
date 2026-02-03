"""
Verification script for Phase 12.
Ensures numeric engine handles flash crashes and JPY scaling correctly.
"""
import sys
import os
from decimal import Decimal

# Ensure paths
sys.path.append(os.getcwd())

from services.pricing.precision_engine import PrecisionEngine

def run_verification():
    print("=== Starting Phase 12 Verification ===")

    print("\n[1/2] Verifying Scaling Logic...")
    test_cases = [
        ("EUR/USD", 1.08505, "1.08505"),
        ("EUR/USD", 1.085, "1.08500"),
        ("USD/JPY", 149.5, "149.500"),
        ("USD/JPY", 149.0012, "149.001"),
    ]
    
    for symbol, price, expected in test_cases:
        formatted = PrecisionEngine.format_for_display(symbol, price)
        if formatted == expected:
            print(f"✅ {symbol}: Input {price} -> Produced {formatted}")
        else:
            print(f"❌ {symbol}: Input {price} -> Produced {formatted} (Expected {expected})")
            return False

    print("\n[2/2] Stress Testing Flash Crash Scenario...")
    # 1,000 pip flash crash in EUR/USD (1.0800 -> 0.9800)
    crash_entry = 1.08000
    crash_exit = 0.98000
    diff = crash_entry - crash_exit
    pips = PrecisionEngine.get_pip_value("EUR/USD", diff)
    
    print(f"1,000 Pip Crash Calculation: {pips} pips")
    if pips == Decimal("1000"):
        print("✅ Flash crash pip calculation verified with high precision.")
    else:
        print(f"❌ Flash crash pip calculation failed: {pips}")
        return False

    print("\n=== Phase 12 Verification SUCCESS ===")
    return True

if __name__ == "__main__":
    success = run_verification()
    if not success:
        sys.exit(1)
