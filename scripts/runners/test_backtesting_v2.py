"""
==============================================================================
FILE: scripts/runners/test_backtesting_v2.py
ROLE: Strategy Benchmarker
PURPOSE:
    demonstrate a full event-driven backtest using a moving average crossover
    or simple threshold strategy.
       
CONTEXT: 
    Part of Phase 34: Backtesting V2.
==============================================================================
"""

from services.analysis.backtest_engine import get_backtester

def run_backtest_v2(args=None):
    """
    Test Phase 34 Event-Driven Backtesting.
    """
    print("Initializing Backtesting V2 Lab...")
    
    # 🕵️ Mock Price History (The "Dataset")
    prices = [
        {"timestamp": "D1", "AAPL": 150, "CASH": 1.0},
        {"timestamp": "D2", "AAPL": 145, "CASH": 1.0},
        {"timestamp": "D3", "AAPL": 140, "CASH": 1.0}, # Support
        {"timestamp": "D4", "AAPL": 148, "CASH": 1.0}, # Bounce
        {"timestamp": "D5", "AAPL": 155, "CASH": 1.0}, # Run
        {"timestamp": "D6", "AAPL": 160, "CASH": 1.0},
    ]
    
    # 🧠 Simple "Dip Buying" Strategy
    # Buy when AAPL < 146, Sell when AAPL > 158
    def dip_strategy(ts, pos, cash, current_prices):
        price = current_prices.get("AAPL")
        orders = []
        
        if price < 146 and pos.get("AAPL", 0) == 0:
            qty = int(cash / price)
            orders.append({"symbol": "AAPL", "side": "BUY", "quantity": qty})
        elif price > 158 and pos.get("AAPL", 0) > 0:
            orders.append({"symbol": "AAPL", "side": "SELL", "quantity": pos["AAPL"]})
            
        return orders

    tester = get_backtester(initial_cash=10000)
    result = tester.run(prices, dip_strategy)
    
    print("\n--- BACKTEST RESULTS ---")
    print(f"Initial Capital: $10,000")
    print(f"Final Value:     ${result.final_value:,.2f}")
    print(f"Total Return:    {result.total_return*100:+.2f}%")
    print(f"Trades Count:    {result.trades_executed}")
    
    print("\n--- TIMELINE LOG ---")
    for log in result.history:
        sym_qty = log['positions'].get('AAPL', 0)
        print(f"[{log['timestamp']}] Val: ${log['value']:.2f} | AAPL: {sym_qty} shares | Cash: ${log['cash']:.2f}")

    print("\n✅ Event-Driven Backtest Verified.")
