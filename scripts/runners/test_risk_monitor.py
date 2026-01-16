
from services.risk.risk_monitor import get_risk_monitor

def run_test_risk(args=None):
    """
    Test Phase 20 Risk Monitor.
    """
    print("Testing Real-time Risk Monitor...")
    monitor = get_risk_monitor()
    
    # 1. Test VaR Calculation
    print("\n--- Value at Risk (VaR) ---")
    portfolio_val = 1_000_000 # $1M
    daily_vol = 0.02 # 2%
    var = monitor.calculate_parametric_var(portfolio_val, daily_vol)
    print(f"Portfolio Value: ${portfolio_val:,.2f}")
    print(f"Daily Volatility: {daily_vol*100}%")
    print(f"95% VaR (1-Day): ${var:,.2f}")
    
    if var > 32000 and var < 33000:
         print("✅ VaR Calculation Verified (approx $32,900)")
    else:
         print("❌ VaR Calculation Failed")
         
    # 2. Test Concentration Limits
    print("\n--- Concentration Checks ---")
    holdings = [
        {'symbol': 'NVDA', 'sector': 'Tech', 'weight': 0.25}, # > 20% Asset Warning
        {'symbol': 'MSFT', 'sector': 'Tech', 'weight': 0.15},
        {'symbol': 'JPM', 'sector': 'Finance', 'weight': 0.10}
        # Total Tech: 40% > 30% Sector Warning
    ]
    
    warnings = monitor.check_concentration_limits(holdings)
    for w in warnings:
        print(f"ALERT: {w}")
        
    if len(warnings) >= 2:
        print("✅ Concentration Limits Verified: Detects both Asset and Sector violations.")
    else:
         print("❌ Concentration Checks Failed")
