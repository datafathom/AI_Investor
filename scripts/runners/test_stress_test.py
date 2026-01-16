
from services.risk.stress_tester import get_stress_tester

def run_test_stress(args=None):
    """
    Test Phase 22 Stress Testing.
    """
    print("Testing Portfolio Torture Chamber (Stress Tests)...")
    tester = get_stress_tester()
    
    # 1. Black Swan Scenarios
    print("\n--- Black Swan Simulations (on $100k) ---")
    
    # Portfolio: 40% Tech (NVDA), 20% Bonds (SHY), 40% Cash
    portfolio = {"NVDA": 0.4, "SHY": 0.2, "USD": 0.4}
    
    scenarios = ["2008_CRISIS", "COVID_CRASH", "TECH_BUBBLE_POP"]
    
    for sc in scenarios:
        res = tester.simulate_black_swan(portfolio, sc)
        loss = res['est_loss_on_100k']
        pnl_pct = res['pnl_pct']
        print(f"Scenario: {sc:<15} -> Impact: {pnl_pct*100:.1f}% (${loss:,.0f})")
        
    # Verification Check
    # Tech Bubble (-60% Tech) should hit NVDA hard.
    # NVDA is 40% of port. -60% of 40% = -24% impact.
    # Bonds +5%. 20% of port -> +1% impact.
    # Cash 0%.
    # Net: -23%.
    
    res_tech = tester.simulate_black_swan(portfolio, "TECH_BUBBLE_POP")
    if res_tech['pnl_pct'] < -0.2:
        print("✅ Black Swan Logic Verified: Portfolio drops properly in Tech Crash.")
    else:
        print("❌ Black Swan Logic Failed.")
        
    # 2. Monte Carlo
    print("\n--- Monte Carlo Simulation (1 Year) ---")
    stats = tester.run_monte_carlo(iterations=500)
    print(f"Mean Return:       {stats['mean_return']*100:.1f}%")
    print(f"Best Case (95%):   {stats['best_case_95pct']*100:.1f}%")
    print(f"Worst Case (5%):   {stats['worst_case_5pct']*100:.1f}%")
    print(f"Probability of Loss: {stats['prob_loss']*100:.1f}%")
    
    if stats['mean_return'] > -0.5 and stats['mean_return'] < 0.5:
        print("✅ Monte Carlo Simulation Verified: Results within expected bounds.")
    else:
        print("❌ Monte Carlo Failed: Results erratic.")
