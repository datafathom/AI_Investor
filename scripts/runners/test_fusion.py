"""
==============================================================================
FILE: scripts/runners/test_fusion.py
ROLE: Fusion Logic Verifier
PURPOSE: Verifies the creation and normalization of the Market State Tensor.
USAGE: python cli.py test-fusion [--symbol TSLA] [--mock]
==============================================================================
"""

import logging
from services.data.data_fusion_service import DataFusionService

logger = logging.getLogger(__name__)

def run_test_fusion(symbol: str = "TSLA", mock: bool = False, **kwargs):
    """
    Runner to verify Market State Tensor generation.
    """
    print(f"--- Testing Data Fusion for {symbol} (Mock: {mock}) ---")
    
    service = DataFusionService(mock=mock)
    result = service.get_market_state_tensor(symbol)
    
    if not result:
        print("FAILED: No tensor generated.")
        return False
        
    tensor = result['tensor']
    
    print(f"\n[MARKET STATE TENSOR: {symbol}]")
    print(f"Timestamp:      {result['timestamp']}")
    print(f"Aggregate Score: {result['aggregate_score']}")
    print("-" * 40)
    print(f"Price Momentum:   {tensor['price_momentum']:<10} (0-1 Scale)")
    print(f"Retail Sentiment: {tensor['retail_sentiment']:<10} (0-1 Scale)")
    print(f"Smart Money:      {tensor['smart_money']:<10} (0-1 Scale)")
    print(f"Macro Health:     {tensor['macro_health']:<10} (0-1 Scale)")
    print("-" * 40)
    
    # Simple validation
    if all(0.0 <= v <= 1.0 for v in tensor.values()):
        print("\nSUCCESS: All tensor components normalized correctly.")
        return True
    else:
        print("\nFAILURE: Tensor components out of bounds (0-1).")
        return False
