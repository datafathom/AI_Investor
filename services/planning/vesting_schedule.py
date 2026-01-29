"""
Vesting Schedule Tracker.
Tracks RSU/Founder stock vesting events.
"""
import logging
from datetime import datetime, timedelta
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

class VestingTracker:
    """Calculates future vesting events."""
    
    def calculate_vesting(self, grants: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        future_events = []
        now = datetime.now()
        
        for g in grants:
            # Pro-rate monthly or quarterly vesting
            next_date = now + timedelta(days=30)
            future_events.append({
                "ticker": g['ticker'],
                "shares": g['monthly_shares'],
                "date": next_date.isoformat(),
                "est_value": g['monthly_shares'] * g['strike']
            })
            
        return sorted(future_events, key=lambda x: x['date'])
