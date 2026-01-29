
import logging
from decimal import Decimal
from typing import Dict, Any, List

logger = logging.getLogger(__name__)

class ProbateFeeCalculator:
    """
    Calculates statutory probate attorney and executor fees (California Model).
    Fees are based on Gross Asset Value.
    """
    
    def calculate_statutory_fees(self, gross_assets: Decimal) -> Dict[str, Any]:
        """
        Standard CA Tiered Fee Structure:
        - 4% of first $100k
        - 3% of next $100k
        - 2% of next $800k
        - 1% of next $9M
        - 0.5% of next $15M
        """
        logger.info(f"Calculating Probate Fees for Gross Assets: ${gross_assets}")
        
        remaining = gross_assets
        fee = Decimal('0.00')
        tiers = []
        
        # Tier 1: 4% of $100k
        amount = min(remaining, Decimal('100000.00'))
        if amount > 0:
            tier_fee = amount * Decimal('0.04')
            fee += tier_fee
            remaining -= amount
            tiers.append({"tier": "1st $100k", "rate": "4%", "fee": float(tier_fee)})
            
        # Tier 2: 3% of $100k
        amount = min(remaining, Decimal('100000.00'))
        if amount > 0:
            tier_fee = amount * Decimal('0.03')
            fee += tier_fee
            remaining -= amount
            tiers.append({"tier": "Next $100k", "rate": "3%", "fee": float(tier_fee)})

        # Tier 3: 2% of $800k
        amount = min(remaining, Decimal('800000.00'))
        if amount > 0:
            tier_fee = amount * Decimal('0.02')
            fee += tier_fee
            remaining -= amount
            tiers.append({"tier": "Next $800k", "rate": "2%", "fee": float(tier_fee)})

        # Tier 4: 1% of $9M
        amount = min(remaining, Decimal('9000000.00'))
        if amount > 0:
            tier_fee = amount * Decimal('0.01')
            fee += tier_fee
            remaining -= amount
            tiers.append({"tier": "Next $9M", "rate": "1%", "fee": float(tier_fee)})

        # Total fees = Attorney Fee + Executor Fee (usually match)
        total_statutory_cost = fee * 2
        
        return {
            "gross_assets": float(gross_assets),
            "attorney_statutory_fee": float(fee),
            "executor_statutory_fee": float(fee),
            "total_statutory_cost": float(total_statutory_cost),
            "tiers": tiers,
            "estimated_court_costs": 2000.0
        }
