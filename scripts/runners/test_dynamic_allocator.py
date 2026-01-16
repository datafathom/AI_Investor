
from services.strategy.dynamic_allocator import get_dynamic_allocator
import pandas as pd
import numpy as np

def run_test_allocator(args=None):
    """
    Test Phase 18 Dynamic Allocator.
    """
    print("Testing Dynamic Allocator (The Switch)...")
    allocator = get_dynamic_allocator()
    
    # 1. Test Portfolio Buckets across Market Cycles
    print("\n--- Market Cycle Simulation ---")
    scenarios = {
        "CRASH (Fear 10)": 10,
        "BEAR (Fear 30)": 30,
        "NEUTRAL (Fear 50)": 50,
        "BULL (Fear 70)": 70, 
        "BUBBLE (Fear 90)": 90
    }
    
    for name, fear in scenarios.items():
        allocs = allocator.allocate_capital(fear)
        print(f"\nScenario: {name}")
        print(f"  Shield: {allocs['SHIELD']*100:.1f}%")
        print(f"  Alpha:  {allocs['ALPHA']*100:.1f}%")
        print(f"  Cash:   {allocs['CASH']*100:.1f}%")
        
    # 2. Test Full Portfolio Construction
    print("\n--- Full Portfolio Weights ---")
    dates = pd.date_range(end=pd.Timestamp.now(), periods=100)
    
    # Create Assets
    # Safe
    assets = {}
    assets['T-BILL'] = pd.DataFrame({'close': np.linspace(100, 101, 100)})
    assets['GOLD'] = pd.DataFrame({'close': np.linspace(100, 105, 100)})
    
    # Risky
    assets['NVDA'] = pd.DataFrame({'close': np.linspace(100, 200, 100) + np.random.normal(0, 5, 100)}) 
    assets['BTC'] = pd.DataFrame({'close': np.linspace(100, 300, 100) + np.random.normal(0, 10, 100)})
    
    # Test in "Goldilocks" regime (Fear 50)
    # Expect: ~30% Shield, ~60% Alpha
    # Shield split between T-BILL/GOLD (15% each)
    # Alpha split between NVDA/BTC (30% each)
    
    weights = allocator.construct_target_portfolio(assets, 50)
    print("\nTarget Weights (Fear Index 50):")
    for sym, w in weights.items():
        print(f"  {sym}: {w*100:.1f}%")
        
    # Verification
    if 'NVDA' in weights and 'T-BILL' in weights:
        if weights['NVDA'] > weights['T-BILL']:
             print("\n✅ Verification Successful: Alpha assets weighted higher in Bull/Neutral market.")
        else:
             print("\n❌ Verification Failed: Weights do not reflect regime.")
    else:
         print("\n❌ Verification Failed: Assets missing.")
