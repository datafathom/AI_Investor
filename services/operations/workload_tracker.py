import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

class OperationalWorkloadService:
    """Summarizes human capital and data costs per investment model."""
    
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
