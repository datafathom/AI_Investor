"""
Trade Journal Analyzer - Phase 32.
Analyzes historical trades for pattern insights.
"""
import logging
from typing import Dict, Any, List

logger = logging.getLogger(__name__)

class JournalAnalyzer:
    """Extracts insights from trade history."""
    
    @staticmethod
    def analyze_by_day(trades: List[Dict[str, Any]]) -> Dict[str, float]:
        day_pnl = {}
        for trade in trades:
            day = trade.get("day", "Unknown")
            pnl = trade.get("pnl", 0)
            day_pnl[day] = day_pnl.get(day, 0) + pnl
        return day_pnl
    
    @staticmethod
    def get_best_setup(trades: List[Dict[str, Any]]) -> str:
        setups = {}
        for trade in trades:
            setup = trade.get("setup", "Unknown")
            r = trade.get("r_multiple", 0)
            if setup not in setups:
                setups[setup] = []
            setups[setup].append(r)
        best = max(setups.items(), key=lambda x: sum(x[1])/len(x[1]) if x[1] else 0)
        return best[0]
