
from services.analysis.factor_service import get_factor_service
import pandas as pd
import numpy as np

def run_test_factors(args=None):
    """
    Test Phase 15 Factor Analysis & Risk Parity.
    """
    print("Testing Factor Analysis & Risk Parity Engine...")
    service = get_factor_service()
    
    # 1. Simulate Portfolio Data
    # Asset A: Efficient, Low Volatility (Bond-like)
    dates = pd.date_range(end=pd.Timestamp.now(), periods=100)
    df_a = pd.DataFrame(index=dates)
    df_a['close'] = 100 + np.random.randn(100).cumsum() * 0.1 # Low drift
    
    # Asset B: Volatile, High Momentum (Tech-like)
    df_b = pd.DataFrame(index=dates)
    df_b['close'] = 100 + np.random.randn(100).cumsum() * 1.0 # High drift
    
    prices = {
        "BND (Low Vol)": df_a,
        "TSLA (High Vol)": df_b
    }
    
    print("\n--- Calculating Factors ---")
    weights = service.get_portfolio_weights(prices)
    
    print("\n--- Risk Parity Weights ---")
    for sym, w in weights.items():
        print(f"{sym}: {w:.4f}")
        
    # Verification
    high_vol_weight = weights.get("TSLA (High Vol)", 0)
    low_vol_weight = weights.get("BND (Low Vol)", 0)
    
    if low_vol_weight > high_vol_weight:
        print("\nOK Verification Successful: Low Volatility asset has higher weight.")
    else:
        print("\n❌ Verification Failed: Risk Parity logic invalid.")
