import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

class TechDemandCorrelator:
    """Links technology sector growth metrics to data center utilization."""
    
    def analyze_dc_leverage(self, tech_capex_growth: float, dc_rental_growth: float) -> Dict[str, Any]:
        """
        Policy: If Tech CapEx is growing, DC utilization/rent typically follows.
        """
        leverage = dc_rental_growth / tech_capex_growth if tech_capex_growth > 0 else 0
        
        logger.info(f"ANALYSIS_LOG: Tech CapEx growth {tech_capex_growth:.1%} drove {dc_rental_growth:.1%} DC rent growth.")
        
        return {
            "tech_dc_leverage": round(float(leverage), 4),
            "demand_outlook": "BULLISH" if tech_capex_growth > 0.10 else "STABLE"
        }
