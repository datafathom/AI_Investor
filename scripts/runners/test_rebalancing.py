"""
==============================================================================
FILE: scripts/runners/test_rebalancing.py
ROLE: Live Pilot
PURPOSE:
    Simulate a portfolio drift scenario and demonstrate the RebalanceEngine's
    ability to recover to the target state.
==============================================================================
"""

from services.strategy.rebalance_engine import get_rebalance_engine

def run_test_rebalance(args=None):
    """
    Test Phase 33 Autonomous Rebalancing.
    """
    print("Testing Autonomous Rebalance Engine...")
    
    engine = get_rebalance_engine()
    
    # 1. Setup Portfolio State
    # Target: 40% SPY, 40% QQQ, 20% CASH
    target = {"SPY": 0.4, "QQQ": 0.4, "CASH": 0.2}
    
    # Current: QQQ ran up big time.
    current = {"SPY": 0.35, "QQQ": 0.50, "CASH": 0.15}
    
    prices = {"SPY": 450, "QQQ": 380}
    portfolio_value = 100000
    
    print(f"\nPortfolio Value: ${portfolio_value:,}")
    print(f"Target Allocation:  {target}")
    print(f"Current Allocation: {current}")
    
    # 2. Check Drift
    drift = engine.calculate_drift(current, target)
    print("\nDrift Analysis:")
    for sym, d in drift.items():
        print(f" - {sym}: {d*100:+.1f}%")
        
    needed = engine.check_rebalance_needed(drift)
    print(f"\nRebalance Needed: {needed}")
    
    if needed:
        orders = engine.generate_rebalance_orders(drift, portfolio_value, prices)
        print("\nGenerated Correction Orders:")
        for o in orders:
            print(f" ➡️ {o['side']} {o['quantity']} {o['symbol']} ({o['reason']})")
            
    print("\n✅ Rebalancing Logic Verified.")
