import logging
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

class ReturnPrioritizer:
    """Prioritizes assets based on risk-reward efficiency (Sharpe-like ranking)."""
    
    def rank_assets(self, assets: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Score = Return / Volatility
        """
        ranked = []
        for asset in assets:
            ret = asset.get("expected_return", 0)
            vol = asset.get("volatility", 1) # Avoid div by zero
            score = ret / vol
            
            asset["efficiency_score"] = round(score, 4)
            ranked.append(asset)
            
        ranked.sort(key=lambda x: x["efficiency_score"], reverse=True)
        
        if ranked:
            logger.info(f"QUANT_LOG: Top Efficient Asset: {ranked[0].get('ticker')} (Score: {ranked[0]['efficiency_score']})")
            
        return ranked
