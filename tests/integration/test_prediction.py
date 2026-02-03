
from services.analysis.prediction_service import get_prediction_service
import pandas as pd
import numpy as np
import time

def run_test_prediction(symbol="SPY", train=False, **kwargs):
    """
    Test Phase 14 Predictive Modeling Engine.
    Accepts arguments as kwargs from the CLI dispatcher.
    """
    # symbol and train are constrained by function signature
    
    print(f"Testing Prediction Engine for {symbol}...")
    service = get_prediction_service()
    
    # Mock Data
    print("Generating synthetic market data...")
    dates = pd.date_range(end=pd.Timestamp.now(), periods=500, freq='1min')
    df = pd.DataFrame(index=dates)
    
    # Create a predictable pattern: 
    # If RSI is low (proxy: close < mean), next return is positive.
    df['open'] = 100.0
    df['high'] = 101.0
    df['low'] = 99.0
    # Sine wave close prices to create clear mean reversion
    df['close'] = 100 + np.sin(np.linspace(0, 20, 500)) * 2
    df['volume'] = 1000
    
    if train or service.model is None:
        print("\n--- Training Model ---")
        metrics = service.train_model(df)
        print(f"Training Metrics: {metrics}")
        
    print("\n--- Running Inference ---")
    t0 = time.time()
    result = service.predict_direction(df)
    duration = (time.time() - t0) * 1000
    
    print(f"Inference Time: {duration:.2f}ms")
    print(f"Prediction: {result}")
    
    if "prediction" in result:
        print("\n✅ Verification Successful: Model returned valid prediction.")
    else:
        print("\n❌ Verification Failed: Invalid response.")
