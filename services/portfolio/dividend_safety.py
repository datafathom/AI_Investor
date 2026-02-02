import logging
from decimal import Decimal
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

class DividendSafety:
    """
    Identifies 'Dividend Aristocrats' and assesses safety of payouts.
    """
    
    def analyze_dividend_safety(self, stocks: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Assesses safety based on payout ratio and years of growth.
        """
        results = []
        for stock in stocks:
            payout_ratio = stock.get("payout_ratio", 0.5) # Default 50%
            years_growth = stock.get("dividend_years_growth", 0)
            
            # Policy: Safety = (1 - PayoutRatio) * (YearsGrowth / 25)
            # Payout ratio < 60% is preferred.
            safety_score = (1 - payout_ratio) * 10 
            if years_growth >= 25:
                safety_score += 5 # Aristocrat bonus
            
            results.append({
                "ticker": stock["ticker"],
                "payout_ratio": payout_ratio,
                "years_growth": years_growth,
                "safety_score": round(safety_score, 2),
                "is_aristocrat": years_growth >= 25,
                "status": "SECURE" if safety_score > 7 else "CAUTION"
            })
            
        return sorted(results, key=lambda x: x["safety_score"], reverse=True)
