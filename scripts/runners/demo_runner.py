"""
Runner for demo account CLI commands.
"""
from services.brokers.demo_broker import DemoBrokerService

def run_demo_reset():
    """Reset demo account."""
    broker = DemoBrokerService()
    broker.reset_account()
    print("✅ Demo account reset to $100,000.00")

def run_demo_trade(symbol: str, side: str, qty: str, price: str):
    """Execute demo trade."""
    broker = DemoBrokerService()
    try:
        q = float(qty)
        p = float(price)
        trade = broker.execute_market_order(symbol, side, q, p)
        print(f"✅ Trade Executed: {trade}")
    except Exception as e:
        print(f"❌ Trade Failed: {e}")
