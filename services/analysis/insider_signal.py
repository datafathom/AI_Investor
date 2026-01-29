import logging
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

class InsiderSignalService:
    """
    Tracks Form 4 filings to detect significant insider buying.
    Policy: 'Cluster Buying' by multiple officers is a High Conviction signal.
    """
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(InsiderSignalService, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if hasattr(self, '_initialized') and self._initialized:
            return
        self._initialized = True
        logger.info("InsiderSignalService initialized")

    def detect_high_conviction_buying(self, filings: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Analyzes a list of Form 4 transactions.
        """
        buy_count = 0
        total_value_bought = 0.0
        unique_buyers = set()
        
        for filing in filings:
            txn_type = filing.get('transaction_type')
            is_open_market = filing.get('is_open_market', False)
            
            if txn_type == 'BUY' and is_open_market:
                buy_count += 1
                total_value_bought += filing.get('value', 0)
                unique_buyers.add(filing.get('reporting_person'))
                
        signal = "NEUTRAL"
        if len(unique_buyers) >= 3 and total_value_bought > 1000000:
            signal = "HIGH_CONVICTION_BUY"
            logger.info(f"Insider Signal: {signal} - {len(unique_buyers)} insiders bought ${total_value_bought:,.0f}")
        elif total_value_bought > 500000:
            signal = "MODERATE_BUY"
            
        return {
            "signal": signal,
            "net_shares_bought": buy_count,
            "unique_insiders": len(unique_buyers),
            "total_value": total_value_bought
        }
