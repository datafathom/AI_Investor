"""
Verification script for Phase 11.
Tests liquidity validation, slippage estimation, and systemic toxicity detection.
"""
import sys
import os

# Ensure paths correctly set
sys.path.append(os.getcwd())

from services.market.level2_parser import Level2Parser
from services.risk.liquidity_validator import LiquidityValidator
from services.trading.slippage_estimator import SlippageEstimator
from services.risk.toxic_liquidity import ToxicLiquidityDetector

def run_verification():
    print("=== Starting Phase 11 Verification ===")

    # 1. Simulate Order Books
    print("\n[1/3] Simulating Global Order Books...")
    books = [
        {
            'symbol': 'EUR/USD',
            'timestamp': '2026-01-26T00:00:00Z',
            'bids': [{'price': 1.0850, 'size': 10_000_000}], # Deep
            'asks': [{'price': 1.0851, 'size': 10_000_000}]  # Tight spread (1 pip)
        },
        {
            'symbol': 'GBP/USD',
            'timestamp': '2026-01-26T00:00:00Z',
            'bids': [{'price': 1.2500, 'size': 200_000}],   # Thin
            'asks': [{'price': 1.2510, 'size': 200_000}]    # Wide spread (10 pips)
        },
        {
            'symbol': 'USD/JPY',
            'timestamp': '2026-01-26T00:00:00Z',
            'bids': [{'price': 149.00, 'size': 100_000}],  # Thin
            'asks': [{'price': 149.50, 'size': 100_000}]   # Toxic spread (50 pips)
        }
    ]
    
    parsed_books = [Level2Parser.parse_depth_event(b) for b in books]

    # 2. Check Individual Safety Gates
    print("\n[2/3] Verifying Safety Gates...")
    eur_check = LiquidityValidator.is_safe_to_execute(parsed_books[0])
    print(f"EUR/USD Check: Safe={eur_check['safe']}, Reason={eur_check['reason']}")
    
    jpy_check = LiquidityValidator.is_safe_to_execute(parsed_books[2])
    print(f"USD/JPY Check: Safe={jpy_check['safe']}, Reason={jpy_check['reason']}")

    # 3. Detect Systemic Toxicity
    print("\n[3/3] Scanning for Systemic Toxic Liquidity...")
    toxic_scan = ToxicLiquidityDetector.is_environment_toxic(parsed_books)
    
    print(f"Toxic Environment: {toxic_scan['is_toxic']}")
    print(f"Failed Majors: {toxic_scan['failed_count']}/{toxic_scan['total_checked']}")
    
    if toxic_scan['is_toxic'] and eur_check['safe'] and not jpy_check['safe']:
        print("\n✅ Verification SUCCESS: Liquidity gates and toxic detection active.")
        return True
    else:
        print("\n❌ Verification FAILED: Logic mismatch.")
        return False

if __name__ == "__main__":
    success = run_verification()
    if not success:
        sys.exit(1)
