
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

# Small Estate Thresholds (2024 Heuristics)
PROBATE_THRESHOLDS = {
    "CA": 184500.0,
    "NV": 25000.0,
    "NY": 50000.0,
    "FL": 75000.0,
    "TX": 75000.0
}

class ProbateChecker:
    """
    Checks if an estate is above the 'Small Estate' threshold for probate.
    """
    
    def check_threshold(self, state_code: str, gross_assets: float) -> Dict[str, Any]:
        """
        Validates if full probate is required.
        """
        threshold = PROBATE_THRESHOLDS.get(state_code, 50000.0)
        requires_probate = gross_assets > threshold
        
        logger.info(f"Probate Check: State={state_code}, Assets={gross_assets}, Threshold={threshold}, Result={requires_probate}")
        
        return {
            "state": state_code,
            "gross_assets": gross_assets,
            "threshold": threshold,
            "requires_full_probate": requires_probate,
            "procedure": "HEARING / FULL PROBATE" if requires_probate else "SMALL ESTATE AFFIDAVIT"
        }
