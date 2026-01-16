
from services.execution.smart_sor import get_sor

def run_test_sor(args=None):
    """
    Test Phase 25 Smart Order Routing.
    """
    print("Testing Smart Order Router (Iceberg & Limits)...")
    sor = get_sor()
    
    # 1. Iceberg Test
    print("\n--- Iceberg Logic (Qty > 500) ---")
    qty_large = 1200
    strategy = sor.determine_order_strategy("SPY", qty_large, 0.01)
    
    print(f"Total Quantity: {qty_large}")
    print(f"Execution Style: {strategy['execution_style']}")
    print(f"Batches: {strategy['batches']}")
    
    if strategy['execution_style'] == "ICEBERG" and len(strategy['batches']) == 12:
        print("✅ Iceberg Logic Verified: Order split correctly.")
    else:
        print("❌ Iceberg Logic Failed.")
        
    # 2. Volatility Check
    print("\n--- Volatility Logic ---")
    
    # Low Vol
    strat_low = sor.determine_order_strategy("KO", 100, 0.01)
    print(f"Low Vol (1%): Order Type = {strat_low['order_type']}")
    
    # High Vol
    strat_high = sor.determine_order_strategy("GME", 100, 0.05)
    print(f"High Vol (5%): Order Type = {strat_high['order_type']}")
    
    if strat_low['order_type'] == "MARKET" and strat_high['order_type'] == "LIMIT":
        print("✅ Volatility Logic Verified: High vol forces Limit Order.")
    else:
        print("❌ Volatility Logic Failed.")
