import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

class GSTCalculator:
    """Calculates the applicable fraction and tax due for GST transfers."""
    
    def calculate_inclusion_ratio(self, corpus_value: float, exemption_allocated: float) -> float:
        """
        Policy: Inclusion Ratio = 1 - (Exemption / Corpus)
        Used for Dynasty trusts to remain tax-free in perpetuity.
        """
        if corpus_value <= 0: return 0.0
        
        applicable_fraction = exemption_allocated / corpus_value
        inclusion_ratio = 1.0 - applicable_fraction
        
        logger.info(f"TAX_LOG: GST Inclusion Ratio: {inclusion_ratio:.4f} (Allocated: ${exemption_allocated:,.2f} on ${corpus_value:,.2f})")
        return round(float(inclusion_ratio), 4)

    def calculate_gst_tax(self, distribution_amount: float, inclusion_ratio: float, max_estate_tax_rate: float = 0.40) -> float:
        """Tax Due = Distribution * Inclusion Ratio * Max Estate Tax Rate."""
        tax = distribution_amount * inclusion_ratio * max_estate_tax_rate
        return round(float(tax), 2)
