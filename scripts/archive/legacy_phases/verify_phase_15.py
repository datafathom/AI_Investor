"""
Verification script for Phase 15.
Tests Order Block detection and Gamma Flip logic.
"""
import sys
import os
from datetime import datetime

# Ensure paths
sys.path.append(os.getcwd())

from services.analysis.order_blocks import OrderBlockDetector
from services.analysis.supply_demand_zones import SupplyDemandDetector
from services.options.gex_calculator import GEXCalculator
from services.analysis.logic_logger import LogicLogger

def run_verification():
    print("=== Starting Phase 15 Verification ===")

    # 1. Institutional Footprint Check
    print("\n[1/3] Identifying Institutional Order Blocks...")
    candles = [
        {'symbol': 'GBP/USD', 'timestamp': 'T1', 'open': 1.2500, 'high': 1.2510, 'low': 1.2490, 'close': 1.2505},
        {'symbol': 'GBP/USD', 'timestamp': 'T2', 'open': 1.2505, 'high': 1.2515, 'low': 1.2500, 'close': 1.2508},
        {'symbol': 'GBP/USD', 'timestamp': 'T3', 'open': 1.2508, 'high': 1.2510, 'low': 1.2490, 'close': 1.2495}, # Base
        {'symbol': 'GBP/USD', 'timestamp': 'T4', 'open': 1.2495, 'high': 1.2650, 'low': 1.2490, 'close': 1.2640}, # Move
        {'symbol': 'GBP/USD', 'timestamp': 'T5', 'open': 1.2640, 'high': 1.2660, 'low': 1.2630, 'close': 1.2650},
    ]
    
    obs = OrderBlockDetector.find_order_blocks(candles)
    print(f"Detected Blocks: {len(obs)}")
    
    bullish_ob = next((b for b in obs if b['type'] == 'BULLISH_OB'), None)
            
    if bullish_ob:
        print(f"✅ Order Block Detected at {bullish_ob['price_low']} with strength {bullish_ob['strength']:.4f}")
    else:
        print("❌ Order Block detection mismatch.")
        return False

    # 2. Options Regime Check
    print("\n[2/3] Analyzing SPY Gamma Exposure...")
    options_chain = [
        {'strike': 500, 'gamma': 0.1, 'open_interest': 5000, 'type': 'CALL'},
        {'strike': 500, 'gamma': 0.15, 'open_interest': 6000, 'type': 'PUT'} # -90k GEX
    ]
    # GEX = (0.1 * 5000 * 100) - (0.15 * 6000 * 100) = 50,000 - 90,000 = -40,000
    
    gex_data = GEXCalculator.calculate_gex(505.0, options_chain)
    print(f"Regime: {gex_data['market_regime']} | Net GEX: {gex_data['total_gex']}")
    
    if gex_data['market_regime'] == 'SHORT_GAMMA':
        print("✅ GEX Logic verified dealer hedging pressure regime.")
    else:
        print("❌ GEX regime mismatch.")
        return False

    # 3. Logic Justification Test
    print("\n[3/3] Building Institutional Logic Thesis...")
    thesis = LogicLogger.build_justification(
        "GBP/USD", "BULLISH", [], obs, {'institutional_bias': 'LONG'}
    )
    print(f"Thesis: {thesis}")
    
    if "footprints confirmed" in thesis and "momentum" not in thesis.lower():
        print("✅ Logic thesis successfully purged retail terminology.")
    else:
        print("❌ Logic thesis contaminated with retail noise.")
        return False

    print("\n=== Phase 15 Verification SUCCESS ===")
    return True

if __name__ == "__main__":
    success = run_verification()
    if not success:
        sys.exit(1)
