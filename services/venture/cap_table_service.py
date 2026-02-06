import logging
from typing import Dict, Any, List

logger = logging.getLogger(__name__)

class CapTableService:
    """
    Calculates equity distributions and exit scenarios.
    """
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(CapTableService, cls).__new__(cls)
        return cls._instance

    def run_waterfall(self, exit_valuation: float, cap_table: List[Dict[str, Any]]) -> Dict[str, float]:
        """
        Simple liquidation preference engine.
        Assumes 1x Liquidation Preference for 'Preferred' stock.
        """
        logger.info(f"Running Waterfall for Exit: ${exit_valuation:,.2f}")
        
        remaining_cash = exit_valuation
        payouts = {}
        
        # 1. Pay Liquidation Preferences (Preferred Stock)
        # Sort by seniority (Mock: all preferred are equal here for simplicity)
        preferred_holders = [h for h in cap_table if h['type'] == 'Preferred']
        
        for holder in preferred_holders:
            # 1x Pref
            pref_amount = holder['investment_amount'] * 1.0 
            payout = min(remaining_cash, pref_amount)
            payouts[holder['name']] = payout
            remaining_cash -= payout
            
        # 2. Distribute Remaining Cash Pro-Rata (Common + Preferred if participating)
        # Mock: Simplified participation (everyone converts to common for remainder)
        
        if remaining_cash > 0:
            total_shares = sum(h['shares'] for h in cap_table)
            price_per_share = remaining_cash / total_shares
            
            for holder in cap_table:
                # Add pro-rata share
                share_payout = holder['shares'] * price_per_share
                payouts[holder['name']] = payouts.get(holder['name'], 0) + share_payout

        return payouts

# Singleton
cap_table_service = CapTableService()
def get_cap_table_service() -> CapTableService:
    return cap_table_service
