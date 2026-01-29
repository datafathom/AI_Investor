"""
Survival Scorecard Generator.
Generates monthly survival reports.
"""
import logging
from typing import Dict, Any, List
from datetime import datetime

logger = logging.getLogger(__name__)

class SurvivalScorecard:
    """Generates survival scorecards."""
    
    @staticmethod
    def generate_scorecard(trades: List[Dict[str, Any]], drawdown_max: float) -> Dict[str, Any]:
        if not trades:
            return {"score": 0, "grade": "N/A"}
            
        win_count = sum(1 for t in trades if t.get("pnl", 0) > 0)
        total = len(trades)
        consistency = win_count / total
        
        # Survival score formula: Consistency * (1 - Drawdown) * 100
        score = consistency * (1 - abs(drawdown_max)) * 100
        
        grade = "F"
        if score > 80: grade = "A"
        elif score > 60: grade = "B"
        elif score > 40: grade = "C"
        elif score > 20: grade = "D"
        
        return {
            "period": datetime.now().strftime("%Y-%m"),
            "survival_score": round(score, 2),
            "grade": grade,
            "max_drawdown": drawdown_max
        }
