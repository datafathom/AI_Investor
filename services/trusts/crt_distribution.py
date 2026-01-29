
import logging
from decimal import Decimal
from typing import Optional, Dict, Any
from datetime import datetime
from uuid import UUID

logger = logging.getLogger(__name__)

class CRTDistributionService:
    """
    Calculates required distributions for Charitable Remainder Trusts (CRT).
    Supports CRUT (Unitrust) and CRAT (Annuity).
    """
    
    MIN_PAYOUT_RATE = Decimal('0.05')  # IRS 5% minimum
    MAX_PAYOUT_RATE = Decimal('0.50')  # IRS 50% maximum
    
    def calculate_required_distribution(
        self,
        trust_id: UUID,
        payout_type: str,
        payout_rate: Decimal,
        trust_value_jan1: Decimal,
        fixed_annuity_amount: Optional[Decimal] = None
    ) -> Dict[str, Any]:
        """
        Calculate the required distribution for the year.
        
        :param payout_type: 'CRUT' (Unitrust) or 'CRAT' (Annuity)
        :param payout_rate: Percentage for CRUT or fixed rate for CRAT validation
        :param trust_value_jan1: Market value of assets on Jan 1
        :param fixed_annuity_amount: Fixed $ amount for CRAT
        """
        
        if not (self.MIN_PAYOUT_RATE <= payout_rate <= self.MAX_PAYOUT_RATE):
            logger.warning(f"Payout rate {payout_rate} is outside standard IRS range (5%-50%)")
            
        required_amt = Decimal('0.00')
        
        if payout_type == 'CRUT':
            required_amt = (trust_value_jan1 * payout_rate).quantize(Decimal('0.01'))
        elif payout_type == 'CRAT':
            if fixed_annuity_amount:
                required_amt = fixed_annuity_amount.quantize(Decimal('0.01'))
            else:
                required_amt = (trust_value_jan1 * payout_rate).quantize(Decimal('0.01'))
        else:
            raise ValueError(f"Invalid payout type: {payout_type}")
            
        logger.info(f"Trust {trust_id}: Required {payout_type} distribution = ${required_amt}")
        
        return {
            "trust_id": trust_id,
            "payout_type": payout_type,
            "required_distribution": required_amt,
            "calculation_date": datetime.now().isoformat()
        }

    def validate_tier_accounting(self, income_type: str) -> bool:
        """
        CRTs follow a 4-tier distribution rule (LIFO):
        1. Ordinary Income
        2. Capital Gains
        3. Other Income (Tax-exempt)
        4. Corpus (Tax-free)
        """
        valid_tiers = ["ORDINARY", "CAP_GAIN", "EXEMPT", "CORPUS"]
        return income_type in valid_tiers
