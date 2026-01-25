"""
Monte Carlo Service - Simulation & Risk Metrics
Phase 57: GBM simulation, ruin probability, and drawdown analysis.
"""
from dataclasses import dataclass
from typing import Dict, List, Tuple, Optional
import random
import math
import logging

logger = logging.getLogger(__name__)

@dataclass
class SimulationResult:
    paths: List[List[float]]
    quantiles: Dict[str, List[float]]
    ruin_probability: float
    median_final: float
    mean_final: float

@dataclass
class DrawdownMetrics:
    max_drawdown: float
    avg_drawdown: float
    max_duration_days: int
    ulcer_index: float
    pain_index: float
    recovery_days: int

class MonteCarloService:
    def __init__(self) -> None:
        logger.info("MonteCarloService initialized")
    
    async def run_gbm_simulation(
        self,
        initial_value: float,
        mu: float = 0.08,
        sigma: float = 0.15,
        days: int = 252,
        paths: int = 10000,
        dt: float = 1/252
    ) -> SimulationResult:
        all_paths = []
        final_values = []
        ruins = 0
        ruin_threshold = initial_value * 0.5
        
        for _ in range(min(paths, 1000)):  # Limit for performance
            path = [initial_value]
            value = initial_value
            
            for _ in range(days):
                z = random.gauss(0, 1)
                value = value * math.exp((mu - 0.5 * sigma**2) * dt + sigma * math.sqrt(dt) * z)
                path.append(value)
            
            all_paths.append(path)
            final_values.append(value)
            if min(path) < ruin_threshold:
                ruins += 1
        
        # Sort paths by their final value to extract correct quantiles
        all_paths.sort(key=lambda p: p[-1])
        
        quantiles = {
            "p5": [all_paths[int(len(all_paths) * 0.05)][i] for i in range(days + 1)],
            "p50": [all_paths[int(len(all_paths) * 0.50)][i] for i in range(days + 1)],
            "p95": [all_paths[int(len(all_paths) * 0.95)][i] for i in range(days + 1)],
        }
        
        final_values = [p[-1] for p in all_paths]
        
        return SimulationResult(
            paths=all_paths[:100],
            quantiles=quantiles,
            ruin_probability=ruins / len(all_paths),
            median_final=final_values[len(final_values) // 2],
            mean_final=sum(final_values) / len(final_values)
        )
    
    async def calculate_ruin_probability(
        self,
        result: SimulationResult,
        drawdown_limit: float = 0.50
    ) -> float:
        return result.ruin_probability
    
    async def calculate_drawdown_metrics(self, path: List[float]) -> DrawdownMetrics:
        if not path:
            return DrawdownMetrics(0, 0, 0, 0, 0, 0)
        
        peak = path[0]
        drawdowns = []
        current_dd = 0
        dd_start = 0
        max_duration = 0
        current_duration = 0
        
        for i, value in enumerate(path):
            if value >= peak:
                peak = value
                if current_duration > max_duration:
                    max_duration = current_duration
                current_duration = 0
            else:
                dd = (peak - value) / peak
                drawdowns.append(dd)
                current_duration += 1
                if dd > current_dd:
                    current_dd = dd
        
        max_dd = max(drawdowns) if drawdowns else 0
        avg_dd = sum(drawdowns) / len(drawdowns) if drawdowns else 0
        ulcer = math.sqrt(sum(d**2 for d in drawdowns) / len(drawdowns)) if drawdowns else 0
        pain = avg_dd * max_duration
        
        return DrawdownMetrics(
            max_drawdown=max_dd,
            avg_drawdown=avg_dd,
            max_duration_days=max_duration,
            ulcer_index=ulcer,
            pain_index=pain,
            recovery_days=int(max_duration * 1.5)
        )
    
    async def detect_overfit(self, is_sharpe: float, oos_sharpe: float) -> Tuple[bool, float]:
        variance = abs(is_sharpe - oos_sharpe) / max(is_sharpe, 0.01)
        return variance > 0.20, variance

_monte_carlo_service: Optional[MonteCarloService] = None
def get_monte_carlo_service() -> MonteCarloService:
    global _monte_carlo_service
    if _monte_carlo_service is None:
        _monte_carlo_service = MonteCarloService()
    return _monte_carlo_service
