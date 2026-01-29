"""
Unit tests for Risk-Reward vs Probability Edge Comparison.
Verifies expectancy calculation, outlier attribution, and MC simulation.
"""
import pytest
from services.analysis.expectancy_engine import ExpectancyEngine
from services.analysis.alpha_attributor import AlphaAttributor
from services.simulation.monte_carlo_sim import MonteCarloSimulator

def test_expectancy_math():
    # 40% win rate, 3:1 RR (Avg Win 3R, Avg Loss 1R)
    # Exp = (0.4 * 3) - (0.6 * 1) = 1.2 - 0.6 = 0.6R
    exp = ExpectancyEngine.calculate_expectancy(0.4, 3.0, 1.0)
    assert exp == 0.6

    # 90% win rate, 1:10 RR (Avg Win 1R, Avg Loss 10R)
    # Exp = (0.9 * 1) - (0.1 * 10) = 0.9 - 1.0 = -0.1R
    exp_bad = ExpectancyEngine.calculate_expectancy(0.9, 1.0, 10.0)
    assert exp_bad == -0.1

def test_alpha_attribution():
    # Sequence with one lucky 20R trade
    rs = [2.0, -1.0, -1.0, 20.0, -1.0] # 2/5 win rate, but one huge outlier
    result = AlphaAttributor.calculate_adjusted_expectancy(rs, outlier_cap=10.0)
    
    assert result["outliers_found"] == 1
    # Adjusted expectancy treats 20R as 10R
    # rs_adj = [2.0, -1.0, -1.0, 10.0, -1.0] -> sum = 9.0 / 5 = 1.8 (Net)
    # win% = 0.4, avg_win = 6.0, avg_loss = 1.0
    # exp = (0.4 * 6) - (0.6 * 1) = 2.4 - 0.6 = 1.8
    assert result["base_expectancy"] == 1.8

def test_monte_carlo():
    # Run a small sim with high edge
    result = MonteCarloSimulator.run_simulation(0.6, 2.0, 1.0, num_trades=50)
    assert result["trades_completed"] == 50
    assert result["ruin_occurred"] == False
    assert result["final_equity"] > 100000.0 # Highly probable
