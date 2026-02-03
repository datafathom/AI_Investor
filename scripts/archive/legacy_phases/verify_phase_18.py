"""
Verification script for Phase 18.
Simulates a sequence of trades to verify R-multiple calculations and expectancy modeling.
"""
import sys
import os
from decimal import Decimal

# Ensure paths
sys.path.append(os.getcwd())

from services.performance.r_calculator import RCalculator
from services.performance.expectancy_model import ExpectancyModel
from services.performance.agent_stats import AgentStats

def run_verification():
    print("=== Starting Phase 18 Verification ===")
    
    r_calc = RCalculator()
    expectancy_svc = ExpectancyModel()
    stats_svc = AgentStats()

    # 1. Test Initial Risk Calculation
    print("\n[1/3] Testing Entry Risk Calculation (EUR/USD)...")
    entry = Decimal("1.0850")
    stop = Decimal("1.0800") # 50 pip SL
    lots = Decimal("2.0")
    risk_usd = r_calc.calculate_initial_risk(entry, stop, lots, "EUR/USD")
    print(f"Calculated Risk: ${risk_usd:,.2f} for 2.0 lots at 50 pip SL")
    if risk_usd != Decimal("1000.00"):
         print(f"❌ Risk mismatch! Expected $1000, got ${risk_usd}")
         return False
    print("✅ Entry risk calculation accurate.")

    # 2. Test Expectancy Modeling
    print("\n[2/3] Testing Expectancy Formula (Edge Detection)...")
    # Sequence: -1R, -1R, 3R, 2R, -1R (Negative count: 3, Positive: 2)
    # Win Rate: 40% (0.4)
    # Avg Win: 2.5R
    # Avg Loss: 1.0R
    # E = (0.4 * 2.5) - (0.6 * 1.0) = 1.0 - 0.6 = 0.4R
    r_history = [-1.0, -1.0, 3.0, 2.0, -1.0]
    metrics = expectancy_svc.calculate_expectancy(r_history)
    print(f"Metrics: {metrics}")
    
    if metrics["expectancy"] != 0.4:
        print(f"❌ Expectancy mismatch! Expected 0.4, got {metrics['expectancy']}")
        return False
    print("✅ Expectancy model validated (Positive Edge Detected).")

    # 3. Test Agent Leaderboard
    print("\n[3/3] Testing Agent Stats Attribution...")
    journal = [
        {"agent_id": "searcher-A", "r_multiple": 3.0},
        {"agent_id": "searcher-A", "r_multiple": -1.0},
        {"agent_id": "searcher-B", "r_multiple": 0.5},
        {"agent_id": "searcher-B", "r_multiple": 0.5},
    ]
    leaderboard = stats_svc.calculate_leaderboard(journal)
    print(f"Leaderboard: {leaderboard}")
    
    if leaderboard[0]["agent_id"] != "searcher-A": # (3-1)/2 = 1.0R vs (0.5+0.5)/2 = 0.5R
         print("❌ Leaderboard sorting failed!")
         return False
    print("✅ Agent performance attribution accurate.")

    print("\n=== Phase 18 Verification SUCCESS ===")
    return True

if __name__ == "__main__":
    if not run_verification():
        sys.exit(1)
