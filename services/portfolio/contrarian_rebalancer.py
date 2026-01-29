import logging
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

class ContrarianRebalancer:
    """Identifies and recommends rebalancing into out-of-favor asset classes."""
    
    def identify_opportunities(self, asset_performance: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Policy: Rebalance into assets with lowest 1Y performance (Contrarian bias).
        """
        # Sort by 1Y performance ascending
        sorted_assets = sorted(asset_performance, key=lambda x: x.get("perf_1y", 0))
        
        # Pick bottom 2
        opps = sorted_assets[:2]
        
        for opp in opps:
            logger.info(f"PORTFOLIO_LOG: Contrarian Opportunity: {opp.get('ticker')} (1Y Perf: {opp.get('perf_1y'):.2%})")
            
        return opps
