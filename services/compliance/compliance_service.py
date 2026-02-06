"""
Compliance Service
Phase 7 Implementation: The Compliance Shield

Handles rule verification, wash-sale detection, and regulatory checks.
"""

import logging
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta, timezone
from services.compliance.record_vault import get_record_vault

logger = logging.getLogger(__name__)

class ComplianceService:
    _instance = None
    _initialized = False

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ComplianceService, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
        self.vault = get_record_vault()
        self._initialized = True
        logger.info("ComplianceService initialized")

    def check_wash_sale(self, ticker: str, trade_date: datetime) -> Dict[str, Any]:
        """
        Check if a purchase would trigger a wash-sale rule (loss in last 30 days).
        """
        # In production, this would query the DB for realized losses.
        # Here we query the RecordVault for 'trade_execution' records.
        trades = self.vault.get_records_by_type("trade_execution")
        
        thirty_days_ago = trade_date - timedelta(days=30)
        
        for record in trades:
            data = record["data"]
            if data.get("ticker") == ticker:
                # We expect data to have 'pnl' and 'timestamp'
                # For this mock, we assume 'pnl' is plain text in record data
                pnl = data.get("pnl", 0.0)
                ts_str = data.get("executed_at")
                if not ts_str: continue
                
                exec_at = datetime.fromisoformat(ts_str)
                
                if exec_at > thirty_days_ago and pnl < 0:
                    return {
                        "is_wash_sale": True,
                        "reason": f"Realized loss of ${abs(pnl)} on {ticker} on {ts_str}",
                        "last_loss_date": ts_str
                    }
                    
        return {"is_wash_sale": False}

def get_compliance_service() -> ComplianceService:
    return ComplianceService()
