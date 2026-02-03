"""
Verification script for Phase 25.
Compares two distinct strategy architectures to prove mathematical superiority of High RR.
"""
import sys
import os

# Ensure paths
sys.path.append(os.getcwd())

from services.analysis.expectancy_engine import ExpectancyEngine
from services.analysis.alpha_attributor import AlphaAttributor
from services.simulation.monte_carlo_sim import MonteCarloSimulator

def run_verification():
    print("=== Starting Phase 25 Verification ===")
    
    engine = ExpectancyEngine()
    attributor = AlphaAttributor()
    sim = MonteCarloSimulator()

    # 1. Compare Two Strategies
    # Strat A: 90% Win Rate, 1:10 RR (Inverse Risk-Reward)
    # Strat B: 40% Win Rate, 3:1 RR (High Risk-Reward)
    
    print("\n[1/3] Comparing Strategic Expectancy...")
    strat_a = {"name": "High Frequency Scalper", "win_rate": 0.90, "avg_win_r": 1.0, "avg_loss_r": 10.0}
    strat_b = {"name": "High RR Swing", "win_rate": 0.40, "avg_win_r": 3.0, "avg_loss_r": 1.0}
    
    exp_a = engine.calculate_expectancy(strat_a['win_rate'], strat_a['avg_win_r'], strat_a['avg_loss_r'])
    exp_b = engine.calculate_expectancy(strat_b['win_rate'], strat_b['avg_win_r'], strat_b['avg_loss_r'])
    
    print(f"Strat A Expectancy: {exp_a} R/trade")
    print(f"Strat B Expectancy: {exp_b} R/trade")
    
    winner = engine.identify_superior_strategy(strat_a, strat_b)
    if winner == "High RR Swing" and exp_b > exp_a:
        print(f"✅ Superiority Validated: {winner} is mathematically superior.")
    else:
        print("❌ Expectancy engine failed to identify the edge!")
        return False

    # 2. Test Alpha Attribution (Outlier Logic)
    print("\n[2/3] Verifying Alpha Attribution (Luck vs Skill)...")
    # 5 trades: [1.5R, -1.0R, 25.0R, -1.0R, -1.0R]
    results = [1.5, -1.0, 25.0, -1.0, -1.0]
    audit = attributor.calculate_adjusted_expectancy(results, outlier_cap=10.0)
    print(f"Audit: {audit}")
    if audit["outliers_found"] == 1:
        print("✅ Risk Attribution correctly identified luck outlier.")
    else:
        print("❌ Attribution failed to detect outlier!")
        return False

    # 3. Monte Carlo Survival Sim
    print("\n[3/3] Projecting Survival (1000 Trades)...")
    # Project Strat B (High RR)
    projection = sim.run_simulation(0.40, 3.0, 1.0, num_trades=1000)
    print(f"Strat B Projection: Final Equity ${projection['final_equity']:,.2f}, Max DD {projection['max_drawdown_pct']}%")
    if not projection["ruin_occurred"]:
        print("✅ Survival model confirmed long-term edge stability.")
    else:
        print("❌ Survival model failed on positive edge!")
        return False

    print("\n=== Phase 25 Verification SUCCESS ===")
    return True

if __name__ == "__main__":
    if not run_verification():
        sys.exit(1)
