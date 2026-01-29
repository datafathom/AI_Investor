"""
Equity Curve Logger.
Persists periodic snapshots of account equity to TimescaleDB.
"""
import logging
import time
from decimal import Decimal
from datetime import datetime
from typing import Dict, Any

from services.portfolio.pnl_aggregator import PnLAggregator
from services.portfolio.fast_balance import get_balance_service

logger = logging.getLogger(__name__)

class EquityCurveLogger:
    """
    Background worker for logging equity snapshots.
    """
    
    def __init__(self, account_id: str = "DEMO-001"):
        self.account_id = account_id
        self.balance_svc = get_balance_service()
        self.pnl_aggregator = PnLAggregator()

    def log_snapshot(self, open_positions: list, spot_prices: Dict[str, float]):
        """
        Calculates current state and flushes to database.
        """
        balance = self.balance_svc.get_latest_equity()
        unrealized_pnl = self.pnl_aggregator.aggregate_total_pnl(open_positions, spot_prices)
        equity = balance + unrealized_pnl

        # Note: In a production environment, we would use an async DB driver here.
        # This is a representation of the snapshot data packet.
        snapshot = {
            "time": datetime.now(),
            "account_id": self.account_id,
            "balance": balance,
            "unrealized_pnl": unrealized_pnl,
            "equity": equity,
            "timestamp_ms": int(time.time() * 1000)
        }
        
        logger.info(f"EQUITY_SNAPSHOT: Balance ${balance:,.2f} | PnL ${unrealized_pnl:,.2f} | Equity ${equity:,.2f}")
        return snapshot
