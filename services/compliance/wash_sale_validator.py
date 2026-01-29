import logging
from datetime import datetime, timedelta
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

class WashSaleValidator:
    """Prevents IRS Wash Sale violations (re-buying within 30 days of a loss)."""
    
    def check_wash_sale(self, ticker: str, loss_date: datetime, recent_buys: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Policy: A wash sale occurs if you sell for a loss and buy the same/similar asset 
        within 30 days BEFORE or AFTER the sale.
        """
        violations = []
        window_start = loss_date - timedelta(days=30)
        window_end = loss_date + timedelta(days=30)
        
        for buy in recent_buys:
            if buy["ticker"] == ticker:
                buy_date = buy["date"]
                if window_start <= buy_date <= window_end:
                    violations.append(buy)
                    
        is_safe = len(violations) == 0
        
        if not is_safe:
            logger.warning(f"COMPLIANCE_ALERT: Wash sale detected for {ticker}. Buy on {violations[0]['date']} overlaps with loss sale.")
            
        return {
            "is_safe": is_safe,
            "violation_count": len(violations),
            "wash_sale_ticker": ticker if not is_safe else None,
            "verification_status": "VALIDATED" if is_safe else "WASH_SALE_DETECTED"
        }
