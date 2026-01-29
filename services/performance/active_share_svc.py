import logging
from decimal import Decimal
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

class ActiveShareService:
    """
    Quantifies 'Career Risk' by calculating Active Share vs. a benchmark.
    Identifies managers who are herding (Closet Indexing) to protect their jobs.
    """
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(ActiveShareService, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if hasattr(self, '_initialized') and self._initialized:
            return
        self._initialized = True
        logger.info("ActiveShareService initialized")

    def calculate_active_share(self, port_weights: Dict[str, Decimal], bench_weights: Dict[str, Decimal]) -> float:
        """
        Policy: Active Share = 0.5 * Sum(|W_p,i - W_b,i|).
        """
        all_tickers = set(port_weights.keys()) | set(bench_weights.keys())
        total_diff = Decimal('0')
        
        for t in all_tickers:
            wp = port_weights.get(t, Decimal('0'))
            wb = bench_weights.get(t, Decimal('0'))
            total_diff += abs(wp - wb)
            
        active_share = float(total_diff / Decimal('2'))
        
        rank = "HERDING" if active_share < 0.6 else "TRUE_ACTIVE"
        logger.info(f"MANAGER_LOG: Active Share {active_share:.1%}. Rank: {rank}")
        
        return round(active_share, 4)
