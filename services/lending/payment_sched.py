import logging
from decimal import Decimal
from typing import List, Dict, Any
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

class PaymentScheduleTracker:
    """
    Phase 167.5: Interest-Only Payment Schedule Tracker.
    Tracks monthly interest-only payments for UHNW credit lines.
    """
    
    def generate_io_schedule(self, principal: Decimal, rate_pct: float, months: int) -> List[Dict[str, Any]]:
        """
        Logic: Monthly Interest = (Principal * rate) / 12.
        """
        monthly_rate = Decimal(str(rate_pct)) / Decimal('100') / Decimal('12')
        monthly_payment = principal * monthly_rate
        
        schedule = []
        start_date = datetime.now()
        
        for i in range(1, months + 1):
            schedule.append({
                "period": i,
                "due_date": (start_date + timedelta(days=30*i)).strftime("%Y-%m-%d"),
                "interest_payment": round(float(monthly_payment), 2),
                "principal_payment": 0.0,
                "remaining_balance": float(round(principal, 2))
            })
            
        logger.info(f"LENDING_LOG: Generated {months}-month IO schedule for ${principal:,.2f}.")
        return schedule
