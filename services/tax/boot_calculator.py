"""
Boot Tax Calculator for 1031 Exchanges
PURPOSE: Calculate the taxable "boot" (cash received or mortgage reduction)
         when a 1031 exchange does not fully defer capital gains.
         
TAX RATES (2026 Federal):
- Long-term capital gains: 0%, 15%, or 20% depending on income bracket
- Depreciation recapture (Section 1250): 25%
- Net Investment Income Tax (NIIT): Additional 3.8% for high earners
"""

import logging
from decimal import Decimal
from typing import Dict, Any, Optional
from dataclasses import dataclass

logger = logging.getLogger(__name__)

# Federal capital gains brackets (2026 estimated)
LTCG_BRACKETS = [
    {"max_income": 47025, "rate": 0.0},
    {"max_income": 518900, "rate": 0.15},
    {"max_income": float('inf'), "rate": 0.20}
]

DEPRECIATION_RECAPTURE_RATE = Decimal("0.25")
NIIT_RATE = Decimal("0.038")
NIIT_THRESHOLD = Decimal("250000")  # Married filing jointly


@dataclass
class BootTaxResult:
    """Result of boot tax calculation."""
    boot_amount: Decimal
    depreciation_recapture_tax: Decimal
    capital_gain_tax: Decimal
    niit_tax: Decimal
    total_tax_liability: Decimal
    effective_rate: Decimal


class BootCalculator:
    """
    Calculates the taxable 'boot' received in a 1031 exchange.
    Boot occurs when debt is reduced without cash offset or when cash is pulled out.
    
    Enhanced to calculate full tax liability with depreciation recapture.
    """
    
    def calculate_taxable_boot(
        self,
        cash_boot: Decimal,
        mortgage_boot: Decimal,
        offsetting_cash_added: Decimal = Decimal('0.00')
    ) -> Dict[str, Any]:
        """
        Calculates net taxable boot (basic calculation).
        """
        # Mortgage boot can be offset by cash added, but cash boot cannot 
        # be offset by mortgage added.
        net_mortgage_boot = max(Decimal('0.00'), mortgage_boot - offsetting_cash_added)
        total_boot = cash_boot + net_mortgage_boot
        
        logger.info(f"Boot Calculation: Cash={cash_boot}, Mortgage={mortgage_boot}, Offset={offsetting_cash_added}, Result=${total_boot}")
        
        return {
            "cash_boot": cash_boot,
            "mortgage_boot": mortgage_boot,
            "offset_applied": offsetting_cash_added,
            "net_taxable_boot": total_boot,
            "tax_estimate_20pct": (total_boot * Decimal('0.20')).quantize(Decimal('0.01'))
        }
    
    def calculate_full_boot_tax(
        self,
        boot_amount: Decimal,
        accumulated_depreciation: Decimal,
        taxable_income: Decimal,
        filing_status: str = "married_joint"
    ) -> BootTaxResult:
        """
        Calculate total tax liability on boot with full breakdown.
        
        Args:
            boot_amount: Total boot received (cash + mortgage reduction)
            accumulated_depreciation: Depreciation taken on property over hold period
            taxable_income: Investor's other taxable income for LTCG bracket
            filing_status: Tax filing status
            
        Returns:
            BootTaxResult with breakdown of all taxes
        """
        if boot_amount <= 0:
            return BootTaxResult(
                boot_amount=Decimal("0"),
                depreciation_recapture_tax=Decimal("0"),
                capital_gain_tax=Decimal("0"),
                niit_tax=Decimal("0"),
                total_tax_liability=Decimal("0"),
                effective_rate=Decimal("0")
            )
        
        # 1. Depreciation Recapture (taxed first, at 25%)
        # The lesser of boot or accumulated depreciation triggers recapture
        recapture_amount = min(boot_amount, accumulated_depreciation)
        depreciation_tax = recapture_amount * DEPRECIATION_RECAPTURE_RATE
        
        # 2. Remaining boot is capital gain
        remaining_boot = boot_amount - recapture_amount
        ltcg_rate = self._get_ltcg_rate(taxable_income, filing_status)
        capital_gain_tax = remaining_boot * ltcg_rate
        
        # 3. NIIT (Net Investment Income Tax) - 3.8% if above threshold
        niit_tax = Decimal("0")
        if taxable_income > NIIT_THRESHOLD:
            niit_tax = boot_amount * NIIT_RATE
        
        # Total liability
        total_tax = depreciation_tax + capital_gain_tax + niit_tax
        effective_rate = (total_tax / boot_amount * 100) if boot_amount > 0 else Decimal("0")
        
        logger.info(f"Full Boot Tax: Boot=${boot_amount}, Recapture=${depreciation_tax}, LTCG=${capital_gain_tax}, NIIT=${niit_tax}")
        
        return BootTaxResult(
            boot_amount=boot_amount,
            depreciation_recapture_tax=depreciation_tax,
            capital_gain_tax=capital_gain_tax,
            niit_tax=niit_tax,
            total_tax_liability=total_tax,
            effective_rate=effective_rate.quantize(Decimal("0.01"))
        )
    
    def _get_ltcg_rate(self, taxable_income: Decimal, filing_status: str) -> Decimal:
        """Determine long-term capital gains rate based on income."""
        for bracket in LTCG_BRACKETS:
            if float(taxable_income) <= bracket["max_income"]:
                return Decimal(str(bracket["rate"]))
        return Decimal("0.20")


# Singleton
_instance: Optional[BootCalculator] = None

def get_boot_calculator() -> BootCalculator:
    global _instance
    if _instance is None:
        _instance = BootCalculator()
    return _instance

