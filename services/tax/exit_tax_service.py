"""
==============================================================================
FILE: services/tax/exit_tax_service.py
ROLE: Expatriation Tax Calculator (Section 877A)
PURPOSE: Calculate the "Exit Tax" for covered expatriates.
         - Checks Net Worth Threshold (> $2M)
         - Checks Tax Liability Threshold (> $190k)
         - Calculates "Phantom Sale" capital gains on worldwide assets.

INTEGRATION:
    - WealthService: Get total net worth.
    - TaxService: Get average tax liability.
    - PortfolioService: Get unrealized gains for phantom sale.

AUTHOR: AI Investor Team
CREATED: 2026-01-30
==============================================================================
"""

import logging
from decimal import Decimal
from typing import Dict, List, Any
from datetime import date

logger = logging.getLogger(__name__)

class ExitTaxService:
    """
    Manages Expatriation Tax calculations and status determination.
    """

    # 2024 Thresholds (Inflation adjusted)
    NET_WORTH_THRESHOLD = Decimal("2000000.00")
    TAX_LIABILITY_THRESHOLD = Decimal("190000.00")
    EXCLUSION_AMOUNT = Decimal("866000.00") # 2024 Exclusion for Gains

    def check_covered_status(
        self, 
        net_worth: Decimal, 
        avg_annual_tax: Decimal, 
        compliant_5_years: bool
    ) -> Dict[str, Any]:
        """
        Determine if client is a 'Covered Expatriate'.
        """
        is_covered = False
        reasons = []

        if net_worth >= self.NET_WORTH_THRESHOLD:
            is_covered = True
            reasons.append("Net Worth > $2M")
        
        if avg_annual_tax > self.TAX_LIABILITY_THRESHOLD:
            is_covered = True
            reasons.append("Avg Tax Liability > Threshold")
            
        if not compliant_5_years:
            is_covered = True
            reasons.append("Failed 5-Year Compliance Certification")

        return {
            "is_covered_expatriate": is_covered,
            "reasons": reasons
        }

    def calculate_exit_tax(
        self, 
        unrealized_gains: Decimal, 
        status_check: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Calculate the tax bill on the phantom sale of all assets.
        """
        if not status_check.get("is_covered_expatriate"):
            return {"tax_due": Decimal("0.00"), "msg": "Client is not a Covered Expatriate"}

        taxable_gain = max(Decimal("0.00"), unrealized_gains - self.EXCLUSION_AMOUNT)
        est_tax_rate = Decimal("0.238") # 20% Cap Gains + 3.8% NIIT
        tax_bill = taxable_gain * est_tax_rate

        return {
            "total_unrealized_gains": unrealized_gains,
            "exclusion_applied": self.EXCLUSION_AMOUNT,
            "taxable_gain": taxable_gain,
            "estimated_tax_bill": tax_bill
        }
