import logging
from decimal import Decimal
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

class QualityFactorTilt:
    """
    Prioritizes Quality stocks (Profitability, Low Leverage) for Bear Markets.
    """
    
    def score_quality(self, stocks: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Scores stocks based on ROE and Debt-to-Equity.
        """
        scored_stocks = []
        for stock in stocks:
            # Heuristic Quality Score
            # + ROE, - DebtToEquity
            roe = stock.get("roe", 0)
            dte = stock.get("debt_to_equity", 1) # Default high debt if missing
            
            # Simple score: ROE / (1 + DTE)
            quality_score = roe / (1 + dte)
            
            scored_stocks.append({
                "ticker": stock["ticker"],
                "quality_score": round(quality_score, 2),
                "is_quality_buy": quality_score > 15.0 # Threshold for 'Quality'
            })
            
        # Sort by quality
        scored_stocks.sort(key=lambda x: x["quality_score"], reverse=True)
        return scored_stocks
