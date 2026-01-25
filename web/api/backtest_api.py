"""
Backtest API - Monte Carlo & Strategy Robustness
Phase 57: Endpoints for Monte Carlo simulations, ruin probability, and drawdown metrics.
"""

from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Dict, Optional
import logging

from services.analysis.monte_carlo_service import (
    MonteCarloService,
    SimulationResult,
    DrawdownMetrics,
    get_monte_carlo_service
)

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/backtest", tags=["Backtest"])

class SimulationRequest(BaseModel):
    initial_value: float = 1000000.0
    mu: float = 0.08
    sigma: float = 0.15
    days: int = 252
    paths: int = 1000

class SimulationResponse(BaseModel):
    paths: List[List[float]]
    quantiles: Dict[str, List[float]]
    ruin_probability: float
    median_final: float
    mean_final: float

class DrawdownResponse(BaseModel):
    max_drawdown: float
    avg_drawdown: float
    max_duration_days: int
    ulcer_index: float
    pain_index: float
    recovery_days: int

@router.post("/monte-carlo", response_model=SimulationResponse)
async def run_monte_carlo(
    request: SimulationRequest,
    service: MonteCarloService = Depends(get_monte_carlo_service)
) -> SimulationResponse:
    try:
        result = await service.run_gbm_simulation(
            initial_value=request.initial_value,
            mu=request.mu,
            sigma=request.sigma,
            days=request.days,
            paths=request.paths
        )
        return SimulationResponse(
            paths=result.paths,
            quantiles=result.quantiles,
            ruin_probability=result.ruin_probability,
            median_final=result.median_final,
            mean_final=result.mean_final
        )
    except Exception as e:
        logger.exception("Error running simulation")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/drawdown", response_model=DrawdownResponse)
async def get_drawdown_metrics(
    service: MonteCarloService = Depends(get_monte_carlo_service)
) -> DrawdownResponse:
    """Calculate metrics for a sample path."""
    try:
        # Mock path
        sample_path = [100 * (1 + 0.01 * i + 0.02 * (0.5 - i/10)) for i in range(100)]
        metrics = await service.calculate_drawdown_metrics(sample_path)
        return DrawdownResponse(
            max_drawdown=metrics.max_drawdown,
            avg_drawdown=metrics.avg_drawdown,
            max_duration_days=metrics.max_duration_days,
            ulcer_index=metrics.ulcer_index,
            pain_index=metrics.pain_index,
            recovery_days=metrics.recovery_days
        )
    except Exception as e:
        logger.exception("Error calculating drawdown")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/overfit")
async def check_overfit(
    is_sharpe: float = 1.5,
    oos_sharpe: float = 1.0,
    service: MonteCarloService = Depends(get_monte_carlo_service)
):
    is_overfit, variance = await service.detect_overfit(is_sharpe, oos_sharpe)
    return {"is_overfit": is_overfit, "variance": variance}
