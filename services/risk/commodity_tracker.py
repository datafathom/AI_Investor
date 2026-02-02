import logging
from typing import Dict, List, Any

logger = logging.getLogger(__name__)

class CommodityExposureTracker:
    """
    Phase 187.2: Commodity-Tied EM Exposure Tracker.
    Maps emerging market exposure to specific geopolitical catalysts via commodity ties.
    """
    
    # Mapping EM countries to their primary commodity drivers
    EM_COMMODITY_MAP = {
        "BRAZIL": ["Iron Ore", "Soybeans", "Oil"],
        "SAUDI_ARABIA": ["Oil", "Gas"],
        "CHILE": ["Copper"],
        "SOUTH_AFRICA": ["Gold", "Platinum", "Coal"],
        "INDONESIA": ["Coal", "Palm Oil", "Nickel"]
    }

    def get_em_vulnerability(self, country: str, affected_commodities: List[str]) -> Dict[str, Any]:
        """
        Calculates vulnerability of an EM node based on exposure to disrupted commodities.
        """
        primary_commodities = self.EM_COMMODITY_MAP.get(country.upper(), [])
        disrupted = [c for c in affected_commodities if c in primary_commodities]
        
        vulnerability_score = len(disrupted) / len(primary_commodities) if primary_commodities else 0.0
        
        logger.info(f"GEORISK_LOG: {country} vulnerability to {affected_commodities}: {vulnerability_score:.2f}")
        
        return {
            "country": country,
            "primary_commodities": primary_commodities,
            "disrupted_commodities": disrupted,
            "vulnerability_score": round(vulnerability_score, 2),
            "impact_severity": "HIGH" if vulnerability_score > 0.5 else "LOW"
        }

    def list_at_risk_countries(self, catalyst: str) -> List[str]:
        """
        Identifies countries at risk based on a specific catalyst (e.g., 'Oil Supply Shock').
        """
        # Simple keyword mapping for demo
        risky = []
        if "oil" in catalyst.lower():
            risky = ["SAUDI_ARABIA", "BRAZIL"]
        elif "copper" in catalyst.lower():
            risky = ["CHILE"]
            
        return risky
