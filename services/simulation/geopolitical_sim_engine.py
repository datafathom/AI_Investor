import logging
from decimal import Decimal
from typing import Dict, Any, List

logger = logging.getLogger(__name__)

class GeopoliticalSimEngine:
    """
    Simulates portfolio impact of major geopolitical shocks.
    Models scenarios like 'Supply Chain Collapse' or 'Energy War'.
    """
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(GeopoliticalSimEngine, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if hasattr(self, '_initialized') and self._initialized:
            return
        self._initialized = True
        logger.info("GeopoliticalSimEngine initialized")

    def simulate_tail_risk(self, scenario_name: str, sector_exposures: Dict[str, float]) -> Dict[str, Any]:
        """
        Policy: Apply non-linear shocks to sectors based on scenario.
        """
        # Hardcoded logic for Taipei Conflict scenario
        shocks = {
            "TECH": -0.40,
            "DEFENSE": 0.20,
            "ENERGY": 0.15,
            "CONS_DISCRETIONARY": -0.25
        }
        
        impact_pct = 0.0
        for sector, exposure in sector_exposures.items():
            shock = shocks.get(sector.upper(), -0.10) # Default -10% drag
            impact_pct += exposure * shock
            
        logger.info(f"GEO_SIM: Scenario '{scenario_name}' projected impact: {impact_pct:.1%}")
        
        return {
            "scenario": scenario_name,
            "projected_portfolio_delta_pct": round(impact_pct * 100, 2),
            "vulnerability_rating": "CRITICAL" if impact_pct < -0.15 else "MODERATE"
        }
