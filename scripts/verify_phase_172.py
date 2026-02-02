import sys
import os
import logging
from decimal import Decimal

# Add project root to path
sys.path.append(os.getcwd())

from services.private_markets.premium_optimizer import PremiumOptimizer
from services.risk.volatility_unsmoother import VolatilityUnsmoother
from services.performance.true_sharpe import TrueSharpeCalculator
from services.valuation.secondary_market import SecondaryMarketService
from services.wealth.illiquid_tracker import IlliquidAssetTracker

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("VERIFY_PHASE_172")

def verify_172():
    print("\n" + "="*60)
    print("       PHASE 172: PRIVATE MARKETS VERIFICATION")
    print("="*60 + "\n")

    # 1. Premium Optimizer
    print("[*] Testing PremiumOptimizer...")
    opt = PremiumOptimizer()
    res = opt.calculate_illiquidity_premium(Decimal('0.15'), Decimal('0.10'))
    print(f"    Premium: {res['premium_bps']} bps (Expected: 500)")
    
    # 2. Volatility Unsmoother
    print("\n[*] Testing VolatilityUnsmoother...")
    uns = VolatilityUnsmoother()
    vol = uns.get_true_volatility([0.02, 0.025, 0.022, 0.028])
    print(f"    True Vol: {vol:.4f}")

    # 3. True Sharpe Calculator
    print("\n[*] Testing TrueSharpeCalculator...")
    sharpe = TrueSharpeCalculator()
    res = sharpe.calculate_true_sharpe(0.12, 0.04, 0.15)
    print(f"    True Sharpe: {res['true_sharpe']} (Expected: 0.53)")

    # 4. Secondary Market Service
    print("\n[*] Testing SecondaryMarketService...")
    sec = SecondaryMarketService()
    disc = sec.estimate_discount("RE_FUND", 24)
    print(f"    Discount: {disc['estimated_discount_pct']}% (Expected: 14.0%)")

    # 5. Illiquid Tracker
    print("\n[*] Testing IlliquidAssetTracker...")
    tracker = IlliquidAssetTracker()
    lock = tracker.track_lock_up("ASSET-X")
    print(f"    Remaining Months: {lock['remaining_months']}")

    print("\n" + "="*60)
    print("               PHASE 172 VERIFICATION COMPLETE")
    print("="*60 + "\n")

if __name__ == "__main__":
    verify_172()
