import logging
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

class ManagerRanker:
    """Ranks investment managers based on risk-adjusted efficiency."""
    
    def rank_by_sortino(self, managers: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Policy: Sort managers by Sortino ratio descending.
        Inputs: list of {'name': str, 'sortino': float}
        """
        ranked = sorted(managers, key=lambda x: x.get('sortino', 0), reverse=True)
        
        for i, m in enumerate(ranked):
            logger.info(f"QUANT_LOG: Ranking #{i+1}: {m['name']} (Sortino: {m['sortino']:.2f})")
            
        return ranked

    def detect_underperformers(self, managers: List[Dict[str, Any]], bench_sortino: float) -> List[str]:
        """Flags managers failing to beat the risk-adjusted benchmark."""
        return [m['name'] for m in managers if m.get('sortino', 0) < bench_sortino]
