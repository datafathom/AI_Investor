from fastapi import APIRouter
import random
import uuid
from typing import List, Dict

router = APIRouter(prefix="/api/v1/backtest", tags=["Backtest"])

@router.post('/run')
async def run_backtest():
    """Start a backtest."""
    return {"success": True, "data": {"id": str(uuid.uuid4()), "status": "RUNNING"}}

@router.get('/{id}/results')
async def get_results(id: str):
    """Get backtest results."""
    # Mock data
    equity_curve = [{"time": f"2025-01-{i:02d}", "equity": 10000 + (i * random.randint(-100, 200))} for i in range(1, 31)]
    return {
        "success": True,
        "data": {
            "id": id,
            "metrics": {
                "sharpe": 1.8,
                "sortino": 2.1,
                "max_drawdown": -12.5,
                "win_rate": 0.65,
                "total_return_pct": 15.4
            },
            "equity_curve": equity_curve,
            "trades": [
                {"date": "2025-01-05", "symbol": "AAPL", "side": "BUY", "qty": 10, "price": 150.0, "pnl": 0},
                {"date": "2025-01-10", "symbol": "AAPL", "side": "SELL", "qty": 10, "price": 160.0, "pnl": 100.0}
            ]
        }
    }

@router.post('/walk-forward')
async def run_walk_forward():
    """Run walk-forward optimization."""
    return {"success": True, "data": {"id": str(uuid.uuid4()), "status": "OPTIMIZING"}}
