"""
Zen Mode: Disable High-Freq Oscillation - Phase 85.
Prevents over-trading.
"""
import logging
from datetime import datetime, timedelta
from typing import Dict, Any, List

logger = logging.getLogger(__name__)

class OscillationDamper:
    """Prevents high-frequency oscillation."""
    
    def __init__(self, min_hold_hours: int = 24):
        self.recent_trades: List[datetime] = []
        self.min_hold = timedelta(hours=min_hold_hours)
    
    def record_trade(self):
        self.recent_trades.append(datetime.now())
        # Keep last 100
        self.recent_trades = self.recent_trades[-100:]
    
    def should_block(self) -> bool:
        if len(self.recent_trades) < 2:
            return False
        last_trade = self.recent_trades[-1]
        trades_in_window = sum(1 for t in self.recent_trades if last_trade - t < timedelta(hours=1))
        return trades_in_window > 5
