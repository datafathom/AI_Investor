"""
Jurisdictional Arbitrage Mapping - Phase 73.
Maps tax-efficient jurisdictions.
"""
import logging
from typing import Dict, Any, List

logger = logging.getLogger(__name__)

class JurisdictionMapper:
    """Maps tax-efficient jurisdictions."""
    
    JURISDICTIONS = {
        "CAYMAN": {"corp_tax": 0, "cap_gains": 0, "setup_cost": 50000},
        "DELAWARE": {"corp_tax": 0, "cap_gains": 0.20, "setup_cost": 5000},
        "SINGAPORE": {"corp_tax": 0.17, "cap_gains": 0, "setup_cost": 15000},
        "IRELAND": {"corp_tax": 0.125, "cap_gains": 0.33, "setup_cost": 10000}
    }
    
    @staticmethod
    def get_optimal(cap_gains_expected: float) -> str:
        best = min(JurisdictionMapper.JURISDICTIONS.items(), 
                   key=lambda x: cap_gains_expected * x[1]["cap_gains"] + x[1]["setup_cost"])
        return best[0]
