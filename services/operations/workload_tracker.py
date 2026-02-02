import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

class OperationalWorkloadService:
    """Summarizes human capital and data costs per investment model."""
    
    def __init__(self):
        self.seats = {
            "BLOOMBERG": {"cost_per_month": 2400, "active_users": []},
            "REFINITIV": {"cost_per_month": 1800, "active_users": []}
        }

    def assign_seat(self, user_id: str, platform: str) -> bool:
        if platform.upper() in self.seats:
            if user_id not in self.seats[platform.upper()]["active_users"]:
                self.seats[platform.upper()]["active_users"].append(user_id)
                return True
        return False

    def get_monthly_tech_burn(self) -> float:
        total = 0.0
        for platform, data in self.seats.items():
            total += len(data["active_users"]) * data["cost_per_month"]
        return total

    def summarize_monthly_effort(self, research_hrs: float, monitor_hrs: float, trading_mins: float) -> Dict[str, Any]:
        """
        Policy: Monitor time + Research time + Trading time overhead.
        """
        total_hours = research_hrs + monitor_hrs + (trading_mins / 60.0)
        
        logger.info(f"OPS_LOG: Monthly effort: {total_hours:.1f} hours ({research_hrs} hr Research, {monitor_hrs} hr Monitor, {trading_mins} min Trading)")
        
        return {
            "total_effort_hours": round(total_hours, 2),
            "is_scalable": total_hours < 20.0 # Heuristic: if >20 hrs/mo/model, scale is poor.
        }
