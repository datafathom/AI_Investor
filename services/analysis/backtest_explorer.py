"""
Advanced Backtest Explorer V2 - Phase 57.
Enhanced backtest result visualization.
"""
import logging
from typing import Dict, Any, List

logger = logging.getLogger(__name__)

class BacktestExplorer:
    """Analyzes backtest results."""
    
    @staticmethod
    def analyze_results(trades: List[Dict[str, Any]]) -> Dict[str, Any]:
        if not trades:
            return {"error": "No trades"}
        
        wins = [t for t in trades if t.get("pnl", 0) > 0]
        losses = [t for t in trades if t.get("pnl", 0) <= 0]
        
        return {
            "total_trades": len(trades),
            "win_rate": len(wins) / len(trades) * 100,
            "avg_win": sum(t["pnl"] for t in wins) / len(wins) if wins else 0,
            "avg_loss": sum(t["pnl"] for t in losses) / len(losses) if losses else 0,
            "profit_factor": abs(sum(t["pnl"] for t in wins) / sum(t["pnl"] for t in losses)) if losses and sum(t["pnl"] for t in losses) != 0 else 0
        }
