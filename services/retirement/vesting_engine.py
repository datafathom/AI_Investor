import logging
from datetime import datetime, date
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)

class VestingEngine:
    """Calculates vested percentage of employer contributions."""
    
    def calculate_vested_pct(self, hire_date: date, current_date: date, config: Dict[str, Any]) -> float:
        """
        vesting_type: IMMEDIATE, CLIFF, GRADED
        """
        months_service = (current_date.year - hire_date.year) * 12 + (current_date.month - hire_date.month)
        
        v_type = config.get("vesting_type", "IMMEDIATE")
        
        if v_type == "IMMEDIATE":
            return 1.0
            
        elif v_type == "CLIFF":
            cliff_months = config.get("vesting_cliff_months", 36) # 3 years default
            return 1.0 if months_service >= cliff_months else 0.0
            
        elif v_type == "GRADED":
            schedule = config.get("vesting_schedule", {}) # {"12": 0.2, "24": 0.4...}
            if not schedule: return 1.0
            
            # Find highest reached milestone
            reached_pct = 0.0
            for month_limit, pct in sorted(schedule.items(), key=lambda x: int(x[0])):
                if months_service >= int(month_limit):
                    reached_pct = pct
                else:
                    break
            return reached_pct
            
        return 0.0
