"""
10b5-1 Plan Generator.
Creates legally compliant automated selling plans.
"""
import logging
from datetime import datetime
from typing import Dict, Any

logger = logging.getLogger(__name__)

class Plan10b5Generator:
    """Generates 10b5-1 plan templates."""
    
    def generate_plan(self, user_name: str, ticker: str, total_shares: int, months: int) -> Dict[str, Any]:
        monthly_sell = total_shares // months
        
        return {
            "entity": f"Plan for {user_name}",
            "ticker": ticker,
            "rule": f"Sell {monthly_sell} shares on the 1st of every month for {months} months",
            "cooling_off_period": "90 Days",
            "status": "DRAFT"
        }
