from fastapi import APIRouter, HTTPException
from typing import List, Optional, Dict
from pydantic import BaseModel
import logging

from services.quantitative.factor_engine import FactorEngine

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/v1/quantitative", tags=["Quantitative"])

class PortfolioRequest(BaseModel):
    holdings: List[Dict] # [{"ticker": "AAPL", "weight": 0.5}]

@router.get("/factors")
async def list_factors():
    service = FactorEngine()
    return await service.list_factors()

@router.get("/factors/returns")
async def get_factor_returns(days: int = 30):
    service = FactorEngine()
    return await service.get_factor_returns(days)

@router.get("/factors/exposure/{ticker}")
async def get_factor_exposure(ticker: str):
    service = FactorEngine()
    return await service.calculate_exposure(ticker)

@router.post("/factors/portfolio")
async def analyze_portfolio(req: PortfolioRequest):
    service = FactorEngine()
    return await service.analyze_portfolio_factors(req.holdings)

# --- Backtest & Monte Carlo ---
from services.quantitative.backtest_engine import BacktestEngine
from services.quantitative.monte_carlo import MonteCarloSimulator

@router.post("/backtest")
async def run_backtest(strategy: Dict):
    service = BacktestEngine()
    return await service.run_backtest(strategy)

@router.get("/backtest/{id}")
async def get_backtest(id: str):
    service = BacktestEngine()
    res = await service.get_test_results(id)
    if not res:
        raise HTTPException(status_code=404, detail="Backtest not found")
    return res

@router.post("/monte-carlo")
async def run_monte_carlo(params: Dict):
    service = MonteCarloSimulator()
    return await service.run_simulation(params)
