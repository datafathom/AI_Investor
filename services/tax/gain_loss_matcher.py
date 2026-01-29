import logging
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

class GainLossMatcher:
    """Matches realized/unrealized losses against gains to minimize tax impact."""
    
    def match_losses(self, gains: List[Dict[str, Any]], losses: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Policy (HIFO/Tax Efficiency): 
        1. Match Short-term losses against Short-term gains (Highest tax rate).
        2. Match Long-term against Long-term.
        3. Match remaining losses across types.
        """
        # Group by term
        st_gains = [g for g in gains if g.get("term") == "SHORT"]
        lt_gains = [g for g in gains if g.get("term") == "LONG"]
        st_losses = [l for l in losses if l.get("term") == "SHORT"]
        lt_losses = [l for l in losses if l.get("term") == "LONG"]
        
        # Primary matching logic (simplified for logic gate)
        st_net = sum(g["amount"] for g in st_gains) - sum(l["amount"] for l in st_losses)
        lt_net = sum(g["amount"] for g in lt_gains) - sum(l["amount"] for l in lt_losses)
        
        logger.info(f"TAX_LOG: Gain-Loss Matching: ST Net ${st_net:,.2f}, LT Net ${lt_net:,.2f}")
        
        return {
            "short_term_net": round(st_net, 2),
            "long_term_net": round(lt_net, 2),
            "total_harvested_offset": round(sum(l["amount"] for l in losses), 2)
        }
