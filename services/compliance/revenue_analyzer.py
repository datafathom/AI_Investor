import logging
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

class RevenueAnalyzer:
    """Analyzes historical revenue samples for hidden kickbacks."""
    
    def analyze_samples(self, advisor_id: str, samples: List[Dict[str, Any]]) -> float:
        """Returns effective kickback percentage across samples."""
        total = sum(s.get("amount", 0) for s in samples)
        kickbacks = sum(s.get("amount", 0) for s in samples if s.get("type") == "12b-1" or s.get("is_kickback"))
        
        if total <= 0: return 0.0
        
        ratio = kickbacks / total
        logger.info(f"REVENUE_LOG: Advisor {advisor_id} has kickback ratio {ratio:.4f}")
        return ratio
