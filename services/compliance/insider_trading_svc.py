import logging
import datetime
from decimal import Decimal
from typing import Dict, Any, List, Optional

logger = logging.getLogger(__name__)

class InsiderTradingService:
    """
    Phase 185.1: Rule 144 Volume & Affiliate Restriction Engine.
    Controls insider selling of concentrated public stock positions.
    """
    
    def calculate_sellable_volume(self, ticker: str, outstanding_shares: int, avg_weekly_volume: int) -> Dict[str, Any]:
        """
        Rule 144(e) Volume Limit:
        The greater of:
        - 1% of the outstanding shares.
        - The average weekly trading volume for the previous 4 weeks.
        """
        one_percent_limit = int(outstanding_shares * 0.01)
        volume_limit = max(one_percent_limit, avg_weekly_volume)
        
        logger.info(f"RULE144_LOG: {ticker} Limit: {volume_limit:,} (1% of shares: {one_percent_limit:,}, Avg Vol: {avg_weekly_volume:,})")
        
        return {
            "ticker": ticker,
            "one_percent_limit": one_percent_limit,
            "avg_weekly_volume": avg_weekly_volume,
            "max_sellable_volume": volume_limit
        }

    def check_lockup_status(self, ticker: str, lockup_expiry: datetime.date) -> Dict[str, Any]:
        """
        Phase 185.2: Lock-Up Period Validator.
        Verifies if an insider is within a post-IPO or post-acquisition lock-up period.
        """
        today = datetime.date.today()
        is_locked = today < lockup_expiry
        
        days_remaining = (lockup_expiry - today).days if is_locked else 0
        
        logger.info(f"RULE144_LOG: {ticker} Lockup Status: {'LOCKED' if is_locked else 'EXTINGUISHED'} ({days_remaining} days left)")
        
        return {
            "ticker": ticker,
            "is_locked": is_locked,
            "lockup_expiry": lockup_expiry.isoformat(),
            "days_remaining": days_remaining,
            "can_sell": not is_locked
        }

    def validate_sale_compliance(
        self, 
        ticker: str, 
        shares_to_sell: int, 
        outstanding_shares: int, 
        avg_weekly_volume: int,
        lockup_expiry: datetime.date,
        is_affiliate: bool = True
    ) -> Dict[str, Any]:
        """
        Unified compliance check for a proposed insider sale.
        """
        if not is_affiliate:
            return {"compliant": True, "msg": "Non-affiliate not subject to Rule 144 volume limits."}
            
        lockup = self.check_lockup_status(ticker, lockup_expiry)
        if lockup["is_locked"]:
            return {
                "compliant": False, 
                "reason": f"Lock-up period active until {lockup['lockup_expiry']}.",
                "lockup_details": lockup
            }
            
        limits = self.calculate_sellable_volume(ticker, outstanding_shares, avg_weekly_volume)
        if shares_to_sell > limits["max_sellable_volume"]:
            return {
                "compliant": False,
                "reason": f"Sale volume {shares_to_sell:,} exceeds Rule 144(e) limit of {limits['max_sellable_volume']:,}.",
                "volume_details": limits
            }
            
        return {
            "compliant": True,
            "msg": "Proposed sale complies with Rule 144 volume and lock-up restrictions.",
            "volume_details": limits
        }
