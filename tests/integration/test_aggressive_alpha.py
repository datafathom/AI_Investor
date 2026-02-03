
from services.strategy.aggressive_strategy import get_aggressive_strategy
import pandas as pd
import numpy as np

def run_test_aggressive(args=None):
    """
    Test Phase 17 Aggressive Alpha Strategy.
    """
    print("Testing Aggressive Alpha Strategy...")
    strategy = get_aggressive_strategy()
    
    # 1. Test Allocation Logic across Fear Spectrum
    print("\n--- Allocation Logic Verification (Risk-On) ---")
    scenarios = [30, 50, 70, 90]
    for fear_score in scenarios:
        alloc = strategy.calculate_aggressive_allocation(fear_score)
        print(f"Fear Index: {fear_score} -> Aggressive Allocation: {alloc*100:.1f}%")
        
    # 2. Test Asset Filtering
    print("\n--- Growth Asset Selection Verification ---")
    
    # High Momentum + High Vol (Crypto/Tech)
    dates = pd.date_range(end=pd.Timestamp.now(), periods=100)
    df_crypto = pd.DataFrame(index=dates)
    # Strong uptrend + high vol
    df_crypto['close'] = np.linspace(100, 200, 100) + np.random.normal(0, 5, 100)
    
    # Low Momentum (Sideways)
    df_bond = pd.DataFrame(index=dates)
    df_bond['close'] = np.linspace(100, 102, 100) + np.random.normal(0, 0.1, 100)
    
    # Negative Momentum (Crash)
    df_crash = pd.DataFrame(index=dates)
    df_crash['close'] = np.linspace(100, 50, 100) + np.random.normal(0, 5, 100)
    
    assets = {
        "BTC (Growth)": df_crypto,
        "SHY (Bond)": df_bond,
        "ARKK (Crash)": df_crash
    }
    
    growth_list = strategy.select_aggressive_assets(assets)
    print(f"Assets: {list(assets.keys())}")
    print(f"Selected Growth Assets: {growth_list}")
    
    if "BTC (Growth)" in growth_list and "SHY (Bond)" not in growth_list:
        print("\nOK Verification Successful: Correctly identified growth assets.")
    else:
        print("\nERROR Verification Failed: Asset filtering logic incorrect.")
