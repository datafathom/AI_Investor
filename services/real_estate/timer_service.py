
import logging
from datetime import date, timedelta
from typing import Dict, Any

logger = logging.getLogger(__name__)

class ExchangeTimerService:
    """
    Calculates and monitors strict IRS deadlines for 1031 exchanges.
    """
    
    IDENTIFICATION_DAYS = 45
    CLOSING_DAYS = 180
    
    def calculate_deadlines(self, sale_closed_date: date) -> Dict[str, Any]:
        """
        Calculates the 45-day identification and 180-day closing deadlines.
        """
        id_deadline = sale_closed_date + timedelta(days=self.IDENTIFICATION_DAYS)
        close_deadline = sale_closed_date + timedelta(days=self.CLOSING_DAYS)
        
        logger.info(f"Exchange Deadlines: Sale={sale_closed_date}, ID={id_deadline}, Close={close_deadline}")
        
        return {
            "sale_closed_date": sale_closed_date.isoformat(),
            "identification_deadline": id_deadline.isoformat(),
            "closing_deadline": close_deadline.isoformat(),
            "days_remaining_identification": (id_deadline - date.today()).days,
            "days_remaining_closing": (close_deadline - date.today()).days
        }

    def check_deadline_status(self, sale_date: date, identified_date: date = None, purchase_date: date = None) -> str:
        """
        Returns the current compliance status of the exchange window.
        """
        today = date.today()
        id_deadline = sale_date + timedelta(days=self.IDENTIFICATION_DAYS)
        close_deadline = sale_date + timedelta(days=self.CLOSING_DAYS)
        
        if purchase_date and purchase_date <= close_deadline:
            return "COMPLETED"
        if not identified_date and today > id_deadline:
            return "FAILED_ID_WINDOW"
        if identified_date and today > close_deadline and not purchase_date:
            return "FAILED_CLOSE_WINDOW"
        if identified_date:
            return "IDENTIFIED"
            
        return "PENDING"
