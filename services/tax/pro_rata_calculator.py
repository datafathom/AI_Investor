import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

class ProRataCalculator:
    """Calculates the taxable portion of a Roth conversion using the IRS Pro-Rata rule."""
    
    def calculate_taxable_portion(self, conversion_amount: float, total_ira_balance: float, after_tax_basis: float) -> Dict[str, Any]:
        """
        Pro-Rata Rule: (After-Tax Basis / Total IRA Value) = Non-taxable %
        """
        if total_ira_balance <= 0: return {"tax_free_amount": conversion_amount, "taxable_amount": 0.0}
        
        non_tax_ratio = after_tax_basis / total_ira_balance
        tax_free_portion = conversion_amount * non_tax_ratio
        taxable_portion = conversion_amount - tax_free_portion
        
        logger.info(f"TAX_LOG: Pro-Rata result: {non_tax_ratio*100:.1f}% tax-free. Taxable: ${taxable_portion:,.2f}")
        
        return {
            "conversion_amount": conversion_amount,
            "tax_free_amount": round(tax_free_portion, 2),
            "taxable_amount": round(taxable_portion, 2),
            "ratio": round(non_tax_ratio, 4)
        }
