
from services.execution.broker_service import get_broker

def run_test_broker(args=None):
    """
    Test Phase 24 Broker Integration.
    """
    print("Testing Broker Connectivity (Mock Enabled)...")
    
    # 1. Connect
    broker = get_broker("MOCK")
    connected = broker.authenticate()
    print(f"Authentication: {'SUCCESS' if connected else 'FAILED'}")
    
    # 2. Query Balance
    bal = broker.get_cash_balance()
    print(f"Cash Balance: ${bal:,.2f}")
    
    # 3. Buy Order
    print("\n--- Placing LIVE Order (Mock) ---")
    order = broker.place_order("NVDA", 5, "BUY")
    print(f"Order: {order['side']} {order['symbol']} ({order['status']})")
    
    # 4. Verify Positions
    positions = broker.get_positions()
    print(f"Positions: {positions}")
    
    if len(positions) > 0 and positions[0]['symbol'] == 'NVDA':
        print("OK Broker Integration Verified (Mock Mode).")
    else:
        print("ERROR Broker Integration Failed.")
