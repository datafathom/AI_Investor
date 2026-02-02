import logging
from typing import Dict, List, Any
from decimal import Decimal

logger = logging.getLogger(__name__)

class FundFlowService:
    """
    Phase 191.1: Institutional Fund Flow Tracking.
    Analyzes institutional shifts and 'Whale' selling pressure.
    """
    
    def track_whale_selling(self, ticker: str, filing_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Phase 191.2: Whale Tracker.
        Detects aggressive selling by major institutions in the latest 13F deltas.
        """
        selling_pressure = 0.0
        major_sellers = []
        
        for entry in filing_data:
            delta = entry.get("change", 0)
            if delta < -1000000: # Selling > 1M shares
                major_sellers.append(entry["holder"])
                selling_pressure += abs(delta)
        
        risk_level = "LOW"
        if len(major_sellers) > 3 or selling_pressure > 10000000:
            risk_level = "CRITICAL"
        elif len(major_sellers) > 0:
            risk_level = "ELEVATED"
            
        logger.info(f"WHALE_LOG: {ticker} selling pressure: {selling_pressure:,.0f} by {len(major_sellers)} whales.")
        
        return {
            "ticker": ticker,
            "total_whale_sold": selling_pressure,
            "major_sellers": major_sellers,
            "risk_level": risk_level,
            "signal": "EXIT" if risk_level == "CRITICAL" else "MONITOR"
        }

    def detect_sector_overcrowding(self, sector: str, flow_velocity: float) -> Dict[str, Any]:
        """
        Phase 191.3: Concentration Alert.
        Identifies when a sector becomes structurally overcrowded.
        """
        is_overcrowded = flow_velocity > 0.8 # Normalized 0-1
        
        logger.info(f"WHALE_LOG: Sector {sector} overcrowding: {flow_velocity:.2f}. Overcrowded: {is_overcrowded}")
        
        return {
            "sector": sector,
            "crowding_score": round(flow_velocity, 2),
            "is_overcrowded": is_overcrowded,
            "action": "TRIM_EXPOSURE" if is_overcrowded else "HOLD"
        }
