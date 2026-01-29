import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

class PassiveIndexGuard:
    """
    Prevents active stock-picking in accounts designated for passive investing.
    Only allows approved ETFs and Index funds.
    """
    
    def validate_trade(self, account_strategy: str, ticker: str, is_index_fund: bool) -> Dict[str, Any]:
        if account_strategy == "PASSIVE_INDEX":
            if not is_index_fund:
                logger.warning(f"GUARD_BLOCK: Attempted purchase of ${ticker} in passive account blocked.")
                return {
                    "allowed": False,
                    "reason": "Individual stock selection prohibited in passive accounts.",
                    "code": "STOCK_PICK_BLOCKED"
                }
        
        return {"allowed": True}
