
from services.risk.circuit_breaker import get_circuit_breaker

def run_test_circuit_breaker(args=None):
    """
    Test Phase 21 Circuit Breakers.
    """
    print("Testing Circuit Breakers (Freeze & Kill Switch)...")
    cb = get_circuit_breaker()
    cb.reset()
    
    # 1. Test Portfolio Freeze (Drawdown > 3%)
    print("\n--- Portfolio Freeze Test ---")
    pnl_scenarios = [-0.01, -0.02, -0.029, -0.035]
    
    for pnl in pnl_scenarios:
        frozen = cb.check_portfolio_freeze(pnl)
        status = "FROZEN" if frozen else "ACTIVE"
        print(f"Daily PnL {pnl*100:.2f}% -> Status: {status}")
        if frozen:
            print(f"  Reason: {cb.freeze_reason}")
            
    if cb.portfolio_frozen:
        print("OK Portfolio Freeze Verified.")
    else:
        print("ERROR Portfolio Freeze Failed.")
        
    # Reset for next test
    cb.reset()
    
    # 2. Test Asset Kill Switch (Drop > 10%)
    print("\n--- Asset Kill Switch Test ---")
    
    # AAPL: Small dip
    prices_aapl = [150.0, 148.0, 145.0] # Drop ~3%
    halt_aapl = cb.check_asset_kill_switch('AAPL', prices_aapl)
    print(f"AAPL (Drop 3%): {'HALTED' if halt_aapl else 'TRADING'}")
    
    # TSLA: Crash
    prices_tsla = [200.0, 190.0, 170.0] # Drop 15% (200->170)
    halt_tsla = cb.check_asset_kill_switch('TSLA', prices_tsla)
    print(f"TSLA (Drop 15%): {'HALTED' if halt_tsla else 'TRADING'}")
    
    if halt_tsla and not halt_aapl:
        print("OK Asset Kill Switch Verified.")
    else:
        print("ERROR Kill Switch Logic Failed.")
