"""
Agent Statistics Service.
Attributes R-Multiple performance to specific agent personas.
"""
import logging
from typing import Dict, List, Any
from decimal import Decimal

logger = logging.getLogger(__name__)

class AgentStats:
    """
    Identifies top-performing agent personas using R-distribution.
    """

    @staticmethod
    def calculate_leaderboard(trade_journal: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Groups performance by agent_id and calculates average R.
        """
        stats = {}
        
        for trade in trade_journal:
            agent_id = trade.get("agent_id", "UNKNOWN")
            r_multiple = trade.get("r_multiple", 0.0)
            
            if agent_id not in stats:
                stats[agent_id] = {"count": 0, "total_r": 0.0, "wins": 0}
            
            stats[agent_id]["count"] += 1
            stats[agent_id]["total_r"] += r_multiple
            if r_multiple > 0:
                stats[agent_id]["wins"] += 1

        leaderboard = []
        for agent_id, data in stats.items():
            avg_r = data["total_r"] / data["count"] if data["count"] > 0 else 0.0
            win_rate = (data["wins"] / data["count"]) * 100 if data["count"] > 0 else 0.0
            
            leaderboard.append({
                "agent_id": agent_id,
                "avg_r_multiple": round(avg_r, 2),
                "win_rate": round(win_rate, 2),
                "total_trades": data["count"]
            })

        # Sort by best average R-Multiple
        return sorted(leaderboard, key=lambda x: x["avg_r_multiple"], reverse=True)
