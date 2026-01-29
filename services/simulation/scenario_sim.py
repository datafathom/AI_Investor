"""
Scenario Modeling & What-If Simulator - Phase 60.
Projects portfolio under different scenarios.
"""
import logging
from typing import Dict, Any, List

logger = logging.getLogger(__name__)

class ScenarioSimulator:
    """Runs what-if scenarios."""
    
    @staticmethod
    def simulate_market_crash(portfolio_value: float, crash_pct: float = 0.40) -> Dict[str, float]:
        new_value = portfolio_value * (1 - crash_pct)
        return {
            "original": portfolio_value,
            "after_crash": new_value,
            "loss": portfolio_value - new_value,
            "recovery_needed_pct": (portfolio_value / new_value - 1) * 100
        }
    
    @staticmethod
    def simulate_inflation(value: float, years: int, inflation_rate: float = 0.03) -> float:
        return value / ((1 + inflation_rate) ** years)
