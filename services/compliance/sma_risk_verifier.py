import logging
import numpy as np
from typing import Dict, Any

logger = logging.getLogger(__name__)

class SMARiskVerifier:
    """Verifies that SMAs deliver lower volatility than their benchmarks."""
    
    def verify_vol_reduction(self, sma_returns: list[float], benchmark_returns: list[float]) -> Dict[str, Any]:
        if not sma_returns or not benchmark_returns:
            return {"is_verified": False}
            
        sma_vol = np.std(sma_returns) * np.sqrt(252)
        bench_vol = np.std(benchmark_returns) * np.sqrt(252)
        
        reduction = bench_vol - sma_vol
        is_reduced = reduction > 0
        
        logger.info(f"COMPLIANCE_LOG: SMA Vol: {sma_vol:.2%}, Bench Vol: {bench_vol:.2%}. Reduction: {reduction:.2%}")
        
        return {
            "sma_vol": round(float(sma_vol), 4),
            "benchmark_vol": round(float(bench_vol), 4),
            "vol_reduction": round(float(reduction), 4),
            "is_lower_risk": is_reduced
        }
