"""
Homeostasis Service - Zen Mode & Retirement Calculation  
Phase 68: Calculates "Enough" metric, freedom number, and autopilot settings.
"""
from dataclasses import dataclass
from typing import Dict, List, Optional
import logging
import random

logger = logging.getLogger(__name__)

@dataclass
class HomeostasisResult:
    freedom_number: float
    current_value: float
    freedom_progress: float
    years_covered: float
    retirement_probability: float
    monthly_safe_withdrawal: float

@dataclass
class RetirementSimResult:
    success_probability: float
    median_outcome: float
    worst_case_5pct: float
    best_case_95pct: float
    paths_run: int

class HomeostasisService:
    def __init__(self) -> None:
        self._monthly_expenses = 8000
        self._portfolio_value = 1000000.0
        self._safe_withdrawal_rate = 0.04
        self._autopilot_enabled = False
        logger.info("HomeostasisService initialized")
    
    def calculate_freedom_number(self, monthly_expenses: float, years: int = 30) -> float:
        annual = monthly_expenses * 12
        return annual / self._safe_withdrawal_rate
    
    def calculate_homeostasis(self, portfolio_id: str) -> HomeostasisResult:
        freedom_number = self.calculate_freedom_number(self._monthly_expenses)
        progress = self._portfolio_value / freedom_number
        years = self._portfolio_value / (self._monthly_expenses * 12)
        monthly_swr = self._portfolio_value * self._safe_withdrawal_rate / 12
        
        return HomeostasisResult(
            freedom_number=freedom_number,
            current_value=self._portfolio_value,
            freedom_progress=min(1.0, progress),
            years_covered=years,
            retirement_probability=min(0.95, progress * 0.85),
            monthly_safe_withdrawal=monthly_swr
        )
    
    def run_retirement_monte_carlo(
        self,
        portfolio_value: float,
        annual_withdrawal: float,
        years: int = 30,
        simulations: int = 10000
    ) -> RetirementSimResult:
        successes = 0
        outcomes = []
        
        for _ in range(simulations):
            value = portfolio_value
            for _ in range(years):
                annual_return = random.gauss(0.07, 0.15)
                value = value * (1 + annual_return) - annual_withdrawal
                if value <= 0:
                    break
            outcomes.append(max(0, value))
            if value > 0:
                successes += 1
        
        outcomes.sort()
        return RetirementSimResult(
            success_probability=successes / simulations,
            median_outcome=outcomes[len(outcomes) // 2],
            worst_case_5pct=outcomes[int(len(outcomes) * 0.05)],
            best_case_95pct=outcomes[int(len(outcomes) * 0.95)],
            paths_run=simulations
        )
    
    def set_autopilot(self, enabled: bool) -> bool:
        self._autopilot_enabled = enabled
        logger.info(f"Autopilot {'enabled' if enabled else 'disabled'}")
        return enabled
    
    def get_autopilot_status(self) -> bool:
        return self._autopilot_enabled
    
    def should_rebalance(self, portfolio_id: str) -> bool:
        return self._autopilot_enabled and random.random() > 0.7

_homeostasis_service: Optional[HomeostasisService] = None
def get_homeostasis_service() -> HomeostasisService:
    global _homeostasis_service
    if _homeostasis_service is None:
        _homeostasis_service = HomeostasisService()
    return _homeostasis_service
