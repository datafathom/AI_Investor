
from services.execution.algo_execution import get_algo_engine

def run_test_algo(args=None):
    """
    Test Phase 26 Algo Execution.
    """
    print("Testing Algorithmic Execution Engine...")
    engine = get_algo_engine()
    
    # 1. VWAP Test
    print("\n--- VWAP Schedule Generation ---")
    qty = 10000
    # Custom profile: Morning heavy (50%), then quiet
    profile = [0.5, 0.1, 0.1, 0.1, 0.2] 
    
    schedule = engine.generate_vwap_schedule(qty, profile)
    print(f"Total Qty: {qty}")
    print(f"Profile: {profile}")
    print(f"Schedule: {schedule}")
    
    if schedule[0] == 5000 and sum(schedule) == qty:
        print("OK VWAP Schedule Verified.")
    else:
        print("ERROR VWAP Schedule Failed.")
        
    # 2. TWAP Test
    print("\n--- TWAP Schedule Generation ---")
    qty_twap = 1000
    batches = 4
    
    schedule_twap = engine.generate_twap_schedule(qty_twap, batches)
    print(f"Total Qty: {qty_twap}")
    print(f"Batches: {batches}")
    print(f"Schedule: {schedule_twap}")
    
    # 1000 / 4 = 250 each.
    if len(schedule_twap) == 4 and schedule_twap[0] == 250:
         print("OK TWAP Schedule Verified.")
    else:
         print("ERROR TWAP Schedule Failed.")
