
from services.strategy.defensive_strategy import get_defensive_strategy
import pandas as pd
import numpy as np

def run_test_shield(args=None):
    """
    Test Phase 16 Defensive Shield Strategy.
    """
    print("Testing Defensive Shield Strategy...")
    strategy = get_defensive_strategy()
    
    # 1. Test Allocation Logic across Fear Spectrum
    print("\n--- Allocation Logic Verification ---")
    scenarios = [10, 30, 50, 70, 90]
    for fear_score in scenarios:
        alloc = strategy.calculate_shield_allocation(fear_score)
        print(f"Fear Index: {fear_score} -> Shield Allocation: {alloc*100:.1f}%")
        
    # 2. Test Asset Filtering
    print("\n--- Safe Asset Selection Verification ---")
    # Low Vol
    df_safe = pd.DataFrame({'close': np.linspace(100, 102, 252) + np.random.normal(0, 0.05, 252)})
    # High Vol
    df_risky = pd.DataFrame({'close': np.linspace(100, 102, 252) + np.random.normal(0, 3.0, 252)})
    
    assets = {
        "BND (Safe)": df_safe,
        "ARKK (Risky)": df_risky
    }
    
    safe_list = strategy.filter_safe_assets(assets)
    print(f"Assets: {list(assets.keys())}")
    print(f"Selected Safe Assets: {safe_list}")
    
    if "BND (Safe)" in safe_list and "ARKK (Risky)" not in safe_list:
        print("\nOK Verification Successful: Correctly identified safe assets.")
    else:
        print("\nERROR Verification Failed: Asset filtering logic incorrect.")
