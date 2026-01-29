import logging
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

class IntlConcentrationAnalyzer:
    """Analyzes single-company concentration in international indices."""
    
    def analyze_index_skew(self, index_name: str, holdings: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Acceptance: Flag indices where top holding > 20% (e.g. Taiwan/TSMC).
        """
        if not holdings: return {}
        
        # Sort by weight
        sorted_holdings = sorted(holdings, key=lambda x: x.get("weight", 0), reverse=True)
        top_holding = sorted_holdings[0]
        
        weight = top_holding.get("weight", 0)
        is_skewed = weight > 0.20
        
        if is_skewed:
            logger.warning(f"INTL_ALERT: {index_name} is skewed. Top holding {top_holding.get('ticker')} has {weight*100:.1f}% weight.")
            
        return {
            "index_name": index_name,
            "top_ticker": top_holding.get("ticker"),
            "top_weight": round(weight, 4),
            "is_skewed": is_skewed
        }
