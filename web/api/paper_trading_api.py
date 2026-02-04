"""
==============================================================================
FILE: web/api/paper_trading_api.py
ROLE: Paper Trading API Endpoints (FastAPI)
PURPOSE: REST endpoints for paper trading and simulation.
==============================================================================
"""

from fastapi import APIRouter, Query, HTTPException, Depends
from fastapi.responses import JSONResponse
from typing import Optional, List
from pydantic import BaseModel
from datetime import timezone, datetime
import logging
import uuid
from web.auth_utils import get_current_user

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/paper-trading", tags=["Paper Trading"])


class CreatePortfolioRequest(BaseModel):
    user_id: str
    portfolio_name: str = "Paper Trading Portfolio"
    initial_cash: float = 100000.0


class ExecuteOrderRequest(BaseModel):
    portfolio_id: str
    symbol: str
    quantity: int
    order_type: str = "market"
    price: Optional[float] = None


class SimulationRequest(BaseModel):
    strategy_name: str
    start_date: str
    end_date: str
    initial_capital: float = 100000.0
    strategy_config: Optional[dict] = None


# Mock portfolio data
MOCK_PORTFOLIO = {
    "portfolio_id": "paper_001",
    "user_id": "user_1",
    "portfolio_name": "Paper Trading Portfolio",
    "cash": 85000.00,
    "positions": [
        {"symbol": "AAPL", "quantity": 50, "avg_price": 170.00, "current_price": 175.50, "unrealized_pnl": 275.00},
        {"symbol": "MSFT", "quantity": 30, "avg_price": 380.00, "current_price": 395.00, "unrealized_pnl": 450.00}
    ],
    "total_value": 108525.00,
    "total_pnl": 8525.00,
    "pnl_percent": 8.53
}

MOCK_TRADES = [
    {"id": "t1", "symbol": "AAPL", "side": "buy", "quantity": 50, "price": 170.00, "timestamp": "2026-01-15T10:30:00Z"},
    {"id": "t2", "symbol": "MSFT", "side": "buy", "quantity": 30, "price": 380.00, "timestamp": "2026-01-20T14:15:00Z"}
]


@router.get("/portfolio")
async def get_portfolio_summary(
    current_user: dict = Depends(get_current_user)
):
    """Get virtual portfolio details for user."""
    user_id = current_user.get("id") or current_user.get("user_id")
    return {
        "success": True,
        "data": MOCK_PORTFOLIO
    }


@router.get("/portfolio/{portfolio_id}")
async def get_portfolio_by_id(
    portfolio_id: str,
    current_user: dict = Depends(get_current_user)
):
    """Get virtual portfolio by ID."""
    return {
        "success": True,
        "data": MOCK_PORTFOLIO
    }


@router.post("/portfolio/create")
async def create_virtual_portfolio(
    request: CreatePortfolioRequest,
    current_user: dict = Depends(get_current_user)
):
    """Create virtual portfolio for paper trading."""
    portfolio_id = f"paper_{uuid.uuid4().hex[:8]}"
    
    return {
        "success": True,
        "data": {
            "portfolio_id": portfolio_id,
            "user_id": request.user_id,
            "portfolio_name": request.portfolio_name,
            "cash": request.initial_cash,
            "positions": [],
            "total_value": request.initial_cash,
            "created_at": datetime.now(timezone.utc).isoformat() + "Z"
        }
    }


@router.get("/trades")
async def get_trades(
    limit: int = Query(20),
    current_user: dict = Depends(get_current_user)
):
    """Get recent trades for user."""
    return {
        "success": True,
        "data": MOCK_TRADES[:limit]
    }


@router.post("/order/execute")
async def execute_paper_order(
    request: ExecuteOrderRequest,
    current_user: dict = Depends(get_current_user)
):
    """Execute paper trading order."""
    order_id = f"ord_{uuid.uuid4().hex[:8]}"
    fill_price = request.price or 175.50  # Mock market price
    
    return {
        "success": True,
        "data": {
            "order_id": order_id,
            "portfolio_id": request.portfolio_id,
            "symbol": request.symbol,
            "quantity": request.quantity,
            "order_type": request.order_type,
            "fill_price": fill_price,
            "total_value": request.quantity * fill_price,
            "status": "filled",
            "executed_at": datetime.now(timezone.utc).isoformat() + "Z"
        }
    }


@router.get("/portfolio/{portfolio_id}/performance")
async def get_portfolio_performance(
    portfolio_id: str,
    current_user: dict = Depends(get_current_user)
):
    """Get portfolio performance metrics."""
    return {
        "success": True,
        "data": {
            "portfolio_id": portfolio_id,
            "total_return": 8.53,
            "sharpe_ratio": 1.45,
            "max_drawdown": -3.2,
            "win_rate": 0.67,
            "avg_trade_pnl": 425.00,
            "best_trade": {"symbol": "NVDA", "pnl": 1250.00},
            "worst_trade": {"symbol": "META", "pnl": -320.00}
        }
    }


@router.post("/simulation/run")
async def run_simulation(
    request: SimulationRequest,
    current_user: dict = Depends(get_current_user)
):
    """Run historical simulation/backtest."""
    return {
        "success": True,
        "data": {
            "simulation_id": f"sim_{uuid.uuid4().hex[:8]}",
            "strategy_name": request.strategy_name,
            "start_date": request.start_date,
            "end_date": request.end_date,
            "initial_capital": request.initial_capital,
            "final_value": request.initial_capital * 1.15,
            "total_return": 15.0,
            "sharpe_ratio": 1.32,
            "max_drawdown": -8.5,
            "total_trades": 45,
            "winning_trades": 28,
            "losing_trades": 17
        }
    }
