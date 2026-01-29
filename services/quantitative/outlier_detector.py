import logging
import numpy as np
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

class VolatilityOutlierFilter:
    """Identifies tail events (3+ sigma) in return series."""
    
    def detect_outliers(self, returns: List[float], sigma_threshold: float = 3.0) -> List[Dict[str, Any]]:
        if len(returns) < 10: return []
        
        mean = np.mean(returns)
        std = np.std(returns)
        
        outliers = []
        for i, r in enumerate(returns):
            z_score = abs(r - mean) / std if std > 0 else 0
            if z_score >= sigma_threshold:
                outliers.append({
                    "index": i,
                    "return": round(r, 4),
                    "z_score": round(z_score, 2),
                    "is_tail_event": True
                })
                
        if outliers:
            logger.warning(f"RISK_LOG: Detected {len(outliers)} outliers at {sigma_threshold} sigma threshold.")
            
        return outliers
