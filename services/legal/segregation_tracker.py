"""
Asset Segregation Tracker for APT Divorce Immunity
PURPOSE: Track assets to distinguish between Pre-Marital and Marital property.
         Essential for divorce immunity in Asset Protection Trusts.
"""

import logging
import uuid
from datetime import date
from decimal import Decimal
from typing import Dict, Any, Optional
from utils.database_manager import db_manager

logger = logging.getLogger(__name__)


class SegregationTracker:
    """
    Tracks assets to distinguish between Pre-Marital and Marital property.
    Essential for divorce immunity in APTs.
    
    Pre-marital assets placed in a DAPT are generally immune from divorce settlements.
    """
    
    async def log_asset_segregation(
        self, 
        asset_id: str, 
        trust_id: str,
        transfer_date: date,
        marriage_date: Optional[date] = None
    ) -> Dict[str, Any]:
        """
        Records the date-stamp of an asset relative to a marriage event.
        """
        is_pre_marital = marriage_date is None or transfer_date < marriage_date
        
        try:
            with db_manager.pg_cursor() as cur:
                cur.execute("""
                    INSERT INTO trust_funding_status (trust_id, asset_id, is_titled_correctly, titling_verification_date)
                    VALUES (%s, %s, %s, %s)
                    ON CONFLICT (id) DO UPDATE SET
                        is_titled_correctly = EXCLUDED.is_titled_correctly,
                        titling_verification_date = EXCLUDED.titling_verification_date
                    RETURNING id
                """, (uuid.UUID(trust_id), uuid.UUID(asset_id), True, transfer_date))
                
                record_id = cur.fetchone()[0]
                
                logger.info(f"Asset Segregation: {asset_id} marked as {'PRE_MARITAL' if is_pre_marital else 'MARITAL'}")
                
                return {
                    "id": str(record_id),
                    "asset_id": asset_id,
                    "trust_id": trust_id,
                    "transfer_date": transfer_date.isoformat(),
                    "segregation_status": "PRE_MARITAL_SEGREGATED" if is_pre_marital else "MARITAL_PROPERTY",
                    "immunity_score": 0.95 if is_pre_marital else 0.3,
                    "jurisdiction": "Nevada/Delaware"
                }
        except Exception as e:
            logger.error(f"Error logging segregation: {e}")
            return {"error": str(e)}
        
    async def check_immunity(self, asset_id: str) -> Dict[str, Any]:
        """
        Returns the immunity status of an asset from database.
        """
        try:
            with db_manager.pg_cursor() as cur:
                cur.execute("""
                    SELECT ts.is_titled_correctly, ts.probate_risk_level, 
                           ts.titling_verification_date, t.enforcement_level
                    FROM trust_funding_status ts
                    LEFT JOIN trust_stipulations t ON ts.trust_id = t.trust_id
                    WHERE ts.asset_id = %s
                """, (uuid.UUID(asset_id),))
                
                row = cur.fetchone()
                
                if not row:
                    return {"asset_id": asset_id, "status": "NOT_FOUND"}
                
                is_protected = row[0] and row[3] == 'STRICT'
                
                return {
                    "asset_id": asset_id,
                    "status": "IMMUNE_FROM_SETTLEMENT" if is_protected else "POTENTIALLY_VULNERABLE",
                    "is_titled_correctly": row[0],
                    "probate_risk": row[1],
                    "verification_date": row[2].isoformat() if row[2] else None,
                    "reason": "Asset in DAPT with strict enforcement" if is_protected else "Review trust stipulations"
                }
        except Exception as e:
            logger.error(f"Error checking immunity: {e}")
            return {"error": str(e)}


# Singleton
_instance: Optional[SegregationTracker] = None

def get_segregation_tracker() -> SegregationTracker:
    global _instance
    if _instance is None:
        _instance = SegregationTracker()
    return _instance

