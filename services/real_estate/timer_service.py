
import logging
import uuid
from datetime import date, timedelta
from typing import Dict, Any, List, Optional
from utils.database_manager import db_manager

logger = logging.getLogger(__name__)

class ExchangeTimerService:
    """
    Calculates and monitors strict IRS deadlines for 1031 exchanges.
    Uses TimescaleDB for persistent tracking of exchange windows.
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

    async def create_exchange(self, exchange_id: uuid.UUID, sale_closed_date: date) -> Dict[str, Any]:
        """
        Create a new 1031 exchange record in the database.
        """
        try:
            with db_manager.pg_cursor() as cur:
                cur.execute("""
                    INSERT INTO exchange_timers (exchange_id, sale_closed_date, status)
                    VALUES (%s, %s, 'PENDING')
                    RETURNING id, identification_deadline, closing_deadline
                """, (exchange_id, sale_closed_date))
                row = cur.fetchone()
                
                logger.info(f"Created 1031 exchange {exchange_id} with sale date {sale_closed_date}")
                
                return {
                    "id": str(row[0]),
                    "exchange_id": str(exchange_id),
                    "sale_closed_date": sale_closed_date.isoformat(),
                    "identification_deadline": row[1].isoformat() if row[1] else None,
                    "closing_deadline": row[2].isoformat() if row[2] else None,
                    "status": "PENDING"
                }
        except Exception as e:
            logger.error(f"Error creating exchange: {e}")
            return {"error": str(e)}

    async def get_exchange(self, exchange_id: uuid.UUID) -> Optional[Dict[str, Any]]:
        """
        Retrieve an exchange record from the database.
        """
        try:
            with db_manager.pg_cursor() as cur:
                cur.execute("""
                    SELECT id, exchange_id, sale_closed_date, identification_deadline, 
                           closing_deadline, identified_date, purchase_closed_date, status
                    FROM exchange_timers WHERE exchange_id = %s
                    ORDER BY created_at DESC LIMIT 1
                """, (exchange_id,))
                row = cur.fetchone()
                
                if not row:
                    return None
                
                return {
                    "id": str(row[0]),
                    "exchange_id": str(row[1]),
                    "sale_closed_date": row[2].isoformat() if row[2] else None,
                    "identification_deadline": row[3].isoformat() if row[3] else None,
                    "closing_deadline": row[4].isoformat() if row[4] else None,
                    "identified_date": row[5].isoformat() if row[5] else None,
                    "purchase_closed_date": row[6].isoformat() if row[6] else None,
                    "status": row[7],
                    "days_remaining_id": (row[3] - date.today()).days if row[3] else None,
                    "days_remaining_close": (row[4] - date.today()).days if row[4] else None
                }
        except Exception as e:
            logger.error(f"Error fetching exchange: {e}")
            return None

    async def update_status(self, exchange_id: uuid.UUID, status: str, 
                           identified_date: date = None, purchase_closed_date: date = None) -> bool:
        """
        Update the status of an exchange (e.g., mark as identified or completed).
        """
        try:
            with db_manager.pg_cursor() as cur:
                cur.execute("""
                    UPDATE exchange_timers 
                    SET status = %s, 
                        identified_date = COALESCE(%s, identified_date),
                        purchase_closed_date = COALESCE(%s, purchase_closed_date)
                    WHERE exchange_id = %s
                """, (status, identified_date, purchase_closed_date, exchange_id))
                
                logger.info(f"Updated exchange {exchange_id} to status {status}")
                return True
        except Exception as e:
            logger.error(f"Error updating exchange: {e}")
            return False

    async def get_active_exchanges(self) -> List[Dict[str, Any]]:
        """
        Get all active (non-completed, non-failed) exchanges.
        """
        try:
            with db_manager.pg_cursor() as cur:
                cur.execute("""
                    SELECT exchange_id, sale_closed_date, identification_deadline, 
                           closing_deadline, identified_date, status
                    FROM exchange_timers 
                    WHERE status IN ('PENDING', 'IDENTIFIED')
                    ORDER BY closing_deadline ASC
                """)
                rows = cur.fetchall()
                
                return [
                    {
                        "exchange_id": str(r[0]),
                        "sale_closed_date": r[1].isoformat() if r[1] else None,
                        "identification_deadline": r[2].isoformat() if r[2] else None,
                        "closing_deadline": r[3].isoformat() if r[3] else None,
                        "identified_date": r[4].isoformat() if r[4] else None,
                        "status": r[5],
                        "days_remaining_close": (r[3] - date.today()).days if r[3] else None
                    }
                    for r in rows
                ]
        except Exception as e:
            logger.error(f"Error fetching active exchanges: {e}")
            return []


# Singleton
_instance: Optional[ExchangeTimerService] = None

def get_exchange_timer_service() -> ExchangeTimerService:
    global _instance
    if _instance is None:
        _instance = ExchangeTimerService()
    return _instance

