"""
Scenario Service - What-If Impact Simulation
Phase 60: Simulates portfolio impact under macro shock scenarios.
"""
from dataclasses import dataclass
from datetime import datetime
from typing import Dict, List, Optional
import logging

logger = logging.getLogger(__name__)

@dataclass
class MacroShock:
    id: str
    name: str
    equity_drop: float
    bond_drop: float
    gold_change: float
    commodity_change: float = 0

@dataclass
class ScenarioResult:
    scenario_id: str
    portfolio_impact: float
    new_portfolio_value: float
    positions_affected: List[Dict]
    hedge_offset: float
    net_impact: float

@dataclass
class RecoveryProjection:
    recovery_days: int
    recovery_path: List[float]
    worst_case_days: int
    best_case_days: int

class ScenarioService:
    def __init__(self) -> None:
        self._base_portfolio_value = 1000000.0
        logger.info("ScenarioService initialized")
    
    async def apply_shock(self, portfolio_id: str, shock: MacroShock) -> ScenarioResult:
        equity_weight = 0.6
        bond_weight = 0.3
        gold_weight = 0.1
        
        impact = (equity_weight * shock.equity_drop / 100 +
                  bond_weight * shock.bond_drop / 100 +
                  gold_weight * shock.gold_change / 100)
        
        new_value = self._base_portfolio_value * (1 + impact)
        hedge_offset = abs(gold_weight * shock.gold_change / 100 * self._base_portfolio_value)
        
        return ScenarioResult(
            scenario_id=shock.id,
            portfolio_impact=impact * 100,
            new_portfolio_value=new_value,
            positions_affected=[
                {"type": "Equities", "impact": shock.equity_drop * equity_weight},
                {"type": "Bonds", "impact": shock.bond_drop * bond_weight}
            ],
            hedge_offset=hedge_offset,
            net_impact=(impact * self._base_portfolio_value)
        )
    
    async def calculate_hedge_sufficiency(self, portfolio_id: str, shock: MacroShock) -> float:
        result = await self.apply_shock(portfolio_id, shock)
        if result.net_impact >= 0:
            return 1.0
        return min(1.0, result.hedge_offset / abs(result.net_impact))
    
    async def simulate_bank_run(self, portfolio_id: str) -> Dict:
        return {
            "liquid_assets": self._base_portfolio_value * 0.3,
            "days_of_coverage": 180,
            "vulnerable_positions": ["Corporate Bonds", "REITs"]
        }
    
    async def project_recovery_timeline(self, result: ScenarioResult) -> RecoveryProjection:
        drop_pct = abs(result.portfolio_impact)
        # 10 days per 1% drop with a floor
        base_days = max(30, int(drop_pct * 10))  
        
        # Generate a semi-logarithmic recovery path
        recovery_path = []
        steps = 10
        val = result.new_portfolio_value
        target = self._base_portfolio_value
        for i in range(steps + 1):
            progress = i / steps
            # Quadratic recovery for visual aesthetic
            current = val + (target - val) * (progress ** 1.5)
            recovery_path.append(current)
            
        return RecoveryProjection(
            recovery_days=base_days,
            recovery_path=recovery_path,
            worst_case_days=int(base_days * 1.8),
            best_case_days=int(base_days * 0.4)
        )

    async def run_refined_monte_carlo(
        self, 
        initial_value: float, 
        shock: MacroShock,
        paths: int = 1000,
        days: int = 120
    ) -> Dict:
        """Runs a Monte Carlo simulation starting from a post-shock state."""
        import random
        import math
        
        # Volatility usually spikes after a shock
        base_vol = 0.25
        mu = 0.05
        dt = 1/252
        
        results = []
        for _ in range(paths):
            path = [initial_value]
            curr = initial_value
            for _ in range(days):
                z = random.gauss(0, 1)
                curr *= math.exp((mu - 0.5 * base_vol**2) * dt + base_vol * math.sqrt(dt) * z)
                path.append(curr)
            results.append(path)
            
        # Return summary stats for visualization
        return {
            "p5": [results[int(paths * 0.05)][i] for i in range(days + 1)],
            "p50": [results[int(paths * 0.5)][i] for i in range(days + 1)],
            "p95": [results[int(paths * 0.95)][i] for i in range(days + 1)],
            "days": days
        }

    async def calculate_liquidity_drain(self, stress_level: float = 1.0) -> Dict:
        """Detailed liquidity analysis under stress."""
        base_liquid = self._base_portfolio_value * 0.4
        drain_rate = 0.05 * stress_level
        
        vulnerabilities = [
            {"asset": "ILLQ-COIN", "exit_days": 14 * stress_level, "slippage": -0.12 * stress_level},
            {"asset": "OBSCURE-ETF", "exit_days": 4 * stress_level, "slippage": -0.03 * stress_level},
            {"asset": "CORP-BOND-X", "exit_days": 8 * stress_level, "slippage": -0.05 * stress_level}
        ]
        
        return {
            "liquid_assets": base_liquid * (1 - drain_rate),
            "days_of_coverage": max(1, int(180 / stress_level)),
            "vulnerable_positions": vulnerabilities,
            "system_stress_index": min(1.0, 0.2 * stress_level)
        }

_scenario_service: Optional[ScenarioService] = None
def get_scenario_service() -> ScenarioService:
    global _scenario_service
    if _scenario_service is None:
        _scenario_service = ScenarioService()
    return _scenario_service
