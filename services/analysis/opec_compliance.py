"""
OPEC Compliance Monitor.
Tracks production cuts and quota adherence.
"""
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

class OPECCompliance:
    """Monitors OPEC+ production adherence."""
    
    def check_compliance(self, country: str, quota: float, actual: float) -> bool:
        cheating = actual > quota * 1.05 # 5% tolerance
        if cheating:
             logger.info(f"OPEC_LOG: {country} is over-producing (Actual: {actual}, Quota: {quota})")
        return not cheating
