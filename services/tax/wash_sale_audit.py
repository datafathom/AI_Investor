"""
Wash-Sale Audit Trail - Phase 91.
Tracks wash sale prevention history.
"""
import logging
from datetime import datetime
from typing import Dict, Any, List

logger = logging.getLogger(__name__)

class WashSaleAudit:
    """Audit trail for wash sale prevention."""
    
    def __init__(self):
        self.events: List[Dict[str, Any]] = []
    
    def log_sale(self, symbol: str, amount: float):
        self.events.append({"type": "SALE", "symbol": symbol, "amount": amount, "date": datetime.now().isoformat()})
    
    def log_blocked_buy(self, symbol: str, reason: str):
        self.events.append({"type": "BLOCKED_BUY", "symbol": symbol, "reason": reason, "date": datetime.now().isoformat()})
    
    def get_report(self) -> Dict[str, Any]:
        blocked = [e for e in self.events if e["type"] == "BLOCKED_BUY"]
        return {"total_events": len(self.events), "blocked_trades": len(blocked)}
