"""
==============================================================================
FILE: services/risk/stress_tester.py
ROLE: Portfolio Torture Chamber
PURPOSE:
    Simulate extreme scenarios to test portfolio resilience.
    
    1. Black Swan Scenarios:
       - 2008 Crisis (-40% Equities)
       - Covid 2020 (-30% Equities, +Gold)
       - Flash Crash (-10% Instant)
       
    2. Monte Carlo Simulation:
       - Random walk simulation of future equity curves.
       - Calculate Probability of Ruin or Loss > X%.
       
ROADMAP: Phase 22 - Stress Testing
==============================================================================
"""

import logging
from typing import Dict, Any, List
import numpy as np

logger = logging.getLogger(__name__)

class StressTester:
    def __init__(self):
        # Predefined Scenarios (Impact on Asset Classes)
        self.SCENARIOS = {
            "2008_CRISIS": {"EQUITY": -0.40, "TECH": -0.50, "BOND": 0.10, "GOLD": 0.05, "CASH": 0.0},
            "COVID_CRASH": {"EQUITY": -0.30, "TECH": -0.20, "BOND": 0.05, "GOLD": 0.10, "CASH": 0.0},
            "TECH_BUBBLE_POP": {"EQUITY": -0.10, "TECH": -0.60, "BOND": 0.05, "GOLD": 0.0, "CASH": 0.0}
        }

    def simulate_black_swan(self, 
                          portfolio: Dict[str, float], 
                          scenario_name: str) -> Dict[str, Any]:
        """
        Simulate the PnL impact of a specific Black Swan event.
        Args:
            portfolio: Dict {'NVDA': 0.3, 'BND': 0.5, 'CASH': 0.2} (Weights)
            scenario_name: '2008_CRISIS', etc.
        """
        scenario = self.SCENARIOS.get(scenario_name)
        if not scenario:
            return {"error": "Scenario not found"}
            
        initial_val = 100000.0 # Normalized base
        final_val = 0.0
        
        details = {}
        
        for asset, weight in portfolio.items():
            # Simplistic mapping: Detect asset class
            asset_class = "EQUITY" # Default
            if asset in ["BND", "SHY", "TLT"]: asset_class = "BOND"
            elif asset in ["GLD", "GOLD"]: asset_class = "GOLD"
            elif asset in ["CASH", "USD"]: asset_class = "CASH"
            elif asset in ["NVDA", "MSFT", "AAPL", "BTC"]: asset_class = "TECH"
            
            shock = scenario.get(asset_class, scenario.get("EQUITY", -0.2)) # Fallback to generic equity shock
            
            asset_val = initial_val * weight
            shocked_val = asset_val * (1 + shock)
            final_val += shocked_val
            
            details[asset] = {
                "weight": weight,
                "shock": shock,
                "pnl": shocked_val - asset_val
            }
            
        pnl_pct = (final_val - initial_val) / initial_val
        return {
            "sceanrio": scenario_name,
            "pnl_pct": pnl_pct,
            "est_loss_on_100k": pnl_pct * 100000,
            "details": details
        }

    def run_monte_carlo(self, 
                        portfolio_vol: float = 0.15, 
                        portfolio_return: float = 0.08, 
                        years: int = 1,
                        iterations: int = 1000) -> Dict[str, float]:
        """
        Run Monte Carlo simulation for portfolio path.
        Returns statistics on potential outcomes.
        """
        # Geometric Brownian Motion
        # dS/S = mu*dt + sigma*dW
        
        dt = 1/252 # Daily steps
        days = 252 * years
        results = []
        
        for _ in range(iterations):
            price = 1.0 # Start normalized at 1.0
            for _ in range(days):
                shock = np.random.normal(0, 1)
                # Simple return calc
                ret = (portfolio_return * dt) + (portfolio_vol * (dt**0.5) * shock)
                price *= (1 + ret)
            results.append(price)
            
        results = np.array(results)
        
        return {
            "mean_return": np.mean(results) - 1.0,
            "worst_case_5pct": np.percentile(results, 5) - 1.0, # 5th percentile outcome (VaR-like)
            "best_case_95pct": np.percentile(results, 95) - 1.0,
            "prob_loss": np.mean(results < 1.0) # Probability of losing money
        }

# Singleton
_instance = None

def get_stress_tester() -> StressTester:
    global _instance
    if _instance is None:
        _instance = StressTester()
    return _instance
