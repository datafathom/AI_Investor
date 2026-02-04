import logging
from datetime import timezone, datetime
from typing import List, Dict, Any
from config.database import SessionLocal
from sqlalchemy import text

logger = logging.getLogger(__name__)

class PriceTelemetryService:
    """
    Manages storage and retrieval of high-frequency price data (TimescaleDB).
    """
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(PriceTelemetryService, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if hasattr(self, '_initialized') and self._initialized:
            return
        self._initialized = True
        logger.info("PriceTelemetryService initialized")

    def store_tick(self, symbol: str, price: float, volume: float = 0, source: str = "UNKNOWN"):
        """
        Inserts a price tick into the hypertable.
        """
        if not SessionLocal:
            logger.warning("DB not available. Skipping tick storage.")
            return

        query = text("""
            INSERT INTO price_telemetry (time, symbol, price, volume, source)
            VALUES (:time, :symbol, :price, :volume, :source)
        """)
        
        try:
            db = SessionLocal()
            db.execute(query, {
                "time": datetime.now(timezone.utc),
                "symbol": symbol,
                "price": price,
                "volume": volume,
                "source": source
            })
            db.commit()
            db.close()
        except Exception as e:
            logger.error(f"Telemetry Write Error: {e}")

    def get_latest_price(self, symbol: str) -> float:
        """Retrieves the most recent price for a symbol."""
        if not SessionLocal:
            return 0.0

        query = text("""
            SELECT price FROM price_telemetry 
            WHERE symbol = :symbol 
            ORDER BY time DESC 
            LIMIT 1
        """)
        
        try:
            db = SessionLocal()
            result = db.execute(query, {"symbol": symbol}).fetchone()
            db.close()
            if result:
                return float(result[0])
        except Exception as e:
            logger.error(f"Telemetry Read Error: {e}")
            
        return 0.0
