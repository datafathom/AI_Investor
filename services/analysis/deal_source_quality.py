import logging
from typing import Dict, Any, List
from decimal import Decimal

logger = logging.getLogger(__name__)

class DealSourceQuality:
    """
    Phase 179.3: Deal Source Attribution Tracking.
    Tracks where the best deals come from and scores sources based on conversion.
    """
    
    def analyze_source(self, source_name: str, deal_history: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Policy: Source Score = (Total MOIC / Count) * (Conversion Rate).
        """
        total_deals = len(deal_history)
        if total_deals == 0:
            return {"source": source_name, "score": 0, "status": "UNKNOWN"}
            
        conversions = sum(1 for d in deal_history if d.get('invested', False))
        total_moic = sum(Decimal(str(d.get('moic', 0))) for d in deal_history)
        
        avg_moic = float(total_moic / Decimal(str(total_deals)))
        conversion_rate = conversions / total_deals
        
        quality_score = avg_moic * conversion_rate * 5 # Scale to 1-10ish
        
        logger.info(f"ANALYSIS_LOG: Source {source_name} quality scored: {quality_score:.2f}")
        
        return {
            "source": source_name,
            "quality_score": round(quality_score, 1),
            "conversion_rate": round(conversion_rate, 2),
            "avg_moic": round(avg_moic, 2),
            "recommendation": "PRIORITIZE" if quality_score > 7 else "MONITOR"
        }
