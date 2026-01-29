"""
Gas Fee Deduction Logic.
Attaches transaction fees to cost basis.
"""
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

class GasLogicHandler:
    """Handles crypto gas accounting."""
    
    def apply_gas_to_basis(self, acquisition_cost: float, gas_fee_usd: float) -> float:
        total_basis = acquisition_cost + gas_fee_usd
        logger.info(f"GAS_LOG: Applied ${gas_fee_usd} to basis. New total: ${total_basis}")
        return total_basis
