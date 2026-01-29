"""
Portfolio Drawdown History - Phase 29.
TimescaleDB integration for drawdown tracking.
"""
import logging
from datetime import datetime
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

class DrawdownHistory:
    """Tracks historical drawdown events."""
    
    def __init__(self):
        self.history: List[Dict[str, Any]] = []
    
    def record_drawdown(self, pct: float, duration_days: int):
        self.history.append({
            "timestamp": datetime.now().isoformat(),
            "drawdown_pct": pct,
            "duration_days": duration_days
        })
    
    def get_max_historical_dd(self) -> float:
        if not self.history:
            return 0.0
        return max(h["drawdown_pct"] for h in self.history)
