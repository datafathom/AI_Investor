
from services.execution.paper_exchange import get_paper_exchange

def run_test_paper(args=None):
    """
    Test Phase 23 Paper Trading.
    """
    print("Testing Paper Trading Simulator...")
    exchange = get_paper_exchange()
    
    # 1. Check Initial Balance
    summary = exchange.get_account_summary()
    print(f"Initial Balance: ${summary['cash']:,.2f}")
    
    # 2. Buy AAPL
    print("\n--- BUY Order ---")
    order_buy = exchange.submit_market_order('AAPL', 10, 'BUY', 150.0)
    print(f"Executed: {order_buy['side']} {order_buy['quantity']} {order_buy['symbol']} @ ${order_buy['price']:.2f} ({order_buy['status']})")
    
    summary = exchange.get_account_summary()
    print(f"Balance: ${summary['cash']:,.2f}")
    print(f"Positions: {summary['positions']}")
    
    if summary['cash'] == 100000.0 - 1500.0 and summary['positions']['AAPL']['quantity'] == 10:
        print("✅ BUY Order Verified.")
    else:
        print("❌ BUY Order Failed.")
        
    # 3. Sell AAPL
    print("\n--- SELL Order ---")
    order_sell = exchange.submit_market_order('AAPL', 5, 'SELL', 160.0) # Profit $10/share
    print(f"Executed: {order_sell['side']} {order_sell['quantity']} {order_sell['symbol']} @ ${order_sell['price']:.2f} ({order_sell['status']})")
    
    summary = exchange.get_account_summary()
    print(f"Balance: ${summary['cash']:,.2f}")
    print(f"Positions: {summary['positions']}")
    
    expected_cash = 98500.0 + (5 * 160.0) # 98500 + 800 = 99300
    if summary['cash'] == expected_cash and summary['positions']['AAPL']['quantity'] == 5:
        print("✅ SELL Order Verified.")
    else:
         print(f"❌ SELL Order Failed. Expected ${expected_cash}, got ${summary['cash']}")
         
    # 4. Fail Case
    print("\n--- Insufficient Funds Check ---")
    order_fail = exchange.submit_market_order('BRK.A', 1, 'BUY', 500000.0) # Too expensive
    print(f"Order Status: {order_fail['status']} ({order_fail['reason']})")
    
    if order_fail['status'] == "REJECTED":
        print("✅ Insufficient Funds Logic Verified.")
    else:
        print("❌ Rejection Logic Failed.")
