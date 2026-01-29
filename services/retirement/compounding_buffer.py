import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

class CompoundingBufferCalculator:
    """Calculates the necessary 'growth buffer' to maintain real purchasing power."""
    
    def calculate_required_buffer(self, portfolio_value: float, inflation_expectation: float) -> float:
        """
        Required growth reinvestment to keep principal flat in real terms.
        """
        buffer_needed = portfolio_value * inflation_expectation
        logger.info(f"RET_LOG: Required compounding reinvestment: ${buffer_needed:,.2f} for {inflation_expectation:.2%} inflation.")
        return round(buffer_needed, 2)
