
import time
import pandas as pd
import numpy as np
from services.analysis.feature_service import get_feature_service

def run_test_features(args=None):
    """
    Test Phase 13 Feature Engineering Pipeline.
    """
    symbol = args.symbol if args and hasattr(args, 'symbol') else "SPY"
    benchmark = args.benchmark if args and hasattr(args, 'benchmark') else False
    
    print(f"Testing Feature Engineering for {symbol}...")
    service = get_feature_service()
    
    # Generate dummy OHLCV data
    print("Generating mock market data...")
    dates = pd.date_range(end=pd.Timestamp.now(), periods=500, freq='1min')
    df = pd.DataFrame(index=dates)
    df['open'] = np.random.randn(500).cumsum() + 100
    df['high'] = df['open'] + np.random.rand(500)
    df['low'] = df['open'] - np.random.rand(500)
    df['close'] = df['open'] + np.random.randn(500) * 0.5
    df['volume'] = np.random.randint(1000, 100000, 500)
    
    # Run Pipeline
    start_time = time.time()
    result_df = service.generate_features(df)
    duration = (time.time() - start_time) * 1000  # ms
    
    print(f"\n✅ Features Generated in {duration:.2f}ms")
    print("\n--- Latest Feature Vector ---")
    latest = service.get_latest_feature_vector(result_df)
    for k, v in latest.items():
        print(f"{k}: {v:.4f}")
        
    # Verification
    assert 'rsi' in result_df.columns
    assert 'macd' in result_df.columns
    assert 'bb_upper' in result_df.columns
    
    # Benchmarking
    if benchmark:
        print("\n--- Running Benchmark (1000 iter) ---")
        times = []
        for _ in range(1000):
            t0 = time.time()
            service.generate_features(df)
            times.append((time.time() - t0) * 1000)
            
        avg_time = np.mean(times)
        p99_time = np.percentile(times, 99)
        print(f"Average: {avg_time:.2f}ms")
        print(f"P99: {p99_time:.2f}ms")
        
        if avg_time > 50:
            print("⚠️ WARNING: Performance is slower than 50ms target!")
        else:
            print("🚀 Performance Target Met (< 50ms)")
            
    print("\n✅ Verification Successful.")
