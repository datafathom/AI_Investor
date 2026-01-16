
from services.analysis.fear_greed_service import get_fear_greed_service
import json

def run_test_fear_greed(args=None):
    """
    Test the Fear & Greed Index Service.
    """
    print("Testing Fear & Greed Index Service...")
    
    # Use mock=True for stable testing
    service = get_fear_greed_service(mock=True)
    
    symbols = ["SPY", "QQQ"]
    if args and args:
        symbols = args
        
    print(f"Analyzing symbols: {symbols}")
    
    result = service.get_fear_greed_index(symbols=symbols)
    
    print("\n--- Result ---")
    print(json.dumps(result, indent=2))
    
    # Basic assertions
    assert "score" in result
    assert "label" in result
    assert "components" in result
    assert result["score"] >= 0 and result["score"] <= 100
    
    print("\n✅ Verification Successful: Service is returning valid structure.")
