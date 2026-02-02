import logging
from typing import List, Dict, Any
from decimal import Decimal

logger = logging.getLogger(__name__)

class MFOSpendAggregator:
    """
    Phase 175.2: Vendor Negotiation Power Aggregator.
    Aggregates spending across families to unlock institutional/group discounts.
    """
    
    def calculate_group_leverage(self, vendor_name: str, family_spends: List[float]) -> Dict[str, Any]:
        """
        Policy: Unlock 'TIER_1' discount if aggregate spend > $1M.
        """
        total_spend = sum(Decimal(str(s)) for s in family_spends)
        
        discount_pct = 0.0
        if total_spend >= 1_000_000:
            discount_pct = 15.0 # 15% Group Discount
        elif total_spend >= 500_000:
            discount_pct = 10.0
            
        logger.info(f"MFO_LOG: Aggregated spend for {vendor_name}: ${total_spend:,.2f}. Discount: {discount_pct}%")
        
        return {
            "vendor": vendor_name,
            "aggregate_spend": float(total_spend),
            "group_discount_pct": discount_pct,
            "status": "LEVERAGE_ACTIVE" if discount_pct > 0 else "SCALING"
        }
