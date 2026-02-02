import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

class PerceptionGapReporter:
    """
    Phase 170.5: Social Perception vs. Actual Productivity Mapping.
    Identifies gaps between family perception and market reality.
    """
    
    def compare_perception(self, market_valuation: float, internal_valuation: float) -> Dict[str, Any]:
        """
        Gaps > 50% trigger a 'Governance Warning'.
        """
        gap_pct = ((internal_valuation / market_valuation) - 1) * 100 if market_valuation > 0 else 0
        
        if gap_pct > 50.0:
            logger.warning(f"REPORT_LOG: Significant perception gap: {gap_pct:.2f}% above market.")
            
        return {
            "perception_gap_pct": round(gap_pct, 2),
            "governance_status": "CRITICAL" if gap_pct > 75 else "STABLE",
            "recommendation": "RESET_KPI_TARGETS" if gap_pct > 50 else "NONE"
        }
