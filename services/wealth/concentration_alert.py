"""
Concentration Alert System.
Detects dangerous over-concentration in assets/sectors.
"""
import logging
from typing import Dict, Any, List

logger = logging.getLogger(__name__)

class ConcentrationAlert:
    """Alerts on over-concentration."""
    
    MAX_ASSET_PCT = 0.20 # 20% max in single stock
    MAX_SECTOR_PCT = 0.35 # 35% max in single sector
    
    def check_portfolio(self, holdings: List[Dict[str, Any]]) -> List[str]:
        total_value = sum(h["value"] for h in holdings)
        if total_value == 0:
            return []
            
        alerts = []
        sector_totals = {}
        
        for h in holdings:
            symbol = h["symbol"]
            pct = h["value"] / total_value
            
            # Asset Check
            if pct > self.MAX_ASSET_PCT:
                alerts.append(f"HIGH_CONCENTRATION: {symbol} is {pct*100:.1f}%")
                
            # Sector Accumulate
            sector = h.get("sector", "Unknown")
            sector_totals[sector] = sector_totals.get(sector, 0) + h["value"]
            
        for sector, val in sector_totals.items():
            sect_pct = val / total_value
            if sect_pct > self.MAX_SECTOR_PCT:
                alerts.append(f"SECTOR_CONCENTRATION: {sector} is {sect_pct*100:.1f}%")
                
        return alerts
